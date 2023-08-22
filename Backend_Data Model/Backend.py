import os
import sys
from typing import Tuple

import numpy as np
import scipy.io.wavfile as wav
from speechpy.feature import mfcc

mean_signal_length = 32000  


def get_feature_vector_from_mfcc(file_path: str, flatten: bool,
                                 mfcc_len: int = 39) -> np.ndarray:

    fs, signal = wav.read(file_path)
    s_len = len(signal)
  
    if s_len < mean_signal_length:
        pad_len = mean_signal_length - s_len
        pad_rem = pad_len % 2
        pad_len //= 2
        signal = np.pad(signal, (pad_len, pad_len + pad_rem),
                        'constant', constant_values=0)
    else:
        pad_len = s_len - mean_signal_length
        pad_len //= 2
        signal = signal[pad_len:pad_len + mean_signal_length]
    mel_coefficients = mfcc(signal, fs, num_cepstral=mfcc_len)
    if flatten:
        # Flatten the data
        mel_coefficients = np.ravel(mel_coefficients)
    return mel_coefficients


def get_data(data_path: str, flatten: bool = True, mfcc_len: int = 39,
             class_labels: Tuple = ("Neutral", "Angry", "Happy", "Sad")) -> \
        Tuple[np.ndarray, np.ndarray]:

    data = []
    labels = []
    names = []
    cur_dir = os.getcwd()
    sys.stderr.write('curdir: %s\n' % cur_dir)
    os.chdir(data_path)
    for i, directory in enumerate(class_labels):
        sys.stderr.write("started reading folder %s\n" % directory)
        os.chdir(directory)
        for filename in os.listdir('.'):
            filepath = os.getcwd() + '/' + filename
            feature_vector = get_feature_vector_from_mfcc(file_path=filepath,
                                                          mfcc_len=mfcc_len,
                                                          flatten=flatten)
            data.append(feature_vector)
            labels.append(i)
            names.append(filename)
        sys.stderr.write("ended reading folder %s\n" % directory)
        os.chdir('..')
    os.chdir(cur_dir)
    return np.array(data), np.array(labels)


#################################################################################################
# For Connecting Backend to Data Model - FIle reading
# import joblib
# import soundfile
# import librosa as lR
#
# def extractFeatures(fileName , mfcc , chroma , mel) :
#     with soundfile.SoundFile(fileName) as audioFile:
#
#         X = audioFile.read(dtype="float32")
#         sampleRate = audioFile.samplerate
#
#         if chroma :
#             # stft - Short Time Fourier Transform
#             stft = np.abs(lR.stft(X))
#         result = np.array([])
#
#         if mfcc :
#             mfcc = np.mean(lR.feature.mfcc(y = X, sr=sampleRate , n_mfcc=40).T,axis = 0)
#             result = np.hstack((result,mfcc))
#         if chroma :
#             chroma = np.mean(lR.feature.chroma_stft(S = stft , sr = sampleRate).T,axis = 0)
#             result = np.hstack((result,chroma))
#         if mel :
#             mel = np.mean(lR.feature.melspectrogram(X,sr=sampleRate).T,axis = 0)
#             result = np.hstack((result,mel))
#         return result
#
# classifier = joblib.load("SERmodel.pkl")

# Using Flask

# from flask import Flask , request,redirect, url_for,flash,jsonify
#
# app = Flask(__name__)
#
# @app.route('/api/' , methods=['POST'])
# def makecalc():
#     data = request.get_json()
#     prediction = np.array2string(classifier.predict(ans))
#
#     return jsonify(prediction)
#
# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0')
#
# import requests
# import json
#
# url = 'http://0.0.0.0:5000/api/'
# j_data = json.dump(newFeature)
# headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
# r = requests.post(url,data=j_data,headers=headers)
# print(r,r.next)