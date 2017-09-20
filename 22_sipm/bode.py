#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, c):
     return c

with open ("bode/sipm-fe-ch1_new.txt","r") as channel1:
    lines=channel1.readlines()
    result=[]
    for line in lines:
        result.append(line.strip().split('\t'))
result_cropped = result[11::]
frequency= []
log_mag = []
phase = []
for i in range(len(result_cropped)):
    frequency.append(result_cropped[i][5])
    log_mag.append(result_cropped[i][6])
    phase.append(result_cropped[i][7])


frequency=np.array(frequency,dtype="f")
log_mag=np.array(log_mag,dtype="f")
phase=np.array(phase,dtype="f")

with open ("bode/sipm-fe-ch2_new.txt","r") as channel2:
    lines=channel2.readlines()
    result2=[]
    for line in lines:
        result2.append(line.strip().split('\t'))
result_cropped2 = result2[11::]
frequency2= []
log_mag2 = []
phase2 = []
for i in range(len(result_cropped2)):
    frequency2.append(result_cropped2[i][5])
    log_mag2.append(result_cropped2[i][6])
    phase2.append(result_cropped2[i][7])


frequency2=np.array(frequency2,dtype="f")
log_mag2=np.array(log_mag2,dtype="f")
phase2=np.array(phase2,dtype="f")


fig = plt.figure(1)
fig.suptitle("Channel 1")
ax1 = fig.add_subplot(211)
ax1.semilogx(frequency, log_mag)
#~ ax1.plot(frequency, log_mag,'.')
ax1.grid(True)
ax1.set_title("Gain")
plt.xlabel("Frequenz [GHz]")
plt.ylabel("Gain [db]")
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_title("Phase")
ax2.plot(frequency, phase)
ax2.grid(True)
plt.xlabel("Frequenz [GHz]")
plt.ylabel("Phase [$^\circ$]")
plt.subplots_adjust(hspace=0.5, wspace=1.0)
#~ fig.tight_layout()





#~ print len(frequency)
print "-------------------------------"
print "Channel1"

popt,pcov=curve_fit(func,frequency[0:200],log_mag[0:200],p0=[12.])
print "Plateau",popt[0],"+-",np.sqrt(pcov[0][0])
print "Gain",10.**(popt[0]/20.),np.sqrt(pcov[0][0]*(popt[0]/20. *10.**(popt[0]/20. -1))**2.)

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
		

width_x=frequency[index]
print "Bandbreite",width_x*1000.,"MHz","+-",(frequency[index+1]-frequency[index])*1000.


#~ textstr = 'Plateau$=%.2f$\n=%.2f$\n$\sigma=%.2f$'%(mu, median, sigma)




ax1.axvline(ymin=min(log_mag),ymax=max(log_mag), x=width_x, linewidth=1, color = 'k')
plt.savefig("bode_channel1.pdf")


fig = plt.figure(2)
fig.suptitle("Channel 2")
ax3 = fig.add_subplot(211)
ax3.semilogx(frequency2, log_mag2)
ax3.grid(True)
ax3.set_title("Gain")
plt.xlabel("Frequenz [GHz]")
plt.ylabel("Gain [db]")
ax4 = fig.add_subplot(212, sharex=ax3)
ax4.set_title("Phase")
ax4.plot(frequency2, phase2)
ax4.grid(True)
plt.xlabel("Frequenz [GHz]")
plt.ylabel("Phase [$^\circ$]")
plt.subplots_adjust(hspace=0.5, wspace=1.0)





print "-------------------------------"
print "Channel2"

popt2,pcov2=curve_fit(func,frequency2[0:200],log_mag2[0:200],p0=[12.])
print "Plateau",popt2[0],"+-",np.sqrt(pcov2[0][0])
print "Gain",10.**(popt2[0]/20.),np.sqrt(pcov2[0][0]*(popt2[0]/20. *10.**(popt2[0]/20. -1))**2.)
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
print "Bandbreite",width_x2*1000,"MHz","+-",(frequency2[index2+1]-frequency2[index2])*1000.


ax3.axvline(ymin=min(log_mag2),ymax=max(log_mag2), x=width_x2, linewidth=2, color = 'k')
plt.savefig("bode_channel2.pdf")


frequency3=frequency
log_mag3=np.array(log_mag2-log_mag,dtype="f")
phase3=np.array(phase2-phase,dtype="f")



fig = plt.figure(3)
fig.suptitle("Channel 2 - Channel 1")
ax5 = fig.add_subplot(211)
ax5.semilogx(frequency3, log_mag3)
ax5.grid(True)
ax5.set_title("Gain")
plt.xlabel("Frequenz [GHz]")
plt.ylabel("Gain [db]")
ax6 = fig.add_subplot(212, sharex=ax5)
ax6.set_title("Phase")
ax6.plot(frequency3, phase3)
ax6.grid(True)
plt.xlabel("Frequenz [GHz]")
plt.ylabel("Phase [$^\circ$]")
plt.subplots_adjust(hspace=0.5, wspace=1.0)

print "-------------------------------"
print "Channel 2 - Channel 1"

popt3,pcov3=curve_fit(func,frequency[0:220],log_mag3[0:220],p0=[12.])
print "Plateau",popt3[0],"+-",np.sqrt(pcov3[0][0])
print "Gain",10.**(popt3[0]/20.),np.sqrt(pcov3[0][0]*(popt3[0]/20. *10.**(popt3[0]/20. -1))**2.)

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
#~ print "Bandbreite",width_x3,log_mag3[index3]*100
print "Bandbreite",width_x3*1000,"MHz","+-",(frequency3[index3+1]-frequency3[index3])*1000.
print "-------------------------------"


ax5.axvline(ymin=min(log_mag3),ymax=max(log_mag3), x=width_x3, linewidth=2, color = 'k')

plt.savefig("bode_channel2minus.pdf")


