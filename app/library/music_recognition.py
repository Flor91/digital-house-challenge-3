import os
import logging

from pydub import AudioSegment
import requests
from urllib.parse import urlparse
from fastapi import HTTPException
import librosa
import librosa.display

import pandas as pd
import numpy as np
from scipy import stats
import skimage.io

import warnings

DOWNLOAD_FILES_FOLDER = 'static/songs/'


def is_downloadable(url):
    """
    Does the url contain a downloadable audio resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')

    if 'mpeg3' not in content_type.lower() and 'audio' not in content_type.lower():
        logging.error("Content type {content_type} not valid")
        raise HTTPException(status_code=404, detail=f"Content type {content_type} not valid")


def save_track(url, name=None):
    """
    Save the track file in local folder
    """
    is_downloadable(url)

    if name:
        filename = name + '.mp3'
        ext = 'mp3'
    else:
        a = urlparse(url)
        filename = os.path.basename(a.path)
        name, ext = filename.split(".")

    if os.path.isfile(DOWNLOAD_FILES_FOLDER + name + '.wav'):
        logging.info("File already exists")
    else:
        # Only download file if it does not exists in local folder
        r = requests.get(url, allow_redirects=True)
        open(DOWNLOAD_FILES_FOLDER + filename, 'wb').write(r.content)

        if ext != 'wav':
            # Convert the first 30 seconds of the track into wav file
            sound = AudioSegment.from_file(DOWNLOAD_FILES_FOLDER + filename)[:30*1000]
            sound.export(DOWNLOAD_FILES_FOLDER + name + ".wav", format="wav")

            os.remove(DOWNLOAD_FILES_FOLDER + filename)

    return name + ".wav"


def columns():
    feature_sizes = dict(chroma_stft=12, chroma_cqt=12, chroma_cens=12,
                         tonnetz=6, mfcc=20, rmse=1, zcr=1,
                         spectral_centroid=1, spectral_bandwidth=1,
                         spectral_contrast=7, spectral_rolloff=1)
    moments = ('mean', 'std', 'skew', 'kurtosis', 'median', 'min', 'max')

    columns = []
    for name, size in feature_sizes.items():
        for moment in moments:
            it = ((name, moment, '{:02d}'.format(i+1)) for i in range(size))
            columns.extend(it)

    names = ('feature', 'statistics', 'number')
    columns = pd.MultiIndex.from_tuples(columns, names=names)

    # More efficient to slice if indexes are sorted.
    return columns.sort_values()


def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled


def spectogram_image(y, sr, filename):
    mels = librosa.feature.melspectrogram(y=y, sr=sr)
    mels = np.log(mels + 1e-9)  # add small number to avoid log(0)

    # min-max scale to fit inside 8-bit range
    img = scale_minmax(mels, 0, 255).astype(np.uint8)
    img = np.flip(img, axis=0)  # put low frequencies at the bottom in image
    img = 255 - img  # invert. make black==more energy

    # save as PNG
    img_out = 'static/img/melspectrograms/' + filename.split('.')[0] + '.png'
    skimage.io.imsave(img_out, img)


def compute_features(filename):

    features = pd.Series(index=columns(), dtype=np.float32)

    # Catch warnings as exceptions (audioread leaks file descriptors).
    warnings.filterwarnings('error', module='librosa')

    def feature_stats(name, values):
        features[name, 'mean'] = np.mean(values, axis=1)
        features[name, 'std'] = np.std(values, axis=1)
        features[name, 'skew'] = stats.skew(values, axis=1)
        features[name, 'kurtosis'] = stats.kurtosis(values, axis=1)
        features[name, 'median'] = np.median(values, axis=1)
        features[name, 'min'] = np.min(values, axis=1)
        features[name, 'max'] = np.max(values, axis=1)

    try:
        filepath = DOWNLOAD_FILES_FOLDER + filename
        x, sr = librosa.load(filepath, sr=None, mono=True, duration=10)  # kaiser_fast

        #spectogram_image(x, sr, filename)

        f = librosa.feature.zero_crossing_rate(x, frame_length=2048, hop_length=512)
        feature_stats('zcr', f)

        cqt = np.abs(librosa.cqt(x, sr=sr, hop_length=512, bins_per_octave=12,
                                 n_bins=7*12, tuning=None))
        assert cqt.shape[0] == 7 * 12
        assert np.ceil(len(x)/512) <= cqt.shape[1] <= np.ceil(len(x)/512)+1

        f = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)
        feature_stats('chroma_cqt', f)
        f = librosa.feature.chroma_cens(C=cqt, n_chroma=12, n_octaves=7)
        feature_stats('chroma_cens', f)
        f = librosa.feature.tonnetz(chroma=f)
        feature_stats('tonnetz', f)

        del cqt
        stft = np.abs(librosa.stft(x, n_fft=2048, hop_length=512))
        assert stft.shape[0] == 1 + 2048 // 2
        assert np.ceil(len(x)/512) <= stft.shape[1] <= np.ceil(len(x)/512)+1
        del x

        f = librosa.feature.chroma_stft(S=stft**2, n_chroma=12)
        feature_stats('chroma_stft', f)

        f = librosa.feature.rms(S=stft)
        feature_stats('rmse', f)

        f = librosa.feature.spectral_centroid(S=stft)
        feature_stats('spectral_centroid', f)
        f = librosa.feature.spectral_bandwidth(S=stft)
        feature_stats('spectral_bandwidth', f)
        f = librosa.feature.spectral_contrast(S=stft, n_bands=6)
        feature_stats('spectral_contrast', f)
        f = librosa.feature.spectral_rolloff(S=stft)
        feature_stats('spectral_rolloff', f)

        mel = librosa.feature.melspectrogram(sr=sr, S=stft**2)
        del stft
        f = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
        feature_stats('mfcc', f)

    except Exception as e:
        print('{}: {}'.format(filename, repr(e)))

    return features.to_json()
