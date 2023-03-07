from ROOT import *
#fname = 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/20000/CCF670CF-51AD-FA46-8EEF-A10CE19C3474.root'
fname = 'root://cms-xrd-global.cern.ch//store/data/Run2017D/SingleMuon/NANOAOD/Nano14Dec2018-v1/80000/3E9394FA-EC63-114B-8AB1-18BD46BC5D43.root'

f = TFile.Open(fname)
i = 0
for event in f.Events:
  i += 1
  if hasattr(event, 'Muon_pt'): print 'Muon_pt'
  if hasattr(event, 'Muon_genPartFlav'): print 'Muon_genPartFlav'
  if i >= 10: exit()
