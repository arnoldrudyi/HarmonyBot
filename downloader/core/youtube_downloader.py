import io
import requests

import pytubefix

from downloader.utils.logger_cogs import logger
from downloader.database.connect import SessionLocal
from downloader.models.audio import Audio


session = SessionLocal()


def fetch_audio_info(link):
    video = pytubefix.YouTube(link)
    audio = session.query(Audio).filter(Audio.url == video.video_id).first()
    if audio is None:
        thumbnail_bytecode = requests.get(video.thumbnail_url).content
        audio_bytecode = fetch_audio_bytecode(video)
        if audio_bytecode is not None:
            return {
                'title': video.title,
                'author': video.author,
                'length': video.length,
                'thumbnail': thumbnail_bytecode,
                'audio': audio_bytecode,
                'video_id': video.video_id
            }
        else:
            return None

    return {
        'unique_id': audio.unique_id
    }


def fetch_audio_bytecode(video):
    try:
        audio_bytecode_buffer = io.BytesIO()
        video.streams.get_by_itag(139).stream_to_buffer(audio_bytecode_buffer)
        bytecode = audio_bytecode_buffer.getvalue()
        audio_bytecode_buffer.close()

        return bytecode
    except Exception as e:
        logger.error(f'Error occurred while downloading the file: {repr(e)}')
        return None
