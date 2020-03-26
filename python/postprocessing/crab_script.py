#!/usr/bin/env python
import os, sys, json
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
filepath = ['root://cms-xrd-global.cern.ch//store/data/Run2017B/DoubleMuon/NANOAOD/Nano14Dec2018-v1/280000/FB901F01-98AA-214F-A2C2-D67630861952.root']

### SKIM 
#cut = 'Jet_pt > 200 && (nElectron + nMuon) >= 2 && nGenDressedLepton >= 2'
cut = '(nElectron + nMuon) >= 2'

### SLIM FILE
slimfile = "SlimFile.txt"

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.skimNRecoLeps import *
from PhysicsTools.NanoAODTools.postprocessing.modules.addTnPvarMuon import *
isData   = 'data' in sys.argv[-1]
doTnP    = 'TnP'  in sys.argv[-1]
doJECunc = 'JEC'  in sys.argv[-1]
if         '2018' in sys.argv[-1] : year = 18
elif       '2016' in sys.argv[-1] : year = 16
else                              : year = 17

### Json file
jsonfile = {}
if isData:
  if     year == 18: jsonfile = 'Cert_314472-322057_13TeV_PromptReco_Collisions18_JSON.txt'
  elif   year == 17: jsonfile = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt' 
  elif   year == 16: jsonfile = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
  jsonfile = './json/' + jsonfile

mod = []
if not isData: 
  if   year == 16:  mod.append(puWeight2016())
  elif year == 17:  mod.append(puAutoWeight())
  elif year == 18:  mod.append(puAutoWeight())
  else           :  mod.append(puAutoWeight())

if doTnP:
  if   year == 17: mod.append(addTnPMuon17())
  elif year == 16: mod.append(addTnPMuon16())
  elif year == 18: mod.append(addTnPMuon18())
  else           : mod.append(addTnPMuon())
  slimfile = "SlimFileTnP.txt"
  cut = 'nMuon >= 2 && Muon_pt[0] > 25 && Muon_pt[1] >= 12'
else:
  mod.append(skimRecoLeps())
  if doJECunc and not isData: mod.append(jetmetUncertainties2017All())

print '>> Slim file: ', slimfile
print '>> cut: ', cut
print '>> ' + ('Is data!' if isData else 'Is MC!')
print '>> ' + ('Creating a TnP Tree' if doTnP else 'Creating a skimmed nanoAOD file')
if doJECunc: print '>> Adding JEC uncertainties'

#mod = [puAutoWeight(),jetmetUncertainties2017All(), skimRecoLeps()]
p=PostProcessor(".",filepath,cut,slimfile,mod,provenance=True,fwkJobReport=True,jsonInput=jsonfile,outputbranchsel=slimfile) #jsonInput
p.run()

print "DONE"
os.system("ls -lR")
