import glob

nanoPath = "/pool/phedex/nanoAODv10/27sep2022/Data/"

#-------DoubleMuon-------# 
doubleMuon = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "DoubleMuon/27sep2022_data_DoubleMuon_Run2022C-PromptNanoAODv10-v1/*/*/*root"),
  "isData": True,
  "name" : "DoubleMuon_Run2022C", #name for the output files
}

#-------SingleMuon-------# 
singleMuon = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "SingleMuon/27sep2022_data_SingleMuon_Run2022C-PromptNanoAODv10-v1/*/*/*root"),
  "isData": True,
  "name" : "SingleMuon_Run2022C", #name for the output files
} 
#-------Muon-------# 
muon_Run2022C = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "Muon/27sep2022_data_Muon_Run2022C-PromptNanoAODv10-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022C", #name for the output files
}
muon_Run2022D = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "Muon/27sep2022_data_Muon_Run2022D-PromptNanoAODv10-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022D", #name for the output files
} 
muon_Run2022D_v1_v1 = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "Muon/27sep2022_data_Muon_Run2022D-PromptNanoAODv10_v1-v1/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022D_v1_v1", #name for the output files
}
muon_Run2022E = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "Muon/31oct2022_Muon_Run2022E-PromptNanoAODv10_v1-v3/*/*/*root"),
  "isData": True,
  "name" : "Muon_Run2022E", #name for the output files
}  

#-------EGamma-------# 
eGamma_Run2022C = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "EGamma/27sep2022_data_EGamma_Run2022C-PromptNanoAODv10-v2/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022C", #name for the output files
}
eGamma_Run2022D = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "EGamma/27sep2022_data_EGamma_Run2022D-PromptNanoAODv10-v2/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022D", #name for the output files
}  
eGamma_Run2022D_v1_v1 = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "EGamma/27sep2022_data_EGamma_Run2022D-PromptNanoAODv10_v1-v1/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022D_v1_v1", #name for the output files
} 
eGamma_Run2022E = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "EGamma/data22EF_26oct2022_EGamma_Run2022E-PromptNanoAODv10_v1-v2/*/*/*root"),
  "isData": True,
  "name" : "EGamma_Run2022E", #name for the output files
}

#-------MuonEG-------# 
muonEG_Run2022C = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "MuonEG/27sep2022_data_MuonEG_Run2022C-PromptNanoAODv10-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022C", #name for the output files
}
muonEG_Run2022D = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "MuonEG/27sep2022_data_MuonEG_Run2022D-PromptNanoAODv10-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022D", #name for the output files
}
muonEG_Run2022D_v1_v1 = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "MuonEG/27sep2022_data_MuonEG_Run2022D-PromptNanoAODv10_v1-v1/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022D_v1_v1", #name for the output files
}
muonEG_Run2022E = {
  "xsec": 1.0,
  "year": "2022",
  "files": glob.glob(nanoPath + "MuonEG/31oct2022_MuonEG_Run2022E-PromptNanoAODv10_v1-v3/*/*/*root"),
  "isData": True,
  "name" : "MuonEG_Run2022E", #name for the output files
}

samples = [doubleMuon, singleMuon, muon_Run2022C, muon_Run2022D, muon_Run2022D_v1_v1, eGamma_Run2022C, eGamma_Run2022D, eGamma_Run2022D_v1_v1, muonEG_Run2022C, muonEG_Run2022D, muonEG_Run2022D_v1_v1, eGamma_Run2022E, muon_Run2022E, muonEG_Run2022E]