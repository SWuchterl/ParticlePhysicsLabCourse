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


frequency=np.array(frequency,dtype="f")
log_mag=np.array(log_mag,dtype="f")
phase=np.array(phase,dtype="f")

with open ("bode/sipm__fe_ch2.txt","r") as channel2:
    lines=channel2.readlines()
    result2=[]
    for line in lines:
        result2.append(line.strip().split('\t'))
result_cropped2 = result2[11::]
frequency2= []
log_mag2 = []
phase2 = []
for i in range(len(result_cropped2)):
    frequency2.append(result_cropped2[i][1])
    log_mag2.append(result_cropped2[i][2])
    phase2.append(result_cropped2[i][3])


frequency2=np.array(frequency2,dtype="f")
log_mag2=np.array(log_mag2,dtype="f")
phase2=np.array(phase2,dtype="f")


plt.figure(1)
ax1 = plt.subplot(211)
plt.semilogx(frequency, log_mag)
plt.grid(True)
plt.xlabel("Frequenz [GHz]")
ax2 = plt.subplot(212, sharex=ax1)
plt.plot(frequency, phase)
plt.grid(True)





#~ print len(frequency)

print "Channel1"

popt,pcov=curve_fit(func,frequency[0:200],log_mag[0:200],p0=[12.])
print "fit",popt,np.sqrt(pcov)
y_fit=[]
for i in xrange(len(frequency[0:200])):
	y_fit.append(popt)
y_fit=np.array(y_fit,dtype="f")

ax1.plot(frequency[0:200],y_fit)


width_y=popt[0]-3.

temp=10.
index=0
for i in xrange(len(frequency)):
	if(np.abs(width_y-log_mag[i])<temp):
		temp=np.abs(width_y-log_mag[i])
		index=i
		
#~ print index
width_x=frequency[index]
print "bandbreite",width_x


ax1.axvline(ymin=min(log_mag),ymax=max(log_mag), x=width_x, linewidth=2, color = 'k')
#~ plt.show()
plt.savefig("bode_channel1.pdf")

plt.figure(2)
ax3 = plt.subplot(211)
plt.semilogx(frequency2, log_mag2)
plt.grid(True)
plt.xlabel("Frequenz [GHz]")
ax4 = plt.subplot(212, sharex=ax3)
plt.plot(frequency2, phase2)
plt.grid(True)


print "channel2"

popt2,pcov2=curve_fit(func,frequency2[0:200],log_mag2[0:200],p0=[12.])
print "fit",popt2,np.sqrt(pcov2)
y_fit2=[]
for i in xrange(len(frequency2[0:200])):
	y_fit2.append(popt2)
y_fit2=np.array(y_fit2,dtype="f")

ax3.plot(frequency2[0:200],y_fit2)


width_y2=popt2[0]-3.
temp2=10.
index2=0
for i in xrange(len(frequency2)):
	if(np.abs(width_y2-log_mag2[i])<temp2):
		temp2=np.abs(width_y2-log_mag2[i])
		index2=i
		
width_x2=frequency2[index2]
print "breite2",width_x2


ax3.axvline(ymin=min(log_mag2),ymax=max(log_mag2), x=width_x2, linewidth=2, color = 'k')
#~ plt.show()
plt.savefig("bode_channel2.pdf")


frequency3=frequency
log_mag3=np.array(log_mag2-log_mag,dtype="f")
phase3=np.array(phase2-phase,dtype="f")





plt.figure(3)
ax5 = plt.subplot(211)
plt.semilogx(frequency3, log_mag3)
plt.grid(True)
plt.xlabel("Frequenz [GHz]")
ax6 = plt.subplot(212, sharex=ax5)
plt.plot(frequency3, phase3)
plt.grid(True)



print "channel2minus"

popt3,pcov3=curve_fit(func,frequency[0:220],log_mag3[0:220],p0=[12.])
print "fit",popt3,np.sqrt(pcov3)
y_fit3=[]
for i in xrange(len(frequency3[0:220])):
	y_fit3.append(popt3)
y_fit3=np.array(y_fit3,dtype="f")

ax5.plot(frequency3[0:220],y_fit3)


width_y3=popt3[0]-3.
temp3=10.
index3=0
for i in xrange(len(frequency3)):
	if(np.abs(width_y3-log_mag3[i])<temp3):
		temp3=np.abs(width_y3-log_mag3[i])
		index3=i
		
width_x3=frequency3[index3]
print "breite3",width_x3,log_mag3[index3]


ax5.axvline(ymin=min(log_mag3),ymax=max(log_mag3), x=width_x3, linewidth=2, color = 'k')











plt.savefig("bode_channel2minus.pdf")







