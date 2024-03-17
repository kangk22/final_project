import json
import base64
import random
import keys
from requests import post, get

SPOTIFY_CLIENT_ID = keys.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = keys.SPOTIFY_CLIENT_SECRET

def get_token():
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        return None
    return json_result[0]

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def get_album_info(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_songs_in_album(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    return json_result

def get_random_album(albums):
    random_album = random.choice(albums)
    return random_album

def get_random_song(songs):
    random_song = random.choice(songs)
    return random_song

def check_song_in_album(token, album_id, song_name):
    songs = get_songs_in_album(token, album_id)
    for song in songs:
        if song['name'] == song_name:
            return True
    return False

if __name__ == "__main__":
    token = get_token()
    artist = search_for_artist(token, "My Chemical Romance")
    print("Artist: " + artist['name'])
    albums = get_albums_by_artist(token, artist['id'])
    random_album = get_random_album(albums)
    print("Album: " + random_album['name'])
    songs = get_songs_in_album(token, random_album['id'])
    random_song = get_random_song(songs)
    print("Song: " + random_song['name'])
    print("Audio: " + random_song['preview_url'])
