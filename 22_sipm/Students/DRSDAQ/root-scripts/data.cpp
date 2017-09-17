// C++ header
#include <stdlib.h>	// std lib
#include <sstream>	// stringstream
#include <iostream>	// cout
#include <unistd.h>	// usleep()
#include <typeinfo>
#include <TF1Convolution.h>


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

	TH1D *h1 = new TH1D("h1", "Positions of maxima", 100, 500., 600.); // histogram for poisitions of maxima
	TH1D *finger = new TH1D("finger", "Pulseheightspectrum", 100, 0., 1050.); // histogram for fingerspectrum

	//TCanvas* canvas = new TCanvas("canvas", "canvas", 800, 800);

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
		//myGraph->Draw("AL");
		myGraph->GetXaxis()->SetRangeUser(0,1024);
		//myGraph->GetYaxis()->SetRangeUser(-550,50);
		myGraph->GetYaxis()->SetRangeUser(-300,900);
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
  		//line_baseline->Draw();
		delete h2;

		//Peak with Max():
		int n = myGraph->GetN();
		int locmax = TMath::LocMax(n,y);

		Double_t max = data_wave->Max(); // range constrain to avoid spikes from max_position_... plot
		TLine *line_max = new TLine(0,max,1024,max);
  		line_max->SetLineColor(kRed);
  		//line_max->Draw();
		h1->Fill(locmax);

		//fingerspectrum
		Double_t pulseheight = max - baseline;
		finger->Fill(pulseheight);

		//canvas->Update();
		//usleep(500000);
		// delete the graph to prevent memory overflow
		delete myGraph;
	}
	//delete canvas;
	TCanvas* canvas1 = new TCanvas("canvas1", "canvas1", 800, 800);
	h1->Draw("HIST");
	canvas1->SaveAs((string("max_position_")+pathIn+string(".pdf")).c_str());
	delete canvas1;
	TCanvas* canvas_finger = new TCanvas("canvas_finger", "canvas_finger", 800, 800);
	//canvas_finger->SetLogy();
	gStyle->SetOptStat(0);
    Double_t par[6];
	TF1 *g    = new TF1("g","gaus(0)",210,800);
    TF1 *l    = new TF1("l","landau(0)",210,800);
    TF1Convolution *f_conv = new TF1Convolution(g,l,210,800,true);
    f_conv->SetRange(210,800);
    f_conv->SetNofPointsFFT(1000);
    TF1   *total = new TF1("total",*f_conv, 210., 800., f_conv->GetNpar());
    total->SetLineColor(kRed);
    //total->SetParameters(150., 400., 20.);
    g->SetParameters(150., 400., 20.);
    g->SetLineColor(kYellow);
    l->SetLineColor(kGreen);
    l->SetParameters(150., 410., 20.);
	finger->Fit(g,"R");
	finger->Fit(l,"R+");
	g->GetParameters(&par[0]);
	l->GetParameters(&par[3]);
	total->SetParameters(5000., 5000., 500., -5000., 500.);
    finger->Fit(total,"R+");
    auto legend = new TLegend(0.6,0.65,0.9,0.75);
    legend->AddEntry(finger, "Histogram", "f");
    legend->AddEntry(g, "Gaussian fit", "l");
    legend->AddEntry(l, "Landau fit", "l");
    legend->AddEntry(total, "Convolution fit", "l");
    legend->Draw("SAME");
	//total->SetParNames("Constant gaus1","Mean gaus1","Sigma gaus1","Constant gaus2","Mean gaus2","Sigma gaus2", "Constant gaus3","Mean gaus3","Sigma gaus3");
	TPaveText *pt = new TPaveText(.6,.75,.9,.9, "blNDC");
	pt->AddText(Form("Peak of gaussian fit: %g #pm %g",g->GetParameter(1),g->GetParError(1)));
	pt->AddText(Form("#chi^{2}/ndof of gaussian fit: %g / %d",g->GetChisquare(),g->GetNDF()));
	pt->AddText(Form("Peak of landau fit: %g #pm %g",l->GetParameter(1),l->GetParError(1)));
	pt->AddText(Form("#chi^{2}/ndof of landau fit: %g / %d",l->GetChisquare(),l->GetNDF()));
	pt->AddText(Form("Peak of convolution fit: %g #pm %g",total->GetMaximumX(200,800), (1050./(100.* TMath::Sqrt(12)))));
	pt->AddText(Form("#chi^{2}/ndof of convolution fit: %g / %d",total->GetChisquare(),total->GetNDF()));
	pt->SetFillStyle(0);
	//cout << "Chi^2: " << total->GetChisquare() << endl;
	//cout << "Degrees of freedom (ndof): " << total->GetNDF() << endl;
	//cout << "===> Chi^2/ndof: " << total->GetChisquare()/total->GetNDF() << endl;
	gStyle->SetOptFit(0);
	canvas_finger->Modified();
    canvas_finger->Update();
 	finger->Draw("SAME");
    finger->GetXaxis()->SetTitle("U in [mV]");
    finger->GetYaxis()->SetTitle("Events / Bin");
	pt->Draw("SAME");
	canvas_finger->SaveAs((string("pulseheightspectrum_")+pathIn+string(".pdf")).c_str());
	delete canvas_finger;

    /*
	TFile f("data_results.root", "RECREATE");
	finger->Write();
	h1->Write();
	f.Close();
    */
	file->Close();

	delete data_wave;
	delete data_time;
}
