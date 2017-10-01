import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt
from numpy import sqrt, sin, cos, log, exp

# useful functions


def lineare_regression(x, y, ey):
    s = sum(1. / ey**2)
    sx = sum(x / ey**2)
    sy = sum(y / ey**2)
    sxx = sum(x**2 / ey**2)
    sxy = sum(x * y / ey**2)
    delta = s * sxx - sx * sx
    b = (sxx * sy - sx * sxy) / delta
    a = (s * sxy - sx * sy) / delta
    eb = np.sqrt(sxx / delta)
    ea = np.sqrt(s / delta)
    cov = -sx / delta
    corr = cov / (ea * eb)
    chiq = sum(((y - (a * x + b)) / ey)**2)
    return(a, ea, b, eb, chiq, corr)


def linear(x, a, b):
    return a * x + b


def chi2(y_exp, y_obs, y_err):
    return sum(((y_obs - y_exp)**2.) / (y_err**2.))


# Read in data
data = np.loadtxt('../data/mittwoch.TKA', skiprows=2)
# data = np.loadtxt('../data/dienstag.TKA', skiprows=2)
channel = np.linspace(0., len(data), len(data))

# plot raw data
plt.figure(1)
plt.errorbar(channel, data, yerr=np.sqrt(data), fmt=".")
plt.yscale("log")
plt.title('Muon decay')
plt.ylabel('Events/Bin')
plt.xlabel('Channel')
plt.grid()
plt.savefig("raw_log.pdf")

# REBINNING
length = len(channel)
nBins = 80
binLength = length / nBins
binnedX = []
binnedY = []

for i in range(nBins):
    tempSumY = sum(data[i * binLength:(i + 1) * binLength])
    tempSumX = sum(channel[i * binLength:(i + 1) * binLength])
    meanX = tempSumX / binLength
    binnedX.append(meanX)
    binnedY.append(tempSumY)

bin_means, bin_edges, binnumber = stats.binned_statistic(
    channel, data, statistic='sum', bins=nBins)

# Plot binned data
plt.figure(2)
# plt.hlines(bin_means, bin_edges[:-1], bin_edges[1:], color='green')
plt.hlines(binnedY, bin_edges[:-1], bin_edges[1:], color='green')
plt.errorbar(binnedX, binnedY, yerr=np.sqrt(binnedY), fmt=".",
             linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
plt.grid()
plt.title('Muon decay')
plt.ylabel('Events/Bin')
plt.xlabel('Channel')
plt.savefig("binned_lin.pdf")

plt.figure(3)
plt.hlines(np.log(binnedY), bin_edges[:-1], bin_edges[1:], color='green')
plt.errorbar(binnedX, np.log(binnedY),
             yerr=np.sqrt(binnedY) / binnedY, fmt=".")
plt.grid()
plt.title('Muon decay')
plt.ylabel('ln(Events/Bin)')
plt.xlabel('Channel')
plt.savefig("binned_ln.pdf")

"""
read in calibration
"""
temp = np.loadtxt("../calibration/values/cali" + str(100) + ".txt", skiprows=0)
A = temp[0]
B = temp[2]
erA = np.sqrt(temp[1])
erB = np.sqrt(temp[3])
A = round(A, 6)
erA = round(erA, 6)

# transform
X = np.array(binnedX)
Y = np.array(binnedY)
erX = np.zeros(len(binnedX))
erY = np.sqrt(binnedY)
logY = np.log(Y)
erLogY = erY / Y
calX = A * X
erCalX = X * erA


calLength = len(calX)
"""
BACKGROUND ESTIMATION
"""
cut = 11.5
# find bin
cutBin = 0
for i in range(calLength):
    if((calX[i] < cut)and(calX[i + 1] > cut)):
        cutBin = i + 1
detCut = calX[cutBin]
bkgMean = np.mean(Y[cutBin:])
bkgStd = np.std(Y[cutBin:])
bkgErr = bkgStd / np.sqrt(len(Y[cutBin:]))
ratio_bkg = Y / bkgMean
er_ratio_bkg = np.sqrt((erY / bkgMean)**2. + (Y / bkgMean**2. * bkgErr)**2.)

# make background plot
fig = plt.figure()
fig.suptitle("Background Estimation")
ax1 = fig.add_subplot(211)
ax1.errorbar(calX, Y, xerr=erCalX, yerr=erY, fmt='.')
# plt.hlines(logY,A*bin_edges[:-1],A*bin_edges[1:],color="green")
ax1.axvline(detCut, 0., 10.)
ax1.axhline(bkgMean, 0, 1, color="orange")
ax1.grid()
plt.xlabel("t [$\mu s$]")
plt.ylabel("Events/Bin")
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_title("ratio")
ax2.errorbar(calX[8:], ratio_bkg[8:], yerr=er_ratio_bkg[8:], fmt=".")
ax2.axhline(1., 0, 1, color="black", alpha=0.7)
ax2.grid()
plt.xlabel("t [$\mu s$]")
plt.ylabel(r"$ \frac{Events}{Events_{Bkg}}$ / Bin")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
fig.savefig("background.pdf")


"""
TRANSFORM/subtract and do first fit
"""
X_new = calX[:cutBin]
erX_new = erCalX[:cutBin]
Y_new = Y[:cutBin] - bkgMean
ar_ToDelete = []
for i in range(len(X_new)):
    if (Y_new[i] < 0.):
        Y_new[i] = 1.
        ar_ToDelete.append(i)

Y_new = np.delete(Y_new, ar_ToDelete)
X_new = np.delete(X_new, ar_ToDelete)

erY_new = np.sqrt(Y[:cutBin] + bkgErr**2.)

erY_new = np.delete(erY_new, ar_ToDelete)
erX_new = np.delete(erX_new, ar_ToDelete)

Y_new_log = np.log(Y_new)
erY_new_log = erY_new / Y_new

# plot both regions to find cut
plt.figure(5)
plt.errorbar(X_new, Y_new_log, xerr=erX_new, yerr=erY_new_log, fmt=".")
plt.grid()
plt.xlabel("t [$\mu s$]")
plt.ylabel("ln(Events/Bin)")
plt.xticks(np.arange(0., max(X_new) + 1., 1.0))
plt.title("Finding pos. range")
plt.savefig("region1+2.pdf")

secondCut = 5.
cutBin_new = 0
for i in range(len(X_new)):
    if((X_new[i] < secondCut)and(X_new[i + 1] > secondCut)):
        cutBin_new = i + 1

X_pos = X_new[cutBin_new:cutBin]
Y_pos = Y_new[cutBin_new:cutBin]
Y_pos_log = Y_new_log[cutBin_new:cutBin]
erX_pos = erX_new[cutBin_new:cutBin]
erY_pos_log = erY_new_log[cutBin_new:cutBin]
erY_pos = erY_new[cutBin_new:cutBin]

# FIT
# pos_fit,pos_cov=curve_fit(linear,X_pos,Y_pos_log,sigma=erY_pos_log)
# pos_fit,pos_cov=np.polyfit(X_pos,Y_pos_log,1,w=1./(erY_pos_log),cov=True)
a_pos, ea_pos, b_pos, eb_pos, chiq_pos, corr_pos = lineare_regression(
    X_pos, Y_pos_log, erY_pos_log)
chiNdof_pos = chiq_pos / (len(X_pos) - 2.)
X_fit_pos = np.linspace(secondCut, cut, 1000)

Y_fit_pos = linear(X_fit_pos, a_pos, b_pos)
Y_fit_pos_up = linear(X_fit_pos, a_pos + 1. * ea_pos, b_pos + 1. * eb_pos)
Y_fit_pos_down = linear(X_fit_pos, a_pos - 1. * ea_pos, b_pos - 1. * eb_pos)
Y_fit_pos_res = Y_pos_log - linear(X_pos, a_pos, b_pos)

# plot fit with residues
fig_pos_fit = plt.figure()
ax1 = fig_pos_fit.add_subplot(211)
ax1.grid()
ax1.errorbar(X_pos, Y_pos_log, xerr=erX_pos, yerr=erY_pos_log,
             fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
plt.xlabel("t [$\mu s$]")
plt.ylabel("ln(Events/Bin)")
ax1.set_title("pos. range fit")
ax1.plot(X_fit_pos, Y_fit_pos, label="fit")
ax1.text(6.5, -1., 'a= (' + str(round(a_pos, 2)) + " $\pm$ " + str(round(ea_pos, 2)) + ") $\mu s^{-1}$ \nb= " + str(round(b_pos, 1)) + " $\pm$ " + str(round(eb_pos, 1)) + "\n $\chi ^2 / ndof=$" + str(round(chiNdof_pos, 2)), style='italic', fontsize="small",
         bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
ax1.fill_between(X_fit_pos, Y_fit_pos_up, Y_fit_pos_down,
                 alpha=.25, label="$1\sigma$ fit")
ax1.legend(loc="best")
ax2 = fig_pos_fit.add_subplot(212)
ax2.errorbar(X_pos, Y_fit_pos_res, yerr=erY_pos_log, fmt=".",
             linewidth=0.5, capsize=1.5, markersize=2.5)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
ax2.set_title("Residues")
ax2.grid()
ax2.set_ylim([-6., 6.])
ax2.axhline(0., 0, 1, color="black", alpha=0.5)
plt.xlabel("t [$\mu s$]")
plt.ylabel("data-fit")
fig_pos_fit.savefig("fit_pos.pdf")


# plot region 1+2 with fit for region 2 to check cut
Y_toPlotRes = linear(X_new, a_pos, b_pos)
res_pos = Y_new_log - Y_toPlotRes
er_Res_pos = erY_new_log

fig_res = plt.figure()
ax1 = fig_res.add_subplot(211)
ax1.set_title("check pos. range cut")
plt.xlabel("t [$\mu s$]")
plt.ylabel("ln(Events/Bin)")
ax1.errorbar(X_new, Y_new_log, xerr=erX_new, yerr=erY_new_log,
             fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
ax1.grid()
ax1.plot(X_new, Y_toPlotRes, linewidth=0.5, color="red", label="fit")
ax1.legend(loc="best")
plt.xticks(np.arange(0., max(X_new) + 1., 1.0))
ax2 = fig_res.add_subplot(212)
ax2.grid()
ax2.errorbar(X_new, res_pos, yerr=er_Res_pos, fmt=".",
             linewidth=0.5, capsize=1.5, markersize=2.5)
ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
ax2.set_ylim([-1.5, 1.5])
plt.xlabel("t [$\mu s$]")
plt.ylabel("data-fit")
ax2.axvline(secondCut, color="black", alpha=0.5)
ax2.set_title("Residues")
plt.subplots_adjust(hspace=0.5, wspace=0.5)
fig_res.savefig("region1+2_fit_pos.pdf")

# fit exponential in this region


def exponential_one(x, A, tau):
    return A * np.exp(x / tau)


par_exp_pos, pcov_exp_pos = curve_fit(
    exponential_one, X_pos, Y_pos, sigma=erY_pos, p0=[300., -2.])
exp_pos_err = np.sqrt(np.diag(pcov_exp_pos))
print par_exp_pos[1], exp_pos_err[1]

X_pos_exp_fit = np.linspace(X_pos[0], X_pos[-1], 1000)
Y_pos_exp_fit = exponential_one(X_pos_exp_fit, par_exp_pos[0], par_exp_pos[1])

Y_pos_exp_up = exponential_one(
    X_pos_exp_fit, par_exp_pos[0] + 1. * exp_pos_err[0], par_exp_pos[1] + 2. * exp_pos_err[1])
Y_pos_exp_down = exponential_one(
    X_pos_exp_fit, par_exp_pos[0] - 1. * exp_pos_err[0], par_exp_pos[1] - 2. * exp_pos_err[1])
Y_pos_exp_res = Y_pos - exponential_one(X_pos, par_exp_pos[0], par_exp_pos[1])

Y_exp_pos_temp = exponential_one(X_pos, par_exp_pos[0], par_exp_pos[1])
chi2_exp_pos = chi2(Y_exp_pos_temp, Y_pos, erY_pos) / (len(Y_pos) - 2.)

fig_pos_exp = plt.figure()
ax1 = fig_pos_exp.add_subplot(211)
ax1.grid()
ax1.set_title("exp. fit pos. range")
plt.xlabel("t [$\mu s$]")
plt.ylabel("ln(Events/Bin)")
plt.errorbar(X_pos, Y_pos, yerr=erY_pos, fmt=".", linewidth=0.5,
             capsize=1.5, markersize=2.5, label="data")
plt.plot(X_pos_exp_fit, Y_pos_exp_fit, label="fit")
ax1.fill_between(X_pos_exp_fit, Y_pos_exp_up, Y_pos_exp_down,
                 alpha=.25, label="$2\sigma$ fit")
ax1.text(7.5, 150., r'A= ' + str(round(par_exp_pos[0], 1)) + " $\pm$ " + str(round(exp_pos_err[0], 1)) + " \n" + r"($\tau$= " + str(round(par_exp_pos[1], 3)) + " $\pm$ " + str(round(exp_pos_err[1], 3)) + ") $\mu s^{-1}$ \n $\chi ^2 / ndof=$" + str(round(chi2_exp_pos, 2)), style='italic', fontsize="small",
         bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
plt.legend(loc="best")
ax2 = fig_pos_exp.add_subplot(212)
ax2.set_title("Residues")
plt.xlabel("t [$\mu s$]")
plt.ylabel("data-fit")
ax2.grid()
ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
ax2.errorbar(X_pos, Y_pos_exp_res, yerr=erY_pos, fmt=".",
             linewidth=0.5, capsize=1.5, markersize=2.5)
plt.subplots_adjust(hspace=0.5, wspace=0.5)
fig_pos_exp.savefig("expFit_pos.pdf")
