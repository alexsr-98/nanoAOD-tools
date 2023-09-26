import glob

nanoPath = "/beegfs/data/nanoAODv11/30march2023/MC/2022PostEE/"

samples = {
#-------ttbar-------# | NLO Powheg+Pythia8 
  # Dileptonic
"ttbar_dileptonic" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : True, # split the sample for train and signal extraction
},
  # Semileptonic
"ttbar_semileptonic" : {
  "xsec": 403.2549,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : True, # split the sample for train and signal extraction
},  
  # Uncertainties
"ttbar_UEup" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_TuneCP5Up_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_TuneCP5Up_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_UEdown" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_TuneCP5Down_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_TuneCP5Down_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_Hdampup" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_Hdamp-418_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_Hdamp-418_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_Hdampdown" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_Hdamp-158_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_Hdamp-158_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_CR1" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_TuneCP5CR1_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_TuneCP5CR1_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_CR2" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_TuneCP5CR2_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_TuneCP5CR2_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_ERDOn" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_TuneCP5_ERDOn_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_TuneCP5_ERDOn_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_mtopdown" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_MT-171p5_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_MT-171p5_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"ttbar_mtopup" : {
  "xsec": 97.4488,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTto2L2Nu_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTto2L2Nu_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
#-------tW-------# | NLO DR
# - SMP samples - #
#"tw_minus" : {
#  "xsec": 23.8979,
#  "year": "2022PostEE",
#  "files": glob.glob(nanoPath + "TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
#  "isData": False,
#  "name" : "TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
#  "split" : True, # split the sample for train and signal extraction
#},
#"tw_plus" : {
#  "xsec": 23.8979,
#  "year": "2022PostEE",
#  "files": glob.glob(nanoPath + "TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
#  "isData": False,
#  "name" : "TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
#  "split" : True, # split the sample for train and signal extraction
#},
# - GEN samples - #
"tw_minus_dilep" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : True, # split the sample for train and signal extraction
},
"tw_plus_dilep" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : True, # split the sample for train and signal extraction
},
"tw_minus_semilep" : {
  "xsec": 19.2468,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_semilep" : {
  "xsec": 19.2468,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
  # Uncertainties
"tw_minus_dilep_ERDOn" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_TuneCP5_ERDOn_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_TuneCP5_ERDOn_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_ERDOn" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_TuneCP5_ERDOn_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_TuneCP5_ERDOn_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_CR1" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_TuneCP5CR1_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_TuneCP5CR1_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_CR1" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_TuneCP5CR1_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_TuneCP5CR1_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_CR2" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_TuneCP5CR2_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_TuneCP5CR2_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_CR2" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_TuneCP5CR2_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_TuneCP5CR2_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_UEup" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_TuneCP5Up_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_TuneCP5Up_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_UEup" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_TuneCP5Up_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_TuneCP5Up_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_UEdown" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_TuneCP5Down_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_TuneCP5Down_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_UEdown" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_TuneCP5Down_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_TuneCP5Down_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_Hdampup" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_Hdamp-418_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_Hdamp-418_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_Hdampup" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_Hdamp-418_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_Hdamp-418_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_Hdampdown" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_Hdamp-158_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_Hdamp-158_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_Hdampdown" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_Hdamp-158_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_Hdamp-158_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_mtopup" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_mtopup" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_MT-173p5_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_mtopdown" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_MT-171p5_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_MT-171p5_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_mtopdown" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_MT-171p5_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_MT-171p5_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_minus_dilep_ds" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWminusto2L2Nu_DS_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWminusto2L2Nu_DS_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_plus_dilep_ds" : {
  "xsec": 4.6511,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TbarWplusto2L2Nu_DS_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TbarWplusto2L2Nu_DS_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
# - Samples for differential - #
"tw_amcDR1_dilep" : {
  "xsec": 4.6511*2,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWto2L2Nu-DR1_TuneCP5_13p6TeV_amcatnlo-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWto2L2Nu-DR1_TuneCP5_13p6TeV_amcatnlo-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_amcDR2_dilep" : {
  "xsec": 4.6511*2,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWto2L2Nu-DR2_TuneCP5_13p6TeV_amcatnlo-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWto2L2Nu-DR2_TuneCP5_13p6TeV_amcatnlo-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_amcDSFSBW_dilep" : {
  "xsec": 4.6511*2,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWto2L2Nu-DS-FS-BW_TuneCP5_13p6TeV_amcatnlo-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWto2L2Nu-DS-FS-BW_TuneCP5_13p6TeV_amcatnlo-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_amcDSFS_dilep" : {
  "xsec": 4.6511*2,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWto2L2Nu-DS-FS_TuneCP5_13p6TeV_amcatnlo-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWto2L2Nu-DS-FS_TuneCP5_13p6TeV_amcatnlo-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_amcDSIS_dilep" : {
  "xsec": 4.6511*2,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWto2L2Nu-DS-IS_TuneCP5_13p6TeV_amcatnlo-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWto2L2Nu-DS-IS_TuneCP5_13p6TeV_amcatnlo-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"tw_amcDSISBW_dilep" : {
  "xsec": 4.6511*2,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TWto2L2Nu-DS-IS-BW_TuneCP5_13p6TeV_amcatnlo-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TWto2L2Nu-DS-IS-BW_TuneCP5_13p6TeV_amcatnlo-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},


#-------Wjets-------#
  # NLO
"wjets_LNu" : { 
  "xsec": 64481.58,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},

#-------DY-------#
  # LO
"dy_M10to50_2Jets" : { 
  "xsec": 19982.5,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8", #name for the output files
  "split" : True, # split the sample for train and signal extraction
},
"dy_M50_2Jets" : {
  "xsec": 6345.99,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8", #name for the output files
  "split" : True, # split the sample for train and signal extraction
},       

#-------WW-------#
# LO
#"ww" : {
#  "xsec": 116.8,
#  "year": "2022PostEE",
#  "files": glob.glob(nanoPath + "WW_TuneCP5_13p6TeV_pythia8/*/*/*/*root"),
#  "isData": False,
#  "name" : "WW_TuneCP5_13p6TeV_pythia8", #name for the output files
#  "split" : False, # split the sample for train and signal extraction
#},
# NLO
"ww_2l2nu" : {
  "xsec": 12.98,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},

#-------WZ-------#
# LO
#"wz" : {
#  "xsec": 54.2776,
#  "year": "2022PostEE",
#  "files": glob.glob(nanoPath + "WZ_TuneCP5_13p6TeV_pythia8/*/*/*/*root"),
#  "isData": False,
#  "name" : "WZ_TuneCP5_13p6TeV_pythia8", #name for the output files
#  "split" : False, # split the sample for train and signal extraction
#},
# NLO
"wz_2l2q" : {
  "xsec": 8.17,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"wz_3lnu" : {
  "xsec": 5.31,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
#-------ZZ-------#
# LO
#"zz" : {   #### WARNING: USING NOT POSTEE SAMPLE
#  "xsec": 16.7,
#  "year": "2022PostEE",
#  "files": glob.glob("/beegfs/data/nanoAODv11/30march2023/MC/2022/ZZ_TuneCP5_13p6TeV_pythia8/mcRun3_2022_april2023_ZZ_TuneCP5_13p6TeV_pythia8/230417_084416/*/*root"),
#  "isData": False,
#  "name" : "ZZ_TuneCP5_13p6TeV-pythia8", #name for the output files
#  "split" : False, # split the sample for train and signal extraction
#},
# NLO
"zz_4l" : {
  "xsec": 1.65,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "ZZto4L_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"zz_2l2q" : {
  "xsec": 8.08,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
"zz_2l2nu" : {
  "xsec": 1.19,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
    ##### ttW

    ##### ttZ
"ttz_ztoqq" : {
  "xsec": 0.6209,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "TTZ-ZtoQQ-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/*/*/*/*root"),
  "isData": False,
  "name" : "TTZ-ZtoQQ-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8", #name for the output files
  "split" : False, # split the sample for train and signal extraction
},
    ###### ttGamma (UL)
#"ttgamma_semilep" : {   #### WARNING: USING NOT POSTEE SAMPLE
#  "xsec": 5.6265, # Scalateed from ttbar xsec
#  "year": "2022PostEE",
#  "files": glob.glob("/pool/phedex/userstorage/asoto/ULSamples_tWRun3/TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/mcRun3_PostEE_april2023_TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/*/*/*root"),
#  "isData": False,
#  "name" : "TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8", #name for the output files
#  "split" : False, # split the sample for train and signal extraction
#},
#"ttgamma_dilep" : {   #### WARNING: USING NOT POSTEE SAMPLE
#  "xsec": 1.6558,
#  "year": "2022PostEE",
#  "files": glob.glob("/pool/phedexrw/userstorage/asoto/ULSamples_tWRun3/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/mcRun3_PostEE_april2023_TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/*/*/*root"),
#  "isData": False,
#  "name" : "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8", #name for the output files
#  "split" : False, # split the sample for train and signal extraction
#},

    ###### VVV
}