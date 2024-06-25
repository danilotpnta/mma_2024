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


# Function to get the embeddings from an audio file
def get_embeddings(file_path: str, model_name: str = "danilotpnta/HuBERT-Genre-Clf"):

    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    model = HubertForSequenceClassification.from_pretrained(model_name)

    try:
        # Load audio
        audio, _ = torchaudio.load(file_path)

        # Process the audio file
        inputs = feature_extractor(
            audio.squeeze().numpy(),
            sampling_rate=16000,
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
    umap_model = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=n_components,
        random_state=42,
    )
    embeddings_3d = umap_model.fit_transform(embeddings)

    # Extract the components
    df = pd.DataFrame(embeddings_3d, columns=["c1", "c2", "c3"])

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

    # Check for NaN or infinite values in the entire embedding matrix
    if np.any(np.isnan(embeddings)) or np.any(np.isinf(embeddings)):
        raise ValueError("Embedding matrix contains NaN or infinite values")

    print("Getting the t-SNE projections...")
    df_tsne = get_projections_tsne(embeddings)
    print("Getting the UMAP projections...")
    df_umap = get_projections_umap(embeddings)
    print("Done!")

    xt, yt, zt = df_tsne["c1"], df_tsne["c2"], df_tsne["c3"]
    xu, yu, zu = df_umap["c1"], df_umap["c2"], df_umap["c3"]

    return xt, yt, zt, xu, yu, zu


def predict_genre(file_path: str, model_name: str = "danilotpnta/HuBERT-Genre-Clf"):

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
    if folder_name in genre_list:
        genre = folder_name

    else:
        genre = predictions[0]["label"]

    return genre, predictions


# For testing and data refinement
if __name__ == "__main__":

    import ast

    path = "metadata.csv"
    df = pd.read_csv(path)

    df["embeddings"] = df["embeddings"].apply(lambda x: np.array(ast.literal_eval(x)))

    embeddings = []
    for embed in list(df["embeddings"]):
        embeddings.append(embed)

    embeddings = np.array(embeddings)
    df_tsne = get_projections_tsne(embeddings)
    df_umap = get_projections_umap(embeddings)

    xt, yt, zt = df_tsne["c1"], df_tsne["c2"], df_tsne["c3"]
    xu, yu, zu = df_umap["c1"], df_umap["c2"], df_umap["c3"]

    df["x_tsne"], df["y_tsne"], df["z_tsne"] = list(xt), list(yt), list(zt)
    df["x_umap"], df["y_umap"], df["z_umap"] = list(xu), list(yu), list(zu)

    df.to_csv("metadata_new.csv")
