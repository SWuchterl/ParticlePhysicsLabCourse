import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import os

# dataMean=[]
# dataErr=[]
# lengthMax=0.
times=[0.108,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.2,1.4,1.6,1.8,2.,2.3,2.6,2.9,3.2,3.5,3.8,4.1,4.4,4.72,5.,5.52,6.,6.52,7.,7.52,8.,8.52,9.,9.5,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.]
# times=[0.123,0.215,0.315,0.43,0.515,0.615,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.,2.3,2.6,2.9,3.2,3.5,3.8,4.1,4.4,4.72,5.,5.52,6.,6.52,7.,7.52,8.,8.52,9.,9.5,10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,20.]
erTimes=[0.002,0.002,0.002,0.004,0.004,0.004,0.004,0.004,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
# erTimes=[0.004,0.004,0.004,0.004,0.004,0.004,0.004,0.004,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]

def func(x,a,b):
    return a*x+b

for NBins in range(10,200,10):
    print "-----"+str(NBins)+"--------"
    dataMean=[]
    dataErr=[]
    lengthMax=0.
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
            # bin_means, bin_edges, binnumber = stats.binned_statistic(x[0:tempMaxIndex+100],temp[0:tempMaxIndex+100],statistic='mean', bins=100)
            bin_means, bin_edges, binnumber = stats.binned_statistic(x[0:tempMaxIndex+100],temp[0:tempMaxIndex+100],statistic='mean', bins=NBins)
        else:
            if(i==45):
                # bin_means, bin_edges, binnumber = stats.binned_statistic(x[tempMaxIndex-100:],temp[tempMaxIndex-100:],statistic='mean', bins=100)
                bin_means, bin_edges, binnumber = stats.binned_statistic(x[tempMaxIndex-100:],temp[tempMaxIndex-100:],statistic='mean', bins=NBins)
            else:
                # bin_means, bin_edges, binnumber = stats.binned_statistic(x[tempMaxIndex-100:tempMaxIndex+100],temp[tempMaxIndex-100:tempMaxIndex+100],statistic='mean', bins=100)
                bin_means, bin_edges, binnumber = stats.binned_statistic(x[tempMaxIndex-100:tempMaxIndex+100],temp[tempMaxIndex-100:tempMaxIndex+100],statistic='mean', bins=NBins)
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
        if not os.path.exists("time_channels/"+str(NBins)):
            os.makedirs("time_channels/"+str(NBins))
        plt.savefig("time_channels/"+str(NBins)+"/"+str(i)+".pdf")
        plt.close()


    times=np.array(times)
    erTimes=np.array(erTimes)
    erTimes_new=np.array(erTimes)/np.sqrt(12.)
    # erTimes_new=np.array(erTimes)
    dataMean=np.array(dataMean)
    dataErr=np.array(dataErr)

    popt_without,pcov_without=curve_fit(func,dataMean,times)
    popt,pcov=curve_fit(func,dataMean,times,sigma=erTimes)
    print "a:",popt[0]*1000.,"+-",np.sqrt(pcov[0][0])*1000.
    print "b:",popt[1]*1000.,"+-",np.sqrt(pcov[1][1])*1000.

    x_linspace=np.linspace(0.,lengthMax,lengthMax)
    y_fit=func(dataMean,popt[0],popt[1])
    # y_fit_without=func(dataMean,popt_without[0],popt_without[1])
    y_res=times-y_fit
    # y_res_without=times-y_fit_without
    y_linspace=func(x_linspace,popt[0],popt[1])
    # y_linspace_without=func(x_linspace,popt_without[0],popt_without[1])

    def chi2(y_exp,y_obs,y_err):
        return sum(((y_obs-y_exp)**2.)/(y_err**2.))

    errNewY=np.sqrt(erTimes_new**2. +(popt[0]*dataErr)**2.)
    chi=chi2(y_fit,times,errNewY)/(len(erTimes)-2.)
    print "chi2/ndof",chi

    fig = plt.figure()
    fig.suptitle("Time Calibration")
    ax1 = fig.add_subplot(211)

    ax1.errorbar(dataMean,times,xerr=dataErr,yerr=erTimes_new,fmt=".",linewidth=0.5,capsize=1.5,markersize=2.5,label="data")
    ax1.grid(True)
    ax1.set_title("Measurement")
    plt.ylabel("$\Delta$ time [$\mu s$]")
    plt.xlabel("Channel Number")
    plt.plot(x_linspace,y_linspace,label="fit")

    ax1.text(10000, 4, 'a= '+str(round(popt[0]*1000.,4))+" $\pm$ "+str(round(np.sqrt(pcov[0][0])*1000.,4))+"\nb= "+str(round(popt[1]*1000.,2))+" $\pm$ "+str(round(np.sqrt(pcov[1][1])*1000.,2))+"\n $\chi ^2 / ndof=$"+str(round(chi,2)), style='italic',fontsize="small",
            bbox={'facecolor':'grey', 'alpha':0.6, 'pad':5})
    plt.legend(loc="best")
    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2.set_title("Resdiues")


    ax2.errorbar(dataMean,y_res,xerr=dataErr,yerr=errNewY,fmt=".",linewidth=0.5,capsize=1.5,markersize=2.5)
    ax2.grid(True)
    plt.ylabel("data-fit [$\mu s$]")
    plt.axhline(0.,0.,len(dataMean),color='red',alpha=0.8,lw=0.5)
    plt.xlabel("Channel Number")
    plt.ylim((-0.15,0.15))
    plt.subplots_adjust(hspace=0.5, wspace=1.0)

    if not os.path.exists("plots/"):
        os.makedirs("plots/")
    fig.savefig("plots/timecali_"+str(NBins)+".pdf")

    if not os.path.exists("values/"):
        os.makedirs("values/")
    with open('values/cali'+str(NBins)+'.txt', 'wb') as datei:
        datei.write(str(popt[0])+ '\n')
        datei.write(str(pcov[0][0])+ '\n')
        datei.write(str(popt[1])+ '\n')
        datei.write(str(pcov[1][1])+ '\n')
        datei.write(str(popt_without[0])+ '\n')
        datei.write(str(pcov_without[0][0])+ '\n')
        datei.write(str(popt_without[1])+ '\n')
        datei.write(str(pcov_without[1][1])+ '\n')
        datei.close()
