import argparse, os, sys
import CentralSettings as cs

#################################################################################3
def SubmitDatasets(pathtofile, isTest = False, prodName = 'prodTest', doPretend = False,
                   options = '', outTier = 'T2_ES_IFCA', username = "rodrigvi", verbose = False):
    pathtofile = cs.CheckPathDataset(pathtofile)
    if (pathtofile == ''):
        raise RuntimeError('FATAL: file with datasets not found')

    isData = cs.GuessIsData(pathtofile)
    year   = cs.GuessYear(pathtofile)

    thexsec = None
    theDBS  = "global"

    if "/" in pathtofile:
        if "top" in pathtofile.split("/")[-1].split("_")[0]:
            theDBS = "phys03"
    elif "top" in pathtofile.split("_")[0]:
        theDBS = "phys03"

    if verbose:
        print '> Opening samples file: ', pathtofile, ('(DATA)' if isData else "(MC)")

    for line in cs.ReadLines(pathtofile):
        workarea = "./temp_postproc_" + prodName
        if not os.path.isdir(workarea) and not doPretend:
            os.mkdir(workarea)

        if not isData:
            actualdataset = line.split("/")[1]
            if not actualdataset in cs.xsecDictExtended:
                raise RuntimeError("FATAL: a MC sample does not have its corresponding xsec in the xsecDictExtended. Sample: " + line)
            else:
                thexsec = cs.xsecDictExtended[line.split("/")[1]]

        cs.LaunchCRABTask( (line, isData, prodName, year, thexsec, options, theDBS, isTest, username, doPretend, verbose) )
    print "\n> All tasks submitted!"
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
    parser.add_argument('--username', "-u", default = 'rodrigvi'   , help = 'Your CERN username')
    parser.add_argument('file'            , default = ''           , nargs='?', help = 'txt file with datasets')

    args        = parser.parse_args()
    verbose     = args.verbose
    doPretend   = args.pretend
    dotest      = args.test
    sampleName  = args.dataset
    prodName    = args.prodName
    options     = args.options
    outTier     = args.outTier
    username    = args.username
    fname       = args.file
    doDataset   = False if sampleName == '' else True
    year        = args.year


    SubmitDatasets(fname, dotest, prodName, doPretend, options, outTier, username, verbose)

