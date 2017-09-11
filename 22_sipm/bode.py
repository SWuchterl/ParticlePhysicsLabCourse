#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, c):
     return c

with open ("bode/sipm__fe_ch1.txt","r") as channel1:
    lines=channel1.readlines()
    result=[]
    for line in lines:
        result.append(line.strip().split('\t'))
    result_cropped = result[11::]
    frequency= []
    log_mag = []
    phase = []
    for i in range(len(result_cropped)):
        frequency.append(result_cropped[i][1])
        log_mag.append(result_cropped[i][2])
        phase.append(result_cropped[i][3])

    ax1 = plt.subplot(211)
    plt.semilogx(frequency, log_mag)
    plt.grid(True)
    ax2 = plt.subplot(212, sharex=ax1)
    plt.plot(frequency, phase)
    plt.grid(True)
    plt.show()
