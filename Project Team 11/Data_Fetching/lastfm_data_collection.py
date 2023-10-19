import requests


API_KEY = '633e428ce3dee2b7f144fdaebf99fa31'

# Define the base URL for Last.fm API
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

# Function to fetch top tracks of a classical artist
def get_classical_artist_top_tracks(artist_name):
    params = {
        'method': 'artist.getTopTracks',
        'artist': artist_name,
        'api_key': API_KEY,
        'format': 'json'
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'toptracks' in data and 'track' in data['toptracks']:
            tracks = data['toptracks']['track']
            return tracks
    return []


if __name__ == '__main__':
    artist_name = 'Ludwig van Beethoven'  
    top_tracks = get_classical_artist_top_tracks(artist_name)
    
    if top_tracks:
        print(f"Top tracks for {artist_name}:")
        for i, track in enumerate(top_tracks, start=1):
            print(f"{i}. Track Name: {track['name']}, Playcount: {track['playcount']}")
    else:
        print(f"No data found for {artist_name}")
