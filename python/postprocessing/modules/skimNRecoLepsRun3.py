import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class skipNRecoLeps(Module):
    def __init__(self, isdata = False, year = 17, recalibjets = '', era = ''):
        self.minelpt    =  8# 12 # 10 for 5 TeV, 18 for 13 # 7 for multilep
        self.minmupt    =  8#  0 for 5 TeV, 18 for 13 # 7 for multilep
        self.leadleppt  = 12# 12 for 5 TeV, 18 for 13
        self.maxeleta = 2.5
        self.maxmueta = 2.5
        self.isData = isdata
        self.year = year
        self.era = era
        self.filenameJECrecal = recalibjets
        self.filenameJEC = recalibjets
        if self.filenameJEC == '': self.filenameJEC = self.GetFileNameJEC(self.isData, self.filenameJEC, self.year, self.era)
        #self.jetReCalibrator = self.OpenJECcalibrator()
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def GetFileNameJEC(self, isdata, version = '', year = '', era = ''):
      f = version
      if f == '':
        if   year == 16: f = 'Summer16_23Sep2016V4'
        elif year == 17: f = 'Fall17_17Nov2017_V32'
        elif year == 18: f = 'Autumn18_V3'
      if isdata: f+= '_DATA'
      else:      f+= '_MC'
      return f

    def analyze(self, event):
        #jets = Collection(event, 'Jet')
        elec = Collection(event, 'Electron')
        muon = Collection(event, 'Muon')

        event_pass = False
        nlepgood = 0; pts = []
        minLeadingPt = 23; minSubleadingPt = 14;
        # Loose muons, no iso
        for mu in muon:
          if True: # These are loose!
            nlepgood += 1 
            pts.append(mu.pt)

        # Loose electrons MVA - OR - loose cutbased
        for el in elec:
          #if el.pt > self.minelpt and abs(el.eta) < self.maxeleta: #and (el.cutBased >= 1): 
          if el.cutBased >= 1  or  el.mvaNoIso_WPL: 
            nlepgood += 1
            pts.append(el.pt)

        # At least two leptons with some pT cuts
        pts.sort() # sort by pT
        pts = pts[::-1] # Decreasing order
        if nlepgood >= 2 and pts[0] >= minLeadingPt and pts[1] >= minSubleadingPt:
          event_pass = True

        return event_pass

skimRecoLeps = lambda : skipNRecoLeps()
