import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import configparser
from json import JSONDecodeError


config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('SPOTIFY', 'username')
scope = config.get('SPOTIFY', 'scope')


def connect():
    os.environ['SPOTIPY_CLIENT_ID'] = config.get('SPOTIFY', 'SPOTIPY_CLIENT_ID')
    os.environ['SPOTIPY_CLIENT_SECRET'] = config.get('SPOTIFY', 'SPOTIPY_CLIENT_SECRET')
    os.environ['SPOTIPY_REDIRECT_URI'] = config.get('SPOTIFY', 'SPOTIPY_REDIRECT_URI')

    try:
        token = spotipy.util.prompt_for_user_token(username, scope)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = spotipy.util.prompt_for_user_token(username, scope)

    # Create Spotify object
    auth_manager = SpotifyClientCredentials()
    #sp = spotipy.Spotify(auth_manager=auth_manager)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return sp


def get_song_details(spotify_id):
    spotipy_connector = connect()
    track_info = spotipy_connector.track(spotify_id)
    artist = track_info['artists'][0]['name']
    name = track_info['name'].replace('/', '-')
    url = track_info['preview_url']

    audio_features = spotipy_connector.audio_features(spotify_id)[0]
    return name, artist, url, audio_features


def get_songs_in_playlist(playlist_id):
    spotipy_connector = connect()
    tracks = spotipy_connector.playlist_items(playlist_id)['items']
    return [i['track'] for i in tracks if i['track']['preview_url'] != None]


def main():
    connect()


if __name__ == "__main__":
    main()