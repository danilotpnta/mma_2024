import lightning as L
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

from models.fcn_classifier import GenreFCN

def cli_main():
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=True, mode='min')
    cli = LightningCLI(GenreFCN, DataPlaceholder, trainer_defaults={"callbacks": [early_stopping]})



if __name__ == "__main__":
    cli_main()

    
# --print-config