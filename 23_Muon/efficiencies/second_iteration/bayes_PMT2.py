import ROOT
import numpy as np
from ROOT import TH1F, TGraphAsymmErrors, TCanvas, TF1
from array import *
from ROOT.TMath import Erf, Sqrt
from scipy.special import erf

x_data = [1780., 1808., 1854., 1906., 1952., 2001.,
          2051., 2103., 2158., 2201., 2251.]
y_data4 = [14., 33., 181., 531., 1039., 1508.,
           1609., 1926., 1834., 1880., 1933.]
y_data3 = [2259., 2249., 2204., 2166.,
           2249., 2205., 2128., 2263., 2164., 2101., 2172.]


hist4 = TH1F("hist", "4er", 100, x_data[0], x_data[-1])
hist3 = TH1F("hist", "3er", 100, x_data[0], x_data[-1])

for i in range(len(x_data)):
    for j in range(int(y_data4[i])):
        hist4.Fill(x_data[i])
    for k in range(int(y_data3[i])):
        hist3.Fill(x_data[i])

eff = TGraphAsymmErrors(hist4, hist3, "cl=0.683 b(1,1) mode")


def erfunc(x, par):
    ret = par[0] / 2. * (erf((x[0] - par[1]) / (np.sqrt(2.) * par[2])) + 1.)
    return ret


Errfunc = TF1("errFunc", erfunc, x_data[0], x_data[-1], 3)
Errfunc.SetParameters(1., 1950., 70.)
eff.Fit("errFunc", "", "", x_data[0], x_data[-1])


print "mean: ", Errfunc.GetParameter(0)
print "mean unc.: ", Errfunc.GetParError(0)
print "sigma: ", Errfunc.GetParameter(1)
print "sigma unc.: ", Errfunc.GetParError(1)
print "mean+2*sigma: ", Errfunc.GetParameter(0) + 2. * Errfunc.GetParameter(1)
print "mean+2*sigma unc.: ", np.sqrt(Errfunc.GetParError(0)**2. + 2 * Errfunc.GetParError(1)**2.)

c1 = TCanvas('c1', 'Example', 1000, 1000)
ROOT.gStyle.SetOptFit(1)
eff.Draw()
c1.SaveAs("bayes2.pdf")

with open('PMT2_first_bayes.txt', 'wb') as f:
    f.write('mean: ' + str(Errfunc.GetParameter(0)) + '\n')
    f.write('mean unc.: ' + str(Errfunc.GetParError(0)) + '\n')
    f.write('sigma: ' + str(Errfunc.GetParameter(1)) + '\n')
    f.write('sigma unc.: ' + str(Errfunc.GetParError(1)) + '\n')
    f.write('mean+2*sigma: ' + str(Errfunc.GetParameter(0) +
                                   2. * Errfunc.GetParameter(1)) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(Errfunc.GetParError(0)**2. + 2 * Errfunc.GetParError(1)**2.)) + '\n')
    f.close()
