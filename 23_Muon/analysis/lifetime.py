import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt
# from astropy.stats import freedman_bin_width

# Read in data
data = np.loadtxt('../data/mittwoch.TKA', skiprows=2)
channel = np.linspace(0., len(data), len(data))

#plot raw data
plt.figure(1)
plt.errorbar(channel,data,yerr=np.sqrt(data),fmt=".")
plt.yscale("log")
plt.title('Muon decay')
plt.ylabel('Events/Bin')
plt.xlabel('Channel')
plt.grid()
plt.savefig("raw_log.pdf")

#REBINNING
length=len(channel)
nBins=40
binLength=length/nBins
binnedX=[]
binnedY=[]

for i in range(nBins):
    tempSumY=sum(data[i*binLength:(i+1)*binLength])
    tempSumX=sum(channel[i*binLength:(i+1)*binLength])
    meanX=tempSumX/binLength
    binnedX.append(meanX)
    binnedY.append(tempSumY)

bin_means, bin_edges, binnumber = stats.binned_statistic(channel, data, statistic='sum', bins=nBins)

#Plot binned data
plt.figure(2)
# plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], color='green')
plt.hlines(binnedY, bin_edges[:-1], bin_edges[1:], color='green')
plt.errorbar(binnedX,binnedY,yerr=np.sqrt(binnedY),fmt=".",linewidth=0.5,capsize=1.5,markersize=2.5,label="data")
plt.grid()
plt.title('Muon decay')
plt.ylabel('Events/Bin')
plt.xlabel('Channel')
plt.savefig("binned_lin.pdf")

plt.figure(3)
plt.hlines(np.log(binnedY), bin_edges[:-1], bin_edges[1:], color='green')
plt.errorbar(binnedX,np.log(binnedY),yerr=np.sqrt(binnedY)/binnedY,fmt=".")
plt.grid()
plt.title('Muon decay')
plt.ylabel('ln(Events/Bin)')
plt.xlabel('Channel')
plt.savefig("binned_ln.pdf")


#read in calibration
temp=np.loadtxt("../calibration/values/cali"+str(100)+".txt",skiprows=0)
A=temp[0]
B=temp[2]
erA=np.sqrt(temp[1])
erB=np.sqrt(temp[3])

#transform
X=np.array(binnedX)
Y=np.array(binnedY)
erX=np.zeros(len(binnedX))
erY=np.sqrt(binnedY)

logY=np.log(Y)
erLogY=erY/Y

calX=A*X
erCalX=X*erA

plt.figure(4)
# plt.errorbar(calX,Y,xerr=erCalX,yerr=erY,fmt='.')
plt.hlines(logY,A*bin_edges[:-1],A*bin_edges[1:],color="green")
plt.errorbar(calX,logY,xerr=erCalX,yerr=erLogY,fmt='.')
# plt.show()

calLength=len(calX)
calBinWidth=(calX[5]-calX[4])/2.

# BACKGROUND ESTIMATION
cut=12.5
#find bin
cutBin=0
for i in range(calLength):
    if((calX[i]<cut)and(calX[i+1]>cut)):
        cutBin=i+1
detCut=calX[cutBin]-calBinWidth
print "cut=",detCut
plt.axvline(detCut,0.,10.)
# plt.show()
