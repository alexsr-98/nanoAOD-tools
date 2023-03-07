import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

fname = 'Run2017_LowPU_v2'#"Run2018_Step2Closure_CoarseEtaR9Gain_v2"#'Run2017_LowPU_v2'
try:
  ROOT.gSystem.Load("libPhysicsToolsNanoAODTools")
  dummy = ROOT.EnergyScaleCorrection
except Exception as e:
  print "Could not load module via python, trying via ROOT", e
  if "/EnergyScaleCorrection_cc.so" not in ROOT.gSystem.GetLibraries():
    print "Load C++ Worker"
    ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/src/EnergyScaleCorrection.cc++" % os.environ['CMSSW_BASE'])
  dummy = ROOT.EnergyScaleCorrection

corrFiles = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/elecES/%s" %(os.environ['CMSSW_BASE'], fname)
print corrFiles
eleCorr = ROOT.EnergyScaleCorrection(corrFiles, ROOT.EnergyScaleCorrection.ECALELF); 
run = 319337
r9  = 0.8999023
eT = 64.503718
abseta = 2.1279296
cor = eleCorr.scaleCorr(run, eT, abseta, r9);
err = eleCorr.scaleCorrUncert(run, eT, abseta, r9);
eleSmear    = eleCorr.smearingSigma(run, eT, abseta, r9, 12, 0, 0.)
eleSmearUp  = eleCorr.smearingSigma(run, eT, abseta, r9, 12, 1, 0.)
eleSmearDo  = eleCorr.smearingSigma(run, eT, abseta, r9, 12,-1, 0.)
print 'cor = ', cor
print 'err = ', err
print 'Smear: [up, nom, do] = [%1.8f, %1.8f, %1.8f]'%(eleSmearUp, eleSmear, eleSmearDo)
