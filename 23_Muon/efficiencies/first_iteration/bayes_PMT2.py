import ROOT
import numpy as np
from ROOT import TH1F, TGraphAsymmErrors, TCanvas, TF1
from array import *
from ROOT.TMath import Erf, Sqrt
from scipy.special import erf

x_data = [1750., 1801., 1850., 1900., 1952., 2003.,
          2052., 2101., 2152., 2200., 2252., 2289.]
y_data4 = [5., 30., 166., 559., 1090., 1676.,
           1910., 1963., 2004., 2024., 2071., 2004.]
y_data3 = [2456., 2434., 2456., 2451.,
           2369., 2451., 2438., 2320., 2311., 2283., 2340., 2277.]


hist4 = TH1F("hist", "efficiency PMT2", 100, x_data[0], x_data[-1])
hist3 = TH1F("hist", "3er", 100, x_data[0], x_data[-1])

for i in range(len(x_data)):
    for j in range(int(y_data4[i])):
        hist4.Fill(x_data[i])
    for k in range(int(y_data3[i])):
        hist3.Fill(x_data[i])

eff = TGraphAsymmErrors(hist4, hist3, "cl=0.683 b(1,1) mode")

eff.GetYaxis().SetRangeUser(0., 1.5)


def erfunc(x, par):
    ret = par[0] / 2. * (erf((x[0] - par[1]) / (np.sqrt(2.) * par[2])) + 1.)
    return ret


Errfunc = TF1("errFunc", erfunc, x_data[0], x_data[-1], 3)
Errfunc.SetParameters(1., 1950., 70.)
eff.Fit("errFunc", "", "", x_data[0], x_data[-1])


print "mean: ", Errfunc.GetParameter(1)
print "mean unc.: ", Errfunc.GetParError(1)
print "sigma: ", Errfunc.GetParameter(2)
print "sigma unc.: ", Errfunc.GetParError(2)
print "mean+2*sigma: ", Errfunc.GetParameter(1) + 2. * Errfunc.GetParameter(2)
print "mean+2*sigma unc.: ", np.sqrt(Errfunc.GetParError(1)**2. + 2 * Errfunc.GetParError(2)**2.)

c1 = TCanvas('c1', 'Example', 1000, 1000)
ROOT.gStyle.SetOptFit(1)
eff.Draw("AP")
eff.SetTitle("Efficiency PMT2; Voltage [V]; efficiency")
c1.SaveAs("bayes_fitPMT_2_first.pdf")

with open('PMT2_first_bayes.txt', 'wb') as f:
    f.write('mean: ' + str(Errfunc.GetParameter(1)) + '\n')
    f.write('mean unc.: ' + str(Errfunc.GetParError(1)) + '\n')
    f.write('sigma: ' + str(Errfunc.GetParameter(2)) + '\n')
    f.write('sigma unc.: ' + str(Errfunc.GetParError(2)) + '\n')
    f.write('mean+2*sigma: ' + str(Errfunc.GetParameter(1) +
                                   2. * Errfunc.GetParameter(2)) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(Errfunc.GetParError(1)**2. + 2 * Errfunc.GetParError(2)**2.)) + '\n')
    f.close()
