import os
import joblib
import soundfile
import librosa as lR
import numpy as np
import requests
import json
from flask import Flask , request,redirect, url_for,flash,jsonify
from librosa.core import stft
import matplotlib.pyplot as plt
from scipy.io import wavfile

import pandas
import pickle

# fileName = "2021-02-01T17_17_24.190Z.wav"
# fileName = "2021-03-21_18-47-32.wav"
fileName = "./Test_Files/2021-03-21_16-15-02.wav"
pkl_file = "Emotion_Detection_Model.pkl"

from pydub import AudioSegment
audio = AudioSegment.from_file(fileName)
print("DURATION IN SECONDS : " ,audio.duration_seconds , "LEN : " , len(fileName))


from pydub import AudioSegment
sound = AudioSegment.from_file(fileName)

start = 0
fileNumber = 1

tempArray = []
tempInt = 0

if(audio.duration_seconds < 60):
    print("len//5")
    for i in range(len(fileName) // 5, int(audio.duration_seconds) + len(fileName) // 5, len(fileName) // 5):
        part = sound[start * 1000: i * 1000]
        start = start + len(fileName) // 5

        if(fileNumber < 10):
            part.export("./temp_files/file_0" + str(fileNumber) + ".wav", format="wav")
        else:
            part.export("./temp_files/file_" + str(fileNumber) + ".wav", format="wav")

        tempInt = len(fileName) // 5
        fileNumber = fileNumber + 1

elif (audio.duration_seconds < 180 and audio.duration_seconds > 60):
    for i in range(len(fileName) // 10, int(audio.duration_seconds) + len(fileName) // 10 , len(fileName) // 10 ):
        part = sound[start * 1000: i * 1000]
        tempArray.append(start)
        start = start + len(fileName) // 10

        if (fileNumber < 10):
            part.export("./temp_files/file_0" + str(fileNumber) + ".wav", format="wav")
        else:
            part.export("./temp_files/file_" + str(fileNumber) + ".wav", format="wav")

        tempInt = len(fileName) // 10
        fileNumber = fileNumber + 1

else:
    print("len//20")
    for i in range(len(fileName) // 20, int(audio.duration_seconds) + len(fileName) // 20, len(fileName) // 20):
        part = sound[start * 1000: i * 1000]
        start = start + len(fileName) // 20

        if (fileNumber < 10):
            part.export("./temp_files/file_0" + str(fileNumber) + ".wav", format="wav")
        else:
            part.export("./temp_files/file_" + str(fileNumber) + ".wav", format="wav")

        tempInt = len(fileName) // 20
        fileNumber = fileNumber + 1


def getFileList() :
    files = os.listdir("./temp_files")
    return files


def extractFeatures(fileName , mfcc , chroma , mel) :
    with soundfile.SoundFile(fileName) as audioFile:

        X = audioFile.read(dtype="float32")
        sampleRate = audioFile.samplerate

        if chroma:
            # stft - Short Time Fourier Transform
            stft = np.abs(lR.stft(X))
        result = np.array([])

        if mfcc :
            mfcc = np.mean(lR.feature.mfcc(y = X, sr=sampleRate , n_mfcc=40).T,axis = 0)
            result = np.hstack((result,mfcc))
        if chroma :
            chroma = np.mean(lR.feature.chroma_stft(S = stft , sr = sampleRate).T,axis = 0)
            result = np.hstack((result,chroma))
        if mel :
            mel = np.mean(lR.feature.melspectrogram(X,sr=sampleRate).T,axis = 0)
            result = np.hstack((result,mel))
        return result


classifier = joblib.load("SERmodel.pkl")
newFeature = extractFeatures(fileName, mfcc=True, chroma=True, mel=True)
ans = []
ans.append(newFeature)
ans = np.array(ans)


test = []

fileList = getFileList()
fileList.sort()


for file in fileList:
    insideTest = []

    features = extractFeatures("./temp_files/"+file, mfcc=True, chroma=True, mel=True)
    insideTest.append(features)
    insideTest = np.array(insideTest)
    test.append(insideTest)

Dict = {}


app = Flask(__name__)

# @app.route('/getFile', methods=['GET'])
# def getFile():
#


@app.route('/api/getData' , methods=['GET'])
def makecalc():
    data = request.get_json()

    for i in range(0, len(test)):
        pr = np.array2string(classifier.predict(test[i]))

        print("File Name : " + fileList[i] + "  ", pr)

        clpr = str(pr).replace('[', '')
        clpr = clpr.replace("]", '')
        clpr = clpr.replace("'", '')

        if (i == len(test) - 1):
            Dict[tempArray[i] + tempInt] = clpr
        else:
            Dict[tempArray[i + 1]] = clpr

    result = []
    for k,v in Dict.items() :
        result.append({'TimeFrame' : k , 'Emotion' : v})

    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

url = 'http://0.0.0.0:5000/api/'
j_data = json.dump(newFeature)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url,data=j_data,headers=headers)
print(r,r.next)
