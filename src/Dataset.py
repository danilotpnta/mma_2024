import os
import pandas
import ast
from src.dataloaders import gtzan_loader
from src import config


class Dataset:

    data = None
    count = None
    attr_data = None

    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(config.SAMPLE_DATASET_PATH)

    @staticmethod
    def get():
        return Dataset.data

    @staticmethod
    def get_attr_data():
        return Dataset.attr_data

    @staticmethod
    def class_count():
        return Dataset.count

    @staticmethod
    def files_exist():
        return os.path.isfile(config.SAMPLE_DATASET_PATH)

    @staticmethod
    def fma_files_exist():
        mp3_dir = os.path.join(config.DATA_DIR, "fma_small")
        wav_dir = os.path.join(config.DATA_DIR, "fma_small_wav")
        return (
            os.path.isdir(mp3_dir)
            and os.path.isdir(wav_dir)
            and os.path.isdir(os.path.join(config.DATA_DIR, "fma_metadata"))
        )

    @staticmethod
    def download():
        gtzan_loader.load()
