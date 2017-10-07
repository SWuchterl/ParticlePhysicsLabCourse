import ROOT
import numpy as np
from ROOT import TH1F, TGraphAsymmErrors, TCanvas, TF1
from array import *
from ROOT.TMath import Erf, Sqrt
from scipy.special import erf

x_data = [1750., 1801., 1849., 1901., 1949., 2000.,
          2052., 2099., 2149., 2201., 2251.]
y_data4 = [8., 47., 180., 590., 1067., 1521.,
           1784., 1890., 1918., 1966., 1941.]
y_data3 = [2321., 2272., 2257., 2158.,
           2215., 2173., 2230., 2226., 2180., 2244., 2180.]


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


print "mean: ", Errfunc.GetParameter(0)
print "mean unc.: ", Errfunc.GetParError(0)
print "sigma: ", Errfunc.GetParameter(1)
print "sigma unc.: ", Errfunc.GetParError(1)
print "mean+2*sigma: ", Errfunc.GetParameter(0) + 2. * Errfunc.GetParameter(1)
print "mean+2*sigma unc.: ", np.sqrt(Errfunc.GetParError(0)**2. + 2 * Errfunc.GetParError(1)**2.)

c1 = TCanvas('c1', 'Example', 1000, 1000)
ROOT.gStyle.SetOptFit(1)
eff.Draw()
c1.SaveAs("bayes_fitPMT_2_third.pdf")

with open('PMT2_third_bayes.txt', 'wb') as f:
    f.write('mean: ' + str(Errfunc.GetParameter(0)) + '\n')
    f.write('mean unc.: ' + str(Errfunc.GetParError(0)) + '\n')
    f.write('sigma: ' + str(Errfunc.GetParameter(1)) + '\n')
    f.write('sigma unc.: ' + str(Errfunc.GetParError(1)) + '\n')
    f.write('mean+2*sigma: ' + str(Errfunc.GetParameter(0) +
                                   2. * Errfunc.GetParameter(1)) + '\n')
    f.write('mean+2*sigma unc.: ' +
            str(np.sqrt(Errfunc.GetParError(0)**2. + 2 * Errfunc.GetParError(1)**2.)) + '\n')
    f.close()
