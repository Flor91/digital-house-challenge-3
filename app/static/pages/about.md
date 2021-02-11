# Music Genre Recognition

<br>

![musica](../static/musica.jpeg)

<br>
Music genres are categories that have arisen through a complex interplay of cultures, artists, and market forces to characterize similarities between compositions and organize music collections.

## Notebooks

1. [Data Analysis](notebooks/Data%20Analysis.ipynb)
    - Exploracion y analisis de los datasets
    - Enriquecimiento de los datos
    - Limpieza de datos
    - Generacion de un unico dataset integrado y limpio
2. [Visualizaciones](notebooks/Visualizaciones.ipynb)
3. [Clasificacion](notebooks/Clasificacion_Avanzada.ipynb)
4. [Modelos y Resultados](notebooks/Modelos_y_resultados.ipynb)


## App

[Music Genre Recognition API](app/README.md) developed with [FastAPI](https://fastapi.tiangolo.com/)

- Full Docker integration (Docker based).
- Production ready Python web server using Uvicorn and Gunicorn. 
- Python FastAPI backend:
    - Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
    - Intuitive: Great editor support. Completion everywhere. Less time debugging.
    - Easy: Designed to be easy to use and learn. Less time reading docs.
    - Short: Minimize code duplication. Multiple features from each parameter declaration.
    - Robust: Get production-ready code. With automatic interactive documentation.
    - Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.
    - Many other features including automatic validation, serialization, interactive documentation, authentication with OAuth2 JWT tokens, etc.
- SQLAlchemy models (independent of Flask extensions, so they can be used with Celery workers directly).
- Alembic migrations.


## Data for Model training

The FMA aims to overcome this hurdle by providing 917 GiB and 343 days of Creative Commonslicensed audio from 106,574 tracks from 16,341 artists and 14,854 albums, arranged in a hierarchical taxonomy of 161 genres. It provides full-length and high-quality audio, pre-computed features, together with track- and user-level metadata, tags, and free-form text such as biographies.

- tracks.csv: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks.

- genres.csv: all 163 genres with name and parent (used to infer the genre hierarchy and top-level genres).

- features.csv: Nine audio features computed across time and summarized with seven statistics (mean, standard deviation, skew, kurtosis, median, minimum, maximum):
    1. Chroma, 84 attributes
    2. Tonnetz, 42 attributes
    3. Mel Frequency Cepstral Coefficient (MFCC), 140 attributes
    4. Spectral centroid, 7 attributes
    5. Spectral bandwidth, 7 attributes
    6. Spectral contrast, 49 attributes
    7. Spectral rolloff, 7 attributes
    8. Root Mean Square energy, 7 attributes
    9. Zero-crossing rate, 7 attributes


- echonest.csv: audio features provided by Spotify for a subset of 13,129 tracks. ([More info by Spotify](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-features))
    1. acousticness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
    2. danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
    3. Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
    4. instrumentalness: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
    5. liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
    6. speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
    7. tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.*
    8. valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).


## Setup

1. Download project with 
`git clone https://github.com/[username]/digital-house-challenge-3.git`
    - To update changes from GH into local repo: 
        `git pull origin master`
    - Save local changes to github with:
        `git add [filenames]`
        `git commit -m '[Commit message]'`
        `Git push origin master`
2. Download fma dataset [fma_metadata.zip](https://os.unil.cloud.switch.ch/fma/fma_metadata.zip) in data/ folder
3. Python environment used: dhdsblend
    - To activate run `conda activate dhdsblend`
4. Install additional python libraries `pip install -r app/requirements.txt`


To use Spotify API, create file named 'config.ini' with the following information:

```
[SPOTIFY]
username = 
scope = user-read-private user-read-playback-state user-modify-playback-state
SPOTIPY_CLIENT_ID = 
SPOTIPY_CLIENT_SECRET = 
SPOTIPY_REDIRECT_URI = https://google.com.ar
```

### Additional Python libraries

1. [Spotipy](https://spotifypy.readthedocs.io/en/latest/)
Spotify.py is a modern, friendly, and Pythonic API library for the Spotify API.

2. [Librosa](https://librosa.org/doc/latest/index.html)
It is a Python module to analyze audio signals in general but geared more towards music.


## Datasets a explorar:
- [GTZAN Music Genre Classification](https://www.kaggle.com/andradaolteanu/gtzan-dataset-music-genre-classification)
  - [Notebook > Genre Classification using Deep Learning](https://www.kaggle.com/imsparsh/gtzan-genre-classification-deep-learning-val-92-4?scriptVersionId=50852675)
- [FMA: A Dataset For Music Analysis](https://github.com/mdeff/fma)
- [Podcasts dataset](https://podcastsdataset.byspotify.com/)
- [Spotify Playlists](chrome-extension://klbibkeccnjlkjkiokjodocebajanakg/suspended.html#ttl=AIcrowd%20%7C%20Spotify%20Million%20Playlist%20Dataset%20Challenge%20%7C%20Challenges&pos=2287&uri=https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)
- [Spotify Datasets](https://research.atspotify.com/datasets/)

### Data augmentation
- [Spotify API](https://developer.spotify.com/documentation/web-api/reference/tracks/)
