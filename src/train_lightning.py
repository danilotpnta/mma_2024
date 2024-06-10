import os
from torch import optim, nn, utils, Tensor
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
import lightning as L
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

from models.fcn_classifier import GenreFCN

def cli_main():
    early_stopping = EarlyStopping('val_loss')
    cli = LightningCLI(GenreFCN, DataPlaceholder)
                    #    Todo: add early stopping
                    #    trainer_defaults={})


if __name__ == "__main__":
    cli_main()

    
# --print-config