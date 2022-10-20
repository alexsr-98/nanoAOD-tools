#!/usr/bin/env python
print "> Beginning crab_script.py"
import os, sys, json
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper    import inputFiles, runsAndLumis # This takes care of converting the input files from CRAB

#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2        import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer     import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleResProducer
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr          import *

#from PhysicsTools.NanoAODTools.postprocessing.modules.custom.skimNRecoLeps    import *
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.leptonSkimmer     import leptonSkimmer
#from PhysicsTools.NanoAODTools.postprocessing.modules.custom.jetMetGrouper    import *
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.datasetName      import datasetNamer
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.dataTagger       import dataTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.xsecTagger       import xsecTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.yearTagger       import yearTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.calculateVariatedElePt import calculateVariatedElePt

print "> Finished imports. Defining extra modules..."

#PrefCorr2016 = lambda: PrefCorr(jetroot    = "L1prefiring_jetpt_2016BtoH.root",    jetmapname    = "L1prefiring_jetpt_2016BtoH",
                                #photonroot = "L1prefiring_photonpt_2016BtoH.root", photonmapname = "L1prefiring_photonpt_2016BtoH")

#PrefCorr2017 = lambda: PrefCorr(jetroot    = "L1prefiring_jetpt_2017BtoF.root",    jetmapname    = "L1prefiring_jetpt_2017BtoF",
                                #photonroot = "L1prefiring_photonpt_2017BtoF.root", photonmapname = "L1prefiring_photonpt_2017BtoF")


print "> Setting parameters..."

### SLIM FILE
slimfilein  = "SlimFileIn.txt"
slimfileout = "SlimFileOut.txt"
print "\t- Job number (inside CRAB task):", sys.argv[1]
theargs = sys.argv[-1].replace("theargs=", "")

print "\t- Using as arguments:", theargs

argdict = {"jobnum" : sys.argv[1]}
for el in theargs.split(","):
    subels = el.split(":")
    argdict[subels[0]] = subels[1]

minargs = ["isData", "year", "datasetname"]
if any([el not in argdict for el in minargs]):
    raise RuntimeError("FATAL: minimum arguments not provided. Only these were provided: " + theargs)


isData = int(argdict["isData"])
year   = int(argdict["year"]) if "apv" not in argdict["year"].lower() else 2016
isAPV  = "apv" in argdict["year"].lower()

### General skim (others are applied later)
cut = ""
if not isData:
    cut = '((nElectron + nMuon) >= 2) || (nGenDressedLepton >= 2)'
else:
    cut = '((nElectron + nMuon) >= 2)'

compatibleyears = [5, 2016, 2017, 2018]
if year not in compatibleyears:
    raise RuntimeError("FATAL: unknown year set.")

print '\t- Year : ', str(year), "" if not isAPV else "APV"
print '\t- Slim file in : ', slimfilein
print '\t- Slim file out: ', slimfileout
print '\t- Skim cut: ', cut
print '\t- ' + ('This is data' if isData else 'This is MC')

era = '' if not 'era' in argdict else argdict["era"]
if era != '':
    print '\t- Found era: ', era


print "> Setting json file..."
### Json file
jsonfile = runsAndLumis()


print "> Setting post-processing modules..."
mod = []


# Muon scale (Rochester)
print "\t- Adding muon energy (Rochester) corrections and uncertainties."
if   year == 2016:
    muonScaleRes2016 = lambda: muonScaleResProducer('roccor.Run2.v5',
                                                    'RoccoR2016aUL.txt' if isAPV else 'RoccoR2016bUL.txt', 2016)
    mod.append(muonScaleRes2016())
elif year == 2017:
    muonScaleRes2017 = lambda: muonScaleResProducer('roccor.Run2.v5',
                                                    'RoccoR2017UL.txt', 2017)
    mod.append(muonScaleRes2017())
elif year == 2018:
    muonScaleRes2018 = lambda: muonScaleResProducer('roccor.Run2.v5',
                                                    'RoccoR2018UL.txt', 2018)
    mod.append(muonScaleRes2018())
elif year ==  5:
    muonScaleRes2017 = lambda: muonScaleResProducer('roccor.Run2.v5',
                                                    'RoccoR2017UL.txt', 2017)
    mod.append(muonScaleRes2017())


# Propagate unc. in electron scale and energy to pt
print "\t- Propagate electron energy (either scale or resolution) corrections to pT."
propagateElPt = lambda : calculateVariatedElePt(isData)
mod.append(propagateElPt())


# Selecting reconstructed and counting (only) good particle-level leptons
IDDict = {}
IDDict["muons"] = {
    "pt"       : 20,
    "eta"      : 2.4,
    "isorelpf" : 0.15,
}

IDDict["elecs"] = {
    "pt"   : 20,
    "eta0" : 1.4442,
    "eta1" : 1.566,
    "eta2" : 2.4,
    "dxy_b" : 0.05,
    "dz_b"  : 0.10,
    "dxy_e" : 0.10,
    "dz_e"  : 0.20,
    "etasc_be" : 1.479,
}

muonID = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.corrected_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )

elecID = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
                       #and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.deltaEtaSC - l.eta) <= IDDict["elecs"]["etasc_be"]) ### COMO IGUAL ES
                       #else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )


muonID_lepenUp = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.correctedUp_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )
muonID_lepenDn = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.correctedDown_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )


elecID_lepscaleUp = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.scaleUp_pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
elecID_lepscaleDn = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.scaleDown_pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )

elecID_lepsigmaUp = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.sigmaUp_pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
elecID_lepsigmaDn = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.sigmaDown_pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )


from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = lambda : collectionMerger(input = ["Electron", "Muon"],
                                     output = "LepGood",
                                     selector = dict(Muon = muonID, Electron = elecID))

lepMerge_muenUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodmuUp",
                                            selector = dict(Muon = muonID_lepenUp, Electron = elecID))
lepMerge_muenDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodmuDown",
                                            selector = dict(Muon = muonID_lepenDn, Electron = elecID))

mod.append(lepMerge())
mod.append(lepMerge_muenUp())
mod.append(lepMerge_muenDn())

if isData:
    lepMerge_elscaleUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                                output = "LepGoodelscaleUp",
                                                selector = dict(Muon = muonID, Electron = elecID_lepscaleUp))
    lepMerge_elscaleDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                                output = "LepGoodelscaleDown",
                                                selector = dict(Muon = muonID, Electron = elecID_lepscaleDn))

    mod.append(lepMerge_elscaleUp())
    mod.append(lepMerge_elscaleDn())
else:
    lepMerge_elsigmaUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                                output = "LepGoodelsigmaUp",
                                                selector = dict(Muon = muonID, Electron = elecID_lepsigmaUp))
    lepMerge_elsigmaDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                                output = "LepGoodelsigmaDown",
                                                selector = dict(Muon = muonID, Electron = elecID_lepsigmaDn))
    mod.append(lepMerge_elsigmaUp())
    mod.append(lepMerge_elsigmaDn())



# Reconst. lepton skim
print "\t- Adding skim in reconstructed leptons properties."
detailedSkim = lambda : leptonSkimmer(isData)
mod.append(detailedSkim())


# Dataset name
print "\t- Adding dataset name branch."
datasetNameMod = lambda : datasetNamer(argdict["datasetname"])
mod.append(datasetNameMod())


# Data or MC tag
print "\t- Adding data tag."
dataTagMod = lambda : dataTagger(isData)
mod.append(dataTagMod())


# xsec value
if not isData:
    print "\t- Adding xsec branch."
    xsecTagMod = lambda : xsecTagger(float(argdict["xsec"]))
    mod.append(xsecTagMod())

# year value
print "\t- Adding year branch."
yearTagMod = lambda : yearTagger(year)
mod.append(yearTagMod())


if not isData:
    print "\t- Adding PU weights."
    if   year == 2016:
        mod.append(puWeight_UL2016())
        #mod.append(PrefCorr2016())
    elif year == 2017:
        mod.append(puWeight_UL2017())
        #mod.append(PrefCorr2017())
    elif year == 2018:
        mod.append(puWeight_UL2018())
    else:
        raise RuntimeError("FATAL: no working PU & prefiring corrections set for year " + str(year) + ".")


# JEC uncs.
#if not isData:
    #print "\t- Adding JEC and JER uncertainties."
    #JECJERuncsMod = createJMECorrector(dataYear      = year,
                                       #jesUncert     = "All",
                                       #metBranchName = "MET" if (year != 2017) else "METFixEE2017",
                                       #splitJER      = True,
                                       #applyHEMfix   = True,)
    #mod.append(JECJERuncsMod())

    #if   year == 2016:
        #mod.append(jetMetCorrelate2016())
    #elif year == 2017:
        #mod.append(jetMetCorrelate2017())
    #elif year == 2018:
        #mod.append(jetMetCorrelate2018())
    #else:
        #raise RuntimeError("FATAL: no working JEC uncs. set for year " + str(year) + ".")



print "> Finished setting of modules. Starting execution."
p = PostProcessor(".",
                  inputFiles(),
                  cut,
                  slimfilein,
                  mod,
                  provenance      = True,
                  fwkJobReport    = True,
                  jsonInput       = jsonfile,
                  outputbranchsel = slimfileout)
p.run()

print "> Finished execution."
os.system("ls -lR")
