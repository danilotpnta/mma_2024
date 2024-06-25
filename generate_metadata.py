import os
import librosa
import argparse
import requests
import traceback
import numpy as np
import pandas as pd
from re import sub
from pathlib import Path
from transformers.utils import logging
from dashboard.src.utils.key_extractor import extract_keys
from dashboard.src.utils.metadata_collector import get_metadata
from dashboard.src.utils.feature_extractor import get_all_projections, predict_genre


def generate_metadata(folder: str):

    print("Generating the Metadata. This may take a while...")

    # Column names
    columns = [
        "keys",
        "key",
        "album_cover_path",
        "genre",
        "genres",
        "tempo",
        "title",
        "artist",
        "loudness",
    ]

    # Directories
    dir_wav = os.path.join("dashboard\data", folder)
    dir_img = os.path.join(dir_wav, "images")
    save_loc = os.path.join(dir_wav, f"metadata_{folder}.csv")
    default_img = "data/plain_cover.jpg"  # In case an image can't be downloaded

    # Creating the image directory
    Path(dir_img).mkdir(parents=True, exist_ok=True)

    # For the filepaths
    filepaths = []

    df_dict = {}
    for dir_path, _, files in os.walk(dir_wav):
        for file in files[:1]:
            if file.endswith(".wav"):

                # Get the filepath
                filename = os.path.join(dir_path, file)
                try:
                    y, sr = librosa.load(filename)

                    # Filepath
                    filepaths.append(filename)

                    # Key Extraction
                    top_3_keys = extract_keys(y, sr)
                    top_key = list(top_3_keys.keys())[0]

                    #  Song Metadata
                    title, artists, cover_link = get_metadata(filename)

                    # Saving the album cover
                    cover_path = os.path.join(dir_img, file)
                    cover_path = sub(".wav", ".jpg", cover_path)

                    # Downloading
                    if cover_link != "Not Found":
                        response = requests.get(cover_link)
                        if response.status_code == 200:

                            with open(cover_path, "wb") as f:
                                f.write(response.content)

                        else:
                            print(
                                f"Failed to download image. Status code: {response.status_code}"
                            )
                            cover_path = default_img

                    else:
                        cover_path = default_img

                    # Loudness in dB
                    rms = librosa.feature.rms(y=y)
                    rms_db = librosa.amplitude_to_db(rms, ref=np.max)
                    mean_db = np.mean(rms_db)

                    # Tempo
                    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
                    if isinstance(tempo, np.ndarray):
                        tempo = tempo.item()

                    tempo = round(tempo, 2)

                    # Get the genre
                    genre, predictions = predict_genre(filename)

                    # Adding to the dictionary
                    df_dict[filename] = [
                        top_3_keys,
                        top_key,
                        cover_path,
                        genre,
                        predictions,
                        tempo,
                        title,
                        artists,
                        mean_db,
                    ]

                    print(f"Processed file: '{file}'")

                except Exception as e:
                    print(f"Error processing '{filename}': {e}")
                    traceback.print_exc()  # For more robust error showing
                    continue

    df = pd.DataFrame.from_dict(df_dict, orient="index", columns=columns)
    df.reset_index(drop=True, inplace=True)  # Use integer index instead of filepath
    df["filepath"] = filepaths

    # Getting the embeddings
    print("\nSong processing finished! Generating the embeddings...")
    xt, yt, zt, xu, yu, zu = get_all_projections(df)

    df["x_tsne"], df["y_tsne"], df["z_tsne"] = list(xt), list(yt), list(zt)
    df["x_umap"], df["y_umap"], df["z_umap"] = list(xu), list(yu), list(zu)

    # Saving
    df.to_csv(save_loc, index_label="index")

    print(f"\nDataset processing done! Saved to '{save_loc}'!\n")


if __name__ == "__main__":

    # Disable HuggingFace warnings
    logging.set_verbosity_error()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_loc",
        type=str,
        default="gtzan",
        help="Folder containing the .wav files (please make a folder '/dashboard/data/[your_dataset_name]' and put the folder containing the .wav files in there).",
    )

    parsed_args = parser.parse_args()

    generate_metadata(parsed_args.data_loc)
