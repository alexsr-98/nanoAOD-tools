import os, sys, argparse
import ROOT
from postProcessHelper import command, slurmscaff, logPath, jobName

'''
This script reads the output of postprocess and check that the number of input files is the same as the number of output files
'''

def confirm(dontAsk = False):
    '''
    Ask for confirmation before submitting
    '''
    if dontAsk:
        return True
    confirm = input("Are you sure you want to submit? [y/n] ")
    if confirm == "y":
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "python postProcessHelper.py [options]", description = "Script to postProcess nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file',     '-f', metavar = 'file',     dest = "file",   required = True, default = "")
    parser.add_argument('--output',     '-o', metavar = 'output',     dest = "output",   required = True, default = "")
    parser.add_argument('--checkSkim' , '-cS', action = 'store_true'  , default = True, help = 'Check that the skim is done correctly, i.e that the number of output files is the same as input files')
    parser.add_argument('--checkZombies' , '-cZ', action = 'store_true'  , default = False, help = 'Check if there are zombie files') 
    parser.add_argument('--checkNanoMerger' , '-cN', action = 'store_true'  , default = False, help = 'Check that the merge is done correctly, i.e that the number of entries is the same before and after merge') 
    parser.add_argument('--queue',     '-q', metavar = 'queue',     dest = "queue",   required = False, default = "")
    parser.add_argument('--verbose' , '-v', action = 'store_true'  , help = 'Activate the verbosing') #### Not implemented



    args        = parser.parse_args()
    samplesFile = args.file
    output = args.output
    checkSkim = args.checkSkim
    checkZombies = args.checkZombies
    checkNanoMerger = args.checkNanoMerger
    queue = args.queue
    verbose = args.verbose

    
    if checkSkim:
        sys.path.append('./' + "datasets")  
        exec("from {samplesFile} import samples".format(samplesFile=samplesFile))

        for sample in samples:
            listName = [samples[sample]["name"]]
            files = samples[sample]["files"]
            isData = samples[sample]["isData"]
            year = samples[sample]["year"]
            xsec = samples[sample]["xsec"]
            try: 
                split = samples[sample]["split"]
            except:
                split = False
            if split:
                listName = [samples[sample]["name"] + "_analysis", samples[sample]["name"] + "_train"]
            for name in listName:
                # Now look in the output folder for the folder with name samples[sample]["name"]
                # and count the number of files
                # and compare with the number of files in the input folder
                # print if they are different or not
                submitAll = False # Submit all the files that are missing
                try:
                    # Look for .root files
                    outputAllFiles = os.listdir(output + name)
                except:
                    print("Folder not found: " + output + name)
                    continue
                outputRootFiles = [f for f in outputAllFiles if f.endswith(".root")]
    
                nInputFiles = len(files)
                nOutputFiles = len(outputRootFiles)

                outputFilesCompatibleName = [] # Name without the skim suffix to compare with the input files
                for file in outputRootFiles:
                    outputFilesCompatibleName.append(file.split("_Skim")[0] + ".root")
                
                if checkZombies:
                    # Check if there are zombie files
                    for file in outputRootFiles:
                        #print(output + name + "/" + file)
                        try:
                            f = ROOT.TFile.Open(output + name + "/" + file)
                        except:
                            print("\033[91m" + "Zombie file: " + file + "\033[0m")
                            # Remove the file
                            os.system("rm " + output + name + "/" + file)
                        # Get the Events tree and check if it is null
                        t = f.Get("Events")
                        if t == None:
                            print("\033[91m" + "Zombie file: " + file + "\033[0m")
                            # Remove the file
                            os.system("rm " + output + name + "/" + file)
                        f.Close()
                
                if nInputFiles != nOutputFiles:
                    # Print in color yellow the word WARNING and red the word different
                    print("\033[93m" + "WARNING" + "\033[0m" + " different number of input and output files for sample " + name)
                    print("Input files: " + str(nInputFiles))
                    print("Output files: " + str(nOutputFiles))
                    missingFiles = []
                    # Print the files that are missing
                    for file in files:
                        if file.split("/")[-1] not in outputFilesCompatibleName:
                            if verbose:
                                print("\033[91m" + "Missing file: " + file + "\033[0m")
                            missingFiles.append(file)
                    if len(missingFiles) > 0:
                        for file in missingFiles:
                            if not split:
                                formatedCommand = command.format(files = " -f " + file, name = samples[sample]["name"], isData = isData, year = year, xsec = xsec, outputPath = output, split = "''")
                                if verbose:
                                    print(formatedCommand)
                            else:
                                if "_train" in name:
                                    formatedCommand = command.format(files = " -f " + file, name = samples[sample]["name"], isData = isData, year = year, xsec = xsec, outputPath = output, split = "even")
                                    if verbose:
                                        print(formatedCommand)
                                elif "_analysis" in name:
                                    formatedCommand = command.format(files = " -f " + file, name = samples[sample]["name"], isData = isData, year = year, xsec = xsec, outputPath = output, split = "odd")
                                    if verbose:
                                        print(formatedCommand)
                                else:
                                    print("ERROR: file not found in train or analysis folder")

                            if queue != "":
                                if confirm(dontAsk = submitAll):
                                    os.system(slurmscaff.format(extraS = "", nth = 1, queue = queue, jobname = jobName, logpath = logPath.format(year = year), files = "_" + file.split("/")[-1].split(".")[0], command = formatedCommand))
                                    print(slurmscaff.format(extraS = "", nth = 1, queue = queue, jobname = jobName, logpath = logPath.format(year = year), files = "_" + file.split("/")[-1].split(".")[0], command = formatedCommand))
                                    submitAll = True
                            else:
                                if confirm(dontAsk = submitAll):
                                    os.system(formatedCommand)
                                    print(formatedCommand)
                                    submitAll = True


                else:
                    # Print in color green the word same
                    print("\033[92m" + "Same" + "\033[0m" + " number of input and output files for sample " + name)
                    print("Input files: " + str(nInputFiles))
                    print("Output files: " + str(nOutputFiles))
        
    if checkNanoMerger:
        outputFiles = []
        outputMergedFiles = []
        for root, dirs, files in os.walk(output):
            for file in files:
                if file.endswith(".root") and len(dirs) == 0:
                    outputFiles.append(os.path.join(root, file))
                elif file.endswith(".root") and len(dirs) > 0:
                    outputMergedFiles.append(os.path.join(root, file))
        
        nEntriesOutputFiles = 0
        nEntriesOutputMergedFiles = 0
        for file in outputFiles:
            # Open root file and get the number of entries
            f = ROOT.TFile.Open(file)
            t = f.Get("Events")
            nEntriesOutputFiles += t.GetEntries()
            f.Close()
        for file in outputMergedFiles:
            # Open root file and get the number of entries
            f = ROOT.TFile.Open(file)
            t = f.Get("Events")
            nEntriesOutputMergedFiles += t.GetEntries()
            f.Close()
        
        if nEntriesOutputFiles != nEntriesOutputMergedFiles:
            # Print in color yellow the word WARNING and red the word different
            print("\033[93m" + "WARNING" + "\033[0m" + " different number of entries before and after merge")
            print("Entries before merge: " + str(nEntriesOutputFiles))
            print("Entries after merge: " + str(nEntriesOutputMergedFiles))
            print("Difference: " + str(nEntriesOutputFiles - nEntriesOutputMergedFiles))
        else:
            # Print in color green the word same
            print("\033[92m" + "Same" + "\033[0m" + " number of entries before and after merge")
            print("Entries before merge: " + str(nEntriesOutputFiles))
            print("Entries after merge: " + str(nEntriesOutputMergedFiles))









