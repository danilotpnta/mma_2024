import os
import pandas
import config
import ast

class Dataset:

    data = None
    count = None
    attr_data = None

    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(config.DATASET_PATH)
        # Dataset.data = pandas.read_csv(config.DATASET_PATH).sample(frac=0.1, random_state=42)
        # Dataset.data.reset_index(drop=True, inplace=True)
        # Dataset.data.drop(columns=['id'], inplace=True)
        # Dataset.data['id'] = Dataset.data.index
        # Dataset.data['key'] = Dataset.data['keys'].map(lambda x: list(ast.literal_eval(x).keys())[0])

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
        return os.path.isfile(config.DATASET_PATH)

    @staticmethod
    def download():
        pass
