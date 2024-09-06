import glob

nanoPath = "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/"

samples = {
#-------DoubleMuon-------# 
"doublemuon_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "DoubleMuon/dataRun3_2022_oct2023_DoubleMuon_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "DoubleMuon_Run2022C", #name for the output files
},  
#-------SingleMuon-------# 
"singlemuon_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "SingleMuon/dataRun3_2022_oct2023_SingleMuon_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "SingleMuon_Run2022C", #name for the output files
},  
#-------Muon-------# 
"muon_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "Muon/dataRun3_2022_oct2023_Muon_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022C", #name for the output files
},
"muon_Run2022D" : {
  "xsec": 3.0063,
  "year": "2022",
  "files": glob.glob(nanoPath + "Muon/dataRun3_2022_oct2023_Muon_Run2022D-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022D", #name for the output files
},    

#-------EGamma-------#  
"eGamma_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_2022_oct2023_EGamma_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022C", #name for the output files
},
"eGamma_Run2022D" : {
  "xsec": 3.0063,
  "year": "2022",
  "files": glob.glob(nanoPath + "EGamma/dataRun3_2022_oct2023_EGamma_Run2022D-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022D", #name for the output files
},

#-------MuonEG-------# 
"muonEG_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_2022_oct2023_MuonEG_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022C", #name for the output files
},
"muonEG_Run2022D" : {
  "xsec": 3.0063,
  "year": "2022",
  "files": glob.glob(nanoPath + "MuonEG/dataRun3_2022_oct2023_MuonEG_Run2022D-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022D", #name for the output files
},

#-------JetHT-------#
#"jetHT_Run2022C" : {
#  "xsec": 5.0707,
#  "year": "2022",
#  "files": glob.glob(nanoPath + "JetHT/dataRun3_2022_oct2023_JetHT_Run2022C-22Sep2023-v1/*/*/*root"),
#  "isData": True,
#  "name" : "JetHT_Run2022C", #name for the output files
#},
#-------MET-------# 
"MET_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "MET/dataRun3_2022_oct2023_MET_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "MET_Run2022C", #name for the output files
},
#-------JetMET-------# 
"jetMET_Run2022C" : {
  "xsec": 5.0707,
  "year": "2022",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_2022_oct2023_JetMET_Run2022C-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022C", #name for the output files
},
"jetMET_Run2022D" : {
  "xsec": 3.0063,
  "year": "2022",
  "files": glob.glob(nanoPath + "JetMET/dataRun3_2022_oct2023_JetMET_Run2022D-22Sep2023-v1/*/*/*root"),
  "isData": True,
  "name" : "JetMET_Run2022D", #name for the output files
},
}
