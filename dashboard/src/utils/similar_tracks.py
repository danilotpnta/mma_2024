import config
import numpy as np
from Dataset import Dataset


def get_similar_tracks(track_id, proj):
    d = Dataset.get()

    if proj == "umap":
        x, y, z = d.loc[d["id"] == track_id, ["x_umap", "y_umap", "z_umap"]].values[0]
    elif proj == "tsne":
        x, y, z = d.loc[d["id"] == track_id, ["x_tsne", "y_tsne", "z_tsne"]].values[0]
    else:
        raise Exception("Projection not found")

    d["distance"] = np.sqrt(
        (d[f"x_{proj}"] - x) ** 2
        + (d[f"y_{proj}"] - y) ** 2
        + (d[f"z_{proj}"] - z) ** 2
    )

    similar_tracks = (
        d.sort_values("distance").head(config.IMAGE_GALLERY_SIZE + 1)["id"].to_list()
    )
    similar_tracks.remove(track_id)

    return similar_tracks
