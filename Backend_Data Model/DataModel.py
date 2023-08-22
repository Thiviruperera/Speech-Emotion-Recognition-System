# Main Libraries librosa - To abstract features of the audio files  / numpy - For linear algebraic operations
import os
import librosa as lR
import numpy as np
import pandas as pd

from glob import glob

# For read and write sound files as well as represent audio data as NumPy Array
import soundfile

import glob
from IPython import get_ipython
# get_ipython().magic("matplotlib inline")

# For Audio file visualization numpy and plt
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# SKLEARN Libraries
from sklearn.metrics._plot.tests.test_plot_confusion_matrix import y_pred
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib

# For Saving the model
import pickle


# File loading from the REVEDESS data set
from sklearn.semi_supervised.tests.test_self_training import y_test


def getFilesList(pathName):

    filesList = os.listdir(pathName)
    allFiles = list()

    for entry in filesList:

        fullPath = os.path.join(pathName,entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getFilesList(fullPath)

        else:
            allFiles.append(fullPath)

    return allFiles


pathName = "./speech-emotion-recognition-ravdess-data"
filesList = getFilesList(pathName)
len(filesList)
print("Number of Files in Data set : ", len(filesList))


# One Audio File Visualization if needed :
# audioFile, sfrq = lR.load(filesList[0])
# time = np.arange(0,len(audioFile)) / sfrq
# fig  , ax  = plt.subplots()
# ax.plot(time , audioFile)
# ax.set_xlabel("Time (s)")
# ax.set_ylabel("Sound Amplitute")
# plt.show()

# Audio files Visualization for All files - Use other codes from above
# for file in range (0 , len(filesList) , 1) :
#    audioFile , sfreq = lR.load(filesList[file])

#
# sampleRate , samples = wavfile.read(filesList[0])
# frequency , time , spectrogram = signal.spectrogram(samples , sampleRate)
# plt.pcolormesh(time , frequency , spectrogram)
# plt.imshow(spectrogram)
# plt.xlabel("Time (s)")
# plt.ylabel("Frequency (Hz)")
# plt.show()

# In depth visualization and plotting functions to be called later

# Redirect the cleaned files to another directory

# for feature extraction process
def extractFeatures(fileName , mfcc , chroma , mel) :
    with soundfile.SoundFile(fileName) as audioFile:

        X = audioFile.read(dtype="float32")
        sampleRate = audioFile.samplerate

        if chroma :
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


emotions = {'01': 'neutral', '02': 'calm', '03': 'happy', '04': 'sad', '05': 'angry', '06': 'fearful', '07': 'disgust', '08':'surprised'}
observedEmotions = ['neutral', 'calm', 'happy',  'angry', 'disgust', 'surprised']

# load the data to extract the features of the files
# x - Feature , Y - Emotion


def extractFilesFeatures(test_size = 0.25) :

    x,y = [] , []
    for file in glob.glob('C:\\Users\\SajanaNK\\PycharmProjects\\SDGP_SER\\Backend_Data Model\\speech-emotion-recognition-ravdess-data\\Actor_*\\*.wav') :
        fileName = os.path.basename(file)
        emotion = emotions[fileName.split("-")[2]]
        if emotion not in observedEmotions:
            continue
        feature = extractFeatures(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append([emotion, fileName])
    return train_test_split(np.array(x), y, test_size= test_size ,random_state=9)


# Splitting the Dataset
xTrain, xTest, yTrain, yTest = extractFilesFeatures(test_size=0.25)
#print(np.shape(xTrain), np.shape(xTest), np.shape(yTrain), np.shape(yTest))

yTestMap = np.array(yTest).T
yTest = yTestMap[0]
testFileName = yTestMap[1]

yTrainMap = np.array(yTrain).T
yTrain = yTrainMap[0]
trainFileName = yTrainMap[1]

#print(np.shape(yTrain), np.shape(yTest))
#print(*testFileName, sep='\n')


# Get or Observe the shape of the dataset
#print((xTrain[0], xTest[0]))

# Get number of features extracted
#print(f'Features extracted: {xTrain.shape[1]}')

# Initialize the Multi Layer Perceptron Classifier
model=MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)


# Fit/ Train model
#print("[Data Model] - Train the Model")
model.fit(xTrain, yTrain)


# Saving the model to a file for new testing data other than in data sheet
#print("[Data Model] - Saving the model .pkl format")
pklFileName = "Emotion_Detection_Model.pkl"

joblib.dump(model,"SERModel.pkl")

with open(pklFileName, 'wb') as file:
    pickle.dump(model, file)

# Loading the model back to the file
with open(pklFileName, 'rb') as file:
    emotionDetectionModel = pickle.load(file)

# emotionDetectionModel


# Prediction
yPred = emotionDetectionModel.predict(xTest)
# yPred


# Saving the prediction to a file
yPredl = pd.DataFrame(yPred, columns=['Predictions'])
yPredl['FileNames'] = testFileName
#print(yPredl)
yPredl.to_csv('PredictionFile.csv')

accuracy = accuracy_score(y_true=yTest, y_pred=yPred)
print("Accuracy: {:.2f}%".format(accuracy*100))

# For testing Purposes

# fileName = "2021-02-01T17_17_24.190Z.wav"
# ans = []
# newFeature = extractFeatures(fileName , mfcc=True, chroma=True, mel=True)
# ans.append(newFeature)
# ans = np.array(ans)
# emotionDetectionModel.predict(ans)
# print(emotionDetectionModel.predict(ans))

# pkl_file = "Emotion_Detection_Model.pkl"
# loaded_model = pickle.load(open(pkl_file,'rb'))
# result = loaded_model.score(xTest,yTest)
# print(result)

def predictionStuff(fileName):
    ans = []
    newFeature = extractFeatures(fileName , mfcc=True, chroma=True, mel=True)
    ans.append(newFeature)
    ans = np.array(ans)
    emotionDetectionModel.predict(ans)
    print(emotionDetectionModel.predict(ans))