import os
import asyncio
import librosa
import argparse
import requests
import traceback
import threading
import numpy as np
import pandas as pd
from re import sub
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dashboard.src.utils.key_extractor import extract_keys
from dashboard.src.utils.metadata_collector import get_metadata
from dashboard.src.utils.feature_extractor import get_all_projections, predict_genre


# Thread-local storage for multiprocessing
thread_local = threading.local()


def get_session():

    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()

    return thread_local.session


# To combine predictions into one dictionary
def combine_dictionaries(dict_list):

    combined_dict = {}
    for d in dict_list:

        u = {d["label"]: d["score"]}

        combined_dict.update(u)

    return combined_dict


def process_file(filename, dir_img, default_img):

    try:

        y, sr = librosa.load(filename)

        # Key Extraction
        top_3_keys = extract_keys(y, sr)
        top_key = list(top_3_keys.keys())[0]

        # Song Metadata
        title, artists, cover_link = get_metadata(filename)

        # Saving the album cover
        cover_path = os.path.join(dir_img, os.path.basename(filename))
        cover_path = sub(".wav", ".jpg", cover_path)

        # Downloading (only if the file doesn't exist already)
        if not os.path.isfile(cover_path):
            session = get_session()

            if cover_link != 0:
                response = session.get(cover_link, timeout=20)

                if response.status_code == 200:  # If response is successful
                    with open(cover_path, "wb") as f:
                        f.write(response.content)
                else:
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
        print(f"File processed: {filename}")

        return {
            "filepath": filename,
            "keys": top_3_keys,
            "key": top_key,
            "album_cover_path": cover_path,
            "genre": genre,
            "pred_genres": predictions,
            "sorted_pred_genres": combine_dictionaries(predictions),
            "tempo": tempo,
            "title": title,
            "artist": artists,
            "loudness": mean_db,
        }

    except Exception as e:
        print(f"Error processing '{filename}': {e}")
        traceback.print_exc()

        return None


def generate_metadata(folder: str):

    print("Generating the Metadata. This may take a while...")

    # Column names
    columns = [
        "filepath",
        "keys",
        "key",
        "album_cover_path",
        "genre",
        "pred_genres",
        "sorted_pred_genres",
        "tempo",
        "title",
        "artist",
        "loudness",
    ]

    # Directories
    dir_wav = os.path.join("dashboard/data", folder)
    dir_img = os.path.join(dir_wav, "images")
    save_loc = os.path.join(dir_wav, f"metadata.csv")
    default_img = "data/album_cover.png"  # In case an image can't be downloaded

    # Creating the image directory
    Path(dir_img).mkdir(parents=True, exist_ok=True)

    # Collect filepaths
    filepaths = [
        os.path.join(dir_path, file)
        for dir_path, _, files in os.walk(dir_wav)
        for file in files
        if file.endswith(".wav")
    ]

    print(f"{len(filepaths)} files found! Generating metadata...")

    results = []
    with ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(process_file, filename, dir_img, default_img): filename
            for filename in filepaths
        }

        for future in as_completed(future_to_file):
            result = future.result()
            if result is not None:
                results.append(result)

    df = pd.DataFrame(results, columns=columns)
    df = df.reset_index(drop=True)

    # Getting the embeddings
    print("\nSong processing finished! Generating the embeddings...")
    xt, yt, zt, xu, yu, zu = get_all_projections(df)

    df["x_tsne"], df["y_tsne"], df["z_tsne"] = list(xt), list(yt), list(zt)
    df["x_umap"], df["y_umap"], df["z_umap"] = list(xu), list(yu), list(zu)

    # Renaming columns to remove the "dashboard" part
    df["filepath"] = df["filepath"].str.replace("dashboard/", "", regex=False)
    df["album_cover_path"] = df["album_cover_path"].str.replace(
        "dashboard/", "", regex=False
    )

    # Saving
    df.to_csv(save_loc, index_label="id")

    print(f"\nDataset processing finished! Dataframe saved to '{save_loc}'!\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_loc",
        type=str,
        default="gtzan",
        help="Folder containing the .wav files (please make a folder '/dashboard/data/[your_dataset_name]' and put the folder containing the .wav files in there).",
    )

    parsed_args = parser.parse_args()
    generate_metadata(parsed_args.data_loc)
