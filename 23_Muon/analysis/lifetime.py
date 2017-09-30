import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt
# from astropy.stats import freedman_bin_width
from numpy import sqrt,sin,cos,log,exp

# Read in data
# data = np.loadtxt('../data/mittwoch.TKA', skiprows=2)
data = np.loadtxt('../data/dienstag.TKA', skiprows=2)
# data = np.loadtxt('../data/david.TKA', skiprows=2)
# data = np.loadtxt('../data/david_test.TKA', skiprows=2)
# data = np.loadtxt('../data/Weekend.TKA', skiprows=2)
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
nBins=80
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
A=round(A,6)
erA=round(erA,6)



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
plt.errorbar(calX,Y,xerr=erCalX,yerr=erY,fmt='.')
# plt.hlines(logY,A*bin_edges[:-1],A*bin_edges[1:],color="green")

calLength=len(calX)
calBinWidth=(calX[5]-calX[4])/2.

# BACKGROUND ESTIMATION
# cut=11.5
cut=11.331
#find bin
cutBin=0
for i in range(calLength):
    if((calX[i]<cut)and(calX[i+1]>cut)):
        cutBin=i+1
# detCut=calX[cutBin]-calBinWidth
detCut=calX[cutBin]
# print "cut=",detCut
plt.axvline(detCut,0.,10.)

bkgMean=np.mean(Y[cutBin:])
bkgStd=np.std(Y[cutBin:])
bkgErr=bkgStd/np.sqrt(len(Y[cutBin:]))

toPlotY=np.zeros(len(calX[cutBin:]))
toPlotY.fill(bkgMean)

# print bkgMean,bkgErr
plt.plot(calX[cutBin:],toPlotY)
plt.savefig("background.pdf")

print bkgMean,bkgErr

"""
TRANSFORM/subtract and do first fit
"""

X_new=calX[:cutBin]
erX_new=erCalX[:cutBin]
Y_new=Y[:cutBin]-bkgMean
for i in range(len(X_new)):
    if (Y_new[i]<0.):
        Y_new[i]=1.
erY_new=np.sqrt(Y[:cutBin]+bkgErr**2.)

Y_new_log=np.log(Y_new)
erY_new_log=erY_new/Y_new

plt.figure(5)
# plt.errorbar(X_new,Y_new,xerr=erX_new,yerr=erY_new,fmt=".")
plt.errorbar(X_new,Y_new_log,xerr=erX_new,yerr=erY_new_log,fmt=".")
plt.grid()
plt.xticks(np.arange(0., max(X_new)+1., 1.0))
plt.savefig("region1+2.pdf")

secondCut=3.5
cutBin_new=0
for i in range(len(X_new)):
    if((X_new[i]<secondCut)and(X_new[i+1]>secondCut)):
        cutBin_new=i+1

plt.figure(6)

X_pos=X_new[cutBin_new:cutBin]
Y_pos=Y_new[cutBin_new:cutBin]
Y_pos_log=Y_new_log[cutBin_new:cutBin]
erX_pos=erX_new[cutBin_new:cutBin]
erY_pos_log=erY_new_log[cutBin_new:cutBin]
erY_pos=erY_new[cutBin_new:cutBin]

def linear(x,a,b):
    return a*x+b

plt.errorbar(X_pos,Y_pos_log,xerr=erX_pos,yerr=erY_pos_log,fmt=".")



def lineare_regression(x,y,ey):

    s   = sum(1./ey**2)
    sx  = sum(x/ey**2)
    sy  = sum(y/ey**2)
    sxx = sum(x**2/ey**2)
    sxy = sum(x*y/ey**2)
    delta = s*sxx-sx*sx
    b   = (sxx*sy-sx*sxy)/delta
    a   = (s*sxy-sx*sy)/delta
    eb  = np.sqrt(sxx/delta)
    ea  = np.sqrt(s/delta)
    cov = -sx/delta
    corr = cov/(ea*eb)
    chiq  = sum(((y-(a*x+b))/ey)**2)

    return(a,ea,b,eb,chiq,corr)








# pos_fit,pos_cov=curve_fit(linear,X_pos,Y_pos_log,sigma=erY_pos_log)
# pos_fit,pos_cov=curve_fit(linear,X_pos,Y_pos_log,sigma=erY_pos_log)
pos_fit,pos_cov=np.polyfit(X_pos,Y_pos_log,1,w=1./(erY_pos_log),cov=True)
a,ea,b,eb,chiq,corr=lineare_regression(X_pos,Y_pos_log,erY_pos_log)
print 1./a,ea/a**2.

# X_fit_pos=np.linspace(secondCut,cut,1000)
# Y_fit_pos=linear(X_fit_pos,pos_fit[0],pos_fit[1])
# plt.plot(X_fit_pos,Y_fit_pos)
# plt.savefig("fit_pos.pdf")
#
# def chi2(y_exp,y_obs,y_err):
#     return sum(((y_obs-y_exp)**2.)/(y_err**2.))
#
# forchi=linear(X_pos,pos_fit[0],pos_fit[1])
# chi=chi2(forchi,Y_pos_log,erY_pos_log)
# print chi
# print chi/(len(X_pos)-2.)
# print pos_cov
# print pos_fit[0],np.sqrt(pos_cov[0][0])
# print 1./pos_fit[0],np.sqrt(pos_cov[0][0])/(pos_fit[0]**2.)
