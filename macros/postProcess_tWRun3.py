#!/usr/bin/env python
print("> Beginning postProcess_tWRun3.py")
import os, sys, json, argparse
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleResProducer

from PhysicsTools.NanoAODTools.postprocessing.modules.custom.leptonSkimmer     import leptonSkimmer ### lo he modificado, hay que devolverlo a lo original
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.datasetName      import datasetNamer
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.dataTagger       import dataTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.xsecTagger       import xsecTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.yearTagger       import yearTagger
from PhysicsTools.NanoAODTools.postprocessing.modules.custom.calculateVariatedElePt import calculateVariatedElePt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "python postProcessHelper.py [options]", description = "Script to postProcess nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--files','-f',action = "append",   dest = "files", required = True, default = [])
    parser.add_argument('--name',     '-n', metavar = 'name',     dest = "name",   required = False, default = "")
    parser.add_argument('--year',     '-y', metavar = 'year',     dest = "year",   required = True, default = 2022)
    parser.add_argument('--isData',     '-iD', metavar = 'isData',     dest = "isData",   required = True, default = "False")
    parser.add_argument('--xsec',     '-xS', metavar = 'xsec',     dest = "xsec",   required = True, default = 0.0)
    parser.add_argument('--outputPath',     '-o', metavar = 'outputPath',     dest = "outputPath",   required = True, default = "")
    
    args        = parser.parse_args()
    files = args.files # list with all the files to pass to the processor
    name = args.name # common name to put to the output skimmed samples
    year = int(args.year) # year of the MC or data
    isData = args.isData == "True" # are the files data files?
    xsec = float(args.xsec) # cross section of the process to which the files belong
    outputPath     = args.outputPath # output path where the output files will be stored
    
    
    ### SLIM FILE
    slimfilein  = "SlimFileIn.txt"
    slimfileout = "SlimFileOut.txt"
    


    ### General skim (others are applied later)
    cut = ""
    if not isData:
        cut = '((nElectron + nMuon) >= 2) || (nGenDressedLepton >= 2)'
    else:
        cut = '((nElectron + nMuon) >= 2) && (run <= 361906 || run >= 362350)' ### REMOVE THIS EVENT CUT FOR DATA
    
    compatibleyears = [2022]
    if year not in compatibleyears:
        raise RuntimeError("FATAL: unknown year set.")

    ### Set golden json
    jsonfile = None
    if year == "2022" and isData:
        jsonfile = '/nfs/fanae/user/asoto/Proyectos/tW-Victor/CMSSW_10_4_0/src/PhysicsTools/NanoAODTools/data/jsonLumi/Cert_Collisions2022_355100_362760_Golden.json'    

    
    ### Set up the modules
    mod = []

    # Muon scale (Rochester), to be implemented
    if year == 2022:
        muonScaleRes2022 = lambda: muonScaleResProducer('',
                                                    '', 2022)
        mod.append(muonScaleRes2022())
      
    # Propagate unc. in electron scale and energy to pt
    ##print("\t- Propagate electron energy (either scale or resolution) corrections to pT.")
    ##propagateElPt = lambda : calculateVariatedElePt(isData)
    ##mod.append(propagateElPt())


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
                          and l.tightId == 1 ) # l.corrected_pt antes estaba esto en lugar de l.pt

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

        #mod.append(lepMerge_elscaleUp())
        #mod.append(lepMerge_elscaleDn())
    else:
        lepMerge_elsigmaUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                                    output = "LepGoodelsigmaUp",
                                                    selector = dict(Muon = muonID, Electron = elecID_lepsigmaUp))
        lepMerge_elsigmaDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                                    output = "LepGoodelsigmaDown",
                                                    selector = dict(Muon = muonID, Electron = elecID_lepsigmaDn))
        #mod.append(lepMerge_elsigmaUp())
        #mod.append(lepMerge_elsigmaDn())

    # Reconst. lepton skim
    print("\t- Adding skim in reconstructed leptons properties.")
    detailedSkim = lambda : leptonSkimmer(isData)
    mod.append(detailedSkim())

    # Dataset name
    print("\t- Adding dataset name branch.")
    datasetNameMod = lambda : datasetNamer(name)
    mod.append(datasetNameMod())

    # Data or MC tag
    print("\t- Adding data tag.")
    dataTagMod = lambda : dataTagger(isData)
    mod.append(dataTagMod())


    # xsec value
    if not isData:
        print("\t- Adding xsec branch.")
        xsecTagMod = lambda : xsecTagger(xsec)
        mod.append(xsecTagMod())

    # year value
    print("\t- Adding year branch.")
    yearTagMod = lambda : yearTagger(year)
    mod.append(yearTagMod())

    # add PU weights
    #if not isData:
    #    print("\t- Adding PU weights.")
    #    if year == 2018:
    #        mod.append(puWeight_UL2018())
    #    else:
    #        raise RuntimeError("FATAL: no working PU & prefiring corrections set for year " + str(year) + ".")

    p = PostProcessor(outputPath + name,
                  files,
                  cut,
                  slimfilein,
                  mod,
                  provenance      = True,
                  fwkJobReport    = False,
                  jsonInput       = jsonfile,
                  outputbranchsel = slimfileout,
                  )
    
    #os.system("mv NANO")
    p.run()









