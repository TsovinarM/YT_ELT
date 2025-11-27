import requests
import json
from dotenv import load_dotenv   
import os
from datetime import date

load_dotenv('./.env')

API_KEY = os.getenv('API_KEY')
CHANEL_HANDLE = 'MrBeast&key'
maxResults = 50

def get_playlist_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANEL_HANDLE}={API_KEY}'

        responce = requests.get(url)
        responce.raise_for_status()
        data = responce.json()

        # print(json.dumps(data,indent = 4))

        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistId)
        return channel_playlistId
    
    except requests.exceptions.RequestException as e:
        raise e



def get_video_ids(playlistId):
    video_ids = []
    pageToken = None
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}'
    # base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId=UUX6OQ3DkcsbYNE6H8uQQuVA&key={API_KEY}'

    try:
        while True:
            url = base_url
            
            if pageToken:
                url += f'&pageToken={pageToken}'
                
            responce = requests.get(url)
            responce.raise_for_status()
            data = responce.json()
            
            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
                print(1)
                
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e 




def extract_video_data(video_ids):
    extracted_data = []
    
    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id:video_id+batch_size]
    
    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ','.join(batch)
            url =  f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}' 
            
            responce = requests.get(url)
            responce.raise_for_status()
            data = responce.json()
            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDitails = item['contentDetails']
                statistics = item['statistics']
            
                video_data = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'publishedAt': snippet['publishedAt'],
                    'duration': contentDitails['duration'],
                    'viewCount': statistics.get('viewCount',None),
                    'likeCount': statistics.get('likeCount', None),
                    'commentCount': statistics.get('commentCount', None)
                }
        
                extracted_data.append(video_data)
        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e 


if __name__ == '__main__':
    playlistId = get_playlist_id() 
    video_ids = get_video_ids(playlistId)
    extract_video_data(video_ids)
