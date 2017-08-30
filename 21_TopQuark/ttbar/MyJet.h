/*
 * MyJet.h
 *
 *  Created on: Feb 1, 2012
 *      Author: csander
 */

#ifndef MYJET_H_
#define MYJET_H_

#include <TLorentzVector.h>
#include <TRandom.h>

class MyJet: public TLorentzVector {

public:

  MyJet();
  MyJet(double px, double py, double pz, double e) {
    SetPxPyPzE(px, py, pz, e);
  };

  virtual ~MyJet();

  void SetBTagDiscriminator(double x) {
    btag = x;
  };
      
  static void SetBTagScaleFactor(double sf) {
    SF_b = sf;
  };

  static const double GetBTagScaleFactor() {
    return SF_b;
  };

  const double GetBTagDiscriminator() const {
    return btag;
  };

  const bool IsBTagged();

  void SetJetID(bool id) {
    jetid = id;
  };
      
  const bool GetJetID() {
    return jetid || Pt() > 32;
  };

private:

  double btag;
  bool jetid;
  static double SF_b;
  static TRandom * Random;
};

#endif /* MYJET_H_ */
