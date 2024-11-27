from pytubefix import Search

from downloader.utils.logger_cogs import logger


def fetch_soundcloud_audio(link: str):
    try:
        video = Search(link.split('/')[4]).results[0]
        return video.video_id
    except Exception as e:
        logger.error(e)
