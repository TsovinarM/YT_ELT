import requests
import json
from dotenv import load_dotenv   
import os

load_dotenv('./.env')

API_KEY = os.getenv('API_KEY')
CHANEL_HANDLE = 'MrBeast&key'

def get_video_count():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forHandle={CHANEL_HANDLE}={API_KEY}'

        responce = requests.get(url)
        responce.raise_for_status()
        data = responce.json()

        # print(json.dumps(data,indent = 4))

        # data.items[0].statistics.videoCount
        channel_items = data["items"][0]
        channel_videocount = channel_items["statistics"]["videoCount"]
        print(channel_videocount)
        return channel_videocount
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == '__main__':
    get_video_count()