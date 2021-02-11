from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from .database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    filename = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True) # spotify_uri for spotify songs
    genre = Column(String, unique=False, index=True, default='unknown')
    librosa_features = Column(JSON, unique=False, index=False)

    __mapper_args__ = {
        'polymorphic_identity': 'spotify_songs'
    }


class SpotifySong(Song):
    __tablename__ = "spotify_songs"

    id = Column(Integer, ForeignKey('songs.id'), primary_key=True, index=True)
    spotify_id = Column(String, unique=True, index=True)
    artist = Column(String, unique=False, index=True)
    analysis_url = Column(String, unique=False, index=False)
    duration_ms = Column(Integer, unique=False, index=False)
    track_href = Column(String, unique=False, index=True)
    album_img = Column(String, unique=False, index=False)
    spotify_features = relationship("SpotifyAudioFeatures", back_populates="spotify_song", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'songs',
    }


class SpotifyAudioFeatures(Base):
    __tablename__ = "spotify_features"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey('spotify_songs.id'))
    spotify_song = relationship("SpotifySong", back_populates="spotify_features")
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    key = Column(Integer)
    liveness = Column(Float)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    tempo = Column(Float)
    time_signature = Column(Integer)
    valence = Column(Float)


