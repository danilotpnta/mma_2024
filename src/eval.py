import os
import argparse
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from utils.data_module import GenreDataModule
from models.w2v_genre_classifier import W2V_GenreClassifier
from models.vgg_genre_classifier import VGGish_GenreClassifier
from transformers import AutoConfig
import torch
import config

def main(args):
    
    # Create DataModule
    data_module = GenreDataModule(batch_size=args.batch_size)

    # Get a list of all checkpoint files
    checkpoint_files = [f for f in os.listdir(args.checkpoint_dir) if f.endswith('.ckpt')]

    # Sort the checkpoint files by modification time in descending order
    checkpoint_files.sort(key=lambda f: os.path.getmtime(os.path.join(args.checkpoint_dir, f)), reverse=True)

    # Pick the latest checkpoint file
    latest_checkpoint_file = checkpoint_files[0]

    # Load the checkpoint
    checkpoint = torch.load(os.path.join(args.checkpoint_dir, latest_checkpoint_file))

    # Load the model state from the checkpoint
    if args.model_type == 'wav2vec':
        model = W2V_GenreClassifier.load_from_checkpoint(checkpoint_path=os.path.join(args.checkpoint_dir, latest_checkpoint_file))
    elif args.model_type == 'vggish':
        model = VGGish_GenreClassifier.load_from_checkpoint(checkpoint_path=os.path.join(args.checkpoint_dir, latest_checkpoint_file))
    else:
        raise ValueError("Unsupported model type. Choose 'wav2vec' or 'vggish'.")

    # Create a trainer
    trainer = Trainer()

    # Evaluate the model on the validation set
    trainer.test(model, datamodule=data_module)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Genre Classification Training Script")
    
    # Add arguments
    parser.add_argument('--batch_size', type=int, default=config.BATCH_SIZE, help='Batch size for training')
    parser.add_argument('--epochs', type=int, default=config.EPOCHS, help='Number of epochs to train')
    parser.add_argument('--num_classes', type=int, default=config.NUM_CLASSES, help='Number of classes in the dataset')
    parser.add_argument('--checkpoint_dir', type=str, default=config.CHECKPOINT_DIR, help='Directory to save checkpoints')
    parser.add_argument('--learning_rate', type=float, default=config.LEARNING_RATE, help='Learning rate for the optimizer')
    parser.add_argument('--model_type', type=str, default='vggish', choices=['wav2vec', 'vggish'], help='Model type to use for training')
    
    
    args = parser.parse_args()
    
    main(args)
