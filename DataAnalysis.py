import urllib
import matplotlib.pyplot as plt
import csv
import sys
from math import *
from matplotlib import *
import numpy as np
from scipy import *
import scipy.signal as signal
import scipy.ndimage as ndimage
import matplotlib.pyplot as mp
from os import listdir
from os.path import isfile, join
import os.path
import time as tm
from statistics import mean, stdev

get_ipython().magic(u'matplotlib inline')

def zero_cross(x_arr, y_arr, filt):
    #Find zero-cross line
    ymax = max(y_arr)
    ymin = min(y_arr)
    alpha = 0.65
    zero_cross = alpha * (ymax-ymin) + ymin
    
    #Zero-Crossing Detection Algorithm
    step_counter = 0
    i = 1
    last = 0
    while i < len(y_arr):
        if float(y_arr[i]) > zero_cross and float(y_arr[i-1]) < zero_cross:
            if(filt == True):
                step_counter += 1
            elif(filt == False):
                if(float(x_arr[i]) > (last + .3)):
                    step_counter += 1
                    last = x_arr[i]
#                 print(step_counter)
        i += 1
    return step_counter

def fourier_transform(time, mag):
    
    magfft=np.fft.fft(magf, n=None, axis=-1)
    Ps=np.abs(magfft)**2
        
    time_step = time[len(time)-1]/(len(magfft)-1)
    freqs = np.fft.fftfreq(len(mag), time_step)
    idx = np.argsort(freqs)
    idxx = np.argsort(Ps[idx])

    freqsIdx = freqs[idx]
    psIdx = Ps[idx]
    freqsPos = []
    psPos = []
    i = 0
    while (i < len(freqsIdx)):
        if freqsIdx[i] > 0 and freqsIdx [i] < 2:
            freqsPos.append(freqsIdx[i])
            psPos.append(psIdx[i])
        i = i + 1
    c1=(time[len(time)-1]*np.abs(freqs[idx][idxx[len(idxx)-1]]))
    return c1

# Put the file name into correct array
def categorize_files(filesArray):
    for person in filesArray:
        for file in person:
            if "arm" in file:
                armFiles.append(file)
            elif "bridge" in file:
                bridgeFiles.append(file)
            elif "bicep" in file:
                bicepFiles.append(file)
            elif "crunch" in file:
                crunchFiles.append(file)
            elif "elbow" in file:
                elbowFiles.append(file)
            elif "lift" in file:
                liftFiles.append(file)
            elif "lunge" in file:
                lungeFiles.append(file)
            elif "pushup" in file:
                pushupFiles.append(file)
            elif "squat" in file:
                squatFiles.append(file)
            elif "upper" in file:
                upperFiles.append(file)

# Return which person the file is from
def getPerson(file):
    if "S10" in file:
        return "S10"
    elif "S11" in file:
        return "S11"
    elif "S12" in file:
        return "S12"
    elif "S13" in file:
        return "S13"
    elif "S14" in file:
        return "S14"
    elif "S15" in file:
        return "S15"
    elif "S16" in file:
        return "S16"
    elif "S17" in file:
        return "S17"
    elif "S18" in file:
        return "S18"
    elif "S1" in file:
        return "S1"
    elif "S2" in file:
        return "S2"
    elif "S3" in file:
        return "S3"
    elif "S4" in file:
        return "S4"
    elif "S5" in file:
        return "S5"
    elif "S6" in file:
        return "S6"
    elif "S7" in file:
        return "S7"
    elif "S8" in file:
        return "S8"
    elif "S9" in file:
        return "S9"

#Accelerometer data for each person
# Copied from File Array Creator
S1 = ['acc_S1arm1_0t.csv', 'acc_S1arm2_0t.csv', 'acc_S1bicep1_0t.csv', 'acc_S1bicep2_0t.csv', 'acc_S1bridge1_0t.csv', 'acc_S1bridge2_0t.csv', 'acc_S1crunch1_0t.csv', 'acc_S1crunch2_0t.csv', 'acc_S1elbow1_0t.csv', 'acc_S1elbow2_0t.csv', 'acc_S1lift1_0t.csv', 'acc_S1lift2_0t.csv', 'acc_S1lunge1_0t.csv', 'acc_S1lunge2_0t.csv', 'acc_S1pushup1_0t.csv', '', 'acc_S1squat1_0t.csv', 'acc_S1squat2_0t.csv', 'acc_S1upper1_0t.csv', 'acc_S1upper2_0t.csv']
S2 = ['acc_S2arm1_0t.csv', 'acc_S2arm2_0t.csv', 'acc_S2bicep1_0t.csv', 'acc_S2bicep2_0t.csv', 'acc_S2bridge1_0t.csv', 'acc_S2bridge2_0t.csv', 'acc_S2crunch1_0t.csv', 'acc_S2crunch2_0t.csv', 'acc_S2elbow1_0t.csv', 'acc_S2elbow2_0t.csv', 'acc_S2lift1_0t.csv', 'acc_S2lift2_0t.csv', 'acc_S2lunge1_0t.csv', 'acc_S2lunge2_0t.csv', 'acc_S2pushup1_0t.csv', '', 'acc_S2squat1_0t.csv', 'acc_S2squat2_0t.csv', 'acc_S2upper1_0t.csv', 'acc_S2upper2_0t.csv']
S3 = ['acc_S3arm1_0t.csv', 'acc_S3arm2_0t.csv', 'acc_S3bicep1_0t.csv', 'acc_S3bicep2_0t.csv', 'acc_S3bridge1_0t.csv', 'acc_S3bridge2_0t.csv', 'acc_S3crunch1_0t.csv', 'acc_S3crunch2_0t.csv', 'acc_S3elbow1_0t.csv', 'acc_S3elbow2_0t.csv', 'acc_S3lift1_0t.csv', 'acc_S3lift2_0t.csv', 'acc_S3lunge1_0t.csv', 'acc_S3lunge2_0t.csv', 'acc_S3pushup1_0t.csv', 'acc_S3pushup2_0t.csv', 'acc_S3squat1_0t.csv', 'acc_S3squat2_0t.csv', '', 'acc_S3upper2_0t.csv']
S4 = ['acc_S4arm1_0t.csv', 'acc_S4arm2_0t.csv', 'acc_S4bicep1_0t.csv', 'acc_S4bicep2_0t.csv', 'acc_S4bridge1_0t.csv', 'acc_S4bridge2_0t.csv', 'acc_S4crunch1_0t.csv', 'acc_S4crunch2_0t.csv', 'acc_S4elbow1_0t.csv', 'acc_S4elbow2_0t.csv', 'acc_S4lift1_0t.csv', 'acc_S4lift2_0t.csv', 'acc_S4lunge1_0t.csv', 'acc_S4lunge2_0t.csv', 'acc_S4pushup1_0t.csv', 'acc_S4pushup2_0t.csv', '', 'acc_S4squat2_0t.csv', 'acc_S4upper1_0t.csv', 'acc_S4upper2_0t.csv']
S5 = ['acc_S5arm1_0t.csv', 'acc_S5arm2_0t.csv', 'acc_S5bicep1_0t.csv', 'acc_S5bicep2_0t.csv', 'acc_S5bridge1_0t.csv', 'acc_S5bridge2_0t.csv', 'acc_S5crunch1_0t.csv', 'acc_S5crunch2_0t.csv', 'acc_S5elbow1_0t.csv', 'acc_S5elbow2_0t.csv', 'acc_S5lift1_0t.csv', 'acc_S5lift2_0t.csv', 'acc_S5lunge1_0t.csv', 'acc_S5lunge2_0t.csv', 'acc_S5pushup1_0t.csv', 'acc_S5pushup2_0t.csv', 'acc_S5squat1_0t.csv', 'acc_S5squat2_0t.csv', 'acc_S5upper1_0t.csv', 'acc_S5upper2_0t.csv']
S6 = ['acc_S6arm1_0t.csv', 'acc_S6arm2_0t.csv', 'acc_S6bicep1_0t.csv', 'acc_S6bicep2_0t.csv', 'acc_S6bridge1_0t.csv', 'acc_S6bridge2_0t.csv', 'acc_S6crunch1_0t.csv', 'acc_S6crunch2_0t.csv', 'acc_S6elbow1_0t.csv', 'acc_S6elbow2_0t.csv', 'acc_S6lift1_0t.csv', 'acc_S6lift2_0t.csv', 'acc_S6lunge1_0t.csv', 'acc_S6lunge2_0t.csv', 'acc_S6pushup1_0t.csv', 'acc_S6pushup2_0t.csv', 'acc_S6squat1_0t.csv', 'acc_S6squat2_0t.csv', 'acc_S6upper1_0t.csv', 'acc_S6upper2_0t.csv']
S7 = ['acc_S7arm1_0t.csv', 'acc_S7arm2_0t.csv', 'acc_S7bicep1_0t.csv', 'acc_S7bicep2_0t.csv', 'acc_S7bridge1_0t.csv', 'acc_S7bridge2_0t.csv', 'acc_S7crunch1_0t.csv', 'acc_S7crunch2_0t.csv', 'acc_S7elbow1_0t.csv', 'acc_S7elbow2_0t.csv', 'acc_S7lift1_0t.csv', 'acc_S7lift2_0t.csv', 'acc_S7lunge1_0t.csv', 'acc_S7lunge2_0t.csv', 'acc_S7pushup1_0t.csv', 'acc_S7pushup2_0t.csv', 'acc_S7squat1_0t.csv', 'acc_S7squat2_0t.csv', 'acc_S7upper1_0t.csv', 'acc_S7upper2_0t.csv']
S8 = ['acc_S8arm1_0t.csv', 'acc_S8arm2_0t.csv', 'acc_S8bicep1_0t.csv', 'acc_S8bicep2_0t.csv', 'acc_S8bridge1_0t.csv', 'acc_S8bridge2_0t.csv', 'acc_S8crunch1_0t.csv', 'acc_S8crunch2_0t.csv', 'acc_S8elbow1_0t.csv', 'acc_S8elbow2_0t.csv', 'acc_S8lift1_0t.csv', 'acc_S8lift2_0t.csv', 'acc_S8lunge1_0t.csv', 'acc_S8lunge2_0t.csv', 'acc_S8pushup1_0t.csv', 'acc_S8pushup2_0t.csv', 'acc_S8squat1_0t.csv', 'acc_S8squat2_0t.csv', 'acc_S8upper1_0t.csv', 'acc_S8upper2_0t.csv']
S9 = ['', 'acc_S9arm2_0t.csv', 'acc_S9bicep1_0t.csv', 'acc_S9bicep2_0t.csv', 'acc_S9bridge1_0t.csv', 'acc_S9bridge2_0t.csv', 'acc_S9crunch1_0t.csv', '', 'acc_S9elbow1_0t.csv', 'acc_S9elbow2_0t.csv', 'acc_S9lift1_0t.csv', 'acc_S9lift2_0t.csv', 'acc_S9lunge1_0t.csv', 'acc_S9lunge2_0t.csv', 'acc_S9pushup1_0t.csv', 'acc_S9pushup2_0t.csv', 'acc_S9squat1_0t.csv', 'acc_S9squat2_0t.csv', 'acc_S9upper1_0t.csv', 'acc_S9upper2_0t.csv']
S10 = ['acc_S10arm1_0t.csv', 'acc_S10arm2_0.csv', 'acc_S10bicep1_0.csv', 'acc_S10bicep2_0.csv', 'acc_S10bridge1_0.csv', 'acc_S10bridge2_0.csv', 'acc_S10crunch1_0.csv', 'acc_S10crunch2_0.csv', 'acc_S10elbow1_0.csv', 'acc_S10elbow2_0.csv', 'acc_S10lift1_0.csv', 'acc_S10lift2_0.csv', '', 'acc_S10lunge2_0.csv', '', '', 'acc_S10squat1_0.csv', 'acc_S10squat2_0.csv', 'acc_S10upper1_0.csv', '']
S11 = ['', 'acc_S11arm2_0.csv', 'acc_S11bicep1_0.csv', 'acc_S11bicep2_0.csv', 'acc_S11bridge1_0.csv', 'acc_S11bridge2_0.csv', 'acc_S11crunch1_0.csv', 'acc_S11crunch2_0.csv', 'acc_S11elbow1_0.csv', 'acc_S11elbow2_0.csv', 'acc_S11lift1_0.csv', 'acc_S11lift2_0.csv', 'acc_S11lunge1_0.csv', 'acc_S11lunge2_0.csv', 'acc_S11pushup1_0.csv', 'acc_S11pushup2_0.csv', 'acc_S11squat1_0.csv', 'acc_S11squat2_0.csv', 'acc_S11upper1_0.csv', 'acc_S11upper2_0.csv']
S12 = ['acc_S12arm1_0.csv', 'acc_S12arm2_0.csv', 'acc_S12bicep1_0.csv', 'acc_S12bicep2_0.csv', 'acc_S12bridge1_0.csv', 'acc_S12bridge2_0.csv', 'acc_S12crunch1_0.csv', 'acc_S12crunch2_0.csv', 'acc_S12elbow1_0.csv', 'acc_S12elbow2_0.csv', 'acc_S12lift1_0.csv', 'acc_S12lift2_0.csv', 'acc_S12lunge1_0.csv', 'acc_S12lunge2_0.csv', 'acc_S12pushup1_0.csv', '', 'acc_S12squat1_0.csv', 'acc_S12squat2_0.csv', 'acc_S12upper1_0.csv', 'acc_S12upper2_0.csv']
S13 = ['acc_S13arm1_0.csv', 'acc_S13arm2_0.csv', 'acc_S13bicep1_0.csv', 'acc_S13bicep2_0.csv', 'acc_S13bridge1_0.csv', 'acc_S13bridge2_0.csv', 'acc_S13crunch1_0.csv', 'acc_S13crunch2_0.csv', 'acc_S13elbow1_0.csv', 'acc_S13elbow2_0.csv', 'acc_S13lift1_0.csv', 'acc_S13lift2_0.csv', '', 'acc_S13lunge2_0.csv', 'acc_S13pushup1_0.csv', 'acc_S13pushup2_0.csv', 'acc_S13squat1_0.csv', 'acc_S13squat2_0.csv', 'acc_S13upper1_0.csv', 'acc_S13upper2_0.csv']
S14 = ['acc_S14arm1_0.csv', 'acc_S14arm2_0.csv', 'acc_S14bicep1_0.csv', 'acc_S14bicep2_0.csv', 'acc_S14bridge1_0.csv', 'acc_S14bridge2_0.csv', 'acc_S14crunch1_0.csv', 'acc_S14crunch2_0.csv', 'acc_S14elbow1_0.csv', 'acc_S14elbow2_0.csv', 'acc_S14lift1_0.csv', 'acc_S14lift2_0.csv', 'acc_S14lunge1_0.csv', 'acc_S14lunge2_0.csv', 'acc_S14pushup1_0.csv', 'acc_S14pushup2_0.csv', 'acc_S14squat1_0.csv', 'acc_S14squat2_0.csv', 'acc_S14upper1_0.csv', 'acc_S14upper2_0.csv']
S15 = ['acc_S15arm1_0.csv', 'acc_S15arm2_0.csv', 'acc_S15bicep1_0.csv', 'acc_S15bicep2_0.csv', 'acc_S15bridge1_0.csv', 'acc_S15bridge2_0.csv', 'acc_S15crunch1_0.csv', 'acc_S15crunch2_0.csv', 'acc_S15elbow1_0.csv', 'acc_S15elbow2_0.csv', 'acc_S15lift1_0.csv', 'acc_S15lift2_0.csv', 'acc_S15lunge1_0.csv', 'acc_S15lunge2_0.csv', 'acc_S15pushup1_0.csv', 'acc_S15pushup2_0.csv', 'acc_S15squat1_0.csv', 'acc_S15squat2_0.csv', 'acc_S15upper1_0.csv', 'acc_S15upper2_0.csv']
S16 = ['acc_S16arm1_0.csv', 'acc_S16arm2_0.csv', 'acc_S16bicep1_0.csv', 'acc_S16bicep2_0.csv', 'acc_S16bridge1_0.csv', 'acc_S16bridge2_0.csv', 'acc_S16crunch1_0.csv', 'acc_S16crunch2_0.csv', 'acc_S16elbow1_0.csv', 'acc_S16elbow2_0.csv', 'acc_S16lift1_0.csv', 'acc_S16lift2_0.csv', 'acc_S16lunge1_0.csv', 'acc_S16lunge2_0.csv', '', '', 'acc_S16squat1_0.csv', 'acc_S16squat2_0.csv', 'acc_S16upper1_0.csv', 'acc_S16upper2_0.csv']
S17 = ['acc_S17arm1_0.csv', 'acc_S17arm2_0.csv', 'acc_S17bicep1_0.csv', 'acc_S17bicep2_0.csv', 'acc_S17bridge1_0.csv', 'acc_S17bridge2_0.csv', 'acc_S17crunch1_0.csv', 'acc_S17crunch2_0.csv', 'acc_S17elbow1_0.csv', 'acc_S17elbow2_0.csv', 'acc_S17lift1_0.csv', 'acc_S17lift2_0.csv', 'acc_S17lunge1_0.csv', 'acc_S17lunge2_0.csv', 'acc_S17pushup1_0.csv', 'acc_S17pushup2_0.csv', 'acc_S17squat1_0.csv', 'acc_S17squat2_0.csv', 'acc_S17upper1_0.csv', 'acc_S17upper2_0.csv']
S18 = ['acc_S18arm1_0.csv', 'acc_S18arm2_0.csv', 'acc_S18bicep1_0.csv', 'acc_S18bicep2_0.csv', 'acc_S18bridge1_0.csv', 'acc_S18bridge2_0.csv', 'acc_S18crunch1_0.csv', 'acc_S18crunch2_0.csv', 'acc_S18elbow1_0.csv', 'acc_S18elbow2_0.csv', 'acc_S18lift1_0.csv', 'acc_S18lift2_0.csv', 'acc_S18lunge1_0.csv', 'acc_S18lunge2_0.csv', '', 'acc_S18pushup2_0.csv', 'acc_S18squat1_0.csv', 'acc_S18squat2_0.csv', 'acc_S18upper1_0.csv', 'acc_S18upper2_0.csv']
subdirectories = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18']
filesArray = [S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15,S16,S17,S18]

#Lists of file names for each exercise
armFiles = []
bicepFiles = []
bridgeFiles = []
crunchFiles = []
elbowFiles = []
liftFiles = []
lungeFiles = []
pushupFiles = []
squatFiles = []
upperFiles = []

# Lists for exercises and analysis techniques used for looping
exerciseList = ["arm", "bicep", "bridge", "crunch", "elbow", "lift", "lunge", "pushup", "squat", "upper"]
# T is Threshold Crossing
# LP is Threshold Crossing with Low Pass Filter
# F is Fourier Transform
analysisTechniqueList = ["T", "LP", "F"]

# Paths
mypath = "Accelerometer Data/"
results = "Accelerometer Data/CompleteResults.csv"
repetitionsFile = "Accelerometer Data/Repetitions.csv"

#List of actual repetition counts
repetitionsList = []

#Dictionary of files and repetitions
repetitionsDict = {}

#Dictionary of errors
errorsDict = {}

#Dictionary of average errors
RMSEDict = {}

#Put the files into correct list
categorize_files(filesArray)

#Get Repetition Data
with open(results, 'w', newline='') as f:
    csv_reader = csv.reader(open(repetitionsFile))
    for row in csv_reader:
        repetitionsList.append(row)
        
#Put each file name as the key into a dictionary with the repetition count as the value
exerciseCount = -1
for person in repetitionsList:
    exerciseCount = -1
    for exerciseRepetition in person:
        exerciseCount = exerciseCount + 1
        if exerciseRepetition != "":
            personIndex = repetitionsList.index(person)
            name = filesArray[personIndex][exerciseCount]
            repetitionsDict[name] = exerciseRepetition
            
#For each analysis technique
for analysisTechnique in range(3):
    percentErrorList = []
    for file, count in repetitionsDict.items():
        person = getPerson(file)
        csv_reader = csv.reader(open(mypath + person + '/' + file))
        #Get data and find magnitude
        verts = []

        for row in csv_reader:
            verts.append(row)

        time = []
        mag = []

        for vert in verts:
            time.append(float(vert[0])-float(verts[0][0]))
            mag.append(sqrt(float(vert[1])**2 + float(vert[2])**2 + float(vert[3])**2))
            #mag.append(float(vert[3]))

        mag= signal.detrend(mag)

        #Butterworth Filter
        N = 2 #Filter order
        fs = (len(mag)-1)/time[len(time)-1]
        Wn = 0.01*fs #Cutoff frequency
        B, A = signal.butter(N, Wn, output='ba')

        magf = signal.filtfilt(B,A, mag)


        #Calculate threshold crossing of the data
        if analysisTechnique == 0:
            #Threshold crossing
            c1=zero_cross(time, mag, False)
            #Get error from repetition
            error = abs(c1 - int(count))
            errorsDict["T" + file] = error
            percentError = (abs(c1 - int(count))/int(count) * 100)
            percentErrorList.append(percentError)
        elif analysisTechnique == 1:
            #Threshold crossing with low pass
            c1=zero_cross(time, magf, True)
            #Get error from repetition
            error = abs(c1 - int(count))
            errorsDict["LP" + file] = error
            percentError = (abs(c1 - int(count))/int(count) * 100)
            percentErrorList.append(percentError)
        elif analysisTechnique == 2:
            #Fourier Transform
            c1=fourier_transform(time, mag)
            #Get error from repetition
            error = abs(c1 - int(count))
            errorsDict["F" + file] = error
            percentError = (abs(c1 - int(count))/int(count) * 100)
            percentErrorList.append(percentError)
            
    #Print error   
    if analysisTechnique == 0:
        print("Threshold Percent: " + str(100 - mean(percentErrorList)))
    elif analysisTechnique == 1:
        print("Threshold Low Pass Percent: " + str(100 - mean(percentErrorList)))
    elif analysisTechnique == 2:
        print("Fourier Percent: " + str(100 - mean(percentErrorList)))
    

#Get the Root Mean Square Error of each exercise and analysis technique pair
for exercise in exerciseList:
    for analysisTechnique in analysisTechniqueList:
        selectedErrorsList = []
        for file, count in errorsDict.items():
            if exercise in file:
                if analysisTechnique in file:
                    selectedErrorsList.append(count*count)
        error = sqrt(mean(selectedErrorsList))
        RMSEDict[exercise + analysisTechnique] = error
        
#Get the Root Mean Square Error of exercsies
for exercise in exerciseList:
    selectedErrorsList = []
    for analysisTechnique in analysisTechniqueList:
        for file, error in errorsDict.items():
            if exercise in file:
                if analysisTechnique in file:
                    selectedErrorsList.append(error*error)
    std = sqrt(mean(selectedErrorsList))
    RMSEDict[exercise] = std
    
#Get the Root Mean Square Error of analysis techniques
for analysisTechnique in analysisTechniqueList:
    selectedErrorsList = []
    for exercise in exerciseList:
        for file, error in errorsDict.items():
            if exercise in file:
                if analysisTechnique in file:
                    selectedErrorsList.append(error*error)
    std = sqrt(mean(selectedErrorsList))
    RMSEDict[analysisTechnique] = std

#Write Error Table
with open(results, 'w', newline='') as f:
    a = csv.writer(f, delimiter=',')
    a.writerow(["Exercise", "Threshold", "ThresholdWithLowPass", "Fourier", "RMSE"])
    for exercise in exerciseList:
        a.writerow([exercise, RMSEDict[exercise + "T"], RMSEDict[exercise + "LP"], RMSEDict[exercise + "F"], RMSEDict[exercise]])
    a.writerow(["RMSE", RMSEDict["T"], RMSEDict["LP"], RMSEDict["F"]])
        
        
print("finished")
print("Check CompleteResults.csv in Accelerometer Data folder")