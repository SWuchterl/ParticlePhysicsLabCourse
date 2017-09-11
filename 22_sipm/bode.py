#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

with open ("bode/sipm__fe_ch1.txt","r") as channel1:
    lines=channel1.readlines()
    result=[]
    for line in lines:
        result.append(line.strip().split('\t'))
    result_cropped = result[11:-1]
    frequency= []
    log_mag = []
    phase = []
    print result_cropped[1][1]
    for i in range(len(result_cropped)):
        frequency[i] = result_cropped[i][1]
        log_mag[i] = result_cropped[i][2]
        phase[i] = result_cropped[i][3]
