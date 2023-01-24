import os, sys, argparse

'''
This script reads the output of postprocess and check that the number of input files is the same as the number of output files
'''



if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "python postProcessHelper.py [options]", description = "Script to postProcess nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file',     '-f', metavar = 'file',     dest = "file",   required = True, default = "")
    parser.add_argument('--output',     '-o', metavar = 'output',     dest = "output",   required = True, default = "")

    args        = parser.parse_args()
    samplesFile = args.file
    output = args.output

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

            




