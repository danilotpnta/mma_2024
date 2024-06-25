import os
import shutil
import zipfile
import subprocess

# Path to download the dataset
dataset_path = "dashboard/data/gtzan"


# For setting up the Kaggle API token
def setup_kaggle_token():

    print("Setting up Kaggle API token...")
    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)

    kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")

    if not os.path.isfile(kaggle_json_path):
        kaggle_token_path = input(
            "Please provide your Kaggle API token. You can download it from https://www.kaggle.com/account\nEnter the path to the kaggle.json: "
        )
        os.makedirs(kaggle_dir, exist_ok=True)
        subprocess.run(["cp", kaggle_token_path, kaggle_json_path], check=True)
        os.chmod(kaggle_json_path, 0o600)
        print("Kaggle API token has been set up.")

    else:
        print("Kaggle API token has already been set up.")


# Downloading the GTZAN dataset
def download_gtzan_dataset():

    print("Downloading GTZAN dataset...")
    subprocess.run(
        [
            "kaggle",
            "datasets",
            "download",
            "-d",
            "andradaolteanu/gtzan-dataset-music-genre-classification",
            "--path",
            dataset_path,
        ],
        check=True,
    )

    archive_path = os.path.join(
        dataset_path, "gtzan-dataset-music-genre-classification.zip"
    )
    print("Download complete. Extracting dataset...")
    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(dataset_path)

    # Because everything is stored in a "Data" folder and that's not ideal, we take it out
    data_dir = os.path.join(dataset_path, "Data")
    if os.path.isdir(data_dir):

        for filename in os.listdir(data_dir):
            src_file = os.path.join(data_dir, filename)
            dest_file = os.path.join(dataset_path, filename)
            shutil.move(src_file, dest_file, copy_function=shutil.copy2)

        os.rmdir(data_dir)

    print("Dataset extracted to the 'gtzan' directory.")


if __name__ == "__main__":

    setup_kaggle_token()
    download_gtzan_dataset()
    print("Finished!")
