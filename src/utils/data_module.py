import pytorch_lightning as pl
from torch.utils.data import DataLoader, Dataset
from . import preprocessing, audio_utils
import config

class AudioDataset(Dataset):
    def __init__(self, file_list, labels):
        self.file_list = file_list
        self.labels = labels

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        audio = self.file_list[idx]
        label = self.labels[idx]
        return audio, label

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
