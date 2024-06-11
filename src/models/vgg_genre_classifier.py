import torch
import torch.nn as nn
import numpy as np
import pytorch_lightning as pl
from torchvggish import vggish as VGGish
from torchmetrics import Accuracy 


class VGGish_GenreClassifier(pl.LightningModule):
    def __init__(self):
        super(VGGish_GenreClassifier, self).__init__()
        self.vggish = VGGish()
        self.vggish.eval()  # Set to eval mode
        self.dropout = nn.Dropout(0.3)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 8)
        self.save_hyperparameters()

    def forward(self, x):
        with torch.no_grad():  # Freeze VGGish feature extraction
            x = self.vggish(x)
        x = self.dropout(x)
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
    def loss(self, preds, labels):
        return nn.functional.cross_entropy(preds, labels.float())

    def step(self, batch):
        inputs, labels = batch

        # Forward pass
        outputs = self(inputs)

        # Compute loss
        loss = self.loss(outputs, labels)
        print("loss: ", loss)

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

        inputs, labels = batch

        # Forward pass
        outputs = self(inputs)

        accuracy = Accuracy(task="multiclass", num_classes=8)

        acc = accuracy(outputs, labels)
        self.log('accuracy', acc)

        return {"test_loss": loss, 'accuracy': acc}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
