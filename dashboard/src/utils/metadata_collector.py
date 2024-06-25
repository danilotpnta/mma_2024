import asyncio
from shazamio import Shazam


def get_metadata(filename: str):

    # Running Shazamio
    async def main():
        shazam = Shazam()
        out = await shazam.recognize(filename)
        return out

    loop = asyncio.get_event_loop()
    metadata = loop.run_until_complete(main())

    # Getting the most important components
    if "track" not in metadata.keys():

        title = "Unknown Title"
        artists = "Unknown Artist"
        cover_link = "Not Found"

        return title, artists, cover_link

    result = metadata["track"]

    title = result["title"]
    artists = result["subtitle"]
    cover_link = result["images"]["coverart"]

    # Add quotation marks in case there are multiple artists
    if "," in artists:
        artists = f"'{artists}'"

    return title, artists, cover_link
