// C++ header
#include <stdlib.h>	// std lib
#include <sstream>	// stringstream
#include <iostream>	// cout
#include <unistd.h>	// usleep()
#include <typeinfo>


using namespace std;

void display(int nEntries = -1) {
	// open the input file
	TFile * file = new TFile((string("./../io/")+string("noise_534V")+string(".root")).c_str(),"READ");
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

	TH1D *h1 = new TH1D("h1", "positions of maxima", 100, 500., 600.); // histogram for poisitions of maxima
	TH1D *finger = new TH1D("finger", "Fingerspectrum", 100, 10., 90.); // histogram for fingerspectrum

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
		Double_t* y = myGraph->GetY();
		for (unsigned int i = 0; i < 1024; i++){
   			h2->Fill(y[i]);
			//cout << y[i] << endl;
		}

		Int_t binmax = h2->GetMaximumBin();
   		Double_t baseline = h2->GetXaxis()->GetBinCenter(binmax);
		TLine *line_baseline = new TLine(0,baseline,1024,baseline);
  		line_baseline->SetLineColor(kGreen);
  		line_baseline->Draw();
		delete h2;

		//Peak with Max():
		int n = myGraph->GetN();
		int locmax = TMath::LocMax(n,y);

		Double_t max = data_wave->GetSub(530, 575).Max(); // range constrain to avoid spikes from max_position_... plot
		TLine *line_max = new TLine(0,max,1024,max);
  		line_max->SetLineColor(kRed);
  		line_max->Draw();
		h1->Fill(locmax);

		//fingerspectrum
		Double_t pulseheight = max - baseline;
		finger->Fill(pulseheight);

		canvas->Update();
		//usleep(500000);
		// delete the graph to prevent memory overflow
		delete myGraph;
	}
	delete canvas;
	TCanvas* canvas1 = new TCanvas("canvas1", "canvas1", 800, 800);
	h1->Draw("HIST");
	canvas1->SaveAs((string("max_position_")+string("noise_534V")+string(".pdf")).c_str());
	delete canvas1;
	TCanvas* canvas_finger = new TCanvas("canvas_finger", "canvas_finger", 800, 800);
	canvas_finger->SetLogy();
	gStyle->SetOptStat(0);
	Double_t par[9];
	TF1 *g1    = new TF1("g1","gaus",12,24);
    TF1 *g2    = new TF1("g2","gaus",30,45);
    TF1 *g3    = new TF1("g3","gaus",45,60);
    //TF1 *total = new TF1("total","gaus(0)+gaus(3)+gaus(6)",15,68);
	finger->Fit(g1,"R");
	finger->Fit(g2,"0R+");
	finger->Fit(g3,"0R+");
	g1->GetParameters(&par[0]);
	g2->GetParameters(&par[3]);
	g3->GetParameters(&par[6]);
	//total->SetParameters(par);
	//total->SetLineColor(kRed);
	//total->SetParNames("Constant gaus1","Mean gaus1","Sigma gaus1","Constant gaus2","Mean gaus2","Sigma gaus2", "Constant gaus3","Mean gaus3","Sigma gaus3");
	//finger->Fit(total,"R+");
	TPaveText *pt = new TPaveText(.6,.85,.9,.9, "blNDC");
	pt->AddText(Form("Mean of first gaussian fit: %g #pm %g",g1->GetParameter(1),g1->GetParError(1)));
	pt->AddText(Form("#chi^{2}/ndof of first gaussian fit: %g / %d",g1->GetChisquare(),g1->GetNDF()));
	//pt->AddText(Form("Mean of second gaussian fit: %g #pm %g",g2->GetParameter(1),g2->GetParError(1)));
	//pt->AddText(Form("#chi^{2}/ndof of second gaussian fit: %g / %d",g2->GetChisquare(),g2->GetNDF()));
	//pt->AddText(Form("Mean of third gaussian fit: %g #pm %g",g3->GetParameter(1),g3->GetParError(1)));
	//pt->AddText(Form("#chi^{2}/ndof of third gaussian fit: %g / %d",g3->GetChisquare(),g3->GetNDF()));
	pt->SetFillStyle(0);
	//cout << "Chi^2: " << total->GetChisquare() << endl;
	//cout << "Degrees of freedom (ndof): " << total->GetNDF() << endl;
	//cout << "===> Chi^2/ndof: " << total->GetChisquare()/total->GetNDF() << endl;
	gStyle->SetOptFit(0);
	canvas_finger->Modified();
    canvas_finger->Update();
 	finger->Draw("SAME");
	pt->Draw("SAME");
	canvas_finger->SaveAs((string("fingerspectrum_")+string("noise_534V")+string(".pdf")).c_str());
	delete canvas_finger;

	file->Close();

	delete data_wave;
	delete data_time;
}
