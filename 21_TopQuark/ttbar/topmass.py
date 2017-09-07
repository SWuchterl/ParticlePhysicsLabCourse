#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import numpy as np
import argparse
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

data_samples = ['Plots/results.root']
mc_samples = ['Plots/ttbar.root', 'Plots/dy.root', 'Plots/wjets.root', 'Plots/ww.root', 'Plots/wz.root', 'Plots/zz.root', 'Plots/qcd.root']
topmasses = ['topmass_hadr','topmass_lept']

labels = {
    'topmass_hadr': "m_{t,hadronic} [GeV]",
    'topmass_lept':"m_{t,semileptonic} [GeV]"
}

for topmass in topmasses:
    NBINS = int(20)
    XLOW =  float(100)
    XUP = float(300)

    c = ROOT.TCanvas("canvas","",600,600)
    #c.SetGrid()
    stacked = ROOT.THStack('stacked', 'stacked')

    #MONTE CARLOS
    #TTbar
    ttbar = ROOT.TH1F('TTbar background', 'TTbar background', NBINS, XLOW, XUP)
    f_ttbar = ROOT.TFile(mc_samples[0])
    t_ttbar = f_ttbar.Get(topmass)
    ttbar.Add(t_ttbar)
    f_ttbar.Close()
    ttbar.SetFillColor(ROOT.kRed)
    stacked.Add(ttbar)

    #DY
    dy = ROOT.TH1F('DY background', 'DY background', NBINS, XLOW, XUP)
    f_dy = ROOT.TFile(mc_samples[1])
    t_dy = f_dy.Get(topmass)
    dy.Add(t_dy)
    f_dy.Close()
    dy.SetFillColor(ROOT.kYellow)
    stacked.Add(dy)

    #W+jets
    wjets = ROOT.TH1F('W+jets background', 'W+jets background', NBINS, XLOW, XUP)
    f_wjets = ROOT.TFile(mc_samples[2])
    t_wjets = f_wjets.Get(topmass)
    wjets.Add(t_wjets)
    f_wjets.Close()
    wjets.SetFillColor(ROOT.kOrange)
    stacked.Add(wjets)

    #WW
    ww = ROOT.TH1F('WW background', 'WW background', NBINS, XLOW, XUP)
    f_ww = ROOT.TFile(mc_samples[3])
    t_ww = f_ww.Get(topmass)
    ww.Add(t_ww)
    f_ww.Close()
    ww.SetFillColor(ROOT.kGreen)
    stacked.Add(ww)

    #WZ
    wz = ROOT.TH1F('WZ background', 'WZ background', NBINS, XLOW, XUP)
    f_wz = ROOT.TFile(mc_samples[4])
    t_wz = f_wz.Get(topmass)
    wz.Add(t_wz)
    f_wz.Close()
    wz.SetFillColor(ROOT.kCyan)
    stacked.Add(wz)

    #ZZ
    zz = ROOT.TH1F('ZZ background', 'ZZ background', NBINS, XLOW, XUP)
    f_zz = ROOT.TFile(mc_samples[5])
    t_zz = f_zz.Get(topmass)
    zz.Add(t_zz)
    f_zz.Close()
    zz.SetFillColor(ROOT.kBlue)
    stacked.Add(zz)

    #QCD
    qcd = ROOT.TH1F('QCD background', 'QCD background', NBINS, XLOW, XUP)
    f_qcd = ROOT.TFile(mc_samples[6])
    t_qcd = f_qcd.Get(topmass)
    qcd.Add(t_qcd)
    f_qcd.Close()
    qcd.SetFillColor(ROOT.kMagenta)
    stacked.Add(qcd)

    #DATA
    data = ROOT.TH1F('data', 'data', NBINS, XLOW, XUP)
    f_data = ROOT.TFile(data_samples[0])
    t_data = f_data.Get(topmass)
    data.Add(t_data)
    f_data.Close()
    #data.SetFillStyle(3001)
    data.SetMarkerStyle(20)
    data.SetMarkerSize(0.8)
    data.SetFillColor(ROOT.kBlack)
    data.Sumw2()

    #Styles
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetLineWidth(1)
    legend = ROOT.TLegend(0.6,0.6,0.8,0.8)
    legend.AddEntry(data, 'Data', 'p')
    legend.AddEntry(ttbar, 'TTbar', 'f')
    legend.AddEntry(dy, 'DY', 'f')
    legend.AddEntry(wjets, 'W+jets', 'f')
    legend.AddEntry(ww, 'WW', 'f')
    legend.AddEntry(wz, 'WZ', 'f')
    legend.AddEntry(zz, 'ZZ', 'f')
    legend.AddEntry(qcd, 'QCD', 'f')

    #fit
    
    
    def func(x,par):
		ret=1./(2.*np.pi)*(par[1])/((x[0]-par[0])**2. + par[1]**2. /4.)
		un=par[3]
		return par[2]*ret+un
    
    
    breitwigner = ROOT.TF1('breitwigner', func, 100,300, 4)
    breitwigner.SetParameters(175.,5.,100.,1.)
    breitwigner.SetParNames("mean","width","ampl","const")
    breitwigner.SetLineColor(ROOT.kGreen)
    breitwigner.SetLineStyle(2)
    breitwigner.SetLineWidth(3)
    data.Fit('breitwigner',"","",100,300)


    stacked.Draw('hist')
    data.Draw('same')
    stacked.GetXaxis().SetTitle(labels[topmass])
    stacked.GetYaxis().SetTitle('Events/Bin')
    c.Modified()
    c.Update()
    c.SaveAs('topmass_plots/'+str(topmass)+'_fit.pdf')
    c.IsA().Destructor(c)