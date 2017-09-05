#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

parser = argparse.ArgumentParser(description="Perform plots for scikit learn classification training.",
	                                 fromfile_prefix_chars="@", conflict_handler="resolve")
parser.add_argument("-d", "--data", nargs="+", required=True, default=None,
	                    help="data file. Format same as for TChain.Add: path/to/file.root.")
parser.add_argument("-m", "--montecarlo", nargs="+", required=True, default=None,
	                    help="monte carlo file. Format same as for TChain.Add: path/to/file.root.")
parser.add_argument("-v", "--variables", nargs="+", required=True, default=None,
	            help="variables.")

args = parser.parse_args()


list_of_variables = args.variables[0].split(";")
print list_of_variables

#plot shape of variables in data
for data in args.data:
	for variable in list_of_variables:
		c1=ROOT.TCanvas("canvas","",600,600)
		ROOT.gStyle.SetOptStat(0)
		ROOT.gStyle.SetOptTitle(0)
		c1.SetGrid()
		c1.SetFillStyle(3001)
		c1.SetTitle(str(variable)+" from data")
		f=ROOT.TFile(data)
		t=f.Get(variable)
		t.Draw()
		c1.SaveAs('data_'+str(variable)+'.pdf')
		f.Close()

#plot shape of variables in MC
for mc in args.montecarlo:
	for variable in list_of_variables:
		c1=ROOT.TCanvas("canvas","",600,600)
		ROOT.gStyle.SetOptStat(0)
		ROOT.gStyle.SetOptTitle(0)
		c1.SetGrid()
		c1.SetFillStyle(3001)
		c1.SetTitle(str(variable)+" from Monte Carlo")
		f=ROOT.TFile(mc)
		t=f.Get(variable)
		t.Draw()
		c1.SaveAs(str(mc)+'_montecarlo_'+str(variable)+'.pdf')
		f.Close()

# do ratio plot for certain variable MC/data
for variable in list_of_variables:
	c = ROOT.TCanvas("canvas","",600,600)
	c.SetGrid()
	stacked = ROOT.THStack('stacked', 'stacked')

	#MONTE CARLOS
	#DY
	dy = ROOT.TH1F('DY background', 'DY background', 50, 0, 250)
	f_dy = ROOT.TFile('dy.root')
	t_dy = f_dy.Get(variable)
	dy.Add(t_dy)
	dy.SetFillColor(ROOT.kYellow)
	stacked.Add(dy)

	#W+jets
	wjets = ROOT.TH1F('W+jets background', 'W+jets background', 50, 0, 250)
	f_wjets = ROOT.TFile('wjets.root')
	t_wjets = f_wjets.Get(variable)
	wjets.Add(t_wjets)
	wjets.SetFillColor(ROOT.kOrange)
	stacked.Add(wjets)

	#WW
	ww = ROOT.TH1F('WW background', 'WW background', 50, 0, 250)
	f_ww = ROOT.TFile('ww.root')
	t_ww = f_ww.Get(variable)
	ww.Add(t_ww)
	ww.SetFillColor(ROOT.kGreen)
	stacked.Add(ww)

	#WZ
	wz = ROOT.TH1F('WZ background', 'WZ background', 50, 0, 250)
	f_wz = ROOT.TFile('wz.root')
	t_wz = f_wz.Get(variable)
	wz.Add(t_wz)
	wz.SetFillColor(ROOT.kCyan)
	stacked.Add(wz)

	#ZZ
	zz = ROOT.TH1F('ZZ background', 'ZZ background', 50, 0, 250)
	f_zz = ROOT.TFile('zz.root')
	t_zz = f_zz.Get(variable)
	zz.Add(t_zz)
	zz.SetFillColor(ROOT.kBlue)
	stacked.Add(zz)

	#QCD
	qcd = ROOT.TH1F('QCD background', 'QCD background', 50, 0, 250)
	f_qcd = ROOT.TFile('qcd.root')
	t_qcd = f_qcd.Get(variable)
	qcd.Add(t_qcd)
	qcd.SetFillColor(ROOT.kMagenta)
	stacked.Add(qcd)

	#TTbar
	ttbar = ROOT.TH1F('TTbar background', 'TTbar background', 50, 0, 250)
	f_ttbar = ROOT.TFile('ttbar.root')
	t_ttbar = f_ttbar.Get(variable)
	ttbar.Add(t_ttbar)
	ttbar.SetFillColor(ROOT.kRed)
	stacked.Add(ttbar)

	#DATA
	data = ROOT.TH1F('data', 'data', 50, 0, 250)
	f_data = ROOT.TFile(args.data[0])
	t_data = f_data.Get(variable)
	data.Add(t_data)
	#data.SetFillStyle(3001)
	data.SetMarkerStyle(20)
	data.SetMarkerSize(0.8)
	data.SetFillColor(ROOT.kBlack)

	#Styles
	#c.SetLogy()
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

	#ratio plot
	rp = ROOT.TRatioPlot(stacked, data)
	c.SetTicks(0,1)
	rp.GetLowYaxis().SetNdivisions(505)
	c.Update()
	stacked.Draw()
	data.Draw('same')
	rp.Draw()
	legend.Draw('same')
	c.SaveAs(str(variable)+'ratio.pdf')
	f_data.Close()
	f_dy.Close()
	f_wjets.Close()
	f_ww.Close()
	f_wz.Close()
	f_zz.Close()
	f_qcd.Close()
	f_ttbar.Close()
