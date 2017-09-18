// C++ header
#include <stdlib.h>	// std lib
#include <sstream>	// stringstream
#include <iostream>	// cout
#include <unistd.h>	// usleep()
#include <typeinfo>


using namespace std;

void display(int nEntries = -1) {
	// open the input file
	TFile * file = new TFile((string("./../io/")+string("data02__OV56")+string(".root")).c_str(),"READ");
	// retrieve the data tree from the input file
	TTree * tree = (TTree*)(file->Get("DataTree"));
	// create variables for the tree data and connect them with the ROOT tree via branch addresses
	int iEvent, eventTime;
	tree->SetBranchAddress("Event_ID", &iEvent);
	tree->SetBranchAddress("Event_time", &eventTime);
	TVectorT<float>* data_wave = new TVectorT<float>(1024);
	TVectorT<float>* data_time = new TVectorT<float>(1024);
	TVectorT<float>* PMT1_wave = new TVectorT<float>(1024);
	TVectorT<float>* PMT1_time = new TVectorT<float>(1024);
	TVectorT<float>* PMT2_wave = new TVectorT<float>(1024);
	TVectorT<float>* PMT2_time = new TVectorT<float>(1024);
	tree->SetBranchAddress("channel1_wave", &data_wave);
	tree->SetBranchAddress("channel1_time", &data_time);
	tree->SetBranchAddress("channel2_wave", &PMT1_wave);
	tree->SetBranchAddress("channel2_time", &PMT1_time);
	tree->SetBranchAddress("channel3_wave", &PMT2_wave);
	tree->SetBranchAddress("channel3_time", &PMT2_time);
	// ROOT canvas to display data

	TH1D *h1 = new TH1D("h1", "positions of maxima", 100, 500., 600.); // histogram for poisitions of maxima
	TH1D *h1PMT1 = new TH1D("h1PMT1", "positions of maxima", 100, 500., 600.); // histogram for poisitions of maxima
	TH1D *h1PMT2 = new TH1D("h1PMT2", "positions of maxima", 100, 500., 600.); // histogram for poisitions of maxima
	TH1D *finger = new TH1D("finger", "Fingerspectrum", 100, 10., 90.); // histogram for fingerspectrum

	//~ TH1D *time_SIPM_PMT1 = new TH1D("time_SIPM_PMT1","zeitaufloesung",160,-60.,20.);
	TH1D *time_SIPM_PMT1 = new TH1D("time_SIPM_PMT1","time resolution detector to PMT1",100,-55.,-30.);
	TH1D *time_SIPM_PMT2 = new TH1D("time_SIPM_PMT2","time resolution detector to PMT2",100,-55.,-30.);
	TH1D *time_PMT1_PMT2 = new TH1D("time_PMT1_PMT2","time resolution PMT1 to PMT2",40,-5.,15.);
	
	TCanvas* canvas = new TCanvas("canvas", "canvas", 1000, 1000);
	canvas->Divide(2,2);

	// ROOT Graph
	TGraph* myGraph;
	//~ TGraph* myGraph2;
	//~ TGraph* myGraph3;
	
	
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
		
		Double_t timeSiPM=0.;
		Double_t timePMT1=0.;
		Double_t timePMT2=0.;
		
		Double_t timeDiff_SIPM_PMT1=0.;
		Double_t timeDiff_SIPM_PMT2=0.;
		Double_t timeDiff_PMT1_PMT2=0.;
		
		
		bool status1=false;
		bool status2=false;
		bool status3=false;
		
		
		canvas->cd(1);
		myGraph = new TGraph(*data_time, *data_wave);
		stringstream sstitle;
		sstitle << "SiPM Event " << iEvent << ", time " << eventTime << "s;t / ns;U / mV";
		myGraph->SetTitle(sstitle.str().c_str());
		// draw with (A)xis and (L)ine, set axis ranges
		myGraph->Draw("AL");
		myGraph->GetXaxis()->SetRangeUser(0,1024);
		myGraph->GetYaxis()->SetRangeUser(-300,900);
		//Baseline
		TH1D *h2 = new TH1D("h2", "noise", 120, -250., -230.);
		Double_t* y = myGraph->GetY();
		Double_t* x = myGraph->GetX();
		for (unsigned int i = 0; i < 1024; i++){
   			h2->Fill(y[i]);
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
		Double_t max = data_wave->GetSub(342, 768).Max(); // range constrain to avoid spikes from max_position_... plot
		TLine *line_max = new TLine(0,max,1024,max);
  		line_max->SetLineColor(kRed);
  		//~ line_max->Draw();
		h1->Fill(locmax);		
		Double_t height = max-baseline;
		Double_t heightHalf = height/2.;		
		if((!(height<40.))&& !(abs(750.-max)<=0.1) ){	
			
			status1=true;
					
			Double_t halfMax =baseline + (max-baseline)/2.;
			TLine *line_halfMax = new TLine(0,halfMax,1024,halfMax);
			line_halfMax->SetLineColor(kBlue);
			line_halfMax->Draw();
			line_max->Draw();
			Double_t temp=10000.;
			Double_t tempOld=10000.;
			Double_t tempX=0.;
			Double_t halfX=0.;
			Double_t tempY=0.;
			Double_t halfY=0.;
			for (unsigned int i = 0; i < locmax; i++){
				tempX =x[i];
				tempY =y[i];
				temp=abs(tempY-halfMax);
				//~ cout<<temp<<endl;
				if( temp<tempOld ){
					tempOld=temp;
					halfX=tempX;
					halfY=tempY;
				}
			}
			TLine *lineTime=new TLine(halfX,baseline,halfX,max);
			lineTime->SetLineColor(kRed);
			lineTime->Draw();		
		
		timeSiPM=halfX;
		}
		
		
		canvas->cd(2);
		myGraph = new TGraph(*PMT1_time, *PMT1_wave);
		stringstream sstitle2;
		sstitle2 << "PMT1 Event " << iEvent << ", time " << eventTime << "s;t / ns;U / mV";
		myGraph->SetTitle(sstitle2.str().c_str());
		myGraph->Draw("AL");
		myGraph->GetXaxis()->SetRangeUser(0,1024);
		myGraph->GetYaxis()->SetRangeUser(-350,850);
		//Baseline
		TH1D *h2PMT1 = new TH1D("h2PMT1", "noise", 120, -250., -230.);
		Double_t* yPMT1 = myGraph->GetY();
		Double_t* xPMT1 = myGraph->GetX();
		for (unsigned int i = 0; i < 1024; i++){
   			h2PMT1->Fill(yPMT1[i]);
		}

		Int_t binmaxPMT1 = h2PMT1->GetMaximumBin();
   		Double_t baselinePMT1 = h2PMT1->GetXaxis()->GetBinCenter(binmaxPMT1);
		TLine *line_baselinePMT1 = new TLine(0,baselinePMT1,1024,baselinePMT1);
  		line_baselinePMT1->SetLineColor(kGreen);
  		line_baselinePMT1->Draw();
		delete h2PMT1;
		//Peak with Max():
		int nPMT1 = myGraph->GetN();
		int locmaxPMT1 = TMath::LocMax(nPMT1,yPMT1);
		Double_t maxPMT1 = PMT1_wave->GetSub(342, 768).Max(); // range constrain to avoid spikes from max_position_... plot
		TLine *line_maxPMT1 = new TLine(0,maxPMT1,1024,maxPMT1);
  		line_maxPMT1->SetLineColor(kRed);
  		//~ line_max->Draw();
		h1PMT1->Fill(locmaxPMT1);		
		Double_t heightPMT1 = maxPMT1-baselinePMT1;
		Double_t heightHalfPMT1 = heightPMT1/2.;		
		if((!(heightPMT1<40.))&& !(abs(750.-maxPMT1)<=0.1) ){			
			
			status2=true;
			
			Double_t halfMaxPMT1 =baselinePMT1 + (maxPMT1-baselinePMT1)/2.;
			TLine *line_halfMaxPMT1 = new TLine(0,halfMaxPMT1,1024,halfMaxPMT1);
			line_halfMaxPMT1->SetLineColor(kBlue);
			line_halfMaxPMT1->Draw();
			line_maxPMT1->Draw();
			Double_t tempPMT1=10000.;
			Double_t tempOldPMT1=10000.;
			Double_t tempXPMT1=0.;
			Double_t halfXPMT1=0.;
			Double_t tempYPMT1=0.;
			Double_t halfYPMT1=0.;
			for (unsigned int i = 0; i < locmaxPMT1; i++){
				tempXPMT1 =xPMT1[i];
				tempYPMT1 =yPMT1[i];
				tempPMT1=abs(tempYPMT1-halfMaxPMT1);
				//~ cout<<tempPMT1<<endl;
				if( tempPMT1<tempOldPMT1 ){
					tempOldPMT1=tempPMT1;
					halfXPMT1=tempXPMT1;
					halfYPMT1=tempYPMT1;
				}
			}
			TLine *lineTimePMT1=new TLine(halfXPMT1,baselinePMT1,halfXPMT1,maxPMT1);
			lineTimePMT1->SetLineColor(kRed);
			lineTimePMT1->Draw();		
		

			timePMT1=halfXPMT1;

		
		}		




		
		canvas->cd(3);
		myGraph = new TGraph(*PMT2_time, *PMT2_wave);
		stringstream sstitle3;
		sstitle3 << "PMT2 Event " << iEvent << ", time " << eventTime << "s;t / ns;U / mV";
		myGraph->SetTitle(sstitle3.str().c_str());
		myGraph->Draw("AL");
		myGraph->GetXaxis()->SetRangeUser(0,1024);
		myGraph->GetYaxis()->SetRangeUser(-350,850);
	//Baseline
		TH1D *h2PMT2 = new TH1D("h2", "noise", 120, -250., -230.);
		Double_t* yPMT2 = myGraph->GetY();
		Double_t* xPMT2 = myGraph->GetX();
		for (unsigned int i = 0; i < 1024; i++){
   			h2PMT2->Fill(yPMT2[i]);
		}

		Int_t binmaxPMT2 = h2PMT2->GetMaximumBin();
   		Double_t baselinePMT2 = h2PMT2->GetXaxis()->GetBinCenter(binmaxPMT2);
		TLine *line_baselinePMT2 = new TLine(0,baselinePMT2,1024,baselinePMT2);
  		line_baselinePMT2->SetLineColor(kGreen);
  		line_baselinePMT2->Draw();
		delete h2PMT2;
		//Peak with Max():
		int nPMT2 = myGraph->GetN();
		int locmaxPMT2 = TMath::LocMax(nPMT2,yPMT2);
		Double_t maxPMT2 = data_wave->GetSub(342, 768).Max(); // range constrain to avoid spikes from max_position_... plot
		TLine *line_maxPMT2 = new TLine(0,maxPMT2,1024,maxPMT2);
  		line_maxPMT2->SetLineColor(kRed);
  		//~ line_max->Draw();
		h1PMT2->Fill(locmaxPMT2);		
		Double_t heightPMT2 = maxPMT2-baselinePMT2;
		Double_t heightHalfPMT2 = heightPMT2/2.;		
		if((!(heightPMT2<40.))&& !(abs(750.-maxPMT2)<=0.1) ){	
			
			status3=true;
					
			Double_t halfMaxPMT2 =baselinePMT2 + (maxPMT2-baselinePMT2)/2.;
			TLine *line_halfMaxPMT2 = new TLine(0,halfMaxPMT2,1024,halfMaxPMT2);
			line_halfMaxPMT2->SetLineColor(kBlue);
			line_halfMaxPMT2->Draw();
			line_maxPMT2->Draw();
			Double_t tempPMT2=10000.;
			Double_t tempOldPMT2=10000.;
			Double_t tempXPMT2=0.;
			Double_t halfXPMT2=0.;
			Double_t tempYPMT2=0.;
			Double_t halfYPMT2=0.;
			for (unsigned int i = 0; i < locmaxPMT2; i++){
				tempXPMT2 =xPMT2[i];
				tempYPMT2 =yPMT2[i];
				tempPMT2=abs(tempYPMT2-halfMaxPMT2);
				//~ cout<<tempPMT2<<endl;
				if( tempPMT2<tempOldPMT2 ){
					tempOldPMT2=tempPMT2;
					halfXPMT2=tempXPMT2;
					halfYPMT2=tempYPMT2;
				}
			}
			TLine *lineTimePMT2=new TLine(halfXPMT2,baselinePMT2,halfXPMT2,maxPMT2);
			lineTimePMT2->SetLineColor(kRed);
			lineTimePMT2->Draw();		
		
			timePMT2=halfXPMT2;
		
		}		

		
		canvas->Update();
		//~ usleep(500000);
		//~ usleep(1000000);
		delete myGraph;
	
	
	
	
	
		//~ timeSiPM=halfX;
		//~ timePMT1=halfXPMT1;
		//~ timePMT2=halfXPMT2;
		
		timeDiff_SIPM_PMT1=timeSiPM-timePMT1;
		timeDiff_SIPM_PMT2=timeSiPM-timePMT2;
		timeDiff_PMT1_PMT2=timePMT1-timePMT2;
	
		if(status1&&status2&&status3){
			time_SIPM_PMT1->Fill(timeDiff_SIPM_PMT1);
			time_SIPM_PMT2->Fill(timeDiff_SIPM_PMT2);
			time_PMT1_PMT2->Fill(timeDiff_PMT1_PMT2);
		}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	}
	
	TCanvas* canvas1 = new TCanvas("canvas1", "canvas1", 800, 800);
		time_SIPM_PMT1->Draw("HIST");
		TF1 *g1    = new TF1("g1","gaus",-55,-30);
		time_SIPM_PMT1->Fit(g1,"R");		
		//~ canvas1->Modified();
		//~ canvas1->Update();
		//~ time_SIPM_PMT1->Draw("HIST");	
		time_SIPM_PMT1->Draw("SAME");	
		gStyle->SetOptFit(1);
		gStyle->SetOptStat("e");
		
	canvas1->SaveAs((string("time_resolution_SIPM_PMT1")+string(".pdf")).c_str());
	delete canvas1;
	TCanvas* canvas2 = new TCanvas("canvas2", "canvas2", 800, 800);
		time_SIPM_PMT2->Draw("HIST");
		TF1 *g2    = new TF1("g2","gaus",-55,-30);
		time_SIPM_PMT2->Fit(g2,"R");
		//~ canvas2->Modified();
		//~ canvas2->Update();
		time_SIPM_PMT2->Draw("SAME");	
		//~ time_SIPM_PMT2->Draw("HIST");	
		//~ gStyle->SetOptFit(1);
		//~ gStyle->SetOptStat("e");
	canvas2->SaveAs((string("time_resolution_SIPM_PMT2")+string(".pdf")).c_str());
	delete canvas2;
	TCanvas* canvas3 = new TCanvas("canvas3", "canvas3", 800, 800);
		time_PMT1_PMT2->Draw("HIST");
		TF1 *g3    = new TF1("g3","gaus",-5,15);
		time_PMT1_PMT2->Fit(g3,"R");
		//~ canvas3->Modified();
		//~ canvas3->Update();
		//~ time_PMT1_PMT2->Draw("HIST");	
		time_PMT1_PMT2->Draw("SAME");	
		//~ gStyle->SetOptFit(1);
		//~ gStyle->SetOptStat("e");
	canvas3->SaveAs((string("time_resolution_PMT1_PMT2")+string(".pdf")).c_str());
	delete canvas3;
	
	


	delete canvas;


	TFile f("zeitaufloesung.root", "RECREATE");
	time_SIPM_PMT1->Write();
	time_SIPM_PMT2->Write();
	time_PMT1_PMT2->Write();
	f.Close();



	file->Close();

	delete data_wave;
	delete data_time;
	delete PMT1_wave;
	delete PMT1_time;
	delete PMT2_wave;
	delete PMT2_time;
}
