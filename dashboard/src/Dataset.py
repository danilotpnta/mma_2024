import os
import pandas
import config


class Dataset:

    data = None
    count = None
    attr_data = None

    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(config.DATASET_PATH)
        Dataset.data = Dataset.data.sample(frac=0.1)

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
