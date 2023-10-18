import os, sys, argparse
sys.path.append('./' + "datasets")

datasetInfo = {
    "mcPostEE_2022"   : "/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/NANOAODSIM",
    "dataPostEE_2022" : {"F" : "/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD", 
                         "G" : "/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD"},
}
    
systematicsStrings = ["TuneCP5_ERDOn", "TuneCP5CR1", "TuneCP5CR2", "TuneCP5Up", "TuneCP5Down", "Hdamp", "MT-17", "DS_TuneCP5"]

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage = "python postProcessHelper.py [options]", description = "Script to postProcess nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file',     '-f', metavar = 'file',     dest = "file",   required = True, default = "")

    args        = parser.parse_args()
    samplesFile = args.file
    exec("from {samplesFile} import samples".format(samplesFile=samplesFile))
    # Create the latex table header
    latexmc_table = "\\begin{tabular}{|c|c|}\n\\hline\nDataset Name & Cross Section (pb) \\\\\n\\hline\n"
    latexdata_table = "\\begin{tabular}{|c|c|}\n\\hline\nDataset Name & Luminosity (\invfb) \\\\\n\\hline\n"
    latexsyst_table = "\\begin{tabular}{|c|c|}\n\\hline\nDataset Name & Cross Section (pb) \\\\\n\\hline\n"
    latexmctrain_table = "\\begin{tabular}{|c|c|}\n\\hline\nDataset Name & Cross Section (pb) \\\\\n\\hline\n"
    # First, order the dictionary into a list by the xsec (higher first)
    samples = sorted(samples.items(), key=lambda x: x[1]['xsec'], reverse=True)
    # Order the ones with the same cross section by name
    samples = sorted(samples, key=lambda x: x[1]['name'])
    # Loop through each dictionary and extract the dataset name and cross section
    isData = False
    if "data" in samplesFile.lower():
        isData = True
    for sample in samples:
        if isData:
            runLetter = sample[1]['name'].split("Run2022")[1]
            dataset_name = (sample[1]['name'] + datasetInfo[samplesFile][runLetter]).replace("_","\_")
        else:
            dataset_name = (sample[1]['name'] + datasetInfo[samplesFile]).replace("_","\_") #### NOTE: the index [0] is the key and [1] is the value
        cross_section = sample[1]['xsec']

        if isData:
            latexdata_table += "{dataset_name} & {luminosity} \\\\\n".format(dataset_name=dataset_name, luminosity=cross_section)
        else:    
            if len([s for s in systematicsStrings if s in sample[1]["name"]]) == 0:
                latexmc_table += "{dataset_name} & {cross_section} \\\\\n".format(dataset_name=dataset_name, cross_section=cross_section)
                if sample[1]["split"]:
                    latexmctrain_table += "{dataset_name} & {cross_section} \\\\\n".format(dataset_name=dataset_name, cross_section=cross_section)
            else:
                latexsyst_table += "{dataset_name} & {cross_section} \\\\\n".format(dataset_name=dataset_name, cross_section=cross_section)
    # Create the latex table footer
    latexmc_table += "\\hline\n\\end{tabular}\n"
    latexdata_table += "\\hline\n\\end{tabular}\n"
    latexsyst_table += "\\hline\n\\end{tabular}\n"
    latexmctrain_table += "\\hline\n\\end{tabular}\n"
    
    # Save the table in the directory ./tablesAN
    if not os.path.exists("tablesAN"):
        os.makedirs("tablesAN")
    
    if isData:
        with open("tablesAN/{samplesFile}.tex".format(samplesFile=samplesFile), "w") as f:
            f.write(latexdata_table)    
            print("Created table: tablesAN/{samplesFile}.tex".format(samplesFile=samplesFile))
    else:
        with open("tablesAN/{samplesFile}.tex".format(samplesFile=samplesFile), "w") as f:
            f.write(latexmc_table)

        with open("tablesAN/{samplesFile}_syst.tex".format(samplesFile=samplesFile), "w") as f:
            f.write(latexsyst_table)

        with open("tablesAN/{samplesFile}_train.tex".format(samplesFile=samplesFile), "w") as f:
            f.write(latexmctrain_table)
        print("Created table: tablesAN/{samplesFile}.tex".format(samplesFile=samplesFile))
        print("Created table: tablesAN/{samplesFile}_syst.tex".format(samplesFile=samplesFile))
        print("Created table: tablesAN/{samplesFile}_train.tex".format(samplesFile=samplesFile))








