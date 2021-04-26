#!/usr/bin/env python
print "> Beginning crab_script.py"
import os, sys, json
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper    import inputFiles, runsAndLumis #this takes care of converting the input files from CRAB

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2        import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer     import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr          import *

from PhysicsTools.NanoAODTools.postprocessing.modules.custom.skimNRecoLeps    import *
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.jetMetGrouper    import *
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.datasetName      import datasetNamer
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.dataTagger       import dataTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.xsecTagger       import xsecTagger

print "> Finished imports. Defining extra modules..."

PrefCorr2016 = lambda: PrefCorr(jetroot    = "L1prefiring_jetpt_2016BtoH.root",    jetmapname    = "L1prefiring_jetpt_2016BtoH",
                                photonroot = "L1prefiring_photonpt_2016BtoH.root", photonmapname = "L1prefiring_photonpt_2016BtoH")

PrefCorr2017 = lambda: PrefCorr(jetroot    = "L1prefiring_jetpt_2017BtoF.root",    jetmapname    = "L1prefiring_jetpt_2017BtoF",
                                photonroot = "L1prefiring_photonpt_2017BtoF.root", photonmapname = "L1prefiring_photonpt_2017BtoF")


print "> Setting parameters..."
### SKIM

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
year   = int(argdict["year"])

cut = ""
if not isData:
    cut = '((nElectron + nMuon) >= 2) || (nGenDressedLepton >= 2)'
else:
    cut = '((nElectron + nMuon) >= 2)'

compatibleyears = [5, 2016, 2017, 2018]
if year not in compatibleyears:
    raise RuntimeError("FATAL: unknown year set.")

print '\t- Year : ', str(year)
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


# Reconst. lepton skim
print "\t- Adding skim in reconstructed leptons properties."
skimRecoLeps = lambda : skipNRecoLeps(isData)
mod.append(skimRecoLeps())


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

#### FIXME: add year

if not isData:
    print "\t- Adding PU and (if required) prefire correction weights."
    if   year == 2016:
        mod.append(puWeight_2016())
        mod.append(PrefCorr2016())
    elif year == 2017:
        mod.append(puWeight_2017())
        mod.append(PrefCorr2017())
    elif year == 2018:
        mod.append(puWeight_2018())
    else:
        raise RuntimeError("FATAL: no working PU & prefiring corrections set for year " + str(year) + ".")


# JEC uncs.
if not isData:
    print "\t- Adding JEC and JER uncertainties."
    JECJERuncsMod = createJMECorrector(dataYear      = year,
                                       jesUncert     = "All",
                                       metBranchName = "MET" if (year != 2017) else "METFixEE2017",
                                       splitJER      = True,)
    mod.append(JECJERuncsMod())

    if   year == 2016:
        mod.append(jetMetCorrelate2016())
    elif year == 2017:
        mod.append(jetMetCorrelate2017())
    elif year == 2018:
        mod.append(jetMetCorrelate2018())
    else:
        raise RuntimeError("FATAL: no working JEC uncs. set for year " + str(year) + ".")



# Muon scale (Rochester)
print "\t- Adding muon energy (Rochester) corrections and uncertainties."
if   year == 2016:
    mod.append(muonScaleRes2016())
elif year == 2017:
    mod.append(muonScaleRes2017())
elif year == 2018:
    mod.append(muonScaleRes2018())
elif year ==  5:
    mod.append(muonScaleRes2017())


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
