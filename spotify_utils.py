import os
import spotipy
from json.decoder import JSONDecodeError
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('SPOTIFY', 'username')
scope = config.get('SPOTIFY', 'scope')


def connect():
    # print(f' SPOTIFY '.center(80, '*'))
    try:
        token = spotipy.util.prompt_for_user_token(username, scope)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = spotipy.util.prompt_for_user_token(username, scope)

    # Create Spotify object
    return spotipy.Spotify(auth=token)





def main():
    os.environ['SPOTIPY_CLIENT_ID'] = config.get('SPOTIFY', 'SPOTIPY_CLIENT_ID')
    os.environ['SPOTIPY_CLIENT_SECRET'] = config.get('SPOTIFY', 'SPOTIPY_CLIENT_SECRET')
    os.environ['SPOTIPY_REDIRECT_URI'] = config.get('SPOTIFY', 'SPOTIPY_REDIRECT_URI')

    connect()


if __name__ == "__main__":
    main()