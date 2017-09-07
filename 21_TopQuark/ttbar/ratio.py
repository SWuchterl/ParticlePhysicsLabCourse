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
efficiency_sample = 'TriggerMeasurement/ttbar.root'

list_of_variables = ['Muon_Pt',
					 'NIsoMuon',
					 'Muon_Eta',
					 'Muon_E',
					 'MET',
					 'Muon_Phi',
					 'Jet_Pt',
					 'Jet_Eta',
					 'Jet_E',
					 'Jet_Phi',
					 'NJetID',
					 'NJetID_btag',
					 'NPrimaryVertices',
					 'DrellYan_mll',
					 'DrellYan_met']

print list_of_variables[4]
binnings = {
	'Muon_Pt': [50, 0, 250],
	'NIsoMuon': [5, 0, 5],
	'Muon_Eta': [20,-3.5, 3.5],
	'Muon_E': [50, 0, 750],
	'MET': [25,0,500],
	'Muon_Phi': [20, -3.5, 3.5],
	'Jet_Pt': [50, 0, 250],
	'Jet_Eta': [10, -3., 3.],
	'Jet_E': [50, 0, 750],
	'Jet_Phi': [20, -3.5, 3.5],
	'NJetID': [10, 0, 10],
	'NJetID_btag': [4, 0, 4],
	'NPrimaryVertices': [36, 0, 36],
	'DrellYan_mll':	[30, 75, 105],
	'DrellYan_met': [40, 0, 80],
	'ForTrigger_Nominator': [250, 0, 250],
	'ForTrigger_Denominator': [250, 0, 250]
}

labels = {
	'Muon_Pt': "p_{T} of all muons [GeV]",
	'NIsoMuon': "Number of isolated muons",
	'Muon_Eta': "Eta of all muons",
	'Muon_E': "Energy distribution [GeV]",
	'MET': "Missing transverse energy [GeV]",
	'Muon_Phi': "Phi of all muons",
	'Jet_Pt': "p_{T} of all jets [GeV]",
	'Jet_Eta': "Eta of all jets",
	'Jet_E': "Energy distribution [GeV]",
	'Jet_Phi': "Phi of all jets",
	'NJetID': "Number of Jets(ID)",
	'NJetID_btag': "Number of b-tagged Jets(ID)",
	'NPrimaryVertices': "Number of primary Vertices",
	'DrellYan_mll':	"m_{ll} [GeV]",
	'DrellYan_met':"E_{T}^{missing} [GeV]"
}

#plot shape of variables in data
for data in data_samples:
	for variable in list_of_variables:
		c1=ROOT.TCanvas("canvas","",600,600)
		ROOT.gStyle.SetOptStat(0)
		#ROOT.gStyle.SetOptTitle(0)
		c1.SetGrid()
		c1.SetFillStyle(3001)
		c1.SetTitle(labels[variable]+" from data")
		f=ROOT.TFile(data)
		t=f.Get(variable)
		t.GetXaxis().SetTitle(labels[variable])
		t.GetYaxis().SetTitle("Events")
		t.Draw()
		c1.SaveAs(str(data)+str(variable)+'.pdf')
		f.Close()

#plot shape of variables in MC
for mc in mc_samples:
	for variable in list_of_variables:
		c1=ROOT.TCanvas("canvas","",600,600)
		ROOT.gStyle.SetOptStat(0)
		#ROOT.gStyle.SetOptTitle(0)
		c1.SetGrid()
		c1.SetFillStyle(3001)
		c1.SetTitle(labels[variable]+" from Monte Carlo")
		f=ROOT.TFile(mc)
		t=f.Get(variable)
		t.GetXaxis().SetTitle(labels[variable])
		t.GetYaxis().SetTitle("Events")
		t.Draw()
		c1.SaveAs(str(mc)+'_montecarlo_'+str(variable)+'.pdf')
		f.Close()

# do ratio plot for certain variable MC/data
for variable in list_of_variables:
	binning = binnings[variable]
	NBINS = int(binning[0])
	XLOW =  float(binning[1])
	XUP = float(binning[2])

	print labels[variable]

	print NBINS
	print XLOW
	print XUP

	print variable

	c = ROOT.TCanvas("canvas","",600,600)
	c.SetGrid()
	stacked = ROOT.THStack('stacked', 'stacked')

	#MONTE CARLOS
	#TTbar
	ttbar = ROOT.TH1F('TTbar background', 'TTbar background', NBINS, XLOW, XUP)
	f_ttbar = ROOT.TFile(mc_samples[0])
	t_ttbar = f_ttbar.Get(variable)
	ttbar.Add(t_ttbar)
	f_ttbar.Close()
	ttbar.SetFillColor(ROOT.kRed)
	stacked.Add(ttbar)


	#DY
	dy = ROOT.TH1F('DY background', 'DY background', NBINS, XLOW, XUP)
	f_dy = ROOT.TFile(mc_samples[1])
	t_dy = f_dy.Get(variable)
	dy.Add(t_dy)
	f_dy.Close()
	dy.SetFillColor(ROOT.kYellow)
	stacked.Add(dy)

	#W+jets
	wjets = ROOT.TH1F('W+jets background', 'W+jets background', NBINS, XLOW, XUP)
	f_wjets = ROOT.TFile(mc_samples[2])
	t_wjets = f_wjets.Get(variable)
	wjets.Add(t_wjets)
	f_wjets.Close()
	wjets.SetFillColor(ROOT.kOrange)
	stacked.Add(wjets)

	#WW
	ww = ROOT.TH1F('WW background', 'WW background', NBINS, XLOW, XUP)
	f_ww = ROOT.TFile(mc_samples[3])
	t_ww = f_ww.Get(variable)
	ww.Add(t_ww)
	f_ww.Close()
	ww.SetFillColor(ROOT.kGreen)
	stacked.Add(ww)

	#WZ
	wz = ROOT.TH1F('WZ background', 'WZ background', NBINS, XLOW, XUP)
	f_wz = ROOT.TFile(mc_samples[4])
	t_wz = f_wz.Get(variable)
	wz.Add(t_wz)
	f_wz.Close()
	wz.SetFillColor(ROOT.kCyan)
	stacked.Add(wz)

	#ZZ
	zz = ROOT.TH1F('ZZ background', 'ZZ background', NBINS, XLOW, XUP)
	f_zz = ROOT.TFile(mc_samples[5])
	t_zz = f_zz.Get(variable)
	zz.Add(t_zz)
	f_zz.Close()
	zz.SetFillColor(ROOT.kBlue)
	stacked.Add(zz)

	#QCD
	qcd = ROOT.TH1F('QCD background', 'QCD background', NBINS, XLOW, XUP)
	f_qcd = ROOT.TFile(mc_samples[6])
	t_qcd = f_qcd.Get(variable)
	qcd.Add(t_qcd)
	f_qcd.Close()
	qcd.SetFillColor(ROOT.kMagenta)
	stacked.Add(qcd)

	#DATA
	data = ROOT.TH1F('data', 'data', NBINS, XLOW, XUP)
	f_data = ROOT.TFile(data_samples[0])
	t_data = f_data.Get(variable)
	data.Add(t_data)
	f_data.Close()
	#data.SetFillStyle(3001)
	data.SetMarkerStyle(20)
	data.SetMarkerSize(0.8)
	data.SetFillColor(ROOT.kBlack)

	#Styles
	c.SetLogy()
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
	stacked.Draw()
	data.Draw('same')
	rp.Draw()
	legend.Draw('same')
	lines = ROOT.std.vector('double')()
	lines.push_back(1.)
	rp.SetGridlines(lines)
	rp.GetLowerRefGraph().SetMinimum(0)
	rp.GetLowerRefGraph().SetMaximum(2)
	rp.GetLowerRefYaxis().SetTitle("MC/Data")
	rp.GetUpperRefYaxis().SetTitle("Events/Bin")
	stacked.GetXaxis().SetTitle(labels[variable])
	c.Modified()
#	rp.GetLowerRefGraph().GetXaxis().SetTitle(str(labels[variable]))
	c.Update()
	c.SaveAs('MC_data_plots/'+str(variable)+'_ratio.pdf')
	c.IsA().Destructor(c)

# EFFICIENCIES
def flattenList(listOfLists):
	"""
	flatten 2D list
	return [1, 2, 3, 4, ...] for input [[1, 2], [3, 4, ...], ...]
	"""
	return [item for subList in listOfLists for item in subList]

#CALCULATE MID EFFICIENCY VALUE WITH UNCS
f=ROOT.TFile(efficiency_sample)
N=f.Get('ForTrigger_Nominator')
Nominator = N.Clone()
D=f.Get('ForTrigger_Denominator')
Denominator = D.Clone()
for i in xrange(26):
	Nominator.SetBinContent( i , 0.)
	Nominator.SetBinError( i , 0.)
	Denominator.SetBinContent( i , 0.)
	Denominator.SetBinError( i , 0.)
Nominator.Rebin(250)
Denominator.Rebin(250)
eff = ROOT.TGraphAsymmErrors(Nominator,Denominator)
eff_value = Nominator.Integral()/Denominator.Integral()
eff_low_unc = eff.GetErrorYlow(0)
eff_high_unc = eff.GetErrorYhigh(0)

print "Efficiency at p_{T}>26 [GeV]", eff_value
print "High error", eff_high_unc
print "Low error", eff_low_unc
f.Close()

#EFFICIENCY PLOT
c1=ROOT.TCanvas("canvas","",600,600)
c1.SetTitle('Efficiency')
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
pt = ROOT.TPaveText(100.,1.05,160.,1.2)
pt.AddText("L = 50 pb")
pt.AddText("Efficiency: "+str(round(eff_value, 4)))
pt.AddText("Higher stat. unc.: "+str(round(eff_high_unc, 4)))
pt.AddText("Lower stat. unc.: "+str(round(eff_low_unc, 4)))

#ERROR BAND
line_up = ROOT.TLine(0.,eff_value+0.05*eff_value,152.,eff_value+0.05*eff_value)
line_up.SetLineStyle(2)
line_down = ROOT.TLine(0.,eff_value-0.05*eff_value,152.,eff_value-0.05*eff_value)
line_down.SetLineStyle(2)
line_mid = ROOT.TLine(0.,eff_value,152.,eff_value)

c1.SetFillStyle(3001)
f=ROOT.TFile(efficiency_sample)
N=f.Get('ForTrigger_Nominator')
N_rebinned = N.Rebin(2)
D=f.Get('ForTrigger_Denominator')
D_rebinned = D.Rebin(2)
efficiency = ROOT.TGraphAsymmErrors(N_rebinned,D_rebinned)
efficiency.GetXaxis().SetRangeUser(0.,150.)
efficiency.GetXaxis().SetTitle(labels["Muon_Pt"])
efficiency.GetYaxis().SetTitle("Efficiency")
efficiency.Draw('AP')
pt.Draw('same')
line_mid.Draw('same')
line_up.Draw('same')
line_down.Draw('same')
c1.Update()
c1.SaveAs('efficiency.pdf')
f.Close()
