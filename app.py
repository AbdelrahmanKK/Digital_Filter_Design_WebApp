from flask import Flask, render_template , request, jsonify
import json
import cmath
import numpy
import csv
import scipy, scipy.signal

# open the file in read mode
filename = open('amazingECG.csv', 'r')
file = csv.DictReader(filename)
originalSignalAmplitude = []
originalSignalTime=[]
for col in file:
    originalSignalAmplitude.append(col['hart'])
    # originalSignalTime.append(col['time'])

for i in range(0, len(originalSignalAmplitude)):
    originalSignalAmplitude[i] = float(originalSignalAmplitude[i])

myZerosFromJS=[]
myPolesFromJS=[]
ZerosReadyForTheFilter=[]
PolesReadyForTheFilter=[]
numberOfPoints=0
global pointer  #this pointer is used to know the index i should return starting from 
pointer =0

filteredSignal=[]


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
     




@app.route('/end_stu_live_session',methods=["GET", "POST"])

def end_stu_live_session():
    ZerosReadyForTheFilter=[]
    PolesReadyForTheFilter=[]
    global pointer
    if request.method == 'POST':
        dataFromJson = request.json
        myZerosFromJS=dataFromJson["zeros"]
        
        myPolesFromJS=dataFromJson["poles"]
        numberOfPoints=dataFromJson["numberOfPoints"]
        for i in range (len(myZerosFromJS)):
            tempZero=complex(myZerosFromJS[i][0],(myZerosFromJS[i][1]))
            ZerosReadyForTheFilter.append(tempZero)

        for i in range (len(myPolesFromJS)):
            tempPole=complex(myPolesFromJS[i][0],(myPolesFromJS[i][1]))
            PolesReadyForTheFilter.append(tempPole)    
        # print(ZerosReadyForTheFilter)
        if (pointer>=len(originalSignalAmplitude)):
            pointer=0
        print(pointer)
        TheChunkToBeFiltered=originalSignalAmplitude[pointer:pointer+numberOfPoints]
        #TheChunkToBeFiltered=originalSignalAmplitude[0:300]
        pointer+=numberOfPoints
        if (len(ZerosReadyForTheFilter)==0):
            filteredSignal=TheChunkToBeFiltered
        else:
            b , a = scipy.signal.zpk2tf(ZerosReadyForTheFilter, PolesReadyForTheFilter, 1)
            filteredSignal=scipy.signal.lfilter(b, a, TheChunkToBeFiltered).tolist()


        filteredSignalArr = numpy.array(filteredSignal)#to array
        filteredSignal=filteredSignalArr.real.tolist()# to real back to list
 
        

    return jsonify(filteredSignal)
    # return render_template("index.html")

@app.route('/urlLopingOriginal',methods=["GET", "POST"])

def urlLopingOriginal():
   if request.method == 'POST':
        return jsonify(originalSignalAmplitude)

if __name__ =="__main__":
    app.run(debug=True)