from enum import Enum
from pydantic import BaseModel, HttpUrl, Json


class GenreNames(str, Enum):
    jazz = "jazz"
    blues = "blues"
    rock = "rock"
    unknown = "unknown"


class SongBase(BaseModel):
    name: str
    genre: GenreNames = 'unknown'


class SongCreate(SongBase):
    url: HttpUrl


class Song(SongBase):
    id: int
    filename: str

    class Config:
        orm_mode = True


class SpotifyAudioFeatures(BaseModel):
    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: float
    speechiness: float
    tempo: float
    time_signature: int
    valence: float

    class Config:
        orm_mode = True


class SpotifySongCreate(BaseModel):
    spotify_id: str
    genre: str = 'unknown'


class SpotifySong(Song):
    name: str
    artist: str
    duration_ms: int
    spotify_features: SpotifyAudioFeatures

    class Config:
        orm_mode = True

