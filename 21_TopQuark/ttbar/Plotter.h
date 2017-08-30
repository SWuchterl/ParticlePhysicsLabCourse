/*
 * Plotter.h
 *
 *  Created on: 25.06.2012
 *      Author: csander
 *  Modified on: 16.08.2013
 *      Author: mweber
 */

#ifndef PLOTTER_H_
#define PLOTTER_H_

#include <vector>
#include <string>
#include <iostream>

#include <TH1D.h>
#include <TStyle.h>
#include <THStack.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TROOT.h>

#include "HistogramManager.h"

class Plotter {
public:
  Plotter();
  virtual ~Plotter();
  void SetData(HistogramManager v, std::string n){
    data.push_back(v);
    data_names.push_back(n);
    N_histos = v.size();
  }
  void ClearData(){
    data.clear();
    data_names.clear();
  }
  void AddBg(HistogramManager v, std::string n){
    bg.push_back(v);
    bg_names.push_back(n);
    N_histos = v.size();
  }
  void ClearBg(){
    bg.clear();
    bg_names.clear();
  }
  void AddSig(HistogramManager v, std::string n){
    signal.push_back(v);
    signal_names.push_back(n);
    N_histos = v.size();
  }
  void ClearSig(){
    signal.clear();
    signal_names.clear();
  }
  void Plot(std::string filename = "result.pdf", bool DrawLog = true);

private:
  std::vector < HistogramManager > data;
  std::vector < HistogramManager > bg;
  std::vector < HistogramManager > signal;

  std::vector < std::string > data_names;
  std::vector < std::string > bg_names;
  std::vector < std::string > signal_names;

  unsigned int N_histos;

};

#endif /* PLOTTER_H_ */
