import os
import argparse
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from utils.data_module import GenreDataModule
from src.models.w2v_genre_classifier import W2V_GenreClassifier
from models.vgg_genre_classifier import VGGish_GenreClassifier
from transformers import AutoConfig
import config

def main(args):
    
    # Create DataModule
    data_module = GenreDataModule(batch_size=args.batch_size)

    # to do get config as:
    # https://www.kaggle.com/code/lujar1762/music-genre-classification-with-wav2vec2

    # model_name_or_path = "facebook/wav2vec2-base-100k-voxpopuli"
    # pooling_mode = "mean"
    # config = AutoConfig.from_pretrained(
    #     model_name_or_path,
    #     num_labels=8,
    #     label2id={label: i for i, label in enumerate(label_list)},
    #     id2label={i: label for i, label in enumerate(label_list)},
    #     finetuning_task="wav2vec2_clf",
    # )
    
    # Create model
    if args.model_type == 'wav2vec':
        model = W2V_GenreClassifier(config)
    elif args.model_type == 'vggish':
        model = VGGish_GenreClassifier()
    else:
        raise ValueError("Unsupported model type. Choose 'wav2vec' or 'vggish'.")
    
    # Ensure the checkpoints directory exists
    os.makedirs(args.checkpoint_dir, exist_ok=True)

    # Callbacks
    checkpoint_callback = ModelCheckpoint(
        dirpath=args.checkpoint_dir,
        filename=f'{args.model_type}-classifier-{{epoch:02d}}-{{val_loss:.2f}}',
        save_top_k=3,
        mode='min',
        monitor='val_loss'
    )
    
    early_stopping_callback = EarlyStopping(monitor='val_loss', patience=5, mode='min')
    
    # Trainer
    trainer = Trainer(
        max_epochs=args.epochs,
        callbacks=[checkpoint_callback, early_stopping_callback]
    )
    
    # Training
    trainer.fit(model, datamodule=data_module)
    
    # Testing
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
