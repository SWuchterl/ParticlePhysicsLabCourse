import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt

# data = np.loadtxt('dienstag.TKA', skiprows=2)
data = np.loadtxt('../data/mittwoch.TKA', skiprows=2)
channel = np.linspace(0., len(data), len(data))

length=len(channel)
nBins=100
binLength=length/nBins

binnedX=[]
binnedY=[]

for i in range(nBins):
    tempSumY=sum(data[i*binLength:(i+1)*binLength])
    tempSumX=sum(channel[i*binLength:(i+1)*binLength])
    meanX=tempSumX/binLength
    binnedX.append(meanX)
    binnedY.append(tempSumY)

# def rebinning(x,y,bins):
# 	x_rebin = np.zeros(bins)
# 	y_rebin = np.zeros(bins)
# 	for i in xrange(bins):
#         for j in xrange(len(x)/bins):
#             x_rebin[i] += x[i*(len(x)/bins) + j]
#             y_rebin[i] += y[i*(len(x)/bins) + j]
#         x_rebin[i] = x_rebin[i]/(len(x)/bins)
#         y_rebin[i] = y_rebin[i]
#     return x_rebin, y_rebin

def rebinning(x,y,bins):
    x_rebin=np.zeros(bins)
    y_rebin=np.zeros(bins)
    for i in xrange(bins):
        for j in xrange(len(x)/bins):
            x_rebin[i]+=x[i*(len(x)/bins)+j]
            y_rebin[i]+=y[i*(len(x)/bins)+j]
        x_rebin[i]=x_rebin[i]/(len(x)/bins)
    return x_rebin,y_rebin


davidX,davidY=rebinning(channel,data,100)

bin_means, bin_edges, binnumber = stats.binned_statistic(
    channel, data, statistic='sum', bins=100)

plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], color='green')
plt.plot(binnedX,binnedY,".")
plt.plot(davidX,davidY,".")
plt.grid()
plt.title('Muon decay')
plt.ylabel('Events/Bin')
plt.xlabel('Channel')
# plt.yscale('log')
plt.savefig('lifetime.pdf', format='pdf')
plt.show()
