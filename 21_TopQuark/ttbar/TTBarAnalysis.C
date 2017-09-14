/*
 * \file TTBarAnalysis.C
 * \author Martin Weber
 *
 */

#include "TTBarAnalysis.h"

#include <iostream>
#include <algorithm>
#include <stdlib.h>

#include <TH1D.h>
#include <sys/stat.h>
#include <typeinfo>
#include <TMath.h>
using namespace std;

TTBarAnalysis::TTBarAnalysis(bool sec, bool trigger, float sf, float wf,
			     double jscale, double jsmear, double mscale,
			     TTree * /*tree*/)
  : MyAnalysis()
{
  weight_factor = wf;
  jet_scale = jscale;
  jet_smear = jsmear;
  muon_scale = mscale;
  MyJet::SetBTagScaleFactor(sf);

  // initialize your variables here
  TotalEvents = 0;
  SelectedEvents = 0;
  trig=trigger;
  second=sec;
  events_total=0;
  events_sel=0;
}

void TTBarAnalysis::CreateHistograms()
{
  // We tell ROOT that we use weighted histograms
  TH1::SetDefaultSumw2();

  // First create a "cut flow" histogram that contains event counts for the
  // different stages of the analysis

  if (!trig){
	  CreateHisto("cutflow", "", 7, 0, 7);
	  CreateHisto("cutflow_MassSelection", "cut flow Mass Selection", 7, 0, 7);

	  // For a cut flow histogram, it is important that we initialize all bins we
	  // are using with zeroes before processing the first event. If this is
	  // forgotten, the cut flow histogram may contain garbage, so be careful!
	  // It will also be useful to put proper names, e.g. "pT" if you cut on pT.
	  // You need to use the same names below in your analysis code!
	  Fill("cutflow", "all", 0);
	  Fill("cutflow", "trigger", 0);
	  Fill("cutflow", "p_{T}#geq26", 0);
	  Fill("cutflow", "N{#mu,Iso} #geq 1", 0);
	  Fill("cutflow", "N_{Jet} #geq 4", 0);
	  Fill("cutflow", "N_{Jet,b} #geq 2", 0);
	  Fill("cutflow", "E_{T}^{missing}#geq20", 0);

	  Fill("cutflow_MassSelection", "all", 0);
	  Fill("cutflow_MassSelection", "trigger", 0);
	  Fill("cutflow_MassSelection", "p_{T}#geq26", 0);
	  Fill("cutflow_MassSelection", "N{#mu,Iso} = 1", 0);
	  Fill("cutflow_MassSelection", "N_{Jet} = 4v5", 0);
	  Fill("cutflow_MassSelection", "N_{Jet,b} = 2", 0);
	  Fill("cutflow_MassSelection", "E_{T}^{missing}#geq20", 0);

	  //N-1 Plots
	  CreateHisto("N-1 NIso", "Number of isolated muons", 5, 0, 5);
	  CreateHisto("N-1 NJet", "Number of Jets (with ID)", 10, 0, 10);
	  CreateHisto("N-1 NBJet", "Number of b-tagged Jets (with ID)", 5, 0, 5);
	  CreateHisto("N-1 MET", "E_{T}^{missing} [GeV]", 30, 0, 300);

	  CreateHisto("N-1 NIso 2", "Number of isolated muons", 5, 0, 5);
	  CreateHisto("N-1 NJet 2", "Number of Jets (with ID)", 10, 0, 10);
	  CreateHisto("N-1 NBJet 2", "Number of b-tagged Jets (with ID)", 5, 0, 5);
	  CreateHisto("N-1 MET 2", "E_{T}^{missing} [GeV]", 25, 0, 500);


	}
  // Now we create all the other histograms that we use in our selection.

  // The first string is the name of the histogram, the second string is the
  // title of the histogram that is used for labelling the x-axis. The three
  // numbers specify the number of bins, and the lower and upper bound of the
  // histogram.

  if (!trig){
	  CreateHisto("Muon_Pt", "p_{T} of all muons [GeV]", 50, 0, 250);
	  CreateHisto("NIsoMuon", "Number of isolated muons", 5, 0, 5);
	  CreateHisto("Muon_Eta", "#eta of all muons", 20, -3.5, 3.5);
	  CreateHisto("Muon_E", "Energy distribution [GeV]", 50, 0, 750);
	  CreateHisto("MET", "Missing transverse energy [GeV]", 40,0,200);
	  CreateHisto("Muon_Phi", "#phi of all muons", 20, -3.5, 3.5);
	  CreateHisto("Jet_Pt", "p_{T} of all jets [GeV]", 50, 0, 250);
	  CreateHisto("Jet_Eta", "#eta of all jets", 10, -3., 3.);
	  CreateHisto("Jet_E", "Energy distribution [GeV]", 50, 0, 750);
	  CreateHisto("Jet_Phi", "#phi of all jets", 20, -3.5, 3.5);
	  CreateHisto("NJetID", "Number of Jets (with ID)", 10, 0, 10);
	  CreateHisto("NJetID_btag", "Number of b-tagged Jets (with ID)", 4, 0, 4);
	  CreateHisto("NPrimaryVertices", "Number of primary Vertices", 36, 0, 36);
	  CreateHisto("DrellYan_mll", "m_{ll} [GeV]", 30, 75, 105);
	  CreateHisto("DrellYan_met", "E_{T}^{missing} [GeV]", 40, 0, 80);

	  CreateHisto("topmass_hadr", "m_{t,hadronic} [GeV]", 50, 100, 300);
	  CreateHisto("topmass_lept", "m_{t,semileptonic} [GeV]", 50, 100, 300);
	  CreateHisto("topmass_both", "m_{t,both} [GeV]", 50, 100, 300);
  }

  if (trig){
	  CreateHisto("ForTrigger_Nominator", "pt [GeV]", 250, 0, 250); // Nom = triggered Events
	  CreateHisto("ForTrigger_Denominator", "pt [GeV]", 250, 0, 250); // Denom =One isolated Muon
  }
}

Bool_t TTBarAnalysis::Process(Long64_t entry)
{
  // The Process() function is called for each event in the ROOT TTree. The
  // entry argument specifies which entry in the currently loaded tree is to
  // be processed.
  //
  // The return value is currently not used.

  // We load the event from the ROOT tree. After this we can access the
  // variables of the event.
  GetEntry(entry);

  // This fills the Muons, Electrons, Photons, Jets and MC information from
  // the ROOT TTree. After this we can use e.g. Muons[0]
  BuildEvent();

  // We count the number of events that we process (e.g. for efficiency calculation).
  ++TotalEvents;
  // Inform us every 10000 events
  if (TotalEvents % 10000 == 0)
    cout << "Next event -----> " << TotalEvents << endl;

  // fill the cutflow histogram at the beginning and after each cut
  if (!trig){
	Fill("cutflow", "all");
	Fill("cutflow_MassSelection", "all");
	}
  //////////////////////////////////////////////////////////////////////
  // implementation of systematic effects

  // As an example, we show how to apply the muon scale uncertainty

	TRandom Random;
	Random.SetSeed();
	double jet_smear_rnd = 1.;


  for (unsigned int i = 0; i < Muons.size(); i++) {
    Muons[i] *= muon_scale;
  }

  for (unsigned int i = 0; i < Jets.size(); i++) {
    Jets[i] *= jet_scale;
  }
  for (unsigned int i = 0; i < Jets.size(); i++) {
	jet_smear_rnd = Random.Gaus(1.,jet_smear);
    Jets[i] *= jet_smear_rnd;
  }
	EventWeight=EventWeight*weight_factor;

  // the following 4 lines are necessary because:
  // if I want to cut on muon Pt for the trigger for example, i need to select events in which is at least one muon. -so uncomment the 2 lines therefore
  // if I want to plot all events, uncomment the other 2 lines
  if (Muons.size()>0){
  //~ if (true){
   bool is =(Muons[0].Pt()>26.);
   //~ bool is =true;


  //////////////////////////////////////////////////////////////////////
  // first, we identify all objects (muons, jets) by applying quality and
  // isolation requirements.



	if (!trig){

		  // Muon isolation
		  vector<int> isomu;
		  for (unsigned int i = 0; i < Muons.size(); i++) {
			if ((Muons[i].IsIsolated()) && (triggerIsoMu24)  && is ){
			  isomu.push_back(i);
			  Fill("Muon_Pt", Muons[i].Pt());
			  Fill("Muon_Eta", Muons[i].Eta());
			  Fill("Muon_E", Muons[i].E());
			  Fill("Muon_Phi", Muons[i].Phi());
					//~
			  //~ // you can also access Muons[i].E(), .Px(), .Py(), .Pz(), .Eta(), .Phi(), ...
			  //~ // and the same with Electrons, Photons, Jets, ...
			  //~ // see Documentation of ROOT TLorentzVector
			}
		  }


		  int NIsoMuon = isomu.size();
		  if ((triggerIsoMu24)){
		  //~ if ((triggerIsoMu24)&&  is){
			Fill("NIsoMuon", NIsoMuon);
			}

			//MET
			if (triggerIsoMu24  && is ){
				Fill("MET", met.Pt());
			}


		  // now start here applying the jet ID...

			// jet id
		  vector<int> jets_ID;
		  vector<int> jets_ID_btag;

		  for (unsigned int i = 0; i < Jets.size(); i++) {
			if ((Jets[i].GetJetID())&&(triggerIsoMu24) && is) {
				  jets_ID.push_back(i);
				  Fill("Jet_Pt", Jets[i].Pt());
				  Fill("Jet_Eta", Jets[i].Eta());
				  Fill("Jet_E", Jets[i].E());
				  Fill("Jet_Phi", Jets[i].Phi());
				if (Jets[i].IsBTagged()){
					jets_ID_btag.push_back(i);
			  }
			}
		  }

		  int NJetID = jets_ID.size();
		  if(triggerIsoMu24 ){
		  //~ if(triggerIsoMu24  && is){
			Fill("NJetID", NJetID);
			}

		  int NJetID_btag = jets_ID_btag.size();
		  //~ if (triggerIsoMu24 && is){
		  if (triggerIsoMu24){
				Fill("NJetID_btag", NJetID_btag);
				Fill("NPrimaryVertices",NPrimaryVertices);
			}

		//Drell Yan region (signal free) -> check MC/Data

			if (Muons.size()==2){
				bool isPt =(Muons[0].Pt()>26.);
					if ( (Muons[0].IsIsolated()) && (Muons[1].IsIsolated())  && isPt){

						float mll = (Muons[0]+Muons[1]).M();
						bool m_cut = (75. <= mll) && (mll <=105.);
						bool cuts = m_cut && (met.Pt() <= 4000000.) && (Muons[0].Pt()>=0) && (Muons[1].Pt()>=0);
						 //~ bool cuts = true;
						if (cuts){
							if(triggerIsoMu24){
								Fill("DrellYan_mll",mll);
								Fill("DrellYan_met",met.Pt());
							}
						}
					}
			}
	}
}
// histos for trigger measurement


	if (trig){

		bool useForTrig=false;
		for (unsigned int i=0; i< Muons.size();i++){
			if (Muons[i].IsIsolated()){
				useForTrig=true;
			}
		}
		if (useForTrig){
			FillNoWeight("ForTrigger_Denominator",Muons[0].Pt());
			if(triggerIsoMu24){
				FillNoWeight("ForTrigger_Nominator", Muons[0].Pt());
			}
		}
	}



  //////////////////////////////////////////////////////////////////////
  // after all objects have been identified, the selection can start

  // the first requirement should be the trigger requirement...
  // ... add it here ...
if (!trig){
	bool hasTriggered = triggerIsoMu24;

  // ... and after the trigger requirement we fill the cut flow again ...

	bool muonSize = (Muons.size()>0);
	//following is for cross section measurement
	if (muonSize){
		bool ptCut= (Muons[0].Pt()>=26.);
		int NIsoMuons = 0;
		for (unsigned int i=0; i< Muons.size();i++){
			if (Muons[i].IsIsolated()){
				NIsoMuons = NIsoMuons+1;
			}
		}
		bool NIsoMuonCut = NIsoMuons>=1;
		int NJets=0;
		int NBJets=0;
		for (unsigned int i=0; i< Jets.size();i++){
			if (Jets[i].GetJetID()){
				NJets = NJets+1;
				if (Jets[i].IsBTagged()){
					NBJets = NBJets+1;
				}
			}
		}
		bool NJetCut = NJets >= 4;
		bool NBJetCut = NBJets >= 2;
		bool metCut = met.Pt()>=20.;


		if (hasTriggered){
			Fill("cutflow", "trigger");
			if(ptCut){
				Fill("cutflow", "p_{T}#geq26");
				if(NIsoMuonCut){
					Fill("cutflow", "N{#mu,Iso} #geq 1");
					if(NJetCut){
						Fill("cutflow", "N_{Jet} #geq 4");
						if(NBJetCut){
							Fill("cutflow", "N_{Jet,b} #geq 2");
							if(metCut){
								Fill("cutflow", "E_{T}^{missing}#geq20");
								events_sel=events_sel+EventWeight;
							}
						}
					}
				}

				if ((NJetCut)&&(NBJetCut)&&(metCut)){
					Fill("N-1 NIso",NIsoMuons);
				}
				if ((NIsoMuonCut)&&(NBJetCut)&&(metCut)){
					Fill("N-1 NJet",NJets);
				}
				if ((NJetCut)&&(NIsoMuonCut)&&(metCut)){
					Fill("N-1 NBJet",NBJets);
				}
				if ((NJetCut)&&(NBJetCut)&&(NIsoMuonCut)){
					Fill("N-1 MET",met.Pt());
				}


			}
		}


	}



	//following is for top mass measurement

	if (muonSize){
		bool ptCut= (Muons[0].Pt()>=26.);
		int NIsoMuons = 0;
		for (unsigned int i=0; i< Muons.size();i++){
			if (Muons[i].IsIsolated()){
				NIsoMuons = NIsoMuons+1;
			}
		}
		bool NIsoMuonCut = NIsoMuons==1;
		int NJets=0;
		int NBJets=0;
		for (unsigned int i=0; i< Jets.size();i++){
			if (Jets[i].GetJetID()){
				NJets = NJets+1;
				if (Jets[i].IsBTagged()){
					NBJets = NBJets+1;
				}
			}
		}
		bool NJetCut = (NJets >= 4) && (NJets <= 5);
		bool NBJetCut = NBJets == 2;
		bool metCut = met.Pt()>=20.;


		if (hasTriggered){
			Fill("cutflow_MassSelection", "trigger");
			if(ptCut){
				Fill("cutflow_MassSelection", "p_{T}#geq26");
				if(NIsoMuonCut){
					Fill("cutflow_MassSelection", "N{#mu,Iso} = 1");
					if(NJetCut){
						Fill("cutflow_MassSelection", "N_{Jet} = 4v5");
						if(NBJetCut){
							Fill("cutflow_MassSelection", "N_{Jet,b} = 2");
							if(metCut){
								Fill("cutflow_MassSelection", "E_{T}^{missing}#geq20");
								events_sel2=events_sel2+EventWeight;


								//top mass combination

								// hadronic NJet 4or5   NBJet 2

								//SECOND iteration: first guess: m_top = 169 GeV
								//~ bool secondIteration = false;
								bool secondIteration = second;

								float m_t=172.5;


								float m_W=80.385;
								vector<MyJet> BJets;
								vector<MyJet> OtherJets;
								for (unsigned int i=0; i< Jets.size();i++){
									if(Jets[i].IsBTagged()){
										BJets.push_back(Jets[i]);
									}else{
										OtherJets.push_back(Jets[i]);
									}
								}

								float temp01_m;
								float temp12_m;
								float temp02_m;

								TLorentzVector resultingFourVector_hadr;

								if(OtherJets.size()==3){
									temp01_m=(OtherJets[0]+OtherJets[1]).M();
									temp12_m=(OtherJets[1]+OtherJets[2]).M();
									temp02_m=(OtherJets[0]+OtherJets[2]).M();

									float dif01=abs(temp01_m-m_W);
									float dif12=abs(temp12_m-m_W);
									float dif02=abs(temp02_m-m_W);

									if ((dif01<dif02)&&(dif01<dif12)){
										resultingFourVector_hadr=((OtherJets[0]+OtherJets[1]));
									}else{
										if ((dif02<dif01)&&(dif02<dif12)){
											resultingFourVector_hadr=((OtherJets[0]+OtherJets[2]));
										}else{
											resultingFourVector_hadr=((OtherJets[1]+OtherJets[2]));
											}
									}


								}else{
									resultingFourVector_hadr=((OtherJets[0]+OtherJets[1]));
								}


								float m_T1_hadr=(resultingFourVector_hadr+BJets[0]).M();
								float m_T2_hadr=(resultingFourVector_hadr+BJets[1]).M();

								float difT1 = abs(m_T1_hadr-m_t);
								float difT2 = abs(m_T2_hadr-m_t);

								if(secondIteration){

									if(difT1<difT2){
										Fill("topmass_hadr",m_T1_hadr);
										Fill("topmass_both",m_T1_hadr);
									}else{
										Fill("topmass_hadr",m_T2_hadr);
										Fill("topmass_both",m_T2_hadr);
									}
								}else{
									Fill("topmass_hadr",m_T1_hadr);
									Fill("topmass_hadr",m_T2_hadr);
								}
								//now look at leptonic branch

								TLorentzVector resultingFourVector_lept;
								TLorentzVector Neutrino1=met;
								TLorentzVector Neutrino2=met;

								float pX_mu=Muons[0].Px();
								float pY_mu=Muons[0].Py();
								float pZ_mu=Muons[0].Pz();
								float pX_met=met.Px();
								float pY_met=met.Py();

								float m_mu=Muons[0].M();
								float e_mu=Muons[0].E();

								float k1=(m_W*m_W/2.)-(m_mu*m_mu/2)+(pX_mu*pX_met)+(pY_mu*pY_met);
								float k2=(e_mu*e_mu)*(pX_met*pX_met + pY_met*pY_met);
								float k3=(pZ_mu*pZ_mu) -(e_mu*e_mu);

								float sol1=-(k1*pZ_mu/k3)+TMath::Sqrt((k1*pZ_mu/k3)*(k1*pZ_mu/k3)-(((k1*k1)-k2)/k3));
								float sol2=-(k1*pZ_mu/k3)-TMath::Sqrt((k1*pZ_mu/k3)*(k1*pZ_mu/k3)-(((k1*k1)-k2)/k3));

								float e1_met=TMath::Sqrt(pX_met*pX_met + pY_met*pY_met + sol1*sol1);
								float e2_met=TMath::Sqrt(pX_met*pX_met + pY_met*pY_met + sol2*sol2);

								Neutrino1.SetPxPyPzE(pX_met, pY_met, sol1, e1_met);
								Neutrino2.SetPxPyPzE(pX_met, pY_met, sol2, e2_met);

								float temp1_m;
								float temp2_m;
								temp1_m=(Muons[0]+Neutrino1).M();
								temp2_m=(Muons[0]+Neutrino2).M();

								float dif1=abs(temp1_m-m_W);
								float dif2=abs(temp2_m-m_W);

								if(dif1<dif2){
									resultingFourVector_lept=Neutrino1+Muons[0];
								}else{
									resultingFourVector_lept=Neutrino2+Muons[0];
								}


								float m_T1_lept=(resultingFourVector_lept+BJets[0]).M();
								float m_T2_lept=(resultingFourVector_lept+BJets[1]).M();


								float difT1_lept = abs(m_T1_lept-m_t);
								float difT2_lept = abs(m_T2_lept-m_t);

								if(secondIteration){
									if(difT1_lept<difT2_lept){
										Fill("topmass_lept",m_T1_lept);
										Fill("topmass_both",m_T1_lept);
									}else{
										Fill("topmass_lept",m_T2_lept);
										Fill("topmass_both",m_T2_lept);
									}
								}else{

									Fill("topmass_lept",m_T1_lept);
									Fill("topmass_lept",m_T2_lept);
								}

							}
						}
					}
				}

				if ((NJetCut)&&(NBJetCut)&&(metCut)){
					Fill("N-1 NIso 2",NIsoMuons);
				}
				if ((NIsoMuonCut)&&(NBJetCut)&&(metCut)){
					Fill("N-1 NJet 2",NJets);
				}
				if ((NJetCut)&&(NIsoMuonCut)&&(metCut)){
					Fill("N-1 NBJet 2",NBJets);
				}
				if ((NJetCut)&&(NBJetCut)&&(NIsoMuonCut)){
					Fill("N-1 MET 2",met.Pt());
				}


			}
		}


	}


	events_total=events_total+EventWeight;
  }

  // ... and then you have to add more code for the selection here ...




  // ... end of the selection. Count selected events
  SelectedEvents++;

  // When the event has been accepted, we return kTRUE, if it is rejected, we
  // return kFALSE.
  return kTRUE;
}
