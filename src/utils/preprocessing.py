import config
from utils import audio_utils
from sklearn.preprocessing import LabelBinarizer

def split_data(tracks_path):

    tracks = audio_utils.load(tracks_path)
    subset = tracks.index[tracks['set', 'subset'] <= 'small']
    tracks = tracks.loc[subset]

    train = tracks.index[tracks['set', 'split'] == 'training']
    val = tracks.index[tracks['set', 'split'] == 'validation']
    test = tracks.index[tracks['set', 'split'] == 'test']
    labels = tracks['track', 'genre_top']

    data_splitted_dic = {
                        'train': train,
                        'val': val,
                        'test': test,
                        'labels': labels
                    }

    return data_splitted_dic

def get_labels(data):

    train = data['train']
    val = data['val']
    test = data['test']
    labels = data['labels']

    encoder = LabelBinarizer()
   
    # Split in training, validation and testing sets.
    train_labels = encoder.fit_transform(labels[train])
    val_labels = encoder.transform(labels[val])
    test_labels = encoder.transform(labels[test])
    
    return train_labels, val_labels, test_labels


if __name__ == '__main__':

    train_labels, val_labels, test_labels = get_labels(config.TRACKS_PATH)

def compute_embeddings(inputs, model):
    return model.forward(inputs)