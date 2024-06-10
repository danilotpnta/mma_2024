import config
import audio_utils
from IPython.display import display
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder, LabelBinarizer
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

AUDIO_DIR = config.AUDIO_DIR

tracks = audio_utils.load(config.TRACKS_PATH)
features = audio_utils.load(config.FEATURES_PATH)
echonest = audio_utils.load(config.ECHONEST_PATH)

subset = tracks.index[tracks['set', 'subset'] <= 'small']
tracks = tracks.loc[subset]

train = tracks.index[tracks['set', 'split'] == 'training']
val = tracks.index[tracks['set', 'split'] == 'validation']
test = tracks.index[tracks['set', 'split'] == 'test']

def pre_process(tracks, features=None, columns=None):
    # Assign an integer value to each genre.
    encoder = LabelBinarizer()
    labels = tracks['track', 'genre_top']
   
    # Split in training, validation and testing sets.
    y_train = encoder.fit_transform(labels[train])
    y_val = encoder.transform(labels[val])
    y_test = encoder.transform(labels[test])

    # here VGGish features
    # X_train = features.loc[train, columns].to_numpy()
    # X_val = features.loc[val, columns].to_numpy()
    # X_test = features.loc[test, columns].to_numpy()
    
    # X_train, y_train = shuffle(X_train, y_train, random_state=42)
    
    # Standardize features by removing the mean and scaling to unit variance.
    scaler = StandardScaler(copy=False)
    # scaler.fit_transform(X_train)
    # scaler.transform(X_val)
    # scaler.transform(X_test)
    
    return y_train, y_val, y_test #, X_train, X_val, X_test

y_train, y_val, y_test = pre_process(tracks)
y_train = pd.DataFrame(y_train, index=train)
display(y_train)
y_val = pd.DataFrame(y_val, index=val)
display(y_val)
y_test = pd.DataFrame(y_test, index=test)
display(y_test)

