import requests


def fetch_youtube_link(link):
    response = requests.get(f'https://api.song.link/v1-alpha.1/links?url={link}')
    if response.status_code == 200 and 'youtube' in response.json()['linksByPlatform']:
        return response.json()['linksByPlatform']['youtube']['url']
    return None
