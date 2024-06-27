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
        print(config.DATASET_PATH)
        Dataset.data = pandas.read_csv(config.DATASET_PATH).sample(frac=0.1, random_state=42)
        Dataset.data.reset_index(drop=True, inplace=True)
        Dataset.data.drop(columns=['id'], inplace=True)
        Dataset.data['id'] = Dataset.data.index
        Dataset.data['key'] = Dataset.data['keys'].map(lambda x: list(ast.literal_eval(x).keys())[0])

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
        gtzan_dir = os.path.join(config.DATA_DIR, "gtzan")
        return (
            os.path.isdir(gtzan_dir)
        )

    @staticmethod
    def download():
        gtzan_loader.load()
