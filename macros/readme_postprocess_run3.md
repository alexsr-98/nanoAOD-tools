# Postprocess Run3

Last updated: **21 Nov 2022**

(Documentation work in progress)

List of important files:

 * postProcess_tWRun3.py: central script where the postprocessing is defined
 * postProcessHelper.py: helper to run the postProcess_tWRun3.py
 * datasets/mc_2022.py: mc samples
 * datasets/data_2022.py: data samples
 * nanoAOD_merger.py: merge the datasets

Steps to run the post processing:
 
 * python postProcessHelper.py -f mc_2022 -q batch -j 120
 * Note: always run: python problemChecker.py -f data_2022 -o /beegfs/data/nanoAODv9/temp/postprocv10Run3/tw_run3/productions/2023-01-24_forData_removeLater/2022/
 * Before running this command check with pretend that everything is ok: 
    python nanoAOD_merger.py -i /beegfs/data/nanoAODv9/temp/postprocv10Run3/tw_run3/productions/2022-10-25/2022/  -v -o ./ 
 * After running this command, check that the number of entries is the same and then rm:
    python problemChecker.py -f data_2022 -o /beegfs/data/nanoAODv9/temp/postprocv10Run3/tw_run3/productions/2023-01-24_forData_removeLater/2022/ -cN

 Important things to take into account:

 * Always review that the correct json file is being used.