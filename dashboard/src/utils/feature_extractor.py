import ast
import umap
import torch
import torchaudio
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.manifold import TSNE
from transformers import (
    pipeline,
    Wav2Vec2FeatureExtractor,
    HubertForSequenceClassification,
)
from transformers.utils import logging


# Function to get the embeddings from an audio file
def get_embeddings(
    file_path: str,
    model_name: str = "danilotpnta/HuBERT-Genre-Clf",
    duration: int = 30,
    target_sr: int = 16000,
):

    # Disable HuggingFace warnings
    logging.set_verbosity_error()

    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    model = HubertForSequenceClassification.from_pretrained(model_name)

    try:
        # Load audio
        audio, sample_rate = torchaudio.load(file_path)

        # Resample the audio if not 16000
        if sample_rate != target_sr:
            audio = torchaudio.functional.resample(
                audio, orig_freq=sample_rate, new_freq=target_sr
            )

        # Convert audio to mono
        if audio.shape[0] > 1:
            audio = torch.mean(audio, dim=0, keepdim=True)

        # Get ideal duration
        num_samples = target_sr * duration

        # Adjust the audio length to be exactly `duration` seconds
        if audio.shape[1] > num_samples:
            audio = audio[:, :num_samples]

        else:
            padding = num_samples - audio.shape[1]
            audio = torch.nn.functional.pad(audio, (0, padding))

        # Process the audio file
        inputs = feature_extractor(
            audio.squeeze().numpy(),
            sampling_rate=target_sr,
            return_tensors="pt",
            padding=True,
        )

        with torch.no_grad():
            # Get the embeddings from the model
            outputs = model(**inputs, output_hidden_states=True)

        # Extract the hidden states
        hidden_states = outputs.hidden_states

        # Select the desired hidden state (e.g., the last hidden state)
        embeddings = hidden_states[-1].squeeze().numpy()

        # Mean pooling
        mean_embeddings = np.mean(embeddings, axis=0)

        # Check for NaN or infinite values
        if np.any(np.isnan(mean_embeddings)) or np.any(np.isinf(mean_embeddings)):
            return None, "Embedding contains NaN or infinite values"

        return mean_embeddings, None

    except Exception as e:
        return None, str(e)


# To deal with NaNs
def clean_embeddings(embeddings):
    # Replace NaN or infinite values with zeros or some other value
    if np.any(np.isnan(embeddings)) or np.any(np.isinf(embeddings)):

        print("Found NaNs or infinite values in embeddings. Replacing them with zeros.")
        embeddings = np.nan_to_num(embeddings, nan=0.0, posinf=0.0, neginf=0.0)

    return embeddings


def get_projections_tsne(
    embeddings: np.array,
    perplexity: int = 30,  # Between 5 and 50
    lr: int = 200,
    n_iter: int = 4000,
):

    # Ensure there are no NaN or infinite values
    if np.any(np.isnan(embeddings)) or np.any(np.isinf(embeddings)):
        raise ValueError("Embeddings contain NaN or infinite values")

    # Check for the number of samples, because perplexity has to be lower than it
    if embeddings.shape[0] <= perplexity:
        perplexity = 5

    # Perform t-SNE with adjusted parameters
    tsne_2d = TSNE(
        n_components=2,
        perplexity=perplexity,
        learning_rate=lr,
        n_iter=n_iter,
        random_state=42,
    )
    embeddings_2d = tsne_2d.fit_transform(embeddings)

    tsne = TSNE(
        n_components=3,
        perplexity=perplexity,
        learning_rate=lr,
        n_iter=n_iter,
        random_state=42,
    )
    embeddings_3d = tsne.fit_transform(embeddings)

    # Extract the components
    df = pd.DataFrame(embeddings_3d, columns=["c1", "c2", "c3"])
    df_2d = pd.DataFrame(embeddings_2d, columns=["c4", "c5"])
    df = pd.concat([df, df_2d], axis=1)

    return df


def get_projections_umap(
    embeddings: np.array,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    n_components: int = 3,
):

    # Check for the number of samples, because n_neighbors has to be lower than it
    if embeddings.shape[0] <= n_neighbors:
        n_neighbors = 2

    # Ensure there are no NaN or infinite values
    if np.any(np.isnan(embeddings)) or np.any(np.isinf(embeddings)):
        raise ValueError("Embeddings contain NaN or infinite values")

    # Perform UMAP with adjusted parameters
    umap_2d = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=2,
        random_state=42,
    )
    embeddings_2d = umap_2d.fit_transform(embeddings)

    umap_model = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        random_state=42,
    )
    embeddings_3d = umap_model.fit_transform(embeddings)

    # Extract the components
    df = pd.DataFrame(embeddings_3d, columns=["c1", "c2", "c3"])
    df_2d = pd.DataFrame(embeddings_2d, columns=["c4", "c5"])
    df = pd.concat([df, df_2d], axis=1)

    return df


def get_all_projections(
    df: pd.DataFrame, model_name: str = "danilotpnta/HuBERT-Genre-Clf"
):

    embeddings = []

    # Iterate over each track to get the embeddings
    print("Extracting the embeddings for all songs...")
    for _, row in df.iterrows():
        filepath = row["filepath"]
        embedding, error_msg = get_embeddings(filepath, model_name)
        if error_msg is not None:
            print(f"Error with file {filepath}: {error_msg}")
            embeddings.append(np.zeros(768))  # Placeholder for invalid embeddings

        else:
            embeddings.append(embedding)

    embeddings = np.array(embeddings)

    # Clean embeddings
    embeddings = clean_embeddings(embeddings)

    print("Getting the t-SNE projections...")
    df_tsne = get_projections_tsne(embeddings)
    print("Getting the UMAP projections...")
    df_umap = get_projections_umap(embeddings)
    print("Done!")

    xt, yt, zt, x2t, y2t = (
        df_tsne["c1"],
        df_tsne["c2"],
        df_tsne["c3"],
        df_tsne["c4"],
        df_tsne["c5"],
    )
    xu, yu, zu, x2u, y2u = (
        df_umap["c1"],
        df_umap["c2"],
        df_umap["c3"],
        df_umap["c4"],
        df_umap["c5"],
    )

    return xt, yt, zt, x2t, y2t, xu, yu, zu, x2u, y2u


def predict_genre(file_path: str, model_name: str = "danilotpnta/HuBERT-Genre-Clf"):

    # Disable HuggingFace warnings
    logging.set_verbosity_error()

    pipe = pipeline("audio-classification", model=model_name)

    # Supported genres
    genre_list = [
        "blues",
        "classical",
        "country",
        "disco",
        "hiphop",
        "jazz",
        "metal",
        "pop",
        "reggae",
        "rock",
    ]

    # Get the predictions (get the top 3)
    predictions = pipe(file_path)[:3]

    folder_name = Path(file_path).parts[-2].lower()

    # If the folder names contain the supported genre names (i.e., in GTZAN), then use that
    if folder_name in genre_list:
        genre = folder_name

    # Otherwise just use the predictions
    else:
        genre = predictions[0]["label"]

    return genre, predictions


def string_to_np_array(string):

    cleaned_string = string.strip("[]")  # Step 1: Remove brackets
    elements = cleaned_string.split()  # Step 2: Split into elements

    return np.array(elements, dtype=float)  # Step 3: Convert to NumPy array


# For testing and data refinement
if __name__ == "__main__":

    path = "metadata.csv"
    df = pd.read_csv(path)

    df["embeddings"] = df["embeddings"].apply(lambda x: string_to_np_array(x))

    embeddings = []
    for embed in list(df["embeddings"]):
        embeddings.append(embed)

    embeddings = np.array(embeddings)

    print("Getting projections...")
    df_tsne = get_projections_tsne(embeddings)
    df_umap = get_projections_umap(embeddings)

    xt, yt, zt, x2t, y2t = (
        df_tsne["c1"],
        df_tsne["c2"],
        df_tsne["c3"],
        df_tsne["c4"],
        df_tsne["c5"],
    )
    xu, yu, zu, x2u, y2u = (
        df_umap["c1"],
        df_umap["c2"],
        df_umap["c3"],
        df_umap["c4"],
        df_umap["c5"],
    )

    df["x_tsne"], df["y_tsne"], df["z_tsne"], df["x_2tsne"], df["y_2tsne"] = (
        list(xt),
        list(yt),
        list(zt),
        list(x2t),
        list(y2t),
    )
    df["x_umap"], df["y_umap"], df["z_umap"], df["x_2umap"], df["y_2umap"] = (
        list(xu),
        list(yu),
        list(zu),
        list(x2u),
        list(y2u),
    )

    print("Saving...")
    df.to_csv("metadata_new.csv")  # Adjust name
