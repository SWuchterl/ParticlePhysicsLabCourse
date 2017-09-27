import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

dataMean=[]
dataErr=[]
lengthMax=0.
times=[0.108,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.2,1.4,1.6,1.8,2.,2.3,2.6,2.9,3.2,3.5,3.8,4.1,4.4,4.72,5.,5.52,6.,6.52,7.,7.52,8.,8.52,9.,9.5,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.]
# times=[0.123,0.215,0.315,0.43,0.515,0.615,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.,2.3,2.6,2.9,3.2,3.5,3.8,4.1,4.4,4.72,5.,5.52,6.,6.52,7.,7.52,8.,8.52,9.,9.5,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.]
# erTimes=[0.002,0.002,0.002,0.004,0.004,0.004,0.004,0.004,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
erTimes=[0.004,0.004,0.004,0.004,0.004,0.004,0.004,0.004,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
for i in range(1,46):
    temp=np.loadtxt("time_calibration/"+str(i)+".TKA",skiprows=2)
    length=len(temp)
    lengthMax=length
    x=np.linspace(0,length,length)
    plt.figure()
    # plt.yscale("log")
    plt.xlabel("channel number")
    plt.ylabel("N")
    plt.title("")
    plt.grid()
    tempMax=np.max(temp)
    tempMaxIndex=np.argmax(temp)


    if (i==1):
        bin_means, bin_edges, binnumber = stats.binned_statistic(x[0:tempMaxIndex+100],temp[0:tempMaxIndex+100],statistic='mean', bins=100)
    else:
        if(i==45):
            bin_means, bin_edges, binnumber = stats.binned_statistic(x[tempMaxIndex-100:],temp[tempMaxIndex-100:],statistic='mean', bins=100)
        else:

            bin_means, bin_edges, binnumber = stats.binned_statistic(x[tempMaxIndex-100:tempMaxIndex+100],temp[tempMaxIndex-100:tempMaxIndex+100],
                statistic='mean', bins=100)
            # plt.plot(x[tempMaxIndex-100:tempMaxIndex+100],temp[tempMaxIndex-100:tempMaxIndex+100],".")
            # tempMean=np.average(x[tempMaxIndex-100:tempMaxIndex+100],weights=temp[tempMaxIndex-100:tempMaxIndex+100])
            # tempStd=np.sqrt(np.average((x[tempMaxIndex-100:tempMaxIndex+100]-tempMean)**2.,weights=temp[tempMaxIndex-100:tempMaxIndex+100]))
            # tempErr=tempStd/np.sqrt(sum(temp[tempMaxIndex-100:tempMaxIndex+100]))
    plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], colors='g', lw=2)
    binCenter = bin_edges[:-1]+(bin_edges[1:]-bin_edges[:-1])/2.
    tempMean=np.average(binCenter,weights=bin_means)
    tempStd=np.sqrt(np.average((binCenter-tempMean)**2.,weights=bin_means))
    tempErr=tempStd/np.sqrt(sum(binCenter))

    plt.axvline(tempMean+tempErr,0.,tempMax,color='orange',alpha=0.2,lw=0.5)
    plt.axvline(tempMean-tempErr,0.,tempMax,color='orange',alpha=0.2,lw=0.5)
    plt.axvline(tempMean,0.,tempMax,color='red',alpha=0.8,lw=0.5)
    dataMean.append(tempMean)
    dataErr.append(tempErr)
    plt.savefig("time_channels/"+str(i)+".pdf")
    plt.close()


def func(x,a,b):
    return a*x+b


times=np.array(times)
# times=times+0.015
erTimes=np.array(erTimes)
erTimes=np.array(erTimes)/np.sqrt(12.)*2.
dataMean=np.array(dataMean)
dataErr=np.array(dataErr)


popt,pcov=curve_fit(func,dataMean,times)
# popt,pcov=curve_fit(func,dataMean,times,sigma=erTimes)
print popt[0],"+-",np.sqrt(pcov[0][0])
print popt[1],"+-",np.sqrt(pcov[1][1])

x_linspace=np.linspace(0.,lengthMax,lengthMax)
y_fit=func(dataMean,popt[0],popt[1])
y_res=times-y_fit
y_linspace=func(x_linspace,popt[0],popt[1])

def chi2(y_exp,y_obs,y_err):
    return sum(((y_obs-y_exp)**2.)/(y_err**2.))

errNewY=np.sqrt(erTimes**2. +(popt[0]*dataErr)**2.)

print chi2(y_fit,times,errNewY)/(len(erTimes)-2.)

fig = plt.figure(1)
fig.suptitle("Time Calibration")
ax1 = fig.add_subplot(211)
ax1.errorbar(dataMean,times,xerr=dataErr,yerr=erTimes,fmt=".",linewidth=0.5,capsize=1.5,markersize=2.5,label="data")
ax1.grid(True)
ax1.set_title("Measurement")
plt.ylabel("$\Delta$ time [$\mu$ s]")
plt.xlabel("Channel Number")
plt.plot(x_linspace,y_linspace,label="fit")

ax1.text(10000, 4, 'a= '+str(round(popt[0]*1000.,4))+" $\pm$ "+str(round(np.sqrt(pcov[0][0])*1000.,4))+"\nb= "+str(round(popt[1]*1000.,2))+" $\pm$ "+str(round(np.sqrt(pcov[1][1])*1000.,2)), style='italic',fontsize="small",
        bbox={'facecolor':'grey', 'alpha':0.6, 'pad':5})
plt.legend(loc="best")
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_title("Resdiues")


# y_res=times-func(times,popt[0],popt[1])
ax2.errorbar(dataMean,y_res,xerr=dataErr,yerr=errNewY,fmt=".",linewidth=0.5,capsize=1.5,markersize=2.5)
ax2.grid(True)
plt.ylabel("data-fit")
plt.xlabel("Channel Number")
plt.subplots_adjust(hspace=0.5, wspace=1.0)


fig.savefig("timecali.pdf")
