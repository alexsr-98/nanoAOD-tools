#!/usr/bin/env python
# This helper is intended to be used for postProcessing samples that are located in your machine locally not in DAS. For this reason it is better to not use crab
import os, sys, json, argparse
from math import ceil

#### Modify as you wish
production = "2023-12-23_temp"
outPath = "/lustrefs/hdd_pool_dir/nanoAODv12/tw-run3/productions/" + production + "/{year}/"
#outPath = "/pool/phedexrw/userstorage/asoto/Proyectos/tw_run3/productions/" + production + "/{year}/"
logPath = outPath + "logs/"
jobName = "postProcess_twRun3"
#######################

slurmscaff   = 'sbatch {extraS} -c {nth} -p {queue} -J {jobname} -e {logpath}/log{files}.%j.%x.err -o {logpath}/log{files}.%j.%x.out --wrap "{command}"'

command = 'python3 postProcess_tWRun3.py {files} -n {name} -y {year} -iD {isData} -xS {xsec} -o {outputPath} -s {split}'

def CheckPathDataset(path):
    ''' Check if the name exists in local folder or in dataset folder '''
    if (os.path.isfile("datasets/" + path + ".py")):
        return path
    else:
        return ''



if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "python postProcessHelper.py [options]", description = "Script to postProcess nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--verbose' , '-v', action = 'store_true'  , help = 'Activate the verbosing') #### Not implemented
    parser.add_argument('--pretend' , '-p', action = 'store_true'  , help = 'Create the files but not send the jobs') 
    parser.add_argument('--test'    , '-t', action = 'store_true'  , help = 'Sends only one or two jobs, as a test') #### Not implemented
    parser.add_argument('--file',     '-f', metavar = 'file',     dest = "file",   required = True, default = "")
    parser.add_argument('--queue',     '-q', metavar = 'queue',     dest = "queue",   required = False, default = "")
    parser.add_argument('--extraSlurmArgs','-eS',metavar='extraslurm',dest="extraslurm",required=False, default = "")
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads',  dest = "nthreads",required = False, default = 1, type = int)

    args        = parser.parse_args()
    verbose     = args.verbose
    doPretend   = args.pretend
    dotest      = args.test
    samplesFile = args.file
    queue = args.queue
    extraSlurmArgs = args.extraslurm
    nthreads = args.nthreads
    

    if CheckPathDataset(samplesFile) == '':
        raise RuntimeError("FATAL: .py samples file is not found")

    else:
        sys.path.append('./' + "datasets")
        exec("from {samplesFile} import samples".format(samplesFile=samplesFile))

    for sample in samples:
        # Extract sample info
        isData = samples[sample]["isData"]
        year = samples[sample]["year"]
        name = samples[sample]["name"]
        files = samples[sample]["files"]
        split = False
        if not isData:
            xsec = samples[sample]["xsec"]
            split = samples[sample]["split"]
        else:
            xsec = 0

        if dotest:
            files = [files[0]]

        # create the folders for each sample
        outPath = outPath.format(year = year)
        logPath = logPath.format(year = year)
        if not os.path.isdir(outPath) and not doPretend:
            os.system("mkdir -p " + outPath)
        if not os.path.isdir(logPath) and not doPretend:
            os.system("mkdir -p " + logPath)
        if not split:
            if not os.path.isdir(outPath + name) and not doPretend:
                os.system("mkdir -p " + outPath + name)
        else:
            if not os.path.isdir(outPath + name + "_train") and not doPretend:
                os.system("mkdir -p " + outPath + name + "_train")
            if not os.path.isdir(outPath + name + "_analysis") and not doPretend:
                os.system("mkdir -p " + outPath + name + "_analysis")
        
        # pararelise this
        numFiles = len(files)
        nthreads = args.nthreads # again to avoid problems
        if nthreads > numFiles:
            nthreads = numFiles
            print("WARNING: nthreads is greater than the number of files, nthreads will be set to the number of files")
        moduleJobs = int(numFiles % nthreads) # we want to distribute n files in m jobs, we can apply the formula: numFiles = ceilJobs * moduleJobs + (ceilJobs-1) * (nthreads-moduleJobs)
        ceilJobs = int(ceil(numFiles / float(nthreads)))
        counter = 0

        print("A total of %3d files will be submited" %numFiles)

        for job in range(1, nthreads+1):
            # create a string with all the files for argparse
            filesString = ''
            listFiles = '_'
            for file in files[counter:(counter+ceilJobs)]:
                filesString += " -f " + file
                listFiles += file.split("/")[-1].split(".")[0] + "_"

            if not split:
                formatedCommandList = [command.format(files = filesString, name = name, isData = isData, year = year, xsec = xsec, outputPath = outPath, split = "''")] 
            else:
                formatedCommandList = [command.format(files = filesString, name = name, isData = isData, year = year, xsec = xsec, outputPath = outPath, split ="even"),
                                   command.format(files = filesString, name = name, isData = isData, year = year, xsec = xsec, outputPath = outPath, split = "odd")]
                
            print("A total of %3d files will be sended in this job:" %len(files[counter:(counter+ceilJobs)]))
            
            for formatedCommand in formatedCommandList:
                if queue == "": # Run in local
                    print(formatedCommand)
                    if not doPretend:
                        os.system(formatedCommand)
                else: # Run in the cluster, at the moment the paralelisation is very simple: nthreads is the number of jobs submitted with 1 thread (notice the nth = 1 in the formula)
                    slurmscaffFormated = slurmscaff.format(extraS = extraSlurmArgs, nth = 1, queue = queue, jobname = jobName, logpath = logPath, files=listFiles, command = formatedCommand)
                    print(slurmscaffFormated)
                    if not doPretend:
                        os.system(slurmscaffFormated)
            
            if job == moduleJobs:
                ceilJobs = ceilJobs - 1
            counter += ceilJobs

        if dotest:
            break