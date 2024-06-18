from Dataset import Dataset
import numpy as np
import config

def get_similar_tracks(track_id, projection = 'UMAP'):
    d = Dataset.get()

    if projection == 'UMAP':
        x, y, z = d.loc[d['id'] == track_id, ['x_umap', 'y_umap', 'z_umap']].values[0]
    elif projection == 't-SNE':
        x, y, z = d.loc[d['id'] == track_id, ['x_tsne', 'y_tsne', 'z_tsne']].values[0]
        projection = 'tsne'
    else:
        raise Exception("Projection not found")
    
    projection = projection.lower()
    d['distance'] = np.sqrt((d[f'x_{projection}'] - x)**2 + (d[f'y_{projection}'] - y)**2 + (d[f'z_{projection}'] - z)**2)

    similar_tracks = d.sort_values('distance').head(config.IMAGE_GALLERY_SIZE+1)['id'].to_list()
    similar_tracks.remove(track_id)
    
    return similar_tracks
