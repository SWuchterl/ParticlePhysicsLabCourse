/* 
 * \file HistogramManager.C
 *
 * \author Martin Weber
 * \date 19.08.2013
 */

#include "HistogramManager.h"

#include <TH1D.h>
#include <TFile.h>

HistogramManager::HistogramManager()
{
}

HistogramManager::~HistogramManager()
{
}

void HistogramManager::Add(const std::string name, TH1D * h)
{
  histo[name] = h;
  hname.push_back(name); 
}

TH1D * HistogramManager::operator[](const std::string name)  
{ 
  return histo[name];
}


TH1D * HistogramManager::operator[](const unsigned int i)
{ 
  return histo[hname[i]]; 
}

unsigned int HistogramManager::size()
{
  return hname.size();
}

void HistogramManager::Write(const char * name)
{
  TFile f(name, "RECREATE");
  for (unsigned int i = 0; i < size(); i++) {
    histo[hname[i]]->Write();
  }
  f.Close();
}
