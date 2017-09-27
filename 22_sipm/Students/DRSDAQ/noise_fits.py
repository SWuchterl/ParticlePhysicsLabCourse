#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from array import array
import numpy as np
import argparse
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Perform topmass plots.",
                                 fromfile_prefix_chars="@", conflict_handler="resolve")
#~ parser.add_argument("--constrain", default=False, action='store_true',
#~ help="Perform topmass plots. Either with or without constrain. [Default: %(default)s]")
args = parser.parse_args()



data_samples = ['root-scripts/finger574.root','root-scripts/finger564.root','root-scripts/finger554.root','root-scripts/finger544.root','root-scripts/finger534.root']
OVs = ['finger574','finger564','finger554','finger544','finger534']
Title = ['574','564','554','544','534']
fitranges = [[[17.,28.],[38.,44.],[55.,65.]],
			[[11.,18.75],[26.,38.],[44.,52.]],
			[[10.5,17.5],[22.,30.],[32.,44.]],
			[[10.5,21.],[22.,38.]],
			[[13.5,18.5],[13.5,18.5]]]



arProb = []
arErrProb = []

for i in xrange(5):
    NBINS = int(100)
    XLOW = float(10)
    XUP = float(90)

    c = ROOT.TCanvas("canvas", "", 800, 800)
    c.SetLogy()
    # c.SetGrid()
    #~ stacked = ROOT.THStack('stacked', 'stacked')

    # MONTE CARLOS
    # TTbar
    #~ ttbar = ROOT.TH1F('TTbar background', 'TTbar background', NBINS, XLOW, XUP)
    #~ f_ttbar = ROOT.TFile(mc_samples_constrained[0] if args.constrain else mc_samples_original[0])
    #~ t_ttbar = f_ttbar.Get(topmass)
    #~ ttbar.Add(t_ttbar)
    #~ f_ttbar.Close()
    #~ ttbar.SetFillColor(ROOT.kRed)
    #~ stacked.Add(ttbar)

    # DATA
    data = ROOT.TH1F('data', 'Noise ' + Title[i][0] + Title[i]
                     [1] + '.' + Title[i][2] + ' OV [V]', NBINS, XLOW, XUP)
    #~ data = ROOT.TH1F('data', 'data')
    f_data = ROOT.TFile(data_samples[i])
    t_data = f_data.Get("finger")
    data.Add(t_data)
    f_data.Close()
    data.SetFillStyle(3001)
    #~ data.SetMarkerStyle(20)
    #~ data.SetMarkerSize(0.8)
    data.SetFillColor(ROOT.kBlue - 4)
    #~ data.Sumw2()

    # Styles
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(1)
    ROOT.gStyle.SetLineWidth(1)
    #~ legend = ROOT.TLegend(0.7,0.5,0.9,0.7)
    #~ legend.AddEntry(data, 'Data', 'p')
    #~ legend.AddEntry(ttbar, 'TTbar', 'f')


    #fit
    def func(x,par):
		ret=par[0]*2.718281**(-0.5*((x[0]-par[1])/par[2])**2.)
		#~ un=par[3]
		#~ return ret+un
		return ret

    #~ gaus1 = ROOT.TF1('g1', func, fitranges[i][0][0],fitranges[i][0][1], 4)
    gaus1 = ROOT.TF1('g1', func, fitranges[i][0][0],fitranges[i][0][1], 3)
    gaus1.SetParNames("amplitude","mean","width")
    gaus1.SetParameters(22000.,20.,5.)
    #~ gaus1.SetParLimits(2,0.,99999999.)



    if(i<3):
		#~ gaus2 = ROOT.TF1('g2', func, fitranges[i][1][0],fitranges[i][1][1], 4)
		gaus2 = ROOT.TF1('g2', func, fitranges[i][1][0],fitranges[i][1][1], 3)
		gaus2.SetParNames("amplitude","mean","width")
		gaus2.SetParameters(2200.,20.,5.)

    if(i<2):
		gaus3 = ROOT.TF1('g3', func, fitranges[i][2][0],fitranges[i][2][1], 3)
		gaus3.SetParNames("amplitude","mean","width")
		gaus3.SetParameters(200.,20.,5.)

    data.Fit('g1',"","",fitranges[i][0][0],fitranges[i][0][1])
    if (i<3):
		data.Fit('g2',"+","",fitranges[i][1][0],fitranges[i][1][1])
    if (i<3):
		data.Fit('g3',"+","",fitranges[i][2][0],fitranges[i][2][1])

    #~ ROOT.gStyle.SetOptFit(1)

    # fit parameter to legend
    data.Draw('same')
    #~ legend.Draw('same')
    data.GetXaxis().SetTitle("U [mV]")
    data.GetYaxis().SetTitle('Events/Bin')
    c.Modified()
    c.Update()
    c.SaveAs('noise_plots/' + str(OVs[i]) + '_gaussFits.pdf')
    errors1 = gaus1.GetParErrors()
    if(i < 3):
        errors2 = gaus2.GetParErrors()
        errors3 = gaus3.GetParErrors()


# calculate probability:

    #~ border1=[30,24,20,20,20]

    border1=[30,22,20,22,20]
    er1_nom=ROOT.Double(0)
    er1_denom=ROOT.Double(0)
    nominator=data.IntegralAndError(border1[i],90,er1_nom)
    denominator=data.IntegralAndError(0,90,er1_denom)
    prob=nominator/denominator
    er1=(er1_nom/nominator)**2.+(er1_denom/denominator)**2.
    er1=np.sqrt(er1)*prob

    arProb.append(prob)
    arErrProb.append(er1)
    print "prob1", prob * 100., "+-", er1 * 100.

    # save to pickle
    with open('noise_plots/noiseGaussFits_' + str(OVs[i]) + '.txt', 'wb') as fitparams:
        fitparams.write('Mean: {0}'.format(gaus1.GetParameter(1)) + ' +/- {0}'.format(errors1[1]) + '\n')
        fitparams.write('Width: {0}'.format(gaus1.GetParameter(2)) + ' +/- {0}'.format(errors1[2]) + '\n')
        fitparams.write('Amplitude: {0}'.format(gaus1.GetParameter(0)) + ' +/- {0}'.format(errors1[0]) + '\n')
        if(i < 3):
            fitparams.write('Mean 2: {0}'.format(gaus2.GetParameter(1)) + ' +/- {0}'.format(errors2[1]) + '\n')
            fitparams.write('Width 2: {0}'.format(gaus2.GetParameter(2)) + ' +/- {0}'.format(errors2[2]) + '\n')
            fitparams.write('Amplitude 2: {0}'.format(gaus2.GetParameter(0)) + ' +/- {0}'.format(errors2[0]) + '\n')
        if(i<3):
            fitparams.write('Mean 3: {0}'.format(gaus3.GetParameter(1)) + ' +/- {0}'.format(errors3[1]) + '\n')
            fitparams.write('Width 3: {0}'.format(gaus3.GetParameter(2)) + ' +/- {0}'.format(errors3[2]) + '\n')
            fitparams.write('Amplitude 3: {0}'.format(gaus3.GetParameter(0)) + ' +/- {0}'.format(errors3[0]) + '\n')


arP = np.array(arProb)
arErrP = np.array(arErrProb)
arV = np.array([5., 4., 3., 2., 1.])
print arV
plt.figure(1)
plt.errorbar(arV,arP*100.,yerr=arErrP*100.,fmt="o-")
plt.xlabel("OV [V]")
plt.ylabel("crosstalk probability [\%]")
#~ plt.grid()
plt.savefig("test.pdf")
