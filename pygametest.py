import display as window
import numpy as np
import matplotlib.pyplot as plt
import math 

# generic function
def readespfile(filename):
    file = open(filename, "r")
    count = 0
    data = []
    avs = []
    for line in file.readlines():
        if count % 2 == 0:
            avs.append(float((line.split(" ")[1])))
        else :
            data.append(int((line.split(" ")[1])))
        count += 1
    
    return (data, avs)

esp1_1m, esp1_1m_av = readespfile("calibration_1m_esp1.txt")
esp2_1m, esp2_1m_av = readespfile("calibration_1m_esp2.txt")
esp3_1m, esp3_1m_av = readespfile("calibration_1m_esp3.txt")

#Store the final data of averages as A

A_esp1 = esp1_1m_av[-1]
A_esp2 = esp2_1m_av[-1]
A_esp3 = esp3_1m_av[-1]

print("{}, {}, {}".format(A_esp1, A_esp2, A_esp3))

# extension on the general function so that it can parse data for 3 esps from same file

# generic function
def readespfile_all(filename):
    file = open(filename, "r")
    count = 0
    data = [[], [], []] 
    avs = [[], [], []]
    for line in file.readlines():
        splitdata = line.split(" ")
        esp = 0
        if count % 2 == 0:
            if splitdata[0] == "esp1rssi":
                esp = 1
            elif splitdata[0] == "esp2rssi":
                esp = 2
            elif splitdata[0] == "esp3rssi":
                esp = 3
            avs[esp-1].append(float(splitdata[1]))   
        else :
            if splitdata[0] == "esp1:":
                esp = 1
            elif splitdata[0] == "esp2:":
                esp = 2
            elif splitdata[0] == "esp3:":
                esp = 3
            data[esp-1].append(int(splitdata[1]))
        count += 1
    
    return (data, avs)

espdatas = {}

def getespdata(distances):
    espdatas[distances] = readespfile_all(distances + ".txt") 

n = 2

# Free space model
def dist(A, RSSI):
    return 10**((A-RSSI)/(10*n))

def getdistances(datas):
    getespdata(datas)

    esp1av = espdatas[datas][1][0][-1]
    esp2av = espdatas[datas][1][1][-1]
    esp3av = espdatas[datas][1][2][-1]

    esp1_d = dist(A_esp1, esp1av)
    esp2_d = dist(A_esp2, esp2av)
    esp3_d = dist(A_esp3, esp3av)

    window.show(esp1_d, esp2_d, esp3_d)

    return (esp1_d, esp2_d, esp3_d)

getdistances("3.59x5.3x2.6")