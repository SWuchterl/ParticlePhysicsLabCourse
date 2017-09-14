// C++ header
#include <stdlib.h>	// std lib
#include <sstream>	// stringstream
#include <iostream>	// cout
#include <unistd.h>	// usleep()
#include <typeinfo>


using namespace std;

void display(string pathIn, int nEntries = -1) {
	// open the input file
	TFile * file = new TFile((string("./../io/")+pathIn+string(".root")).c_str(),"READ");
	// retrieve the data tree from the input file
	TTree * tree = (TTree*)(file->Get("DataTree"));
	// create variables for the tree data and connect them with the ROOT tree via branch addresses
	int iEvent, eventTime;
	tree->SetBranchAddress("Event_ID", &iEvent);
	tree->SetBranchAddress("Event_time", &eventTime);
	TVectorT<float>* data_wave = new TVectorT<float>(1024);
	TVectorT<float>* data_time = new TVectorT<float>(1024);
	tree->SetBranchAddress("channel1_wave", &data_wave);
	tree->SetBranchAddress("channel1_time", &data_time);
	// ROOT canvas to display data

	TH1D *h1 = new TH1D("h1", "positions of maxima", 100, 400., 800.);
	TCanvas* canvas = new TCanvas("canvas", "canvas", 800, 800);

	// ROOT Graph
	TGraph* myGraph;
	// if a second parameter was given display this many events, otherwise show all
	if(nEntries == -1 || nEntries > tree->GetEntries()){
		nEntries = tree->GetEntries();
	}
	cout << "Entries in tree = " << tree->GetEntries() << endl;
	cout << "Entries to show = " << nEntries << endl;

	// start looping over the tree entries
	cout << "Starting loop" << endl;
	for(int iEntry = 0; iEntry < nEntries; iEntry++){
		// get the next tree entry, this will load all tree variables
		tree->GetEntry(iEntry);
		myGraph = new TGraph(*data_time, *data_wave);
		stringstream sstitle;
		sstitle << "Event " << iEvent << ", time " << eventTime << "s;t / ns;U / mV";
		myGraph->SetTitle(sstitle.str().c_str());
		// draw with (A)xis and (L)ine, set axis ranges
		myGraph->Draw("AL");
		myGraph->GetXaxis()->SetRangeUser(0,1024);
		//myGraph->GetYaxis()->SetRangeUser(-550,50);
		myGraph->GetYaxis()->SetRangeUser(-300,0);
		// update the canvas and wait 0.5 s

		//Baseline
		TH1D *h2 = new TH1D("h2", "noise", 120, -250., -230.);
		double* y = myGraph->GetY();
		for (unsigned int i = 0; i < 1024; i++){
   			h2->Fill(y[i]);
			//cout << y[i] << endl;
		}

		int binmax = h2->GetMaximumBin();
   		double baseline = h2->GetXaxis()->GetBinCenter(binmax);
		TLine *line_baseline = new TLine(0,baseline,1024,baseline);
  		line_baseline->SetLineColor(kGreen);
  		line_baseline->Draw();
		delete h2;

		//Peak with Max():
		int n = myGraph->GetN();
		int locmax = TMath::LocMax(n,y);

		Double_t max = data_wave->Max();
		TLine *line_max = new TLine(0,max,1024,max);
  		line_max->SetLineColor(kRed);
  		line_max->Draw();
		h1->Fill(locmax);

		canvas->Update();
		usleep(500000);
		// delete the graph to prevent memory overflow
		delete myGraph;
	}
	delete canvas;
	TCanvas* canvas1 = new TCanvas("canvas1", "canvas1", 800, 800);
	h1->Draw();
	canvas1->SaveAs("max_position.pdf");
	delete canvas1;
	file->Close();

	delete data_wave;
	delete data_time;
}
