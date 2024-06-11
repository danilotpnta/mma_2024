import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset
import librosa
import torch
import numpy as np
from . import preprocessing, audio_utils
import config

def preprocess_wav(file_path):
    # Load WAV file
    y, sr = librosa.load(file_path, sr=None)

    # Ensure the audio is mono
    if len(y.shape) > 1:
        y = np.mean(y, axis=1)
    
    # Resample to 16kHz if necessary
    if sr != 16000:
        y = librosa.resample(y, orig_sr=sr, target_sr=16000)

    # Convert to log-mel spectrogram
    mel_spec = librosa.feature.melspectrogram(y=y, sr=16000, n_mels=64, fmax=8000)
    log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

    # Ensure the shape is (1, 96, 64)
    if log_mel_spec.shape[1] < 96:
        pad_width = 96 - log_mel_spec.shape[1]
        log_mel_spec = np.pad(log_mel_spec, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        log_mel_spec = log_mel_spec[:, :96]

    log_mel_spec = log_mel_spec[np.newaxis, :, :]  # Add channel dimension
    return torch.tensor(log_mel_spec, dtype=torch.float32)

class AudioDataset(Dataset):
    def __init__(self, file_list, labels):
        self.file_list = file_list
        self.labels = labels

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        audio_path = self.file_list[idx]
        label = self.labels[idx]
        mel_spec = preprocess_wav(audio_path)
        if idx == 133297:
            print("133297", audio_path, label)

        elif idx == 108925:
            print("108925", audio_path, label)

        elif idx == 99134:
            print("099134", audio_path, label)


        return mel_spec, label

class GenreDataModule(pl.LightningDataModule):
    def __init__(self, batch_size=32):
        super().__init__()
        self.batch_size = batch_size

    def setup(self, stage=None):
        # Splitting the data
        data_splitted_dic = preprocessing.split_data(config.TRACKS_PATH)

        # Get paths and labels
        train_wav_paths, val_wav_paths, test_wav_paths = audio_utils.get_wav_paths(config.AUDIO_DIR, data_splitted_dic)
        train_labels, val_labels, test_labels = preprocessing.get_labels(data_splitted_dic)

        # Create datasets
        self.train_dataset = AudioDataset(train_wav_paths, train_labels)
        self.val_dataset = AudioDataset(val_wav_paths, val_labels)
        self.test_dataset = AudioDataset(test_wav_paths, test_labels)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False)
