/*
 * \file TTBarAnalysis.h
 * \author Martin Weber
 *
 */
#ifndef TTBarAnalysis_h
#define TTBarAnalysis_h

#include "MyAnalysis.h"

class TTBarAnalysis: public MyAnalysis {
public:
  TTBarAnalysis(float sf = 1., float wf = 1, 
		double jscale = 1., double jsmear = 0., double mscale = 1,
		TTree * /*tree*/ = 0);
  virtual ~TTBarAnalysis() { };

  virtual void CreateHistograms();
  virtual Bool_t Process(Long64_t entry);

  // number of total events
  int TotalEvents;
  // number of selected events
  int SelectedEvents;
  
  // variables for systematic uncertainties
  double weight_factor;
  double jet_scale;
  double jet_smear;
  double muon_scale;

  // add your own variables here
};

#endif
