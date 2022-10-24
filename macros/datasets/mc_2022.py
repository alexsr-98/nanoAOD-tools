import glob

nanoPath = "/pool/phedex/nanoAODv10/27sep2022/MC/"


#-------tW-------#
tw_minus = {
  "xsec": 39.66,
  "year": "2022",
  "files": glob.glob(nanoPath + "26sep2022_TWminus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8/*/*/*root"),
  "isData": False,
  "name" : "TWminus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8", #name for the output files
}








samples = [tw_minus]
