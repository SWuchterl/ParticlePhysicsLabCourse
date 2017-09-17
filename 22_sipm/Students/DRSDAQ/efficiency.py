#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import numpy as np
import argparse
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt

NBINS = int(100)
XLOW =  float(0)
XUP = float(1050)

data = ROOT.TH1F('data', 'pulseheight', NBINS, XLOW, XUP)
f_data = ROOT.TFile('root-scripts/data_results.root')
t_data = f_data.Get('finger')
data.Add(t_data)
f_data.Close()

er_nom=ROOT.Double(0)
er_denom=ROOT.Double(0)

Nominator = ROOT.TH1F('Nominator', 'Nominator', NBINS, XLOW, XUP)
for i in range(NBINS):
    Nominator.SetBinContent(i, data.IntegralAndError(i,1050,er_nom))

Denominator = ROOT.TH1F('Denominator', 'Denominator', NBINS, XLOW, XUP)
for i in range(NBINS):
    Denominator.SetBinContent(i, data.IntegralAndError(0,1050,er_denom))

c1=ROOT.TCanvas("canvas","",600,600)
c1.SetTitle('Efficiency')
c1.SetGrid()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

efficiency = ROOT.TGraphAsymmErrors(Nominator,Denominator, "cl=0.683 b(1,1) mode")
efficiency.GetXaxis().SetRangeUser(0.,1050.)
efficiency.GetXaxis().SetTitle('U in [mV]')
efficiency.GetYaxis().SetTitle("Efficiency")
efficiency.Draw('AP')
c1.Update()
c1.SaveAs('efficiency.pdf')
