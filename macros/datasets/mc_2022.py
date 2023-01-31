import glob

nanoPath = "/pool/phedex/nanoAODv10/27sep2022/MC/"


#-------ttbar-------# | NLO Powheg+Pythia8 
  # Dileptonic
ttbar_dileptonic = {
  "xsec": 97.9140,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8/*/*/*root"),
  "isData": False,
  "name" : "TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8", #name for the output files
}  
  # Semileptonic
ttbar_semileptonic = {
  "xsec": 405.2403,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_TTTo2J1L1Nu_CP5_13p6TeV_powheg-pythia8/*/*/*root"),
  "isData": False,
  "name" : "TTTo2J1L1Nu_CP5_13p6TeV_powheg-pythia8", #name for the output files
}  
  # Uncertainties

#-------tW-------# | NLO DR
tw_minus = {
  "xsec": 24.2,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_TWminus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8/*/*/*root"),
  "isData": False,
  "name" : "TWminus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8", #name for the output files
}
tw_plus = {
  "xsec": 24.2,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_TbarWplus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8/*/*/*root"),
  "isData": False,
  "name" : "TbarWplus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8", #name for the output files
}

#-------Wjets-------#
  # LO
wjets_LNu = {
  "xsec": 63199.9,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_WJetsToLNu_TuneCP5_13p6TeV-madgraphMLM-pythia8/*/*/*root"),
  "isData": False,
  "name" : "WJetsToLNu_TuneCP5_13p6TeV-madgraphMLM-pythia8", #name for the output files
}

#-------DY-------#
  # LO
dy_M10to50 = {
  "xsec": 19317.5,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_DYJetsToLL_M-10to50_TuneCP5_13p6TeV-madgraphMLM-pythia8/*/*/*root"),
  "isData": False,
  "name" : "DYJetsToLL_M-10to50_TuneCP5_13p6TeV-madgraphMLM-pythia8", #name for the output files
}
dy_M50_ext1 = {
  "xsec": 6221.3,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8ext1/*/*/*root"),
  "isData": False,
  "name" : "DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8ext1", #name for the output files
}
dy_M50_ext2 = {
  "xsec": 6221.3,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8ext2/*/*/*root"),
  "isData": False,
  "name" : "DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8ext2", #name for the output files
}         

#-------WW-------#
ww = {
  "xsec": 116.8,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_WW_TuneCP5_13p6TeV-pythia8/*/*/*root"),
  "isData": False,
  "name" : "WW_TuneCP5_13p6TeV-pythia8", #name for the output files
}

#-------WZ-------#
wz = {
  "xsec": 54.2776,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_WZ_TuneCP5_13p6TeV-pythia8/*/*/*root"),
  "isData": False,
  "name" : "WZ_TuneCP5_13p6TeV-pythia8", #name for the output files
}

#-------ZZ-------#
zz = {
  "xsec": 16.7,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_ZZ_TuneCP5_13p6TeV-pythia8/*/*/*root"),
  "isData": False,
  "name" : "ZZ_TuneCP5_13p6TeV-pythia8", #name for the output files
}

    ##### ttW

    ##### ttZ

    ###### ttGamma

    ###### VVV

samples = [ttbar_dileptonic, ttbar_semileptonic, tw_minus, tw_plus, wjets_LNu, dy_M10to50, dy_M50_ext1, dy_M50_ext2, ww, wz, zz]
#samples = [tw_minus, tw_plus]
