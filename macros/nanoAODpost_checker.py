import os, sys, argparse, json, copy
#import scipy.stats as stats
import subprocess as sp
import numpy as np
import ROOT as r
import warnings as wr
from multiprocessing import Pool, Manager

#### Directories with settings
all_data_dataset_groups = ["SingleMuon", "DoubleMuon", "SingleElectron", "DoubleEG", "MuonEG", "LowEGJet", "HighEGJet", "EGamma"]

r.gROOT.SetBatch(True);


def get_datasets(path, debug = False):
    finaldict = {}
    listofds  = []
    totalds   = 0
    print path, os.listdir(path)
    for dg in next(os.walk(path))[1]:
        if "merged" in dg.lower(): continue
#        if "muoneg" not in dg.lower(): continue
#        print dg
        finaldict[dg] = {}
        #for pref in next(os.walk(path + "/" + dg))[1]:
            #finaldict[dg][pref] = {}
            #for d in next(os.walk(path + "/" + dg + "/" + pref))[1]:
                #suff = d.replace(pref + "_", "")
                #finaldict[dg][pref] = {}
                #totalds += 1
                #listofds.append(year + "/" + dg + "/" + pref + "/" + suff)
        for pref in next(os.walk(path + "/" + dg))[1]:
            finaldict[dg][pref] = {}
            totalds += 1
            listofds.append(dg + "/" + pref)
#            break
#        break
    return finaldict, totalds, listofds


def get_real_dataset_info(fulldataset, debug = False):
    #print fulldataset
    #print "/".join(fulldataset.split("/")[1:])

    #miniaodtag = "MINIAOD" + "SIM" * (fulldataset.split("/")[1] not in all_data_dataset_groups)
    miniaodtag = "NANOAOD" + "SIM" * (fulldataset.split("/")[0] not in all_data_dataset_groups)


    #### By dataset info-obtaining

    if debug:
        print "\n> Query to DAS:"
        print 'dasgoclient -query="dataset dataset=/' + "/".join(fulldataset.split("/")[:]) + '/{tag}" -json'.format(tag = miniaodtag)

    output_tot = json.loads(sp.check_output('dasgoclient -query="dataset dataset=/' + "/".join(fulldataset.split("/")[:]) + '/{tag}" -json'.format(tag = miniaodtag), shell = True))

    nfiles   = 0
    totalevs = 0

    if debug: output_tot

    for infodict in output_tot:
        if "filesummaries" in str(infodict[u"das"][u"services"][0]):
            nfiles   = infodict[u"dataset"][0][u"nfiles"]
            totalevs = infodict[u"dataset"][0][u"nevents"]
            break

    #### By file info-obtaining

    #if debug:
        #print "\n> Queries to DAS. First:"
        #print "    " + 'dasgoclient -query="file dataset=/' + "/".join(fulldataset.split("/")[2:]) + '/{tag}" -json'.format(tag = miniaodtag)
        #print " Second:"
        #print "    " + 'dasgoclient -query="file,run,lumi,events dataset=/' + "/".join(fulldataset.split("/")[2:]) + '/{tag}" -json'.format(tag = miniaodtag)

    #output_nfiles  = json.loads(sp.check_output('dasgoclient -query="file dataset=/' + "/".join(fulldataset.split("/")[2:]) + '/{tag}" -json'.format(tag = miniaodtag), shell = True))
    #output_nevents = json.loads(sp.check_output('dasgoclient -query="file,run,lumi,events dataset=/' + "/".join(fulldataset.split("/")[2:]) + '/{tag}" -json'.format(tag = miniaodtag), shell = True))

    #nfiles = len(output_nfiles)

    #totalevs = 0
    #for f in output_nevents:
        #for run in f[u'events']:
            #if run[u'number'] == None:
                #wr.warn("WARNING: null value as number of events encountered.")
                #if debug:
                    #print "File(s) with null value of number of events:"
                    #print f
            #else:
                #totalevs += sum(run[u'number'])

    if debug:
        print "\n======================= DAS output"
        print "nfiles:",  nfiles
        print "nevents:", totalevs
        print "=======================\n"

    #sys.exit()
    return nfiles, totalevs


def get_produced_dataset_info(fulldataset, folder, datadict, ncores = 1, debug = False):
    dg = fulldataset.split("/")[0]; pref = fulldataset.split("/")[1]
    dspath = "/".join([dg, pref])
    subprods = os.listdir(folder + "/" + dspath)
    if debug: print "Initiating postprocessed dataset checking"
    for subprod in subprods:
        datadict[dg][pref]["subprod_" + subprod] = {}

        if debug: print "\n====== Checking subprod:", subprod

        tmpnfiles  = 0
        tmpnevents = 0
        for subdir in next(os.walk(folder + "/" + dspath + "/" + subprod))[1]:
            if debug: print "### Checking subdir:", subdir
            tmppath = folder + "/" + dspath + "/" + subprod + "/" + subdir

            #tmplistoffiles = [get_tree_entries(tmppath + "/" + rootfile) for rootfile in os.listdir(tmppath) if (rootfile[-5:] == ".root")]

            tmptsks = [tmppath + "/" + rootfile for rootfile in os.listdir(tmppath) if (rootfile[-5:] == ".root")]

            pool = Pool(ncores)
            tmplistoffiles = pool.map(get_tree_entries, tmptsks)
            pool.close()
            pool.join()
            del pool

            tmpnevents += sum(tmplistoffiles)
            tmpnfiles  += len(tmplistoffiles)
        #print datadict
        datadict[dg][pref]["subprod_" + subprod]["nfiles"]  = int(tmpnfiles)
        datadict[dg][pref]["subprod_" + subprod]["nevents"] = int(tmpnevents)

        if debug: print "\n    - Detected nfiles:", tmpnfiles, ", detected nevents:", tmpnevents

    #print datadict[dg][pref]
    return


def get_tree_entries(rootfile):
    if debug: print "# Checking file:", rootfile
    tmpfile = r.TFile(rootfile, "READ")

    entries = tmpfile.hCount.GetBinContent(1)
#    entries = tmpfile.Events.GetEntries()

#    entries = 0
#    for ev in tmpfile.Runs:
#        entries += ev.genEventCount

    tmpfile.Close(); del tmpfile;
    return entries


def analyse_dataset(fulldataset, datadict, debug = False):
    #### possible enhancements:
    # check per file rather than in total nevs
    # check file size and compare with the ones in GRID
    dg = fulldataset.split("/")[0]; pref = fulldataset.split("/")[1];

    # Get subproductions
    subprods = []
    for key in datadict[dg][pref]:
        if key[:7] == "subprod": subprods.append(key)

    for subprod in subprods:
        equalnfiles  = False
        equalnevents = False
        # ...first, check if the number of files is the same
        if datadict[dg][pref][subprod]["nfiles"] == datadict[dg][pref]["das_nfiles"]:
            equalnfiles = True

        # ...and secondly, check the number of events
        if datadict[dg][pref][subprod]["nevents"] == datadict[dg][pref]["das_nevents"]:
            equalnevents = True

        # This is when you care about the number of files (if you use fileBased splitting in CRAB)...
#        if equalnfiles and equalnevents:
#            datadict[dg][pref][subprod]["check_result"] = "CORRECT"
#        else:
#            datadict[dg][pref][subprod]["check_result"] = "WRONG:" + ("nfiles" if not equalnfiles else "nevents")

        # And this, when you not
        if equalnevents:
            datadict[dg][pref][subprod]["check_result"] = "CORRECT"
        else:
            datadict[dg][pref][subprod]["check_result"] = "WRONG:nevents"
            
    if len(subprods) == 1:
        datadict[dg][pref]["check_result"] = datadict[dg][pref][subprods[0]]["check_result"]
    else:
        datadict[dg][pref]["check_result"] = "MULTIPLE|"
        tmpallok = True
        lastsubprod = get_latest_subprod(subprods)[0]
        if datadict[dg][pref][lastsubprod]["check_result"] != "CORRECT":
            datadict[dg][pref]["check_result"] += datadict[dg][pref][lastsubprod]["check_result"]
        else:
            datadict[dg][pref]["check_result"] += "CORRECT"
    return


def get_latest_subprod(listofsubprods):
    result = get_ordered_list(8, listofsubprods) # year
    #print "jeje"
    #print result
    if len(result) > 1:
        result = get_ordered_list(10, result) # month
        if len(result) > 1:
            result = get_ordered_list(12, result) # day
            if len(result) > 1:
                result = get_ordered_list(15, result) # hour
                if len(result) > 1:
                    result = get_ordered_list(17, result) # minute
                    if len(result) > 1:
                        result = get_ordered_list(19, result) # second
    return result


def get_ordered_list(index, thelist):
    #print thelist
    if len(thelist) <= 1: return thelist
    tmpdict = {}
    for el in thelist: tmpdict[el] = int(el[index:index + 2])
    listtoreturn =  sorted(thelist, key = lambda x: -tmpdict[x])
    if tmpdict[listtoreturn[0]] == tmpdict[listtoreturn[1]]:
        return [el for el in listtoreturn if tmpdict[el] == tmpdict[listtoreturn[0]]]
    else:
        return listtoreturn[:1]


def check_dataset(tsk, ncores = 1, debug = False):
    fulldataset, datadict, folder = tsk

    if debug:
        print "\nInitiating check for:"
        print "Fulldataset:", fulldataset
        print "Datadict:", datadict
        print "Folder:", folder


    dg = fulldataset.split("/")[0]; pref = fulldataset.split("/")[1];

    #### First, get DAS info
    das_nfiles, das_nevs = get_real_dataset_info(fulldataset, debug)

    datadict[dg][pref]["das_nfiles"]  = das_nfiles
    datadict[dg][pref]["das_nevents"] = das_nevs


    #### Then, get your info
    get_produced_dataset_info(fulldataset, folder, datadict, ncores, debug)

    #### Now, analyse
    analyse_dataset(fulldataset, datadict, debug)
    print "\t- Checked /" + fulldataset

    #if "ZJToEEJ" in fulldataset: sys.exit()
    return


def print_check_results(thedict):
    print "\n> Check results:"
    wrongds = 0
    massivenods = 0
    for d in thedict:
        print "\n- DATASET: " + d
        datasetdict = thedict[d]
#        print datasetdict
        if datasetdict == "NODATASETS":
            print "There are no datasets in this dataset group folder. This might happen due to massive (i.e. in all jobs) execution errors."
            massivenods += 1
        else:
            for suff in datasetdict:
                print datasetdict[suff]["check_result"] + " === /" + d + "/" + suff
            if "WRONG" in datasetdict[suff]["check_result"]: wrongds += 1
    
    print " "
    if (wrongds + massivenods) == 0:
        print "> All datasets are correct!"
    else:
        if wrongds > 0:
            print "> A total of " + str(wrongds) + " datasets have not been correctly postprocessed."
        if massivenods > 0:
            print "> A total of " + str(massivenods) + " dataset groups have not been correctly postprocessed due to massive execution errors."

    if debug:
        print "Finaldict"
        print thedict

    return



if __name__=="__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--folder',   '-f', metavar = 'folder', dest = "folder", help = 'folder where the nanoAOD datasets will be searched on. If not given, ./ is assumed.', required = False, default = "./")
    parser.add_argument('--ncores',   '-n', metavar = 'ncores', dest = "ncores", help = 'number of cores for parallelisation of checking.', required = False, default = 1)
    parser.add_argument('--verbose',   '-v', action  = 'store_true', dest = "debug", help = 'increase logging for debugging.', required = False, default = False)

    args   = parser.parse_args()
    folder = args.folder
    ncores = int(args.ncores)
    debug = args.debug

    datasetdict, totalds, listofds = get_datasets(folder, debug)

    #print datasetdict

    print "> The following " + str(totalds) + " datasets inside the corresponding dataset groups and inside the respective year/supergroup have been found inside the folder " + folder
    for dg in datasetdict:
        print "\n### DATASET: " + dg
        #if datasetdict[dg] == "NODATASETS":
            #print "There are no datasets in this dataset group folder. This might happen due to massive (i.e. in all jobs) execution errors."
        #else:
        for pref in datasetdict[dg]:
            print "\t- " + pref

    #sys.exit()
    print "\n> Beginning check of postprocessed nanoAOD"
    tasks = []

    #manageddict = Manager().dict(datasetdict)
    manageddict = datasetdict

    for el in listofds:
        tasks.append( (el, manageddict, folder) )

    #if ncores == 1:
        #print "- Sequential execution chosen"
        #for el in tasks: check_dataset(el)
    #else:
        #raise RuntimeError("ERROR: still not implemented")
        #print "- Parallelised execution chosen"
        #pool = Pool(ncores)
        #pool.map(check_dataset, tasks)
        #pool.close()
        #pool.join()
        #del pool
    
    for el in tasks: check_dataset(el, ncores, debug)

    print_check_results(manageddict)
    print ""





