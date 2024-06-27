from Dataset import Dataset
from typing import List, Tuple


class Collection:

    data = None
    plot_2d_selection = None
    genre_selection = None
    tempo_selection = None
    key_selection = None
    loudness_selection = None
    filters: List[Tuple[str, str]] = []

    @staticmethod
    def load():
        Collection.data = Dataset.get()
        Collection.plot_2d_selection = set()
        Collection.genre_selection = set()
        Collection.tempo_selection = set()
        Collection.key_selection = set()
        Collection.loudness_selection = set()

    @staticmethod
    def filter_indices_category(feature_name: str, category: str) -> List[int]:
        filtered_data = Collection.data[Collection.data[feature_name].isin([category])]
        return filtered_data.index.tolist()

    @staticmethod
    def update_filter(feature_name: str, category: str, indices: List[int] = None):
        present_categories = [j for i, j in Collection.filters if i == feature_name]
        if category in present_categories:
            Collection.remove_filter(feature_name, category, indices=indices)
            present_categories.remove(category)
        else:
            Collection.add_filter(feature_name, category, indices=indices)
            present_categories.append(category)

        selected_ids = Collection.get_filter_selection_ids()
        print(
            f"Length of selected ids after selecting a {feature_name}: {len(selected_ids)}"
        )
        return present_categories, selected_ids

    @staticmethod
    def add_filter(feature_name: str, category: str, indices: List[int] = None):
        Collection.filters.append((feature_name, category))

        if feature_name == "genre":
            filtered_indices = Collection.filter_indices_category(
                feature_name, category
            )
            Collection.genre_selection.update(filtered_indices)
        elif feature_name == "key":
            filtered_indices = Collection.filter_indices_category(
                feature_name, category
            )
            Collection.key_selection.update(filtered_indices)
        elif feature_name == "tempo":
            Collection.tempo_selection.update(indices)
        elif feature_name == "loudness":
            Collection.loudness_selection.update(indices)

    @staticmethod
    def remove_filter(feature_name: str, category: str, indices: List[int] = None):
        remove_idx = Collection.filters.index((feature_name, category))
        Collection.filters.pop(remove_idx)
        if feature_name == "genre":
            filtered_indices = Collection.filter_indices_category(
                feature_name, category
            )
            Collection.genre_selection.difference_update((filtered_indices))
        elif feature_name == "key":
            filtered_indices = Collection.filter_indices_category(
                feature_name, category
            )
            Collection.key_selection.difference_update((filtered_indices))
        elif feature_name == "tempo":
            Collection.tempo_selection.difference_update((indices))
        elif feature_name == "loudness":
            Collection.loudness_selection.difference_update((indices))

    @staticmethod
    def get_genre_selection():
        return Collection.data.loc[list(Collection.genre_selection)]

    @staticmethod
    def get_genre_selection_ids():
        return list(Collection.genre_selection)

    @staticmethod
    def get_tempo_selection():
        return Collection.data.loc[list(Collection.tempo_selection)]

    @staticmethod
    def get_tempo_selection_ids():
        return list(Collection.tempo_selection)

    @staticmethod
    def get_key_selection():
        return Collection.data.loc[list(Collection.key_selection)]

    @staticmethod
    def get_key_selection_ids():
        return list(Collection.key_selection)

    @staticmethod
    def get_loudness_selection():
        return Collection.data.loc[list(Collection.loudness_selection)]

    @staticmethod
    def get_loudness_selection_ids():
        return list(Collection.loudness_selection)

    @staticmethod
    def get_plot_2d_selection():
        return Collection.data.loc[list(Collection.plot_2d_selection)]

    @staticmethod
    def get_plot_2d_selection_ids():
        return list(Collection.plot_2d_selection)

    @staticmethod
    def get_filter_selection_ids():
        result = set(Collection.data.index.tolist())
        for filter in Collection.filters:
            if filter[0] == "genre":
                result = result & Collection.genre_selection
            elif filter[0] == "tempo":
                result = result & Collection.tempo_selection
            elif filter[0] == "key":
                result = result & Collection.key_selection
            elif filter[0] == "loudness":
                result = result & Collection.loudness_selection

        return list(result)

    @staticmethod
    def get_total_selection_ids():
        return list(
            Collection.genre_selection
            & Collection.tempo_selection
            & Collection.key_selection
            & Collection.loudness_selection
            & Collection.plot_2d_selection
        )
