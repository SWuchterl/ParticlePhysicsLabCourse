import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
# from scipy.interpolate import interp1d
from scipy import stats
import matplotlib.pyplot as plt
from numpy import sqrt, sin, cos, log, exp
import argparse


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


parser = argparse.ArgumentParser(
    description='Analize data with given calibration.')
parser.add_argument(
    '--bins', help='Number of Bins. default = 80', type=int, default=80)
parser.add_argument(
    '--cut1', help='First Cut for background determinaton. default = 12', type=float, default=12.)
parser.add_argument(
    '--cut2', help='Second Cut for pos range. default = 3.5', type=float, default=3.5)
parser.add_argument(
    '--cut3', help='Second Cut for neg range. default = 0.7', type=float, default=0.7)
args = parser.parse_args()
print "Variables set to:"
print "NBins = ", args.bins
print "Cut1 = ", args.cut1
print "Cut2 = ", args.cut2
print "Cut3 = ", args.cut3


def analysis():

    # Read in data
    data = np.loadtxt('../data/mittwoch.TKA', skiprows=2)
    # data = np.loadtxt('../data/dienstag.TKA', skiprows=2)
    # data = np.loadtxt('../data/Weekend.TKA', skiprows=2)
    # data = np.loadtxt('../data/david.TKA', skiprows=2)
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
    # nBins = 80
    nBins = args.bins
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
    temp = np.loadtxt("../calibration/values/cali" +
                      str(100) + ".txt", skiprows=0)
    A = temp[0]
    B = temp[2]
    erA = np.sqrt(temp[1])
    erB = np.sqrt(temp[3])
    # A = temp[4]
    # B = temp[6]
    # erA = np.sqrt(temp[5])
    # erB = np.sqrt(temp[7])
    A = round(A, 6)
    erA = round(erA, 6)

    # transform
    X = np.array(binnedX)
    Y = np.array(binnedY)
    erX = np.zeros(len(binnedX))
    erY = np.sqrt(binnedY)
    logY = np.log(Y)
    erLogY = erY / Y
    calX = A * X + B
    erCalX = np.sqrt((X * erA)**2. + erB**2.)

    print erCalX / calX * 100.

    calLength = len(calX)
    """
    BACKGROUND ESTIMATION
    """
    # #cut = 11.5
    # cut = 12.
    cut = args.cut1
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
    er_ratio_bkg = np.sqrt((erY / bkgMean)**2. +
                           (Y / bkgMean**2. * bkgErr)**2.)

    # make background plot
    fig = plt.figure()
    fig.suptitle("Background Estimation")
    ax1 = fig.add_subplot(211)
    ax1.errorbar(calX, Y, yerr=erY, fmt='.')
    # ax1.errorbar(calX, Y, xerr=erCalX, yerr=erY, fmt='.')
    # plt.hlines(logY,A*bin_edges[:-1],A*bin_edges[1:],color="green")
    ax1.axvline(detCut, 0., 10.)
    ax1.axhline(bkgMean, 0, 1, color="orange")
    ax1.grid()
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("Events/Bin")
    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2.set_title("ratio")
    ax2.errorbar(calX[8:], ratio_bkg[8:], yerr=er_ratio_bkg[8:], fmt=".")
    ax2.axhline(1., 0, 1, color="black", alpha=0.7)
    ax2.grid()
    ax1.axvline(detCut, 1., 5.)
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel(r"$ \frac{Events}{Events_{Bkg}}$ / Bin")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    fig.savefig("background.pdf")

    """
    TRANSFORM/subtract and do first fitY_first = np.delete(Y_first, ar_ToDelete)
    X_first = np.delete(X_first, ar_ToDelete)
    erY_first = np.delete(erY_first, ar_ToDelete)
    erX_first = np.delete(erX_first, ar_ToDelete)

    Y_first_log = np.log(Y_first)
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
    plt.errorbar(X_new, Y_new_log, yerr=erY_new_log, fmt=".")
    # plt.errorbar(X_new, Y_new_log, xerr=erX_new, yerr=erY_new_log, fmt=".")
    plt.grid()
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("ln(Events/Bin)")
    plt.xticks(np.arange(0., max(X_new) + 1., 1.0))
    plt.title("Finding pos. range")
    plt.savefig("region1+2.pdf")

    # ##secondCut = 4.5
    # #secondCut = 5.
    # secondCut = 3.5
    secondCut = args.cut2
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
    # pos_fit, pos_cov = curve_fit(linear, X_pos, Y_pos_log, sigma=erY_pos_log)
    # pos_fit, pos_cov = np.polyfit(
    # X_pos, Y_pos_log, 1, w=1. / (erY_pos_log), cov=True)
    a_pos, ea_pos, b_pos, eb_pos, chiq_pos, corr_pos = lineare_regression(
        X_pos, Y_pos_log, erY_pos_log)
    # chiq_pos = chi2(
    #     linear(X_pos, pos_fit[0], pos_fit[1]), Y_pos_log, erY_pos_log)
    chiNdof_pos = chiq_pos / (len(X_pos) - 2.)
    X_fit_pos = np.linspace(secondCut, cut, 1000)

    # print "covmatrix", pos_cov
    #
    # a_pos = pos_fit[0]
    # b_pos = pos_fit[1]
    # ea_pos = np.sqrt(pos_cov[0][0])
    # eb_pos = np.sqrt(pos_cov[1][1])
    # corr_pos = pos_cov[0][1] * (ea_pos * eb_pos)

    Y_fit_pos = linear(X_fit_pos, a_pos, b_pos)
    Y_fit_pos_up = linear(X_fit_pos, a_pos + 1. * ea_pos, b_pos + 1. * eb_pos)
    Y_fit_pos_down = linear(X_fit_pos, a_pos - 1. *
                            ea_pos, b_pos - 1. * eb_pos)
    Y_fit_pos_res = Y_pos_log - linear(X_pos, a_pos, b_pos)

    # plot fit with residues
    fig_pos_fit = plt.figure()
    ax1 = fig_pos_fit.add_subplot(211)
    ax1.grid()
    ax1.errorbar(X_pos, Y_pos_log, yerr=erY_pos_log,
                 fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    # ax1.errorbar(X_pos, Y_pos_log, xerr=erX_pos, yerr=erY_pos_log,
    #              fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("ln(Events/Bin)")
    ax1.set_title("pos. range fit")
    ax1.plot(X_fit_pos, Y_fit_pos, label="fit")
    ax1.text(6.5, -1., 'a= (' + str(round(a_pos, 2)) + " $\pm$ " + str(round(ea_pos, 2)) + ") $\mu s^{-1}$ \nb= " + str(round(b_pos, 1)) + " $\pm$ " + str(round(eb_pos, 1)) + "\n $\chi ^2 / ndof=$" + str(round(chiNdof_pos, 2)), style='italic', fontsize="small",
             bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
    ax1.fill_between(X_fit_pos, Y_fit_pos_up, Y_fit_pos_down,
                     alpha=.25, label="$1\sigma$ fit")
    ax1.legend(loc="best")
    ax2 = fig_pos_fit.add_subplot(212, sharex=ax1)
    ax2.errorbar(X_pos, Y_fit_pos_res, yerr=erY_pos_log, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    ax2.set_title("Residues")
    ax2.grid()
    ax2.set_ylim([-2.5, 2.5])
    ax2.axhline(0., 0, 1, color="black", alpha=0.5)
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    fig_pos_fit.savefig("fit_pos.pdf")

    # plot region 1+2 with fit for region 2 to check cut
    Y_toPlotRes = linear(X_new, a_pos, b_pos)
    res_pos = Y_new_log - Y_toPlotRes
    er_Res_pos = erY_new_log

    fig_res = plt.figure()
    ax1 = fig_res.add_subplot(211)
    ax1.set_title("check pos. range cut")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("ln(Events/Bin)")
    ax1.errorbar(X_new, Y_new_log, yerr=erY_new_log,
                 fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    # ax1.errorbar(X_new, Y_new_log, xerr=erX_new, yerr=erY_new_log,
    #              fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    ax1.grid()
    ax1.plot(X_new, Y_toPlotRes, linewidth=0.5, color="red", label="fit")
    ax1.legend(loc="best")
    plt.xticks(np.arange(0., max(X_new) + 1., 1.0))
    ax2 = fig_res.add_subplot(212, sharex=ax1)
    ax2.grid()
    ax2.errorbar(X_new, res_pos, yerr=er_Res_pos, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
    ax2.set_ylim([-1.5, 1.5])
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    ax2.axvline(secondCut, color="black", alpha=0.5)
    ax2.set_title("Residues")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    fig_res.savefig("region1+2_fit_pos.pdf")

    # fit exponential in this region

    # def exponential_one(x, A, tau):
    # return A * np.exp(x / tau)
    def exponential_one(x, A, lam):
        return A * np.exp(-1. * x * lam)

    par_exp_pos, pcov_exp_pos = curve_fit(
        exponential_one, X_pos, Y_pos, sigma=erY_pos, p0=[300., -2.])
    exp_pos_err = np.sqrt(np.diag(pcov_exp_pos))
    # print par_exp_pos[1], exp_pos_err[1]

    X_pos_exp_fit = np.linspace(X_pos[0], X_pos[-1], 1000)
    Y_pos_exp_fit = exponential_one(
        X_pos_exp_fit, par_exp_pos[0], par_exp_pos[1])

    Y_pos_exp_up = exponential_one(
        X_pos_exp_fit, par_exp_pos[0] + 2. * exp_pos_err[0], par_exp_pos[1] + 2. * exp_pos_err[1])
    Y_pos_exp_down = exponential_one(
        X_pos_exp_fit, par_exp_pos[0] - 2. * exp_pos_err[0], par_exp_pos[1] - 2. * exp_pos_err[1])
    Y_pos_exp_res = Y_pos - \
        exponential_one(X_pos, par_exp_pos[0], par_exp_pos[1])

    Y_exp_pos_temp = exponential_one(X_pos, par_exp_pos[0], par_exp_pos[1])
    chi2_exp_pos = chi2(Y_exp_pos_temp, Y_pos, erY_pos) / (len(Y_pos) - 2.)

    fig_pos_exp = plt.figure()
    ax1 = fig_pos_exp.add_subplot(211)
    ax1.grid()
    ax1.set_title("exp. fit pos. range")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("Events/Bin")
    plt.errorbar(X_pos, Y_pos,  yerr=erY_pos, fmt=".", linewidth=0.5,
                 capsize=1.5, markersize=2.5, label="data")
    # plt.errorbar(X_pos, Y_pos, xerr=erX_pos, yerr=erY_pos, fmt=".", linewidth=0.5,
    #              capsize=1.5, markersize=2.5, label="data")
    plt.plot(X_pos_exp_fit, Y_pos_exp_fit, label="fit")
    ax1.fill_between(X_pos_exp_fit, Y_pos_exp_up, Y_pos_exp_down,
                     alpha=.25, label="$2\sigma$ fit")
    ax1.text(7.5, 150., r'A= ' + str(round(par_exp_pos[0], 1)) + " $\pm$ " + str(round(exp_pos_err[0], 1)) + " \n" + r"($\lambda$= " + str(round(par_exp_pos[1], 3)) + " $\pm$ " + str(round(exp_pos_err[1], 3)) + ") $\mu s^{-1}$ \n $\chi ^2 / ndof=$" + str(round(chi2_exp_pos, 2)), style='italic', fontsize="small",
             bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
    plt.legend(loc="best")
    ax2 = fig_pos_exp.add_subplot(212, sharex=ax1)
    ax2.set_title("Residues")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    ax2.grid()
    ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
    ax2.errorbar(X_pos, Y_pos_exp_res, yerr=erY_pos, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    fig_pos_exp.savefig("expFit_pos.pdf")

    """
    negative muons, first region
    """

    # extrapolate linear from second region and subtract in log
    # in ln. represenation subtract exp. fit

    cov_pos_linreg = corr_pos * (ea_pos * eb_pos)
    Amplitude_pos = np.exp(b_pos)
    # tau_pos = 1. / a_pos
    lambda_pos = -1. * a_pos
    # print lambda_pos
    erAmplitude_pos = Amplitude_pos * eb_pos
    # erTau_pos = ea_pos / (a_pos)**2.
    erLambda_pos = ea_pos
    # print tau_pos, erTau_pos
    # print Amplitude_pos, erAmplitude_pos
    # print b_pos, eb_pos
    X_first = X_new[:cutBin_new]
    # Y_first = Y_new - (Amplitude_pos * np.exp(-1. * X_new / tau_pos))
    Y_first = Y_new - (Amplitude_pos * np.exp(-1. * X_new * lambda_pos))
    Y_first = Y_first[:cutBin_new]

    ar_ToDelete = []
    for i in range(len(X_first)):
        if (Y_first[i] < 0.):
            Y_first[i] = 1.
            ar_ToDelete.append(i)

    erY_first = erY_new[:cutBin_new]
    # erY_first = np.sqrt(erY_first**2. + (erAmplitude_pos * np.exp(X_first / tau_pos))**2. + (erTau_pos * X_first / (tau_pos**2.) * Amplitude_pos *
    #                                                                                          np.exp(X_first / tau_pos))**2. + 2. * X_first / (tau_pos**2.) * Amplitude_pos * (np.exp(X_first / tau_pos))**2. * cov_pos_linreg)
    erY_first = np.sqrt(erY_first**2. + (erAmplitude_pos * np.exp(-1. * X_first * lambda_pos))**2. + (erLambda_pos * X_first * Amplitude_pos *
                                                                                                      np.exp(-1. * X_first * lambda_pos))**2. + 2. * X_first * Amplitude_pos * (np.exp(-1. * X_first * lambda_pos))**2. * cov_pos_linreg)

    Y_first = np.delete(Y_first, ar_ToDelete)
    X_first = np.delete(X_first, ar_ToDelete)
    erY_first = np.delete(erY_first, ar_ToDelete)
    # erX_first = np.delete(erX_first, ar_ToDelete)
    Y_first_log = np.log(Y_first)
    erY_first_log = erY_first / Y_first

    # #thirdCut = 1.5
    # thirdCut = 0.7
    thirdCut = args.cut3
    cutBin_third = 0
    for i in range(len(X_first)):
        if((X_first[i] < thirdCut)and(X_first[i + 1] > thirdCut)):
            cutBin_third = i + 1

    X_neg = X_first[cutBin_third:cutBin_new]
    Y_neg = Y_first[cutBin_third:cutBin_new]
    Y_neg_log = Y_first_log[cutBin_third:cutBin_new]
    # erX_neg = erX_first[cutBin_third:cutBin_new]
    erY_neg_log = erY_first_log[cutBin_third:cutBin_new]
    erY_neg = erY_first[cutBin_third:cutBin_new]

    # FIT
    neg_fit, neg_cov = curve_fit(linear, X_neg, Y_neg_log, sigma=erY_neg_log)
    chiq_neg = chi2(
        linear(X_neg, neg_fit[0], neg_fit[1]), Y_neg_log, erY_neg_log)
    chiNdof_neg = chiq_neg / (len(X_neg) - 2.)
    X_fit_neg = np.linspace(thirdCut, secondCut, 1000)

    # print "------"
    # print a_pos, a_neg, a_pos - b_neg
    a_neg = neg_fit[0]
    b_neg = neg_fit[1]
    ea_neg = np.sqrt(neg_cov[0][0])
    eb_neg = np.sqrt(neg_cov[1][1])
    corr_neg = neg_cov[0][1] * (ea_neg * eb_neg)
    # print "------"
    # print a_pos, a_neg, a_pos - a_neg
    # print 1. / a_pos, 1. / a_neg, 1. / (a_pos - a_neg)
    Y_fit_neg = linear(X_fit_neg, a_neg, b_neg)
    Y_fit_neg_up = linear(X_fit_neg, a_neg + 1. * ea_neg, b_neg + 1. * eb_neg)
    Y_fit_neg_down = linear(X_fit_neg, a_neg - 1. *
                            ea_neg, b_neg - 1. * eb_neg)
    Y_fit_neg_res = Y_neg_log - linear(X_neg, a_neg, b_neg)

    # plot fit with residues
    fig_neg_fit = plt.figure()
    ax1 = fig_neg_fit.add_subplot(211)
    ax1.grid()
    ax1.errorbar(X_neg, Y_neg_log, yerr=erY_neg_log,
                 fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("ln(Events/Bin)")
    ax1.set_title("neg. range fit")
    ax1.plot(X_fit_neg, Y_fit_neg, label="fit")
    ax1.text(1.7, -2.5, 'a= (' + str(round(a_neg, 2)) + " $\pm$ " + str(round(ea_neg, 2)) + ") $\mu s^{-1}$ \nb= " + str(round(b_neg, 1)) + " $\pm$ " + str(round(eb_neg, 1)) + "\n $\chi ^2 / ndof=$" + str(round(chiNdof_neg, 2)), style='italic', fontsize="small",
             bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
    ax1.fill_between(X_fit_neg, Y_fit_neg_up, Y_fit_neg_down,
                     alpha=.25, label="$1\sigma$ fit")
    ax1.legend(loc="best")
    ax2 = fig_neg_fit.add_subplot(212, sharex=ax1)
    ax2.errorbar(X_neg, Y_fit_neg_res, yerr=erY_neg_log, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    ax2.set_title("Residues")
    ax2.grid()
    ax2.set_ylim([-6., 6.])
    ax2.axhline(0., 0, 1, color="black", alpha=0.5)
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    fig_neg_fit.savefig("fit_neg.pdf")

    # plot region 1+2 with fit for region 2 to check cut
    Y_toPlotRes = linear(X_first, a_neg, b_neg)
    res_neg = Y_first_log - Y_toPlotRes
    er_Res_neg = erY_first_log

    fig_res_neg = plt.figure()
    ax1 = fig_res_neg.add_subplot(211)
    ax1.set_title("check neg. range cut")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("ln(Events/Bin)")
    # ax1.errorbar(X_first, Y_first_log, xerr=erX_first, yerr=erY_first_log,
    ax1.errorbar(X_first, Y_first_log, yerr=erY_first_log,
                 fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    ax1.grid()
    ax1.plot(X_first, Y_toPlotRes, linewidth=0.5, color="red", label="fit")
    ax1.legend(loc="best")
    plt.xticks(np.arange(0., max(X_first) + 1., 1.0))
    ax2 = fig_res_neg.add_subplot(212, sharex=ax1)
    ax2.grid()
    ax2.errorbar(X_first, res_neg, yerr=er_Res_neg, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
    ax2.set_ylim([-5., 5.])
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    ax2.axvline(thirdCut, color="black", alpha=0.5)
    ax2.set_title("Residues")
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    fig_res_neg.savefig("region1+2_fit_neg.pdf")

    # fit exponential in this region

    # def exponential_one(x, A, tau):
    #     return A * np.exp(x / tau)
    # def exponential_one(x, A, tau):
    #     return A * np.exp(x / tau)

    par_exp_neg, pcov_exp_neg = curve_fit(
        exponential_one, X_neg, Y_neg, sigma=erY_neg, p0=[300., -2.])
    exp_neg_err = np.sqrt(np.diag(pcov_exp_neg))
    # print par_exp_pos[1], exp_pos_err[1]

    X_neg_exp_fit = np.linspace(X_neg[0], X_neg[-1], 1000)
    Y_neg_exp_fit = exponential_one(
        X_neg_exp_fit, par_exp_neg[0], par_exp_neg[1])

    Y_neg_exp_up = exponential_one(
        X_neg_exp_fit, par_exp_neg[0] + 2. * exp_neg_err[0], par_exp_neg[1] + 2. * exp_neg_err[1])
    Y_neg_exp_down = exponential_one(
        X_neg_exp_fit, par_exp_neg[0] - 2. * exp_neg_err[0], par_exp_neg[1] - 2. * exp_neg_err[1])
    Y_neg_exp_res = Y_neg - \
        exponential_one(X_neg, par_exp_neg[0], par_exp_neg[1])

    Y_exp_neg_temp = exponential_one(X_neg, par_exp_neg[0], par_exp_neg[1])
    chi2_exp_neg = chi2(Y_exp_neg_temp, Y_neg, erY_neg) / (len(Y_neg) - 2.)

    fig_neg_exp = plt.figure()
    ax1 = fig_neg_exp.add_subplot(211)
    ax1.grid()
    ax1.set_title("exp. fit neg. range")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("Events/Bin")
    plt.errorbar(X_neg, Y_neg, yerr=erY_neg, fmt=".", linewidth=0.5,
                 capsize=1.5, markersize=2.5, label="data")
    plt.plot(X_neg_exp_fit, Y_neg_exp_fit, label="fit")
    ax1.fill_between(X_neg_exp_fit, Y_neg_exp_up, Y_neg_exp_down,
                     alpha=.25, label="$2\sigma$ fit")
    ax1.text(2., 200., r'A= ' + str(round(par_exp_neg[0], 1)) + " $\pm$ " + str(round(exp_neg_err[0], 1)) + " \n" + r"($\lambda$= " + str(round(par_exp_neg[1], 3)) + " $\pm$ " + str(round(exp_neg_err[1], 3)) + ") $\mu s^{-1}$ \n $\chi ^2 / ndof=$" + str(round(chi2_exp_neg, 2)), style='italic', fontsize="small",
             bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
    plt.legend(loc="best")
    ax2 = fig_neg_exp.add_subplot(212, sharex=ax1)
    ax2.set_title("Residues")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    ax2.grid()
    ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
    ax2.errorbar(X_neg, Y_neg_exp_res, yerr=erY_neg, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    fig_neg_exp.savefig("expFit_neg.pdf")

    """
    LAST REGION
    """
    # extrapolate linear from first region and subtract in log
    # in ln. represenation subtract exp. fit

    cov_neg_linreg = corr_neg * (ea_neg * eb_neg)
    Amplitude_neg = np.exp(b_neg)
    lambda_neg = -1. * a_neg
    # print lambda_neg
    erAmplitude_neg = Amplitude_neg * eb_neg
    erLambda_neg = ea_neg
    X_last = X_first[:cutBin_third]
    Y_last = Y_first - (Amplitude_neg * np.exp(-1. * X_first * lambda_neg))
    Y_last = Y_last[:cutBin_third]

    ar_ToDelete = []
    for i in range(len(X_last)):
        if (Y_last[i] < 0.):
            Y_last[i] = 1.
            ar_ToDelete.append(i)

    erY_last = erY_first[:cutBin_third]
    erY_last = np.sqrt(erY_last**2. + (erAmplitude_neg * np.exp(-1. * X_last * lambda_neg))**2. + (erLambda_neg * X_last * Amplitude_neg *
                                                                                                   np.exp(-1. * X_last * lambda_neg))**2. + 2. * X_last * Amplitude_neg * (np.exp(-1. * X_last * lambda_neg))**2. * cov_neg_linreg)

    Y_last = np.delete(Y_last, ar_ToDelete)
    X_last = np.delete(X_last, ar_ToDelete)
    erY_last = np.delete(erY_last, ar_ToDelete)
    Y_last_log = np.log(Y_last)
    erY_last_log = erY_last / Y_last

    X_Z = X_last[:cutBin_third]
    Y_Z = Y_last[:cutBin_third]
    Y_Z_log = Y_last_log[:cutBin_third]
    erY_Z_log = erY_last_log[:cutBin_third]
    erY_Z = erY_last_log[:cutBin_third]

    # FIT
    Z_fit, Z_cov = curve_fit(linear, X_Z, Y_Z_log, sigma=erY_Z_log)
    chiq_Z = chi2(linear(X_Z, Z_fit[0], Z_fit[1]), Y_Z_log, erY_Z_log)
    chiNdof_Z = chiq_Z / (len(X_Z) - 2.)
    X_fit_Z = np.linspace(0, thirdCut, 1000)

    # print "------"
    # print a_pos, a_Z, a_pos - b_Z
    a_Z = Z_fit[0]
    b_Z = Z_fit[1]
    ea_Z = np.sqrt(Z_cov[0][0])
    eb_Z = np.sqrt(Z_cov[1][1])
    corr_Z = Z_cov[0][1] * (ea_Z * eb_Z)
    # print "------"
    # print a_pos, a_Z, a_pos - a_Z
    # print 1. / a_pos, 1. / a_Z, 1. / (a_pos - a_Z)
    Y_fit_Z = linear(X_fit_Z, a_Z, b_Z)
    Y_fit_Z_up = linear(X_fit_Z, a_Z + 1. * ea_Z, b_Z + 1. * eb_Z)
    Y_fit_Z_down = linear(X_fit_Z, a_Z - 1. * ea_Z, b_Z - 1. * eb_Z)
    Y_fit_Z_res = Y_Z_log - linear(X_Z, a_Z, b_Z)

    # plot fit with residues
    fig_Z_fit = plt.figure()
    ax1 = fig_Z_fit.add_subplot(211)
    ax1.grid()
    ax1.errorbar(X_Z, Y_Z_log, yerr=erY_Z_log,
                 fmt=".", linewidth=0.5, capsize=1.5, markersize=2.5, label="data")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("ln(Events/Bin)")
    ax1.set_title("Z range fit")
    ax1.plot(X_fit_Z, Y_fit_Z, label="fit")
    ax1.text(0.1, 4.3, 'a= (' + str(round(a_Z, 2)) + " $\pm$ " + str(round(ea_Z, 2)) + ") $\mu s^{-1}$ \nb= " + str(round(b_Z, 1)) + " $\pm$ " + str(round(eb_Z, 1)) + "\n $\chi ^2 / ndof=$" + str(round(chiNdof_Z, 2)), style='italic', fontsize="small",
             bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
    ax1.fill_between(X_fit_Z, Y_fit_Z_up, Y_fit_Z_down,
                     alpha=.25, label="$1\sigma$ fit")
    ax1.legend(loc="best")
    ax2 = fig_Z_fit.add_subplot(212, sharex=ax1)
    ax2.errorbar(X_Z, Y_fit_Z_res, yerr=erY_Z_log, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    ax2.set_title("Residues")
    ax2.grid()
    ax2.set_ylim([-1.5, 1.5])
    ax2.axhline(0., 0, 1, color="black", alpha=0.5)
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    fig_Z_fit.savefig("fit_Z.pdf")

    # plot region 1+2 with fit for region 2 to check cut
    Y_toPlotRes = linear(X_last, a_Z, b_Z)
    res_Z = Y_last_log - Y_toPlotRes
    er_Res_Z = erY_last_log

    # fit exponential in this region

    par_exp_Z, pcov_exp_Z = curve_fit(
        exponential_one, X_Z, Y_Z, sigma=erY_Z, p0=[300., -2.])
    exp_Z_err = np.sqrt(np.diag(pcov_exp_Z))
    # print par_exp_pos[1], exp_pos_err[1]

    X_Z_exp_fit = np.linspace(X_Z[0], X_Z[-1], 1000)
    Y_Z_exp_fit = exponential_one(X_Z_exp_fit, par_exp_Z[0], par_exp_Z[1])

    Y_Z_exp_up = exponential_one(
        X_Z_exp_fit, par_exp_Z[0] + 2. * exp_Z_err[0], par_exp_Z[1] + 2. * exp_Z_err[1])
    Y_Z_exp_down = exponential_one(
        X_Z_exp_fit, par_exp_Z[0] - 2. * exp_Z_err[0], par_exp_Z[1] - 2. * exp_Z_err[1])
    Y_Z_exp_res = Y_Z - exponential_one(X_Z, par_exp_Z[0], par_exp_Z[1])

    Y_exp_Z_temp = exponential_one(X_Z, par_exp_Z[0], par_exp_Z[1])
    chi2_exp_Z = chi2(Y_exp_Z_temp, Y_Z, erY_Z) / (len(Y_Z) - 2.)

    fig_Z_exp = plt.figure()
    ax1 = fig_Z_exp.add_subplot(211)
    ax1.grid()
    ax1.set_title("exp. fit Z range")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("Events/Bin")
    plt.errorbar(X_Z, Y_Z, yerr=erY_Z, fmt=".", linewidth=0.5,
                 capsize=1.5, markersize=2.5, label="data")
    plt.plot(X_Z_exp_fit, Y_Z_exp_fit, label="fit")
    ax1.fill_between(X_Z_exp_fit, Y_Z_exp_up, Y_Z_exp_down,
                     alpha=.25, label="$2\sigma$ fit")
    ax1.text(0.35, 2000., r'A= ' + str(round(par_exp_Z[0], 1)) + " $\pm$ " + str(round(exp_Z_err[0], 1)) + " \n" + r"($\lambda$= " + str(round(par_exp_Z[1], 3)) + " $\pm$ " + str(round(exp_Z_err[1], 3)) + ") $\mu s^{-1}$ \n $\chi ^2 / ndof=$" + str(round(chi2_exp_Z, 2)), style='italic', fontsize="small",
             bbox={'facecolor': 'grey', 'alpha': 0.3, 'pad': 5})
    plt.legend(loc="best")
    ax2 = fig_Z_exp.add_subplot(212, sharex=ax1)
    ax2.set_title("Residues")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    ax2.grid()
    ax2.axhline(0., 0, 1, color='red', alpha=0.8, lw=0.5)
    ax2.errorbar(X_Z, Y_Z_exp_res, yerr=erY_Z, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    fig_Z_exp.savefig("expFit_Z.pdf")

    """
    DO FAT GLOBAL FIT
    """

    cov_Z_linreg = corr_Z * (ea_Z * eb_Z)
    Amplitude_Z = np.exp(b_Z)
    lambda_Z = -1. * a_Z
    # print lambda_neg
    erAmplitude_Z = Amplitude_Z * eb_Z
    erLambda_Z = ea_Z

    def exponential_four(x, c1, c2, c3, c0, l1, l2, l3):
        # part1 = c1 * np.exp(l1 * x)
        # part2 = c2 * np.exp(l2 * x)
        # part3 = c3 * np.exp(l3 * x)
        return (c0 + c1 * np.exp(-1. * l1 * x) + c2 * np.exp(-1. * l2 * x) + c3 * np.exp(-1. * l3 * x))
        # return (part1 + part2 + part3 + bkgMean)

    X_toFit_global = calX
    Y_toFit_global = Y
    erX_toFit_global = erCalX
    erY_toFit_global = erY
    pStart = [
        Amplitude_pos, Amplitude_neg, Amplitude_Z, bkgMean, lambda_pos, lambda_neg, lambda_Z]
    # print"start", pStart

    # par_glob, cov_glob = curve_fit(
    #     exponential_four, X_toFit_global, Y_toFit_global, p0=pStart, maxfev=10000)
    par_glob, cov_glob = curve_fit(
        exponential_four, X_toFit_global, Y_toFit_global, sigma=erY, p0=pStart, maxfev=10000)
    # print "global"
    # print par_glob, np.sqrt(np.diag(cov_glob))

    # # try gmodel fit
    # from lmfit import Model
    # from lmfit.models import ExponentialModel, ConstantModel
    # exp1 = ExponentialModel(prefix='exp1')
    # exp2 = ExponentialModel(prefix='exp2')
    # exp3 = ExponentialModel(prefix='exp3')
    # const = ConstantModel(prefix='const')
    # gmod = exp1 + exp2 + exp3 + const
    # pars = gmod.make_params(exp1amplitude=Amplitude_pos, exp1decay=1. / lambda_pos, exp2amplitude=Amplitude_neg,
    #                         exp2decay=1. / lambda_neg, exp3amplitude=Amplitude_Z, exp3decay=1. / lambda_Z, constc=bkgMean)
    # result = gmod.fit(Y, x=calX, params=pars, weights=1. /
    #                   erY, method='slsqp')
    # print(result.fit_report())

    X_global = np.linspace(calX[0], calX[-1], 500)
    Y_global = exponential_four(
        X_global, par_glob[0], par_glob[1], par_glob[2], par_glob[3], par_glob[4], par_glob[5], par_glob[6])
    # Y_global = exponential_four(
    #     X_global, Amplitude_pos, Amplitude_neg, Amplitude_Z, bkgMean, lambda_pos, lambda_neg, lambda_Z)

    chiq_global = chi2(exponential_four(
        calX, par_glob[0], par_glob[1], par_glob[2], par_glob[3], par_glob[4], par_glob[5], par_glob[6]), Y_toFit_global, erY_toFit_global)
    chiNdof_global = chiq_global / (len(X_toFit_global) - 7.)

    err_glob = np.sqrt(np.diag(cov_glob))
    # print err_glob
    glob_res = Y_toFit_global - exponential_four(
        calX, par_glob[0], par_glob[1], par_glob[2], par_glob[3], par_glob[4], par_glob[5], par_glob[6])
    # glob_res = Y_toFit_global - exponential_four(
    #     calX, Amplitude_pos, Amplitude_neg, Amplitude_Z, bkgMean, lambda_pos, lambda_neg, lambda_Z)

    # glob_up = exponential_four(
    #     X_global, par_glob[0] + 1. * err_glob[0], par_glob[1] + 1. * err_glob[1], par_glob[2] + 1. * err_glob[2], par_glob[3] + 1. * err_glob[3], par_glob[4] + 1. * err_glob[4], par_glob[5] + 1. * err_glob[5], par_glob[6] + 1. * err_glob[6])
    # glob_down = exponential_four(
    #     X_global, par_glob[0] - 1. * err_glob[0], par_glob[1] - 1. * err_glob[1], par_glob[2] - 1. * err_glob[2], par_glob[3] - 1. * err_glob[3], par_glob[4] - 1. * err_glob[4], par_glob[5] - 1. * err_glob[5], par_glob[6] - 1. * err_glob[6])

    fig_globalFit = plt.figure()
    ax1 = fig_globalFit.add_subplot(211)
    ax1.set_title("global fit")
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("Events/Bin")
    ax1.errorbar(X_toFit_global, Y_toFit_global,
                 yerr=erY_toFit_global, fmt=".")
    # ax1.errorbar(X_toFit_global, Y_toFit_global,
    #              yerr=erY_toFit_global, xerr=erX_toFit_global, fmt=".")
    ax1.plot(X_global, Y_global)
    # plt.plot(calX, result.best_fit, 'r-')
    # ax1.fill_between(X_global, Y_global, glob_up,
    #                  alpha=.25, label="$1\sigma$ fit")
    ax2 = fig_globalFit.add_subplot(212, sharex=ax1)
    ax2.errorbar(calX, glob_res, yerr=erY_toFit_global, fmt=".",
                 linewidth=0.5, capsize=1.5, markersize=2.5)
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    ax2.set_title("Residues")
    ax2.grid()
    ax2.set_ylim([-70., 70.])
    ax2.axhline(0., 0, 1, color="black", alpha=0.5)
    plt.xlabel("$\Delta $t [$\mu s$]")
    plt.ylabel("data-fit")
    fig_globalFit.savefig("globalExp.pdf")

    # collect final values for everything
    ret_pos_lin = [a_pos, ea_pos, b_pos, eb_pos]
    ret_neg_lin = [a_neg, ea_neg, b_neg, eb_neg]
    ret_Z_lin = [a_Z, ea_Z, b_Z, eb_Z]

    ret_pos_exp = [par_exp_pos[0], np.sqrt(np.diag(pcov_exp_pos))[
        0], par_exp_pos[1], np.sqrt(np.diag(pcov_exp_pos))[1]]
    ret_neg_exp = [par_exp_neg[0], np.sqrt(np.diag(pcov_exp_neg))[
        0], par_exp_neg[1], np.sqrt(np.diag(pcov_exp_neg))[1]]
    ret_Z_exp = [par_exp_Z[0], np.sqrt(np.diag(pcov_exp_Z))[
        0], par_exp_Z[1], np.sqrt(np.diag(pcov_exp_Z))[1]]

    ret_global = [par_glob, np.sqrt(np.diag(cov_glob))]
    # ret_global = np.array(ret_global).flatten()
    # print ret_global
    return ret_pos_lin, ret_neg_lin, ret_Z_lin, ret_pos_exp, ret_neg_exp, ret_Z_exp, ret_global, bkgMean, bkgErr


def main():
    # print "do analysis"
    returns = analysis()
    # print "done"
    print "-------------------"
    print "Final results are:"
    print "-------------------"
    print "Background:"
    print "bkg = ", returns[7], " +- ", returns[8]
    print "-------------------"
    print "Positive region"
    print "linear:"
    print "lambda = ", returns[0][0], " +- ", returns[0][1]
    print "tau = ", 1. / returns[0][0], " +- ", returns[0][1] / returns[0][0]**2.
    print "b = ", returns[0][2], " +- ", returns[0][3]
    print "exponential:"
    print "lambda = ", returns[3][2], " +- ", returns[3][3]
    print "A = ", returns[3][0], " +- ", returns[3][1]
    print "-------------------"
    print "Negative region"
    print "linear:"
    print "lambda = ", returns[1][0], " +- ", returns[1][1]
    print "tau = ", 1. / returns[1][0], " +- ", returns[1][1] / returns[1][0]**2.
    print "b = ", returns[1][2], " +- ", returns[1][3]
    print "exponential:"
    print "lambda = ", returns[4][2], " +- ", returns[4][3]
    print "A = ", returns[4][0], " +- ", returns[4][1]
    print "-------------------"
    print "Heavy Nuclei region"
    print "linear:"
    print "lambda = ", returns[2][0], " +- ", returns[2][1]
    print "b = ", returns[2][2], " +- ", returns[2][3]
    print "exponential:"
    print "lambda = ", returns[5][2], " +- ", returns[5][3]
    print "A = ", returns[5][0], " +- ", returns[5][1]
    print "-------------------"
    print "Global Exp. Fit:"
    print "A1 = ", returns[6][0][0], " +- ", returns[6][1][0]
    print "A2 = ", returns[6][0][1], " +- ", returns[6][1][1]
    print "A3 = ", returns[6][0][2], " +- ", returns[6][1][2]
    print "bkg = ", returns[6][0][3], " +- ", returns[6][1][3]
    print "lambda 1 = ", returns[6][0][4], " +- ", returns[6][1][4]
    print "lambda 2 = ", returns[6][0][5], " +- ", returns[6][1][5]
    print "lambda 3 = ", returns[6][0][6], " +- ", returns[6][1][6]


main()
