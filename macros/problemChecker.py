import os, sys, argparse
import ROOT

'''
This script reads the output of postprocess and check that the number of input files is the same as the number of output files
'''



if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "python postProcessHelper.py [options]", description = "Script to postProcess nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file',     '-f', metavar = 'file',     dest = "file",   required = True, default = "")
    parser.add_argument('--output',     '-o', metavar = 'output',     dest = "output",   required = True, default = "")
    parser.add_argument('--checkSkim' , '-cS', action = 'store_true'  , default = True, help = 'Check that the skim is done correctly, i.e that the number of output files is the same as input files') 
    parser.add_argument('--checkNanoMerger' , '-cN', action = 'store_true'  , default = False, help = 'Check that the merge is done correctly, i.e that the number of entries is the same before and after merge') 



    args        = parser.parse_args()
    samplesFile = args.file
    output = args.output
    checkSkim = args.checkSkim
    checkNanoMerger = args.checkNanoMerger

    
    if checkSkim:
        sys.path.append('./' + "datasets")  
        exec("from {samplesFile} import samples".format(samplesFile=samplesFile))

        for sample in samples:
            name = sample["name"]
            files = sample["files"]
            # Now look in the output folder for the folder with name sample["name"]
            # and count the number of files
            # and compare with the number of files in the input folder
            # print if they are different or not
            try:
                # Look for .root files
                outputAllFiles = os.listdir(output + name)
            except:
                print("Folder not found: " + output + name)
                continue
            outputRootFiles = [f for f in outputAllFiles if f.endswith(".root")]

            nInputFiles = len(files)
            nOutputFiles = len(outputRootFiles)

            if nInputFiles != nOutputFiles:
                # Print in color yellow the word WARNING and red the word different
                print("\033[93m" + "WARNING" + "\033[0m" + " different number of input and output files for sample " + name)
                print("Input files: " + str(nInputFiles))
                print("Output files: " + str(nOutputFiles))
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









