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
	backgrounds = ROOT.TH1D('backgrounds', 'backgrounds', 50, 0, 250)
	datas = ROOT.TH1D('datas', 'datas', 50, 0, 250)
	for data in args.data:
		f_data = ROOT.TFile(data)
		t_data = f_data.Get(variable)
		datas.Add(t_data)
	for bkg in args.montecarlo:
		f_bkg = ROOT.TFile(bkg)
		t_bkg = f_bkg.Get(variable)
		backgrounds.Add(t_bkg)
	datas.SetLineColor(ROOT.kRed)
	c.SetLogy()
	rp = ROOT.TRatioPlot(datas, backgrounds)
	c.SetTicks(0,1)
	rp.GetLowYaxis().SetNdivisions(505)
	c.Update()
	c.Draw()
	rp.Draw()
	c.SaveAs('ratio.pdf')
	f_data.Close()
	f_bkg.Close()
