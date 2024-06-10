import lightning as L
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

from src.models.w2v_genre_classifier import W2V_GenreClassifier
from utils.data_module import GenreDataModule

def cli_main():
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=True, mode='min')
    cli = LightningCLI(W2V_GenreClassifier, GenreDataModule, trainer_defaults={"callbacks": [early_stopping]})


if __name__ == "__main__":
    cli_main()

    
# --print-config