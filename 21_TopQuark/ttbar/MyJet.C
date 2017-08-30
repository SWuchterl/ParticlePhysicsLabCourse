/*
 * MyJet.cpp
 *
 *  Created on: Feb 1, 2012
 *      Author: csander
 *  Last modification: 15.08.2013
 *      Author: mweber
 */

#include "MyJet.h"
#include "TRandom2.h"

TRandom * MyJet::Random = 0;
double MyJet::SF_b = 1.;

MyJet::MyJet() {
  // TODO Auto-generated constructor stub
}

MyJet::~MyJet() {
  // TODO Auto-generated destructor stub
}

// updated to include b-tagging scale factor, only works if SF <= 1!
const bool MyJet::IsBTagged() {
  // get random value between 0..1 from jet phi
  int seed = ((Phi()/TMath::Pi()+1)/2.)*10000000;
  if (Random == 0) 
    Random = new TRandom2;
  Random->SetSeed(seed);
  float coin = Random->Uniform(0., 1.);
  if (btag > 1.74) {
    if (coin > SF_b)
      return false;
    else
      return true;
  }
  return false;
};
   
