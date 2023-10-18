import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class leptonSkimmer(Module):
    def __init__(self, _isd):
        self.minpt  =  20
        self.maxeta = 2.4
        self.isd    = _isd
        return

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, ev):
        if self.isd:
            return (ev.nLepGood >= 2)
        else:
            thegenleps = Collection(ev, 'GenDressedLepton')
            nlepgengood = 0
            for iL in thegenleps:
                if iL.pt > self.minpt and abs(iL.eta) < self.maxeta:
                    nlepgengood += 1

            return ((ev.nLepGood >= 2 or ev.nLepGoodelsigmaUp >= 2 or ev.nLepGoodelsigmaDown >= 2 or ev.nLepGoodelscaleUp >= 2 or ev.nLepGoodelscaleDown >= 2)
                    or (nlepgengood >= 2))
