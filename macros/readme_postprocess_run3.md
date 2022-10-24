# Postprocess Run3

Last updated: **24 Oct 2022**

(Documentation work in progress)

List of important files:

 * postProcess_tWRun3.py: central script where the postprocessing is defined
 * postProcessHelper.py: helper to run the postProcess_tWRun3.py
 * datasets/mc_2022.py: mc samples
 * datasets/data_2022.py: data samples
 * nanoAOD_merger.py: merge the datasets

Steps to run the post processing:
 
 * python postProcessHelper.py -f mc_2022 -q batch -j 120
 * python nanoAOD_merger.py -i /pool/phedex/userstorage/asoto/Proyectos/tw_run3/productions/test/  -v -o ./ -rm 