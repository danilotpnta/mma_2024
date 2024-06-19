from Dataset import Dataset
import numpy as np
import config

def get_similar_tracks(track_id, projection = 'UMAP'):
    d = Dataset.get()

    proj = None

    if projection == 'UMAP':
        x, y, z = d.loc[d['id'] == track_id, ['x_umap', 'y_umap', 'z_umap']].values[0]
        proj = 'umap'
    elif projection == 't-SNE':
        x, y, z = d.loc[d['id'] == track_id, ['x_tsne', 'y_tsne', 'z_tsne']].values[0]
        proj = 'tsne'
    else:
        raise Exception("Projection not found")

    d['distance'] = np.sqrt((d[f'x_{proj}'] - x)**2 + (d[f'y_{proj}'] - y)**2 + (d[f'z_{proj}'] - z)**2)

    similar_tracks = d.sort_values('distance').head(config.IMAGE_GALLERY_SIZE+1)['id'].to_list()
    similar_tracks.remove(track_id)
    
    return similar_tracks
