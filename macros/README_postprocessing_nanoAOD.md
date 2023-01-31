# NanoAOD postprocessing instructions
Here follow indications on how to use these scripts to postprocess nanoAOD taking advantage of central tools.

### Installation and setup (fanae)
In a **clean** terminal (and the folder of your choice), do the following to install the necessary code. Please have in your .globus folder the necessary certificate.

```
grid
source /cms/cmsset_default.sh

cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src/

cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --hours 96

git clone https://github.com/vrbouza/nanoAOD-tools.git PhysicsTools/NanoAODTools -b master_uniovi # to be changed in the future

scram b
```

Once installed, only these commands are necessary to submit CRAB tasks:

```
cd CMSSW_10_2_22/src/

grid
source /cms/cmsset_default.sh
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init --voms cms --hours 96
```

### Execution (fanae)
Everything happens inside the PhysicsTools/NanoAODTools/macros folder. The driving script is postprocCRABSub.py . Use the --help argument to get all the possible options. To send crab jobs for a dataset file in the dataset folder you can simply use the following command. Please, note that you must have in your output storage a folder named nanoAOD_postprocessing!

```
python postprocCRABSub.py --prodName NAMING ./datasets/FILE.txt
```

This will start launching tasks to the LCG. By default, the user is set to be "rodrigvi", but you can change it with the -u USER argument:

```
python postprocCRABSub.py --prodName NAMING ./datasets/FILE.txt -u CERNUSERNAME
```

### Production checks while executing
As CRAB and Grafana are not very *helpful* sometimes, a specific Python tool, checkcrab.py, has been developed to cope with different (most probably not all) CRAB errors and problems and to provide a more credible status report than Grafana usually does.

Once you have your production ongoing, you can check its status using this tool as follows (inside the *test* folder).
```
python checkcrab.py WORKAREA NCORES
```
WORKAREA refers to the work area of your crab tasks (created as *temp_postproc_* + *productiontag*, where *productiontag* is set with the --prodName argument in the postprocCRABSub.py script) and is a compulsory argument, whereas NCORES refers to the same as before, and is optional.

NOTE: sometimes, inside each CRAB task, some jobs might fail due to not having enough time to completely execute. When running checkcrab, these jobs will be indeed detected and you will be asked whether you want to resubmit those jobs or not. However, at this moment, the script does not detect the error itself and it performs a "pure" resubmit. This will  be included in the future into the script, but to succesfully execute those tasks, you should do manually a resubmit with the --maxjobruntime option, setting for example --maxjobruntime 2000.

NOTE2: currently, the re-launching feature is DISABLED.

NOTE3: currently, the data-fetching from crab status might have some errors. This will be fixed.


### Production checks after executing: TO BE REVIEWED, DO NOT READ YET, NOR USE!
Once your execution finishes, the script nanoAOD_checker.py allows you to check all produced datasets by first comparing the number of files that are produced with the number of files that are of MINIAOD, and second, by checking that the number of produced events is the same as the total number of events of the MINIAOD.

To use it, you should, in your storage site, establish any CMSSW-supported area, as well as the necessary CRAB & GRID environment and then copy the nanoAOD_checker.py script to the folder where all the production is stored (i.e. the folder named after the "name" variable in the multicrab.py script). Or, you can put it anywhere and then use the --folder (or -f) option to execute it. Then, simply do the following.
```
python nanoAOD_checker.py -n NCORES
```
This will start checking all the datasets in that folder. It is highly recommended to parallelise it, as it needs to loop over **all the files for each dataset**. The result is given at the end. You can set the debug option to true or false inside to get more or less logging.


