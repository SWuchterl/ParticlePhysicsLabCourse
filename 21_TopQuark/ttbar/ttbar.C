#include "TTBarAnalysis.h"
#include "Plotter.h"
#include <iostream>
#include <fstream>
using namespace std;
#include <string>
#include <TChain.h>
#include <TGraphAsymmErrors.h>
#include <TF1.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <TRandom.h>
#include <TMath.h>

int main()
{
  //////////////////////////////////////////////////////////////////////
  // configuration

	//Want trigger eff histos?
	bool measureTrig = false;
	//Want trigger mass constrained top mass histos?
	bool massConstrained = true;


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
  double jet_smear = 0.;
  double muon_scale = 1.0;

  //////////////////////////////////////////////////////////////////////
  // data analysis

 //Gaussian for Jet energy resolution smearing





  // data sample
  //~ TTBarAnalysis *A = new TTBarAnalysis(measureTrig,1.0, 1.0, 1.0, 0.0, 1.0);
  TTBarAnalysis *A = new TTBarAnalysis(massConstrained,measureTrig,1.0, 1.0, 1.0, 0.0, 1.0);
  TChain* ch = new TChain("events");
  ch->Add("files/data.root");
  ch->Process(A);

  // ttbar sample
  TTBarAnalysis *B = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch2 = new TChain("events");
  ch2->Add("files/ttbar.root");
  ch2->Process(B);

  // w+jets sample
  TTBarAnalysis *C = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch3 = new TChain("events");
  ch3->Add("files/wjets.root");
  ch3->Process(C);

  // Drell-Yan sample
  TTBarAnalysis *D = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch4 = new TChain("events");
  ch4->Add("files/dy.root");
  ch4->Process(D);

  // WW sample
  TTBarAnalysis *E = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch5 = new TChain("events");
  ch5->Add("files/ww.root");
  ch5->Process(E);

  TTBarAnalysis *F = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch6 = new TChain("events");
  ch6->Add("files/wz.root");
  ch6->Process(F);

  // ZZ sample
  TTBarAnalysis *G = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
  TChain* ch7 = new TChain("events");
  ch7->Add("files/zz.root");
  ch7->Process(G);

  // QCD sample
  TTBarAnalysis *H = new TTBarAnalysis(massConstrained,measureTrig,BTagScale, weight_factor, jet_scale, jet_smear, muon_scale);
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
  
  
  // Want histos for trigger efficiency measurement?
	

	int status;
    int status2;
    int status3;
	//~ string folderTrig;
    //~ folderTrig = "TriggerMeasurement";
	status = mkdir("TriggerMeasurement", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	//~ string folderElse = "Plots";
	status2 = mkdir("Plots", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
	status3 = mkdir("Plots_constrained", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
  
  if (measureTrig) {
  
	  //~ --------------------------DATA~ 
	  //~ P.SetData(A->histo, std::string("Data")); 

	  // add backgrounds to plotter
	  P.AddBg(B->histo, std::string("TTbar"));
	  P.AddBg(C->histo, std::string("Wjets"));
	  P.AddBg(D->histo, std::string("DY"));
	  P.AddBg(E->histo, std::string("WW"));
	  P.AddBg(F->histo, std::string("WZ"));
	  P.AddBg(G->histo, std::string("ZZ"));
	  P.AddBg(H->histo, std::string("QCD"));

	  // Print logarithmic plots to PDF file "results_log.pdf"
	  P.Plot(string("TriggerMeasurement/results_log.pdf"), true);
	  // Print linear plots to PDF file "results_lin.pdf"
	  P.Plot(string("TriggerMeasurement/results_lin.pdf"), false);
	}
	else{
	  //~ --------------------------DATA~ 
	  P.SetData(A->histo, std::string("Data")); 

	  // add backgrounds to plotter
	  P.AddBg(B->histo, std::string("TTbar"));
	  P.AddBg(C->histo, std::string("Wjets"));
	  P.AddBg(D->histo, std::string("DY"));
	  P.AddBg(E->histo, std::string("WW"));
	  P.AddBg(F->histo, std::string("WZ"));
	  P.AddBg(G->histo, std::string("ZZ"));
	  P.AddBg(H->histo, std::string("QCD"));

	  // Print logarithmic plots to PDF file "results_log.pdf"
      if(!massConstrained){
          P.Plot(string("Plots/results_log.pdf"), true);
          // Print linear plots to PDF file "results_lin.pdf"
          P.Plot(string("Plots/results_lin.pdf"), false);	
      }
      else{
        P.Plot(string("Plots_constrained/results_log.pdf"), true);
          // Print linear plots to PDF file "results_lin.pdf"
          P.Plot(string("Plots_constrained/results_lin.pdf"), false);	
      }
	}



  //////////////////////////////////////////////////////////////////////
  // computation of results

  // here you can add the computation of the results, e.g. trigger efficiency,
  // top quark cross-section or top-quark mass. In order to do this, you need
  // to access the histograms in the individual files. This can be done easily
  // and is shown in an example in the next lines.

  // as an example, extract number of events in muon pT histogram in data
  //~ TH1D * h_data_muonpt = A->histo["Muon_Pt"];
  //~ double NMuonsData = h_data_muonpt->Integral();
  //~ cout << "Found " << NMuonsData << " muons in " << lumi << "/pb data." << endl;
    
    float eventsSelData= A->events_sel;
    float eventsSelData2= A->events_sel2;//for mass measurement/different cuts
    float eventsSelTT =B->events_sel;
    float eventsSelTT2 =B->events_sel2;//for mass measurement/different cuts
    float eventsSelWJets =C->events_sel;
    float eventsSelDY =D->events_sel;
    float eventsSelWW =E->events_sel;
    float eventsSelWZ =F->events_sel;
    float eventsSelZZ =G->events_sel;
    float eventsSelQCD =H->events_sel;
    float eventsTotalTT =B->events_total;
    
    float eventsSelBKG = eventsSelWJets+eventsSelDY+eventsSelWW+eventsSelWZ+eventsSelZZ+eventsSelQCD;
    
    float scaleLumi = 1.;
    float scaleTheo = 1.; //10% for MC cross section fo BKG; in TT it cancels out
    float scaleTrigger = 1.0; //5% for SingleMuonTrigger - put into acceptance
    
    float acceptance = eventsSelTT/eventsTotalTT;
    float crossSection = (eventsSelData-eventsSelBKG*scaleTheo)/(acceptance*scaleTrigger*scaleLumi*lumi);
    
    //stat. Error only on measured Data / sqrt(N)
    float ErrEventsSelData = TMath::Sqrt(eventsSelData);
    float ErrEventsSelBKG = TMath::Sqrt(eventsSelBKG);
    //~ cout << "ErrEventsSelData: " << ErrEventsSelData<<endl;
    //- error propagation gives:
    //~ float ErrCrossSection = ErrEventsSelData/(acceptance*lumi);
    float ErrCrossSection = TMath::Sqrt(ErrEventsSelBKG*ErrEventsSelBKG+ErrEventsSelData*ErrEventsSelData)/(acceptance*lumi);
    
    
    
    cout << "Events Selected and triggered in ttbar: " << eventsSelTT<<endl;
    cout << "Events Selected and triggered in ttbar2: " << eventsSelTT2<<endl;
    cout << "Events Selected and triggered in Data: " << eventsSelData<<endl;
    cout << "Events Selected and triggered in Data2: " << eventsSelData2<<endl;
    cout << "Events total in ttbar: " << eventsTotalTT<<endl;
    cout << "Events selected in BKGs: " << eventsSelBKG<<endl;
    cout << "acceptance: " << acceptance<<endl;
    cout << "cross section[pb^-1]: " << crossSection<<endl;
    cout << "stat Unc. cross section[pb^-1] +- : " << ErrCrossSection<<endl;

    int status4;
    status4 = mkdir("crossSection", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);


    //if one wants to write files with the values.... comment in....

    //~ ofstream myfile;
    //~ myfile.open ("crossSection/crossSection_Smear.txt");
    //~ myfile<< "scaleLumi " << scaleLumi << "\n";
    //~ myfile<< "scaleTheo " << scaleTheo << "\n";
    //~ myfile<< "scaleTrigger " << scaleTrigger << "\n";
    //~ myfile<< "jetScale " << jet_scale << "\n";
    //~ myfile<< "muonScale " << muon_scale << "\n";
    //~ myfile<< "weightFactor " << weight_factor << "\n";
    //~ myfile<< "BTagScale " << BTagScale << "\n";
    //~ myfile<< "jetSmear " << jet_smear << "\n";
    //~ myfile<< "Events Selected and triggered in ttbar: " << eventsSelTT << "\n";
    //~ myfile<< "Events Selected and triggered in Data: " << eventsSelData << "\n";
    //~ myfile<< "Events total in ttbar: " << eventsTotalTT << "\n";
    //~ myfile<< "Events selected in BKGs: " << eventsSelBKG << "\n";
    //~ myfile<< "acceptance: " << acceptance << "\n";
    //~ myfile<< "cross section[pb^-1]: " <<crossSection << "\n";
    //~ myfile<< "stat Unc. cross section[pb^-1]: " <<ErrCrossSection << "\n";
    //~ myfile.close();


  //////////////////////////////////////////////////////////////////////
  // saving results to a file

  // the next lines show how you can write individual histograms to a file,
  // with which you can work later.
  
  //~ TFile f("results.root", "RECREATE");
  //~ h_data_muonpt->Write();
  //~ A->histo["NIsoMuon"]->Write();
  
  // After writing the histograms, you need to close the file.
  //~ f.Close();

  // you can also save all histograms from one process in a file.
  if (measureTrig) {
	  //~ A->histo.Write("results.root");
	  B->histo.Write("TriggerMeasurement/ttbar.root");
	  //~ C->histo.Write("wjets.root");
	  //~ D->histo.Write("dy.root");
	  //~ E->histo.Write("ww.root");
	  //~ F->histo.Write("wz.root");
	  //~ G->histo.Write("zz.root");
	  //~ H->histo.Write("qcd.root");
  }
  else{
      if (!massConstrained){
	  A->histo.Write("Plots/results.root");
  	  B->histo.Write("Plots/ttbar.root");
	  C->histo.Write("Plots/wjets.root");
	  D->histo.Write("Plots/dy.root");
	  E->histo.Write("Plots/ww.root");
	  F->histo.Write("Plots/wz.root");
	  G->histo.Write("Plots/zz.root");
	  H->histo.Write("Plots/qcd.root");
      }
      else{
 	  A->histo.Write("Plots_constrained/results.root");
  	  B->histo.Write("Plots_constrained/ttbar.root");
	  C->histo.Write("Plots_constrained/wjets.root");
	  D->histo.Write("Plots_constrained/dy.root");
	  E->histo.Write("Plots_constrained/ww.root");
	  F->histo.Write("Plots_constrained/wz.root");
	  G->histo.Write("Plots_constrained/zz.root");
	  H->histo.Write("Plots_constrained/qcd.root");       
      }
  }
}
