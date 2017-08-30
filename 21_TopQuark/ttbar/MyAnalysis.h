//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Feb  1 07:53:21 2012 by ROOT version 5.32/00
// from TTree data/
// found on file: data.root
//////////////////////////////////////////////////////////

#ifndef MyAnalysis_h
#define MyAnalysis_h

#include <TROOT.h>
#include <TFile.h>
#include <TChain.h>
#include <TSelector.h>
#include <TH1D.h>
#include <TLorentzVector.h>
#include <vector>

#include "MyJet.h"
#include "MyMuon.h"
#include "MyElectron.h"
#include "MyPhoton.h"
#include "HistogramManager.h"

using namespace std;

bool LorentzVectorSortPt(const TLorentzVector & l1, const TLorentzVector & l2);

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class MyAnalysis: public TSelector {
public:
  TTree *fChain; //!pointer to the analyzed TTree or TChain

private:   
  // Declaration of leaf types
  Int_t NJet;
  Float_t Jet_Px[10]; //[NJet]
  Float_t Jet_Py[10]; //[NJet]
  Float_t Jet_Pz[10]; //[NJet]
  Float_t Jet_E[10]; //[NJet]
  Float_t Jet_btag[10]; //[NJet]
  Float_t Jet_ID[10]; //[NJet]
  Int_t NMuon;
  Float_t Muon_Px[5]; //[NMuon]
  Float_t Muon_Py[5]; //[NMuon]
  Float_t Muon_Pz[5]; //[NMuon]
  Float_t Muon_E[5]; //[NMuon]
  Int_t Muon_Charge[5]; //[NMuon]
  Float_t Muon_Iso[5]; //[NMuon]
  Int_t NElectron;
  Float_t Electron_Px[5]; //[NElectron]
  Float_t Electron_Py[5]; //[NElectron]
  Float_t Electron_Pz[5]; //[NElectron]
  Float_t Electron_E[5]; //[NElectron]
  Int_t Electron_Charge[5]; //[NElectron]
  Float_t Electron_Iso[5]; //[NElectron]
  Int_t NPhoton;
  Float_t Photon_Px[5]; //[NPhoton]
  Float_t Photon_Py[5]; //[NPhoton]
  Float_t Photon_Pz[5]; //[NPhoton]
  Float_t Photon_E[5]; //[NPhoton]
  Float_t Photon_Iso[5]; //[NPhoton]
  Float_t MET_px;
  Float_t MET_py;
  Float_t MChadronicBottom_px;
  Float_t MChadronicBottom_py;
  Float_t MChadronicBottom_pz;
  Float_t MCleptonicBottom_px;
  Float_t MCleptonicBottom_py;
  Float_t MCleptonicBottom_pz;
  Float_t MChadronicWDecayQuark_px;
  Float_t MChadronicWDecayQuark_py;
  Float_t MChadronicWDecayQuark_pz;
  Float_t MChadronicWDecayQuarkBar_px;
  Float_t MChadronicWDecayQuarkBar_py;
  Float_t MChadronicWDecayQuarkBar_pz;
  Float_t MClepton_px;
  Float_t MClepton_py;
  Float_t MClepton_pz;
  Int_t MCleptonPDGid;
  Float_t MCneutrino_px;
  Float_t MCneutrino_py;
  Float_t MCneutrino_pz;
protected:
  Int_t NPrimaryVertices;
  Bool_t triggerIsoMu24;
  Float_t EventWeight;

private:
  // List of branches
  TBranch *b_NJet; //!
  TBranch *b_Jet_Px; //!
  TBranch *b_Jet_Py; //!
  TBranch *b_Jet_Pz; //!
  TBranch *b_Jet_E; //!
  TBranch *b_Jet_btag; //!
  TBranch *b_Jet_ID; //!
  TBranch *b_NMuon; //!
  TBranch *b_Muon_Px; //!
  TBranch *b_Muon_Py; //!
  TBranch *b_Muon_Pz; //!
  TBranch *b_Muon_E; //!
  TBranch *b_Muon_Charge; //!
  TBranch *b_Muon_Iso; //!
  TBranch *b_NElectron; //!
  TBranch *b_Electron_Px; //!
  TBranch *b_Electron_Py; //!
  TBranch *b_Electron_Pz; //!
  TBranch *b_Electron_E; //!
  TBranch *b_Electron_Charge; //!
  TBranch *b_Electron_Iso; //!
  TBranch *b_NPhoton; //!
  TBranch *b_Photon_Px; //!
  TBranch *b_Photon_Py; //!
  TBranch *b_Photon_Pz; //!
  TBranch *b_Photon_E; //!
  TBranch *b_Photon_Iso; //!
  TBranch *b_MET_px; //!
  TBranch *b_MET_py; //!
  TBranch *b_MChadronicBottom_px; //!
  TBranch *b_MChadronicBottom_py; //!
  TBranch *b_MChadronicBottom_pz; //!
  TBranch *b_MCleptonicBottom_px; //!
  TBranch *b_MCleptonicBottom_py; //!
  TBranch *b_MCleptonicBottom_pz; //!
  TBranch *b_MChadronicWDecayQuark_px; //!
  TBranch *b_MChadronicWDecayQuark_py; //!
  TBranch *b_MChadronicWDecayQuark_pz; //!
  TBranch *b_MChadronicWDecayQuarkBar_px; //!
  TBranch *b_MChadronicWDecayQuarkBar_py; //!
  TBranch *b_MChadronicWDecayQuarkBar_pz; //!
  TBranch *b_MClepton_px; //!
  TBranch *b_MClepton_py; //!
  TBranch *b_MClepton_pz; //!
  TBranch *b_MCleptonPDGid; //!
  TBranch *b_MCneutrino_px; //!
  TBranch *b_MCneutrino_py; //!
  TBranch *b_MCneutrino_pz; //!
  TBranch *b_NPrimaryVertices; //!
  TBranch *b_triggerIsoMu24; //!
  TBranch *b_EventWeight; //!

public:   
  MyAnalysis(TTree * /*tree*/= 0);
  virtual Int_t Version() const {
    return 2;
  }
  virtual void Begin(TTree *tree);
  virtual void SlaveBegin(TTree *tree);
  virtual void Init(TTree *tree);
  virtual Bool_t Notify();
  virtual Bool_t Process(Long64_t entry);
  virtual Int_t GetEntry(Long64_t entry, Int_t getall = 0) {
    return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0;
  }
  virtual void SetOption(const char *option) {
    fOption = option;
  }
  virtual void SetObject(TObject *obj) {
    fObject = obj;
  }
  virtual void SetInputList(TList *input) {
    fInput = input;
  }
  virtual TList *GetOutputList() const {
    return fOutput;
  }
  virtual void SlaveTerminate();
  virtual void Terminate();
   
  virtual void CreateHistograms() = 0;
  virtual void CreateHisto(const char * name, const char * title, 
			   int nBins, double xlow, double xup);
  virtual void Fill(const char * name, double value, double weight = 1.);
  virtual void Fill(const char * name, const char * text, double weight = 1.);
  virtual void FillNoWeight(const char * name, double value);
  virtual void WriteHistograms(const char * fname);
  virtual void BuildEvent();

  vector<MyJet> Jets;
  vector<MyMuon> Muons;
  vector<MyElectron> Electrons;
  vector<MyPhoton> Photons;
   
  TLorentzVector hadB, lepB, hadWq, hadWqb, lepWl, lepWn;
  TLorentzVector met;
   
  HistogramManager histo;
};

#endif
