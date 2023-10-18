# Postprocess Run3

Last updated: **17 Apr 2023**

(Documentation work in progress)

The first step of postProcessing is done via crab with this branch:
   * (Run3XuanPostProc)[https://github.com/alexsr-98/nanoAOD-tools/tree/Run3XuanPostProc].

List of important files:

 * postProcess_tWRun3.py: central script where the postprocessing is defined
 * postProcessHelper.py: helper to run the postProcess_tWRun3.py
 * datasets/mc_2022.py: mc samples
 * datasets/data_2022.py: data samples
 * nanoAOD_merger.py: merge the datasets

Steps to run the post processing:
 
 * python postProcessHelper.py -f mcPostEE_2022 -q batch -j 120000
 * Note: always run: python problemChecker.py -f mcPostEE_2022 -o /beegfs/data/nanoAODv11/tw-run3/productions/2023-04-10/2022PostEE/
 * If you want to skip the merging step (not recommeded): python moveAndRename.py -i /beegfs/data/nanoAODv9/temp/postprocv10Run3/tw_run3/productions/2022-10-25/2022/

 * Before running this command check with pretend that everything is ok: NECESITO SOLUCIONAR POR QUE NO HACE CP CUANDO ME PASO DEL TAMANIO
    python nanoAOD_merger.py -i /beegfs/data/nanoAODv11/tw-run3/productions/2023-05-29/2022PostEE/  -v -o ./ -s 10000 &> mergeLog.txt
 * After running this command, check that the number of entries is the same and then rm:
    python problemChecker.py -f data_2022 -o /beegfs/data/nanoAODv9/temp/postprocv10Run3/tw_run3/productions/2023-01-24_forData_removeLater/2022/ -cN

 Important things to take into account:

 * Always review that the correct json file is being used.

**Note:** if crab is used to process nanoAOD always run `fileBased` splitting.
