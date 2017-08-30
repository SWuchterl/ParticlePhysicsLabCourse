#ifndef _HistogramManager_h_
#define _HistogramManager_h_

/* 
 * \file HistogramManager.h
 *
 * \author Martin Weber
 */

#include <vector>
#include <map>
#include <string>

class TH1D;

class HistogramManager {
public:
  HistogramManager();
  ~HistogramManager();

  // add 1D histogram to manager
  void Add(const std::string name, TH1D * h);

  // get number of histograms
  unsigned int size();

  // access histograms by name
  TH1D * operator[](const std::string name);
  
  // access histograms by index
  TH1D * operator[](const unsigned int i);

  // write histograms to a file
  void Write(const char * name);

private:
  std::map<std::string, TH1D *> histo;
  std::vector<std::string> hname;
};

#endif
