# -*- coding: utf-8 -*-
#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

time1 = np.loadtxt("results/time.txt")/(60.*60.) #convert to hours
time2 = np.loadtxt("results/time2.txt")/(60.*60.) #convert to hours
temp1 = np.loadtxt("results/temperature.txt")
temp2 = np.loadtxt("results/temperature2.txt")
current1 = np.loadtxt("results/current.txt")
current2 = np.loadtxt("results/current2.txt")
voltage1 = np.loadtxt("results/voltage.txt")
voltage2 = np.loadtxt("results/voltage2.txt")

t = [time1,time2]
temp = [temp1, temp2]
currents = [current1, current2]
voltage = [voltage1, voltage2]

for (time,temperature,filename) in zip(t, temp, ['first_measurement_temp', 'second_measurement_temp']):
    plt.figure(1)
    plt.title('Temperature during data taking')
    plt.xlabel("Time in hours")
    plt.ylabel("Temperature in [$^\circ$C]")
    plt.grid(True)
    plt.plot(time, temperature)
    plt.savefig(filename+".pdf", format = 'pdf')
    plt.clf()
    plt.close()

for (time,volt,filename) in zip(t, voltage, ['first_measurement_volt', 'second_measurement_volt']):
    plt.figure(1)
    plt.title('Bias voltage during data taking')
    plt.xlabel("Time in hours")
    plt.ylabel("Voltage in [mV]")
    plt.grid(True)
    plt.plot(time, volt)
    plt.savefig(filename+".pdf", format = 'pdf')
    plt.clf()
    plt.close()

for (time,current,filename) in zip(t, currents, ['first_measurement_current', 'second_measurement_current']):
    plt.figure(1)
    plt.title('Current during data taking')
    plt.xlabel("Time in hours")
    plt.ylabel("Current in [mA]")
    plt.grid(True)
    plt.plot(time, current)
    plt.savefig(filename+".pdf", format = 'pdf')
    plt.clf()
    plt.close()
