/*
 * Plotter.C
 *
 *  Created on: 25.06.2012
 *      Author: csander
 *  Modified last on: 15.09.2013
 *      Author: mweber
 */

#include "Plotter.h"
#include <TMath.h>
#include <iostream>

Plotter::Plotter() {
}

Plotter::~Plotter() {
}

void Plotter::Plot(std::string filename, bool DrawLog)
{
  gROOT->Reset();
  //gROOT->SetStyle("Plain");

  TStyle *MyStyle = new TStyle("MyStyle","My Root Styles");
  MyStyle->SetStatColor(0);
  MyStyle->SetCanvasColor(0);
  MyStyle->SetPadColor(0);
  MyStyle->SetPadBorderMode(0);
  MyStyle->SetCanvasBorderMode(0);
  MyStyle->SetFrameBorderMode(0);
  MyStyle->SetOptStat(0);
  MyStyle->SetStatBorderSize(2);
  MyStyle->SetOptTitle(0);
  MyStyle->SetPadTickX(1);
  MyStyle->SetPadTickY(1);
  MyStyle->SetPadBorderSize(2);
  MyStyle->SetPalette(51, 0);
  MyStyle->SetPadBottomMargin(0.15);
  MyStyle->SetPadTopMargin(0.05);
  MyStyle->SetPadLeftMargin(0.15);
  MyStyle->SetPadRightMargin(0.25);
  MyStyle->SetTitleColor(1);
  MyStyle->SetTitleFillColor(0);
  MyStyle->SetTitleFontSize(0.03);
  MyStyle->SetTitleX(0.15);
  MyStyle->SetTitleBorderSize(0);
  MyStyle->SetLineWidth(1);
  MyStyle->SetHistLineWidth(3);
  MyStyle->SetLegendBorderSize(0);
  MyStyle->SetNdivisions(502, "x");
  MyStyle->SetMarkerSize(0.8);
  MyStyle->SetTickLength(0.03);
  MyStyle->SetTitleOffset(1.5, "x");
  MyStyle->SetTitleOffset(1.5, "y");
  MyStyle->SetTitleOffset(1.0, "z");
  MyStyle->SetLabelSize(0.05, "x");
  MyStyle->SetLabelSize(0.05, "y");
  MyStyle->SetLabelSize(0.05, "z");
  MyStyle->SetLabelOffset(0.03, "x");
  MyStyle->SetLabelOffset(0.03, "y");
  MyStyle->SetLabelOffset(0.03, "z");
  MyStyle->SetTitleSize(0.05, "x");
  MyStyle->SetTitleSize(0.05, "y");
  MyStyle->SetTitleSize(0.05, "z");
  gROOT->SetStyle("MyStyle");

  // loop over all histograms
  for (unsigned int i = 0; i < bg[0].size(); i++) {
    THStack *hs = 0;
    TLegend *l;
    int Nset = data.size() + bg.size() + signal.size();
    if (Nset > 20)
      Nset = 20.;
    l = new TLegend(0.76, 0.95 - 0.8 * Nset / 20., 1.0, 0.95, bg[0][i]->GetName());
    l->SetFillStyle(1001);
    l->SetFillColor(kWhite);
    l->SetLineColor(kWhite);
    l->SetLineWidth(2);
    if (bg.size() > 0) {
      hs = new THStack("hs", bg[0][i]->GetName());
      for (unsigned int j = 0; j < bg.size(); j++) {
	TH1D * histo = bg[j][i];
	switch (j) {
	  case 0:
	    histo->SetFillColor(kRed);
	    break;
	  case 1:
	    histo->SetFillColor(kOrange);
	    break;
	  case 2:
	    histo->SetFillColor(kYellow);
	    break;
	  case 3:
	    histo->SetFillColor(kGreen);
	    break;
	  case 4:
	    histo->SetFillColor(kCyan);
	    break;
	  case 5:
	    histo->SetFillColor(kBlue);
	    break;
	  case 6:
	    histo->SetFillColor(kMagenta);
	    break;
	  case 7:
	    histo->SetFillColor(kGray);
	    break;
	  case 8:
	    histo->SetFillColor(kGray + 2);
	    break;
	  default:
	    histo->SetFillColor(kBlack);
	    break;
	}
	hs->Add(histo);
	l->AddEntry(histo, bg_names.at(j).c_str(), "f");
      }
    }
    TCanvas *c = new TCanvas("c", "c", 800, 600);
    c->SetLogy(DrawLog);
    std::string plotname;
    if (data.size() > 0 && data[0][i]->Integral() > 0) {
      TH1D * histo = data[0][i];
      plotname = std::string(histo->GetName());
      //~ histo->SetMaximum(histo->GetMaximum()+4*TMath::Sqrt(histo->GetMaximum()));
      //~ histo->SetMaximum(histo->GetMaximum()*1.1);
      if (DrawLog) {
		histo->SetMinimum(0.1);
		histo->SetMaximum(histo->GetMaximum()*1.5);
      }
      else{
		histo->SetMaximum(histo->GetMaximum()*1.15);

	  }
      histo->GetXaxis()->SetTitleOffset(1.3);
      histo->GetYaxis()->SetTitleOffset(1.3);
      histo->GetYaxis()->SetTitle("Events");
      histo->GetXaxis()->SetNdivisions(505);
      histo->Draw("");
      l->AddEntry(histo, data_names.at(0).c_str(), "p");
      if (bg.size() > 0)
	hs->Draw("histsame");
      histo->SetMarkerStyle(20);
      histo->Draw("psame");
      l->Draw("same");
    }
    if ((data.size() == 0 && bg.size() > 0) || (data.size() > 0 && data[0][i]->Integral() == 0)) {
      TH1D * histo = bg[0][i];
      plotname = std::string(histo->GetName());
      if (DrawLog) {
	hs->SetMinimum(0.1);
	histo->SetMaximum(histo->GetMaximum()*1.5);
      }
      else{
		  histo->SetMaximum(histo->GetMaximum()*1.15);
	  }
      hs->Draw("hist");
      hs->GetXaxis()->SetTitleOffset(1.3);
      hs->GetXaxis()->SetNdivisions(505);
      hs->GetYaxis()->SetTitleOffset(1.3);
      if (bg.size() > 0)
	hs->GetXaxis()->SetTitle(histo->GetXaxis()->GetTitle());
      hs->GetYaxis()->SetTitle("Events");
      l->Draw("same");
    }
    gPad->RedrawAxis();
    if (i == 0 && N_histos > 1) {
      c->Print((filename+std::string("(")).c_str());
    }
    else if (i > 0 && i == N_histos - 1)
      c->Print((filename+std::string(")")).c_str());
    else {
      c->Print(filename.c_str());
    }
  }
}
