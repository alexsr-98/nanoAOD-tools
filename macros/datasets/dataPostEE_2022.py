import glob

nanoPath = "/lustrefs/hdd_pool_dir/nanoAODv11/30march2023/data/2022PostEE/"

samples = {
#-------DoubleMuon-------# 

#-------SingleMuon-------# 

#-------Muon-------# 
##muon_Run2022E = {
##  "xsec": 1.0,
##  "year": "2022PostEE",
##  "files": glob.glob(nanoPath + "Muon/31oct2022_Muon_Run2022E-PromptNanoAODv10_v1-v3/*/*/*root"),
##  "isData": True,
##  "name" : "Muon_Run2022E", #name for the output files
##}
"muon_Run2022F" : {
  "xsec": 17.610,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "Muon/dataRun3_PostEE_april2023_Muon_Run2022F-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022F", #name for the output files
},    
"muon_Run2022G" : {
  "xsec": 3.055,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "Muon/dataRun3_PostEE_april2023_Muon_Run2022G-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022G", #name for the output files
}, 

#-------EGamma-------#  
##eGamma_Run2022E = {
##  "xsec": 1.0,
##  "year": "2022PostEE",
##  "files": glob.glob(nanoPath + "EGamma/data22EF_26oct2022_EGamma_Run2022E-PromptNanoAODv10_v1-v2/*/*/*root"),
##  "isData": True,
##  "name" : "EGamma_Run2022E", #name for the output files
##}
"eGamma_Run2022F" : {
  "xsec": 17.610,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_PostEE_april2023_EGamma_Run2022F-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022F", #name for the output files
},
"eGamma_Run2022G" : {
  "xsec": 3.055,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_PostEE_april2023_EGamma_Run2022G-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022G", #name for the output files
},

#-------MuonEG-------# 
##muonEG_Run2022E = {
##  "xsec": 1.0,
##  "year": "2022PostEE",
##  "files": glob.glob(nanoPath + "MuonEG/31oct2022_MuonEG_Run2022E-PromptNanoAODv10_v1-v3/*/*/*root"),
##  "isData": True,
##  "name" : "MuonEG_Run2022E", #name for the output files
##}
"muonEG_Run2022F" : {
  "xsec": 17.610,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_PostEE_april2023_MuonEG_Run2022F-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022F", #name for the output files
},
"muonEG_Run2022G" : {
  "xsec": 3.055,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_PostEE_april2023_MuonEG_Run2022G-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022G", #name for the output files
},

#-------JetMET-------# 
##jetMET_Run2022E = {
##  "xsec": 1.0,
##  "year": "2022PostEE",
##  "files": glob.glob(nanoPath + "JetMET/31oct2022_MuonEG_Run2022E-PromptNanoAODv10_v1-v3/*/*/*root"),
##  "isData": True,
##  "name" : "MuonEG_Run2022E", #name for the output files
##}
"jetMET_Run2022F" : {
  "xsec": 17.610,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_PostEE_april2023_JetMET_Run2022F-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022F", #name for the output files
},
"jetMET_Run2022G" : {
  "xsec": 3.055,
  "year": "2022PostEE",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_PostEE_april2023_JetMET_Run2022G-PromptNanoAODv11_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022G", #name for the output files
},
}
