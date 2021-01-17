# digital-house-challenge-3

## Setup

1. Download project with `git clone https://github.com/[username]/digital-house-challenge-3.git`
    - To update changes from GH into local repo: 
        `git pull origin master`
    - Save local changes to github with:
        `git add [filenames]`
        `git commit -m '[Commit message]'`
        `Git push origin master`
2. Download fma dataset [fma_metadata.zip](https://os.unil.cloud.switch.ch/fma/fma_metadata.zip) in data/ folder
3. Python environment used: dhdsblend
    - To activate run `conda activate dhdsblend`
4. Install additional python libraries `pip install -r requirements.txt`


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

### Notebooks
- [Music Genre Classification with Python](https://towardsdatascience.com/music-genre-classification-with-python-c714d032f0d8)


### Data augmentation
- [Spotify API](https://developer.spotify.com/documentation/web-api/reference/tracks/)
