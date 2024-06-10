from torch.utils.data import DataLoader, Dataset
from utils import preprocessing, audio_utils
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



# Splitting the data
data_splitted_dic = preprocessing.split_data(config.TRACKS_PATH)

# Get loaders
train_wav_paths, val_wav_paths, test_wav_paths = audio_utils.get_wav_paths(config.AUDIO_DIR, data_splitted_dic)
train_labels, val_labels, test_labels = preprocessing.get_labels(data_splitted_dic)

train_dataset = AudioDataset(train_wav_paths, train_labels)
val_dataset = AudioDataset(val_wav_paths, val_labels)
test_dataset = AudioDataset(test_wav_paths, test_labels)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)