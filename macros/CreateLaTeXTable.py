import os, sys, ast, argparse
import CentralSettings as cs
from multiprocessing import Pool

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


def GetEntriesDAS(tsk):
    sample, verbose, dbs = tsk
    dascommand = 'dasgoclient --query="summary dataset={s} {d}"'.format(s = sample,
                                                                        d = "" if not dbs else "instance=prod/phys03")
    if verbose: print '   - Looking for sample: ', sample
    out     = os.popen(dascommand).read()
    d       = ast.literal_eval(out)[0]
    nev     = d['nevents']
    nfiles  = d['nfiles']
    return '    {{{s}}} & {n} & {xs} \\\\'.format(s  = sample.replace("_", "\_"),
                                                  n  = nev,
                                                  xs = cs.xsecDictExtended[sample.split("/")[1]])


def WriteTable(thelist, outdir, outname):
    outtxt = """\\begin{tabular}{lcc}
    \hline Sample & Events & $\\sigma [pb]$ \\\\
    \\hline\n"""

    for el in thelist:
        outtxt += el + "\n"

    outtxt += """    \hline
\\end{tabular}"""

    with open(outdir + "/" + outname + ".tex", "w") as outF:
        outF.write(outtxt)
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get info from DAS')
    parser.add_argument('--verbose',   '-v', action  = 'store_true',  help = 'Activate the verbosing')
    parser.add_argument('--test',      '-t', action  = 'store_true',  help = 'Sends only one or two jobs, as a test')
    parser.add_argument('--outfolder', '-o', default = 'temp_tables', help = 'Directory where the output should be put')
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads'  ,  dest = "nthreads", required = False, default = 0, type = int)
    parser.add_argument('--dbs',       '-d', action  = 'store_true',  default = False, help = 'Use phys03 dbs.')
    parser.add_argument('dataset',           default = ''          ,  nargs='?', help = 'txt file with datasets')

    args = parser.parse_args()

    verbose   = args.verbose
    dataset   = args.dataset
    nthreads  = args.nthreads
    outfolder = args.outfolder
    dbs       = args.dbs
    tasks     = [ (el, verbose, dbs) for el in cs.ReadLines(dataset)]

    print "> Checking nevents and xsecs..."
    finalresults = []
    if nthreads > 1:
        pool = Pool(nthreads)
        finalresults = pool.map(GetEntriesDAS, tasks)
        pool.close()
        pool.join()
    else:
        for tsk in tasks:
            finalresults.append(GetEntriesDAS(tsk))

    if not os.path.isdir(outfolder):
        os.system("mkdir -p " + outfolder)

    print "> Writing LaTeX table..."
    WriteTable(finalresults, outfolder, dataset.split("/")[-1].replace(".txt", ""))
    print "> Done!"
