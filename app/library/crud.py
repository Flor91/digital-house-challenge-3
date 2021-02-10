from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas
from .music_recognition import save_track, compute_features
from .spotify_utils import get_song_details, get_songs_in_playlist
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()


def get_song_by_url(db: Session, url: int):
    return db.query(models.Song).filter(models.Song.url == url).first()


def get_song_by_name(db: Session, name: str):
    return db.query(models.SpotifySong).filter(models.Song.name == name).first()


def get_songs(db: Session, skip: int = 0, limit: int = 100, q: Optional[str] = None):
    return db.query(models.SpotifySong).offset(skip).limit(limit).all()


def create_song(db: Session, song: schemas.SongCreate):
    filename = save_track(song.url)

    librosa_features = compute_features(filename)

    db_song = models.Song(name=song.name, url=song.url, filename=filename, librosa_features=librosa_features)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def create_spotify_song(db: Session, song: schemas.SpotifySongCreate):
    name, artist, url, audio_features = get_song_details(song.spotify_id)

    if url:
        try:
            searched_song = get_song_by_url(db, url)
            if searched_song:
                error_message = f"Song '{name}' by '{artist}' ID '{song.spotify_id}' already in database"
                print(error_message)
                return searched_song

            filename = save_track(url, name=name)

            librosa_features = compute_features(filename)

            db_song = models.SpotifySong(spotify_id=song.spotify_id, genre=song.genre, name=name, artist=artist, url=url,
                                         filename=filename, duration_ms=audio_features['duration_ms'],
                                         track_href=audio_features['track_href'], librosa_features=librosa_features)

            db_spotify_features = models.SpotifyAudioFeatures(song_id=db_song.id, spotify_song=db_song, acousticness=audio_features['acousticness'],
                                                              danceability=audio_features['danceability'], energy=audio_features['energy'],
                                                              instrumentalness=audio_features['instrumentalness'], key=audio_features['key'],
                                                              liveness=audio_features['liveness'], loudness=audio_features['loudness'],
                                                              mode=audio_features['mode'], speechiness=audio_features['speechiness'],
                                                              tempo=audio_features['tempo'], time_signature=audio_features['time_signature'],
                                                              valence=audio_features['valence'])

            db_song.spotify_features = db_spotify_features

            db.add(db_song)
            db.commit()
            db.refresh(db_song)
            return db_song
        except IntegrityError:
            db.rollback()
            error_message = f"Song '{name}' by '{artist}' ID '{song.spotify_id}' already in database"
            print(error_message)
            raise HTTPException(status_code=404, detail=error_message)
    else:
        error_message = f"There is no preview url for the song '{name}' by '{artist}' ID '{song.spotify_id}'"
        print(error_message)
        raise HTTPException(status_code=404, detail=error_message)


def create_songs_from_playlist(db: Session, playlist_id, genre):
    song_list = []
    tracks = get_songs_in_playlist(playlist_id)

    for track in tracks:
        if not get_song_by_url(db, track['uri']):
            try:
                song_schema = schemas.SpotifySongCreate(spotify_id=track['uri'], genre=genre)
                song = create_spotify_song(db, song_schema)
                song_list.append(song)
            except HTTPException:
                pass
    if len(song_list) > 0:
        return song_list
    else:
        raise HTTPException(status_code=404, detail=f"Playlist did not contain songs with preview_urls, "
                                                    f"or songs are already in the db")