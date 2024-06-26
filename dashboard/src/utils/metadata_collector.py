import os
import asyncio
from shazamio import Shazam, HTTPClient
from aiohttp_retry import ExponentialRetry


async def async_get_metadata(filename: str):

    shazam = Shazam(
        http_client=HTTPClient(
            retry_options=ExponentialRetry(
                attempts=12, max_timeout=204.8, statuses={500, 502, 503, 504, 429}
            ),  # Workaround to Shazam API call limits
        ),
    )
    out = await shazam.recognize(filename)
    return out


def get_metadata(filename: str):

    # Workaround for Windows due to asyncio errors
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    metadata = asyncio.run(async_get_metadata(filename))

    if "track" not in metadata.keys():
        title = "Unknown Title"
        artists = "Unknown Artist"
        cover_link = 0
        return title, artists, cover_link

    result = metadata["track"]
    title = result["title"]
    artists = result["subtitle"]

    if "images" in result.keys():
        cover_link = result["images"]["coverart"]

    else:
        cover_link = 0

    if "," in artists:
        artists = f"'{artists}'"

    return title, artists, cover_link
