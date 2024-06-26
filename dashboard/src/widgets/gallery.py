import dash_bootstrap_components as dbc
from dash import html
from Dataset import Dataset

from utils.image_encoder import encode_image

import config


def create_gallery():
    return html.Div([], id='gallery', className='stretchy-widget border-widget gallery')

def create_gallery_children(track_ids):
    d = Dataset.get()
    image_rows = []
    image_id = 0
    for i in range(0, len(track_ids), config.IMAGE_GALLERY_ROW_SIZE):
        image_cols = []
        for j in range(config.IMAGE_GALLERY_ROW_SIZE):
            if i + j >= len(track_ids):
                break
            album_cover_path = d.loc[d['id'] == track_ids[i + j], 'filename'].map(lambda x: x.replace('wav', 'png')).values[0]
            try:
                image = open(album_cover_path, 'rb').read()
            except:
                print('Unable to open album cover')
                image = open('src/assets/album_cover.png', 'rb').read()
            class_name = d.loc[d['id'] == track_ids[i + j], 'title'].values[0]
            html_card = html.A([
                    html.Img(src=encode_image(image),className='gallery-image rounded border border-dark', style={'maxWidth': '60%'}),
                    html.Div(class_name, className='gallery-text')
                ], id={'type': 'gallery-card', 'index': class_name}, className='gallery-card'
            )
            image_cols.append(dbc.Col(html_card, className='gallery-col', width=3))
            image_id += 1
        image_rows.append(dbc.Row(image_cols, className='gallery-row', justify='start'))

    return image_rows