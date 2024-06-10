import torch.nn as nn
from lightning import LightningModule
import torch

class GenreFCN(LightningModule):
    """Head for genre classification task.
    Sourced from: kaggle.com/code/lujar1762/music-genre-classification-with-wav2vec2"""

    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.final_dropout)
        self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

    def forward(self, x, **kwargs):
        x = self.dropout(x)
        x = self.dense(x)
        x = nn.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x
    
    def loss(self, preds):
        if labels is None:
            labels = torch.ones_like(preds)
        # An arbitrary loss to have a loss that updates the model weights during `Trainer.fit` calls
        return nn.functional.mse_loss(preds, labels)

    def step(self, batch):
        output = self(batch)
        return self.loss(output)

    def training_step(self, batch, batch_idx):
        return {"loss": self.step(batch)}

    def validation_step(self, batch, batch_idx):
        return {"x": self.step(batch)}

    def test_step(self, batch, batch_idx):
        return {"y": self.step(batch)}
    
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer
    
