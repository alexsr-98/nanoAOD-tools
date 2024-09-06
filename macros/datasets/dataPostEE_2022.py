import glob

nanoPath = "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/"

samples = {
#-------Muon-------# 
"muon_Run2022E" : {
  "xsec": 5.8783,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "Muon/dataRun3_2022_oct2023_Muon_Run2022E-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022E", #name for the output files
},
"muon_Run2022F" : {
  "xsec": 18.007,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "Muon/dataRun3_PostEE_oct2023_Muon_Run2022F-22Sep2023-v2/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022F", #name for the output files
},    
"muon_Run2022G" : {
  "xsec": 3.1219,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "Muon/dataRun3_PostEE_oct2023_Muon_Run2022G-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022G", #name for the output files
}, 

#-------EGamma-------#  
"eGamma_Run2022E" : {
  "xsec": 5.8783,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_2022_oct2023_EGamma_Run2022E-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022E", #name for the output files
},
"eGamma_Run2022F" : {
  "xsec": 18.007,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_PostEE_oct2023_EGamma_Run2022F-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022F", #name for the output files
},
"eGamma_Run2022G" : {
  "xsec": 3.1219,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_PostEE_oct2023_EGamma_Run2022G-22Sep2023-v2/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022G", #name for the output files
},

#-------MuonEG-------# 
"muonEG_Run2022E" : {
  "xsec": 5.8783,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_2022_oct2023_MuonEG_Run2022E-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022E", #name for the output files
},
"muonEG_Run2022F" : {
  "xsec": 18.007,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_PostEE_oct2023_MuonEG_Run2022F-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022F", #name for the output files
},
"muonEG_Run2022G" : {
  "xsec": 3.1219,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_PostEE_oct2023_MuonEG_Run2022G-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022G", #name for the output files
},

#-------JetMET-------# 
"jetMET_Run2022E" : {
  "xsec": 5.8783,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_2022_oct2023_JetMET_Run2022E-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022E", #name for the output files
},
"jetMET_Run2022F" : {
  "xsec": 18.007,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_PostEE_oct2023_JetMET_Run2022F-22Sep2023-v2/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022F", #name for the output files
},
"jetMET_Run2022G" : {
  "xsec": 3.1219,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_PostEE_oct2023_JetMET_Run2022G-22Sep2023-v2/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022G", #name for the output files
},
}
