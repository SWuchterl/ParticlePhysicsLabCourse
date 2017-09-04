#include "TTBarAnalysis.h"
#include "Plotter.h"
#include <iostream>
#include <string>
#include <TChain.h>
#include <TGraphAsymmErrors.h>
#include <TF1.h>

int main()
{
  //////////////////////////////////////////////////////////////////////
  // configuration

  // luminosity of data sample
  double lumi = 50.;

  //////////////////////////////////////////////////////////////////////
  // systematic effects handling

  // b-tagging scale factor, default is 0.95
  double BTagScale = 0.95;

  // an additional weight that will be given to the event
  double weight_factor = 1.0;

  // Jet scale and resolution, muon scale
  double jet_scale = 1.0;
  double jet_smear = 0.0;
  double muon_scale = 1.0;

  //////////////////////////////////////////////////////////////////////
  // data analysis

  // data sample
  TTBarAnalysis *A = new TTBarAnalysis(1.0, 1.0, 1.0, 0.0, 1.0);
  TChain* ch = new TChain("events");
  ch->Add("files/data.root");
  ch->Process(A);

  // ttbar sample
  TTBarAnalysis *B = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch2 = new TChain("events");
  ch2->Add("files/ttbar.root");
  ch2->Process(B);

  // w+jets sample
  TTBarAnalysis *C = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch3 = new TChain("events");
  ch3->Add("files/wjets.root");
  ch3->Process(C);

  // Drell-Yan sample
  TTBarAnalysis *D = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch4 = new TChain("events");
  ch4->Add("files/dy.root");
  ch4->Process(D);

  // WW sample
  TTBarAnalysis *E = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch5 = new TChain("events");
  ch5->Add("files/ww.root");
  ch5->Process(E);

  TTBarAnalysis *F = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch6 = new TChain("events");
  ch6->Add("files/wz.root");
  ch6->Process(F);

  // ZZ sample
  TTBarAnalysis *G = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch7 = new TChain("events");
  ch7->Add("files/zz.root");
  ch7->Process(G);

  // QCD sample
  TTBarAnalysis *H = new TTBarAnalysis(BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch8 = new TChain("events");
  ch8->Add("files/qcd.root");
  ch8->Process(H);

  //////////////////////////////////////////////////////////////////////
  // plotting

  // Initialize Plotter
  Plotter P;

  // Develop your analysis blindly, i.e. without looking at the data.  Leave
  // the next line commented out when designing your analysis, and only plot
  // data after deciding on all cuts.
  
  //~ --------------------------DATA
  //~ 
  //~ 
  P.SetData(A->histo, std::string("Data"));
  //~ 
//~ ------------------------------------------------


  // add backgrounds to plotter
  P.AddBg(B->histo, std::string("TTbar"));
  P.AddBg(C->histo, std::string("Wjets"));
  P.AddBg(D->histo, std::string("DY"));
  P.AddBg(E->histo, std::string("WW"));
  P.AddBg(F->histo, std::string("WZ"));
  P.AddBg(G->histo, std::string("ZZ"));
  P.AddBg(H->histo, std::string("QCD"));

  // Print logarithmic plots to PDF file "results_log.pdf"
  P.Plot(string("results_log.pdf"), true);
  // Print linear plots to PDF file "results_lin.pdf"
  P.Plot(string("results_lin.pdf"), false);

  //////////////////////////////////////////////////////////////////////
  // computation of results

  // here you can add the computation of the results, e.g. trigger efficiency,
  // top quark cross-section or top-quark mass. In order to do this, you need
  // to access the histograms in the individual files. This can be done easily
  // and is shown in an example in the next lines.

  // as an example, extract number of events in muon pT histogram in data
  TH1D * h_data_muonpt = A->histo["Muon_Pt"];
  double NMuonsData = h_data_muonpt->Integral();
  cout << "Found " << NMuonsData << " muons in " << lumi << "/pb data." << endl;
  
  //////////////////////////////////////////////////////////////////////
  // saving results to a file

  // the next lines show how you can write individual histograms to a file,
  // with which you can work later.
  TFile f("results.root", "RECREATE");
  h_data_muonpt->Write();
  A->histo["NIsoMuon"]->Write();
  // After writing the histograms, you need to close the file.
  f.Close();

  // you can also save all histograms from one process in a file.
  B->histo.Write("ttbar.root");
}
