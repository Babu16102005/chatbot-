import os, requests
from dotenv import load_dotenv
load_dotenv()
YT_KEY = os.getenv('YOUTUBE_API_KEY')

def search_youtube(query, max_results=5, lang='en'):
    # Uses YouTube Data API v3 (search.list + videos.list for stats)
    if not YT_KEY:
        # return stubbed results for dev
        return [
            {'title': f'{query} - Complete Tutorial', 'url':'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'views':'2.3M', 'videoId':'dQw4w9WgXcQ', 'language':lang},
            {'title': f'{query} - Quick Start', 'url':'https://www.youtube.com/watch?v=3JZ_D3ELwOQ', 'views':'1.1M', 'videoId':'3JZ_D3ELwOQ', 'language':lang},
        ]
    # call YouTube search API
    s_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {'part':'snippet', 'q':query, 'type':'video', 'maxResults': max_results, 'key': YT_KEY}
    r = requests.get(s_url, params=params, timeout=10)
    r.raise_for_status()
    items = r.json().get('items', [])
    video_ids = [it['id']['videoId'] for it in items]
    # fetch stats
    stats_url = 'https://www.googleapis.com/youtube/v3/videos'
    stat_params = {'part':'statistics', 'id':','.join(video_ids), 'key': YT_KEY}
    s2 = requests.get(stats_url, params=stat_params, timeout=10)
    s2.raise_for_status()
    stats_map = {v['id']: v['statistics'] for v in s2.json().get('items', [])}
    results = []
    for it in items:
        vid = it['id']['videoId']
        title = it['snippet']['title']
        url = f'https://www.youtube.com/watch?v={vid}'
        views = stats_map.get(vid, {}).get('viewCount', '0')
        results.append({'title': title, 'url': url, 'views': views, 'videoId': vid, 'language': it['snippet'].get('defaultAudioLanguage','en')})
    return results
