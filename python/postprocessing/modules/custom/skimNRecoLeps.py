import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class skipNRecoLeps(Module):
    def __init__(self):
        self.minelpt    =  15# 12 # 10 for 5 TeV, 18 for 13 # 7 for multilep
        self.minmupt    =  15#  0 for 5 TeV, 18 for 13 # 7 for multilep
        self.maxeleta   = 2.5
        self.maxmueta   = 2.5
        return

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #jets = Collection(event, 'Jet')
        elec = Collection(event, 'Electron')
        muon = Collection(event, 'Muon')

        nlepgood = 0; minptLeading = False
        for mu in muon:
            if mu.pt > self.minmupt and abs(mu.eta) < self.maxmueta:
                nlepgood += 1
        for el in elec:
            if el.pt > self.minelpt and abs(el.eta) < self.maxeleta:
                nlepgood += 1

        return ((nlepgood >= 2) or (event.nGenDressedLepton >= 2))


skimRecoLeps = lambda : skipNRecoLeps()
