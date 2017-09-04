/*
 * \file TTBarAnalysis.C
 * \author Martin Weber
 *
 */

#include "TTBarAnalysis.h"

#include <iostream>
#include <algorithm>

#include <TH1D.h>

using namespace std;

TTBarAnalysis::TTBarAnalysis(float sf, float wf,
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
}

void TTBarAnalysis::CreateHistograms()
{
  // We tell ROOT that we use weighted histograms
  TH1::SetDefaultSumw2();

  // First create a "cut flow" histogram that contains event counts for the
  // different stages of the analysis
  CreateHisto("cutflow", "cut flow", 10, 0, 10);

  // For a cut flow histogram, it is important that we initialize all bins we
  // are using with zeroes before processing the first event. If this is
  // forgotten, the cut flow histogram may contain garbage, so be careful!
  // It will also be useful to put proper names, e.g. "pT" if you cut on pT.
  // You need to use the same names below in your analysis code!
  Fill("cutflow", "all", 0);
  Fill("cutflow", "trigger", 0);
  Fill("cutflow", "2nd", 0);
  Fill("cutflow", "3rd", 0);
  Fill("cutflow", "4th", 0);
  Fill("cutflow", "5th", 0);
  Fill("cutflow", "6th", 0);
  Fill("cutflow", "7th", 0);
  Fill("cutflow", "8th", 0);
  Fill("cutflow", "9th", 0);

  // Now we create all the other histograms that we use in our selection.

  // The first string is the name of the histogram, the second string is the
  // title of the histogram that is used for labelling the x-axis. The three
  // numbers specify the number of bins, and the lower and upper bound of the
  // histogram.
  CreateHisto("Muon_Pt", "Pt of all muons [GeV]", 50, 0, 250);
  CreateHisto("NIsoMuon", "Number of isolated muons", 10, 0, 10);
	CreateHisto("Muon_Eta", "Eta of all muons", 20, -2.6, 2.6);
	CreateHisto("Muon_E", "Energy distribution [GeV]", 50, 0, 750);
	CreateHisto("MET", "Missing transverse energy [GeV]", 25,0,500);
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
  Fill("cutflow", "all");

  //////////////////////////////////////////////////////////////////////
  // implementation of systematic effects

  // As an example, we show how to apply the muon scale uncertainty
  for (unsigned int i = 0; i < Muons.size(); i++) {
    Muons[i] *= muon_scale;
  }

  //////////////////////////////////////////////////////////////////////
  // first, we identify all objects (muons, jets) by applying quality and
  // isolation requirements.

  // Muon isolation
  vector<int> isomu;
  for (unsigned int i = 0; i < Muons.size(); i++) {
    if (Muons[i].IsIsolated()) {
      isomu.push_back(i);
      Fill("Muon_Pt", Muons[i].Pt());
			Fill("Muon_Eta", Muons[i].Eta());
			Fill("Muon_E", Muons[i].E());
      // you can also access Muons[i].E(), .Px(), .Py(), .Pz(), .Eta(), .Phi(), ...
      // and the same with Electrons, Photons, Jets, ...
      // see Documentation of ROOT TLorentzVector
    }
  }
	Fill("MET", met.Pt());

  int NIsoMuon = isomu.size();
  Fill("NIsoMuon", NIsoMuon);

  // now start here applying the jet ID...

  //////////////////////////////////////////////////////////////////////
  // after all objects have been identified, the selection can start

  // the first requirement should be the trigger requirement...
  // ... add it here ...

  // ... and after the trigger requirement we fill the cut flow again ...
  Fill("cutflow", "trigger");

  // ... and then you have to add more code for the selection here ...

  // ... end of the selection. Count selected events
  SelectedEvents++;

  // When the event has been accepted, we return kTRUE, if it is rejected, we
  // return kFALSE.
  return kTRUE;
}
