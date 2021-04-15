import getpass, argparse
import os, sys
from multiprocessing import Process
from datetime import datetime



xsecDict = {"tW_inclusive"  : 35.85, # NNLO
            "tW_nofullyhad" : 19.4674104, # NNLO
}


xsecDictExtended = {"ST_tW_antitop_5f_NoFullyHadronicDecays_TuneEE5C_13TeV-powheg-herwigpp" : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8" : xsecDict["tW_inclusive"]
}


def GetToday():
    return datetime.now.strftime("%Y-%m-%d")


def GetTimeNow():
    now = datetime.now()
    time = str(now.hour) + 'h' + str(now.minute) + 'm' + str(now.second) + 's'
    return time


def GetEra(sampleName, year, isData = True):
    if not isData: return ''
    if isinstance(year, int): year = str(year)
    if len(year) == 2: year = "20%s"%year
    sy = 'Run%s'%(year)
    ls = len(sy)
    find = sampleName.find(sy)
    if find == -1: return ''
    era = sampleName[find+ls:find+ls+1]
    return era


#def GetName_cfg(sampleName, isData = False):
    #''' Returns the name of the cfg file for a given dataset '''
    #if sampleName[0] != '/': sampleName = '/' + sampleName
    #tag = sampleName[1 : sampleName[1:].find('/')+1]
    #genTag = sampleName[ sampleName[1:].find('/')+1 :]
    #genTag = genTag[:genTag[1:].find('/')+1]
    #a = genTag.find('_ext')
    #if a > 0: tag += genTag[a+1:a+5]
    #a = genTag.find('_new_pmx')
    #if a > 0: tag += genTag[a+1:a+8]
    #a = genTag.find('_backup')
    #if a > 0: tag += genTag[a+1:a+7]
    #if (isData): tag += genTag.replace('/','_')

    #filename = 'crab_cfg_' + tag + '.py'
    #return filename


def CheckPathDataset(path):
    ''' Check if the name exists in local folder or in dataset folder '''
    if (os.path.isfile(path)):
        return path
    elif (os.path.isfile(path + '.txt')):
        return path + '.txt'

    path = 'datasets/' + path
    if (os.path.isfile(path)):
        return path
    elif (os.path.isfile(path + '.txt')):
        return path+'.txt'
    return ''


def GuessIsData(path):
    ''' Returns False if the dataset file seems to correspond to mc, True otherwise '''
    name = path.replace('datasets', '')
    if "mc" in name.lower():
        return False
    elif "data" in name.lower():
        return True
    else:
        if 'NANOAOD' in path:
            if 'NANOAODSIM' in path:
                return False
            else:
                return True
    return True


def GuessYear(path):
    thepath = path.lower()
    if   any([el in thepath for el in ["5tev", "5p02"]]): return 5
    elif 'run2018' in thepath: return 2018
    elif 'run2017' in thepath: return 2017
    elif 'run2016' in thepath: return 2016
    elif '2018'    in thepath: return 2018
    elif '2017'    in thepath: return 2017
    elif '2016'    in thepath: return 2016

    raise RuntimeError("FATAL: couldn't guess year from path " + path)
    return


#configurationCache = {}
def LaunchCRABTask(tsk):
    sampleName, isData, productionTag, year, thexsec, options, thedbs, pretend = tsk
    from CRABAPI.RawCommand       import crabCommand
    from CRABClient.UserUtilities import config
    from CRABClient.JobType       import CMSSWConfig

    print "# Launching CRAB task for sample {d} that is data {isd}, year {y}, for prod. tag {p} using the DBS {dbs} and with options {o}".format(d = sampleName, isd = str(isData), dbs = thedbs, p = productionTag, y = year, o = options)
    #print "\nsyspath:", sys.path
    #print "\ncwd:", os.getcwd()
    #sys.exit()

    outputdir = '/store/user/rodrigvi/nanoAOD_postprocessing/' + productionTag
    inFiles   = ['./crab_script.py', '../scripts/haddnano.py', './SlimFileIn.txt', './SlimFileOut.txt']
    lumimask  = ""
    workarea  = "temp_postproc_" + productionTag
    craboptions = "year:" + str(year)
    if options != "":
        craboptions += "," + options
    craboptions += ",datasetname:" + sampleName.split("/")[1]
    era = GetEra(sampleName, year, isData)
    if era != '': craboptions += ',era:%s'%era

    if not isData:
        craboptions += ",isData:0,xsec:" + str(thexsec)
    else:
        craboptions += ",isData:1"

    if (isData):
        # Set as MC... the only way the Count histogram works!! --> So we can compare with the numbers in DAS
        if   year == 2016:
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
            lumiMask = './lumijson/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
            lumijson = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
        elif year == 2017:
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'  # 41.29/fb
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
            lumiMask = './lumijson/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
            #lumijson = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
            lumijson = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
        elif year == 2018:
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
            lumiMask = './lumijson/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
            lumijson = 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
        else:
            raise RuntimeError("FATAL: no lumimask and lumijson set for year " + str(year))

        inFiles.append("./lumijson/" + lumijson)

    config = config()
    def submit(config):
        res = crabCommand('submit', config = config )

    config.General.requestName  = productionTag + "_" + sampleName[0:min([70, len(sampleName)])].replace("/", "_")
    config.General.workArea     = workarea
    config.General.transferLogs = True

    config.JobType.pluginName  = 'Analysis'
    config.JobType.psetName    = '../crab/PSet.py'
    config.JobType.scriptExe   = './crab_script.sh'
    config.JobType.scriptArgs  = ["theargs=" + craboptions] #### Debe haber un "="
    config.JobType.inputFiles  = inFiles

    #config.JobType.maxMemoryMB = 2500
    config.JobType.allowUndistributedCMSSW = True
    config.JobType.sendPythonFolder = True

    config.Data.inputDBS    = thedbs
    config.Data.splitting   = 'FileBased'
    #config.Data.splitting   = 'Automatic'
    config.Data.unitsPerJob = 1
    config.Data.publication = False
    config.Data.totalUnits  = 3
    config.Data.allowNonValidInputDataset = True

    config.Data.outLFNDirBase = outputdir
    config.Data.inputDataset  = sampleName
    config.Data.lumiMask      = lumimask
    config.Data.outputDatasetTag = productionTag + "_" + sampleName[0:min([70, len(sampleName)])].replace("/", "_")

    config.Site.storageSite = 'T2_ES_IFCA'
    #config.Site.storageSite = 'T2_CH_CERN'
    #config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']
    #config.Site.blacklist   = []
    #config.Site.ignoreGlobalBlacklist = True


    #res = crabCommand('submit', config = config)

    if not pretend:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
        del p

    del config
    #CMSSWConfig.configurationCache.clear() #### NOTE: this is done in order to allow the parallelised CRAB job submission. For further
                                           ## information, please check the code on [1], the commit of [2] and the discussion of [3].
                                           ## [1]: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/JobType/CMSSWConfig.py
                                           ## [2]: https://github.com/dmwm/CRABClient/commit/a50bfc2d1f32093b76ba80956ee6c5bd6d61259e
                                           ## [3]: https://github.com/dmwm/CRABClient/pull/4824
    return


def confirm(message = "Do you wish to continue?"):
    """
    Ask user to enter y(es) or n(o) (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n", "yes", "no"]:
        answer = raw_input(message + " [Y/N]\n").lower()
    return answer[0] == "y"


def CheckExistanceOfFolders(listoftasks):
    listoftaskswcreatedfolder = []
    for tsk in listoftasks:
        if os.path.isdir("./" + tsk[3] + "/crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")): listoftaskswcreatedfolder.append(tsk)

    return listoftaskswcreatedfolder


def KillAndErase(tsk):
    print "### Task with folder", "crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")
    print "# Killing..."
    os.system("crab kill -d ./{wa}/{fl}".format(wa = tsk[3], fl = "crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")))
    print "# Erasing..."
    os.system("rm -rf ./{wa}/{fl}".format(wa = tsk[3], fl = "crab_" + tsk[0] + '_' + tsk[1] + ("_" + tsk[2]) * (tsk[2] != "")))
    return


def ReadLines(path):
    lines = []
    f = open(path, 'r')
    for line in f:
        line = line.replace(' ', '')
        line = line.replace('\t', '')
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        if line == '': continue
        if line[0] == '#': continue
        if line.find('#') > 0: line = line[:line.find('#')]
        if len(line) <= 1: continue
        lines.append(line)
    return lines


def SubmitDatasets(pathtofile, isTest = False, prodName = 'prodTest', doPretend = False,
                   options = '', outTier = 'T2_ES_IFCA', verbose = False):
    pathtofile = CheckPathDataset(pathtofile)
    if (pathtofile == ''):
        raise RuntimeError('FATAL: file with datasets not found')

    isData = GuessIsData(pathtofile)
    year   = GuessYear(pathtofile)

    thexsec = None
    theDBS  = "global"

    if "/" in pathtofile:
        if "top" in pathtofile.split("/")[-1].split("_")[0]:
            theDBS = "phys03"
    elif "top" in pathtofile.split("_")[0]:
        theDBS = "phys03"

    if verbose:
        print 'Opening path: ', pathtofile, ('(DATA)' if isData else "(MC)")

    for line in ReadLines(pathtofile):
        #cfgName = GetName_cfg(line, isData)
        print 'line = ', line
        if verbose:
            #print 'Creating cfg file for dataset: ', line
            print '%s!! year = %s, options = %s'%('Data' if isData else 'MC', year, options)

        workarea = "./temp_postproc_" + prodName
        if not os.path.isdir(workarea):
            os.mkdir(workarea)

        if not isData:
            actualdataset = line.split("/")[1]
            if not actualdataset in xsecDictExtended:
                raise RuntimeError("FATAL: a MC sample does not have its corresponding xsec in the xsecDictExtended. Sample: " + line)
            else:
                thexsec = xsecDictExtended[line.split("/")[1]]

        LaunchCRABTask( (line, isData, prodName, year, thexsec, options, theDBS, doPretend) )
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "python SubmitDatasets.py [options]", description = "blabla", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--verbose' , '-v', action = 'store_true'  , help = 'Activate the verbosing')
    parser.add_argument('--pretend' , '-p', action = 'store_true'  , help = 'Create the files but not send the jobs')
    parser.add_argument('--test'    , '-t', action = 'store_true'  , help = 'Sends only one or two jobs, as a test')
    parser.add_argument('--dataset' , '-d', default = ''           , help = 'Submit jobs to run on a given dataset')
    parser.add_argument('--year'    , '-y', default = 0            , help = 'Year')
    parser.add_argument('--prodName', '-n', default = ''           , help = 'Give a name to your production')
    parser.add_argument('--options' , '-o', default = ''           , help = 'Options to pass to your producer')
    parser.add_argument('--outTier'       , default = 'T2_ES_IFCA' , help = 'Your output tier')
    parser.add_argument('file'            , default = ''           , nargs='?', help = 'txt file with datasets')

    args   = parser.parse_args()
    verbose     = args.verbose
    doPretend   = args.pretend
    dotest      = args.test
    sampleName = args.dataset
    prodName    = args.prodName
    options     = args.options
    outTier     = args.outTier
    fname       = args.file
    doDataset   = False if sampleName == '' else True
    year        = int(args.year)


    #if doDataset:
        #if verbose: print 'Creating cfg file for dataset: ', sampleName
        #doData = GuessIsData(sampleName)
        #if year == 0:
            #year = GuessYear(sampleName)
        #print ' >> Is data?: ', doData
        #print ' >> Year    : ', year

        #cfgName = GetName_cfg(sampleName, doData)

        #CreateCrab_cfg(sampleName, doData, dotest, prodName, year, options,outTier)
        #if not doPretend:
            #os.system('crab submit -c ' + cfgName)
            #if not os.path.isdir(prodName): os.mkdir(prodName)
            #os.rename(cfgName, prodName + '/' + cfgName)
            ##os.remove(cfgName)
    #else:
    SubmitDatasets(fname, dotest, prodName, doPretend, options, outTier, verbose)

