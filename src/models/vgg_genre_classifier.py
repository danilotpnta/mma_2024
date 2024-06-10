import torch
import torch.nn as nn
from torchvggish import vggish, vggish_input
import pytorch_lightning as pl

class VGGish_GenreClassifier(pl.LightningModule):
    def __init__(self):
        super(VGGish_GenreClassifier, self).__init__()
        self.vggish = vggish()
        self.vggish.eval()  # Set to eval mode
        self.dropout = nn.Dropout(0.3)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 8)
        self.save_hyperparameters()

    def forward(self, x):
        with torch.no_grad():  # Freeze VGGish feature extraction
            x = self.vggish(x)
        x = self.dropout(x)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x
    
    def loss(self, preds, labels):
        return nn.functional.cross_entropy(preds, labels)

    def step(self, batch):
        inputs, labels = batch
        inputs = vggish_input.wavfile_to_examples(inputs)
        print(inputs, labels)
        outputs = self(inputs)
        loss = self.loss(outputs, labels)
        return loss

    def training_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log('train_loss', loss)
        return {"loss": loss}

    def validation_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log('val_loss', loss)
        return {"val_loss": loss}

    def test_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log('test_loss', loss)
        return {"test_loss": loss}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
