import Dataset
from typing import List, Tuple

class Collection:

    data = None
    plot_2d_selection = None
    feature_selection = None


    @staticmethod
    def load():
        Collection.data = Dataset.get()
        Collection.plot_2d_selection = set()
        Collection.feature_selection = set()


    @staticmethod
    def filter_indices_category(feature_name: str, categories: List[str]) -> List[int]:
        filtered_data = Collection.data[Collection.data[feature_name].isin(categories)]
        return filtered_data.index.tolist()


    @staticmethod
    def add_category_filter(feature_name: str, categories: List[str]):
        filtered_indices = Collection.filter_indices_category(feature_name, categories)
        Collection.feature_selection.update(filtered_indices)
    

    @staticmethod
    def filter_indices_numerical(feature_name: str, intervals: List[Tuple[float, float]]) -> List[int]:
        all_intervals_indices = []
        for lb, ub in intervals:
            filtered_data = Collection.data[(Collection.data[feature_name] >= lb) & (Collection.data[feature_name] <= ub)]
            all_intervals_indices += filtered_data.index.tolist()
        return all_intervals_indices

    @staticmethod
    def add_numerical_filter(feature_name: str, intervals: List[Tuple[float, float]]):
        filtered_indices = Collection.filter_indices_numerical(feature_name, intervals)
        Collection.feature_selection.update(filtered_indices)


    @staticmethod
    def get_feature_selection():
        return Collection.data.loc[list(Collection.feature_selection)]


    @staticmethod
    def get_plot_2d_selection():
        return Collection.data.loc[list(Collection.plot_2d_selection)]
    