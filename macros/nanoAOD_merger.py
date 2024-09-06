from random import sample
import ROOT as r
import os, sys, argparse

r.gROOT.SetBatch(1)

class pcol:
    end    = '\033[0m'
    blue   = '\033[1;94m'
    cyan   = '\033[1;96m'
    green  = '\033[1;92m'
    purple = '\033[1;95m'
    orange = '\033[1;93m'
    red    = '\033[1;91m'
    white  = '\033[1;97m'


def printerror(message):
  print('\033[1;41mERROR\033[0m \033[91m' + message + '\033[0m')


def printwarning(message):
  print('\033[1;43mWARNING\033[0m \033[93m' + message + '\033[0m')


def GetEntries(trees, treeName = 'Events', verbose = False):
    while '  ' in trees: trees = trees.replace('  ', ' ')
    treelist = []
    if ' ' in trees: treelist = trees.split(' ')
    else: treelist.append(trees)
    
    c = r.TChain(treeName, treeName)
    for t in treelist:
        if "" == t: continue
        if verbose: print("\t- Adding", t)
        c.Add(t)
    return c.GetEntries()


def hadd(rootfiles, outname, index, outdir, totsize = None, pretend = False, force = False, verbose = False):
    if not os.path.isdir(outdir):
        os.system("mkdir -p " + outdir)
    
    out = outdir + outname + '_' + str(index) + '.root'
    inp = ''
    for f in rootfiles: inp += f + ' '
    if len(rootfiles) == 1:
        command = 'cp ' + inp + ' ' + out
        if verbose >= 1: printwarning('Only one file! Using cp instead of haddnano.py...')
    else:
        command = 'python3 {src}/src/PhysicsTools/NanoAODTools/scripts/haddnano.py {o} {i}'.format(src = os.environ['CMSSW_BASE'],
                                                                                              o   = out,
                                                                                              i   = inp) # -ff -O
    
    if verbose >= 1: print(' >> ' + pcol.green + 'Hadding ', len(rootfiles), ' files into ' + pcol.red , out + (" " + pcol.white + 'Total: %1.0f MB' %(totsize)) * (isinstance(totsize, float)) + pcol.end)
    
    #print '    ' + pcol.red + command + pcol.end
    
    if os.path.isfile(out):
        if verbose >= 1: printwarning('The output file already exists!: ' + out)
        if verbose >= 1: print(pcol.red + 'Skipping...' + pcol.end)
        print("# Checking " + out)
        iEntries = GetEntries(inp, verbose = verbose)
        oEntries = GetEntries(out, verbose = verbose)
        if iEntries != oEntries:
            printerror('NOT SAME NUMBER OF ENTRIES IN INPUT (%i) AND OUTPUT (%i)'%(iEntries, oEntries))
        else: print(pcol.green + 'GOOD!' + pcol.end)
        return
    if not pretend: 
        os.system(command)
        iEntries = GetEntries(inp, verbose = verbose)
        oEntries = GetEntries(out, verbose = verbose)
        if iEntries != oEntries:
            printerror('NOT SAME NUMBER OF ENTRIES IN INPUT (%i) AND OUTPUT (%i)'%(iEntries, oEntries))
    elif verbose:
        print(" >> You would have executed:", pcol.white + command + pcol.end)
    return


def sortByiF(fnam):
    if "_Skim" in fnam:
        fnam = fnam.replace("_Skim", "")
    return int(fnam.split("/")[-1].split(".root")[0].split("_")[-1])


def haddtrees(dirname, outname, outdir, maxsize = 5000., pretend = False, verbose = 1):
    if not outdir[-1] == '/': outdir += '/'
    index     = 0
    thefiles  = []
    rootfiles = []
    size      = 0.
    if outname[-5:] == '.root':
        outname = outname[:-5]
    
    if verbose >= 1: print('Looking into: ', dirname)
    
    for path, subdirs, files in os.walk(dirname):
        for name in files:
            if name[-5:] != '.root': continue
            thefiles.append(path + '/' + name)
    
    thefiles.sort(key = sortByiF)
    
    for iF in thefiles:
        out   = float(os.path.getsize(iF))/1000000. 
        size  += out
        
        if size < maxsize and len(rootfiles) < 700: 
            if verbose >= 1: print('Adding ' + pcol.orange + iF.split("/")[-1] + pcol.end + ' (' + pcol.cyan + '%1.0f MB' %(out) + pcol.end + '). ' + pcol.white + 'Total: %1.0f MB' %(size) + pcol.end)
            rootfiles.append(iF)
        else:
            hadd(rootfiles, outname, index, outdir, size, pretend)
            index += 1
            rootfiles = []
            size      = out
            if verbose >= 1: print('Adding ' + pcol.orange + iF.split("/")[-1] + pcol.end + ' (' + pcol.cyan + '%1.0f MB' %(out) + pcol.end + '). ' + pcol.white + 'Total: %1.0f MB' %(size) + pcol.end)
            rootfiles.append(iF)

    if   len(rootfiles) == 0:
        printerror('Files not found!')
    else:
        hadd(rootfiles, outname, index, outdir, size, pretend)
        index += 1
    
    return


def GetSampleListInDir(dirname):
    listofsamples = []
    for s in os.listdir(dirname):
        if not s[-5:] == '.root': continue
        s = s[:-5]
        digit = ''
        while s[-1].isdigit(): 
            digit = digit + s[-1]
            s = s[:-1]
        if(len(digit)) > 0 and s[-1] == '_': s = s[:-1]
        else: s += digit
        if not s in listofsamples: listofsamples.append(s)
    return sorted(listofsamples)


def CraftSampleName(name):
    # Deal with 'ext' in the end
    #if   'ext' in name[-3:]: name = name[:-3] + '_' + name[-3:]
    #elif 'ext' in name[-4:]: name = name[:-4] + '_' + name[-4:]
    
    # Rename bits...
#    name = name.replace('madgraphMLM', 'MLM')
#    name = name.replace('ST_tW_top', 'tW')
#    name = name.replace('ST_tW_antitop', 'tbarW')
#    name = name.replace('NoFullyHadronicDecays', 'noFullHad')

    # Delete bits...
#    deleteWords = ['13TeV', 'powheg', 'Powheg', 'pythia8']
    deleteWords = ['MiniAODv2', "RunIISummer20UL16NanoAODv9", "106X", "mcRun2", "asymptotic",
                    "upgrade2018", "RunIISummer20UL18NanoAODv9", "mc2017",
                   "RunIISummer20UL16NanoAODAPVv9", "preVFP", "RunIISummer20UL17NanoAODv9", "realistic"]
    s = name.replace('-', '_').replace("/", "_").split('_')
    a = ''
    for bit in s:
        if bit in deleteWords: continue
        else: a += '_' + bit
    if a.startswith('_'): a = a[1:]
    if a.endswith('_')  : a = a[:-1]
    a = a.replace("/", "_")
    while '__' in a: a = a.replace('__', '_')
    return a


def GetSamplesForHadding(thef, outdirname, verbose = True):
    dirnames    = []
    samplenames = []
    
    for path, subdirs, _ in os.walk(thef):
#        print path, subdirs
        for treeName in subdirs:
            
            if treeName == outdirname: continue
            for spath, ssubdirs, _ in os.walk(thef + "/" + treeName):
                dirName    = spath + '/' 
                sampleName = CraftSampleName(treeName + "/" )
                dirnames.append(dirName)
                samplenames.append(sampleName)
                    
                if verbose >= 1: print(' >> Found sample: ' + pcol.red + treeName + pcol.white + ' (' + pcol.cyan + sampleName + pcol.white + ')' + pcol.end)
                break
        break
    return [dirnames, samplenames]


def haddThoseDatasets(inf, outdirname, pretend = False, maxSize = 5000., verbose = False, removeInfolder=False):
    dirnames, samplenames = GetSamplesForHadding(inf, outdirname, verbose)
#    sys.exit()
    if not pretend:
        if verbose >= 1: print(pcol.red + ' STARTING...' + pcol.end)
    else:
        if verbose >= 1: print(pcol.red + ' PRETENDING...' + pcol.end)
#    print dirnames, "\n", samplenames

    for i in range(len(dirnames)): haddtrees(dirnames[i], samplenames[i], inf + "/" + outdirname, maxSize, pretend, verbose)
    if verbose:
        print("> Samples that have been merged:")
        for el in samplenames: print(el)
    
    if removeInfolder:
        for el in dirnames:
            os.system("rm " + el + "/" + "*.root")
            os.system("rmdir " + el)
    
    return


##########################################################################
##########################################################################
parser = argparse.ArgumentParser(description='Check trees')
parser.add_argument('--infolder', '-i', required = True,         help = 'Path to the folder')
parser.add_argument('--verbose',  '-v', action  = 'store_true',  help = 'Activate the verbosing')
parser.add_argument('--pretend',  '-p', action  = 'store_true',  help = 'Pretend')
parser.add_argument('--outname',  '-o', default = 'mergedFiles', help = 'Output name')
parser.add_argument('--maxSize',  '-s', default = 500.,         help = 'Maximum input size of the chunks to merge (in bytes)')
parser.add_argument('--removeInfolder',  '-rm', action  = 'store_true',         help = 'Remove the folders with the unmerged files')

args = parser.parse_args()

infolder   = args.infolder
verbose    = args.verbose
pretend    = args.pretend
outname    = args.outname
maxSize    = float(args.maxSize)
removeInfolder = args.removeInfolder


haddThoseDatasets(infolder, outname, pretend, maxSize, verbose, removeInfolder)
   
