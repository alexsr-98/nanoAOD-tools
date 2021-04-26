import os, sys, json, copy
from datetime import datetime
from multiprocessing import Process
### General settings
UnretrieveThreshold = 7
nanoAODv = 6

#### Directories with settings
all_data_dataset_groups = ["SingleMuon", "DoubleMuon", "SingleElectron", "DoubleEG", "MuonEG", "LowEGJet", "HighEGJet"]

xsecDict = {"DY_M0to50"       : 106300.0,
            "DY_M10to50"      : 22635.09,
            "DY_M50"          : 6025.2,

            "WWbb_bb4l"       : 52.54,          # NLO

            "ttbar_dilep"     : 88.28769753,    # NNLO
            "ttbar_semilep"   : 365.3994209,    # NNLO
            "ttbar_inclusive" : 831.76,         # NNLO

            "tW_inclusive"    : 35.85,          # NNLO
            "tW_nofullyhad"   : 19.4674104,     # NNLO

            "ttW_lep"         : 0.2043,
            "ttW_ewkNLO_lep"  : 0.491,
            "ttW_had"         : 0.4062,

            "ttZ_lep_M1to10"  : 0.0493,
            "ttZ_lep_M10"     : 0.2529,
            "ttZ_had"         : 0.5297,
            "ttZ_had_dilep"   : 0.0568,

            "ttGamma_dilep"   : 1.495,
            "ttGamma_singlel" : 5.08,

            "WJets_lep"       : 61526.7,

            "WW"              : 115,
            "WW_dilep"        : 12.178,
            "WW_dilep_2scatt" : 1.61704,
            "WW_lnuqq"        : 45.53,

            "WZ"              : 47.13,
            "WZ_lnu2q"        : 10.7408,
            "WZ_2l2q"         : 5.595,
            "WZ_3lnu"         : 4.42965,

            "ZZ"              : 16.523,
            "ZZ_dilep"        : 0.564,
            "ZZ_2l2q"         : 3.28,
            "ZZ_2q2nu"        : 4.04,
            "ZZ_4l"           : 1.256,
            "ZZ_4l_2scatt"    : 0.009697,

            "WWW"             : 0.2086,
            "WWZ"             : 0.1651,
            "WWG"             : 0.2147,
            "WZZ"             : 0.05565,
            "WZG"             : 0.0412,
            "ZZZ"             : 0.01398,
}


xsecDictExtended = {"ST_tW_antitop_5f_NoFullyHadronicDecays_TuneEE5C_13TeV-powheg-herwigpp"         : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneEE5C_13TeV-powheg-herwigpp"             : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCH3_13TeV-powheg-herwig7"           : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCH3_13TeV-powheg-herwig7"               : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"     : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8" : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"           : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"               : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"       : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"           : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"                 : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"                     : xsecDict["tW_inclusive"],

                    "DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8"                         : xsecDict["DY_M10to50"],
                    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"                    : xsecDict["DY_M10to50"],
                    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"                   : xsecDict["DY_M10to50"],
                    "DYJetsToLL_Pt-0To50_TuneCP5_13TeV-amcatnloFXFX-pythia8"                        : xsecDict["DY_M0to50"],
                    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"                        : xsecDict["DY_M50"],
                    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"                       : xsecDict["DY_M50"],
                    "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8"                            : xsecDict["DY_M50"],
                    "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8"                             : xsecDict["DY_M50"],

                    "b_bbar_4l_TuneCP5_13TeV-powheg-pythia8"                                        : xsecDict["WWbb_bb4l"],

                    "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"                                     : xsecDict["ttbar_inclusive"],
                    "TT_TuneCH3_13TeV-powheg-herwig7"                                               : xsecDict["ttbar_inclusive"],
                    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8"                                        : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8"                       : xsecDict["ttbar_semilep"],
                    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8"                                 : xsecDict["ttbar_semilep"],

                    "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8"                                : xsecDict["ttZ_lep_M1to10"],
                    "TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"                        : xsecDict["ttZ_lep_M1to10"],
                    "TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8"                     : xsecDict["ttZ_lep_M10"],
                    "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8"                               : xsecDict["ttZ_lep_M10"],
                    "TTZJetsToQQ_Dilept_TuneCP5_PSweights_13TeV-amcatnlo-pythia8"                   : xsecDict["ttZ_had_dilep"],
                    "TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8"                                        : xsecDict["ttZ_had"],

                    "TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8"             : xsecDict["ttW_lep"],
                    "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8"                       : xsecDict["ttW_lep"],
                    "TTWJetsToLNu_EWK_5f_NLO"                                                       : xsecDict["ttW_ewkNLO_lep"],
                    "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"                   : xsecDict["ttW_had"],
                    "TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8"                        : xsecDict["ttW_had"],

                    "TTGamma_Dilept_TuneCP5_PSweights_13TeV-madgraph-pythia8"                       : xsecDict["ttGamma_dilep"],
                    "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8"                                 : xsecDict["ttGamma_dilep"],
                    "TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8"                   : xsecDict["ttGamma_singlel"],
                    "TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8"                             : xsecDict["ttGamma_singlel"],

                    "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8"                                  : xsecDict["WJets_lep"],
                    "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"                             : xsecDict["WJets_lep"],
                    "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"                            : xsecDict["WJets_lep"],
                    "WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8"                              : xsecDict["WJets_lep"], #### WARNING
                    "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8"                              : xsecDict["WJets_lep"], #### WARNING
                    "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8"                              : xsecDict["WJets_lep"], #### WARNING

                    "WWTo2L2Nu_13TeV-powheg"                                                        : xsecDict["WW_dilep"],
                    "WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8"                                : xsecDict["WW_dilep"],
                    "WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8"                      : xsecDict["WW_dilep"],
                    "WWTo2L2Nu_DoubleScattering_13TeV-pythia8"                                      : xsecDict["WW_dilep_2scatt"],
                    "WWToLNuQQ_13TeV-powheg"                                                        : xsecDict["WW_lnuqq"],
                    "WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8"                                : xsecDict["WW_lnuqq"],
                    "WWToLNuQQ_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8"                      : xsecDict["WW_lnuqq"],
                    "WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8"                                : xsecDict["WW_lnuqq"],

                    "WZTo1L1Nu2Q_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8"                        : xsecDict["WZ_lnu2q"],
                    "WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8"                                : xsecDict["WZ_lnu2q"],
                    "WZToLNu2Q_13TeV_powheg_pythia8"                                                : xsecDict["WZ_lnu2q"],
                    "WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"                                   : xsecDict["WZ_2l2q"],
                    "WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8"                                    : xsecDict["WZ_3lnu"],
                    "WZTo3LNu_13TeV-powheg-pythia8"                                                 : xsecDict["WZ_3lnu"],
                    "WZTo3LNu_TuneCP5_13TeV-powheg-pythia8"                                         : xsecDict["WZ_3lnu"],

                    "ZZTo2L2Nu_13TeV_powheg_pythia8"                                                : xsecDict["ZZ_dilep"],
                    "ZZTo2L2Nu_13TeV_powheg_pythia8_ext1"                                           : xsecDict["ZZ_dilep"],
                    "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8"                                        : xsecDict["ZZ_dilep"],
                    "ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8"                                   : xsecDict["ZZ_2l2q"],
                    "ZZTo2L2Q_TuneCUETP8M1_13TeV_amcatnloFXFX_madspin_pythia8"                      : xsecDict["ZZ_2l2q"],
                    "ZZTo2L2Q_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8"                           : xsecDict["ZZ_2l2q"],
                    "ZZTo4L_13TeV_powheg_pythia8"                                                   : xsecDict["ZZ_4l"],
                    "ZZTo4L_TuneCP5_13TeV_powheg_pythia8"                                           : xsecDict["ZZ_4l"],
                    "ZZTo4L_DoubleScattering_13TeV-pythia8"                                         : xsecDict["ZZ_4l_2scatt"],
                    "ZZTo4L_TuneCP5_DoubleScattering_13TeV-pythia8"                                 : xsecDict["ZZ_4l_2scatt"],

                    "WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8"                                    : xsecDict["WWW"],
                    "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8"                                         : xsecDict["WWW"],
                    "WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8"                                       : xsecDict["WWZ"],
                    "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8"                                         : xsecDict["WWZ"],
                    "WWZ_TuneCP5_13TeV-amcatnlo-pythia8"                                            : xsecDict["WWZ"],
                    "WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8"                                       : xsecDict["WWG"],
                    "WWG_TuneCP5_13TeV-amcatnlo-pythia8"                                            : xsecDict["WWG"],
                    "WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8"                                       : xsecDict["WZG"],
                    "WZG_TuneCP5_13TeV-amcatnlo-pythia8"                                            : xsecDict["WZG"],
                    "WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8"                                       : xsecDict["WZZ"],
                    "WZZ_TuneCP5_13TeV-amcatnlo-pythia8"                                            : xsecDict["WZZ"],
                    "ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8"                                       : xsecDict["ZZZ"],
                    "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8"                                            : xsecDict["ZZZ"],

                    "TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8"                                : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8"                      : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8"                                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8"                                      : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8"                          : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8"                            : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5CR1_QCDbased_13TeV-powheg-pythia8"                            : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_13TeV-powheg-pythia8"                  : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5CR2_GluonMove_13TeV-powheg-pythia8"                           : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5CR2_GluonMove_PSweights_13TeV-powheg-pythia8"                 : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5_PSweights_erdON_13TeV-powheg-pythia8"                        : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5_erdON_13TeV-powheg-pythia8"                                  : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop166p5_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop169p5_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop169p5_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5_PSweights_mtop1695_13TeV-powheg-pythia8"                     : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop171p5_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop171p5_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop173p5_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop173p5_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop175p5_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop175p5_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_TuneCP5_PSweights_mtop1755_13TeV-powheg-pythia8"                     : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop178p5_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["ttbar_dilep"],
                    "TTTo2L2Nu_mtop178p5_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["ttbar_dilep"],


                    "ST_tW_antitop_5f_hdampup_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"               : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_hdampup_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"     : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_hdampdown_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"   : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_hdampdown_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"             : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_hdampup_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"         : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_hdampup_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"                   : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_hdampdown_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"       : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_hdampdown_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"                 : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8"           : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5down_PSweights_13TeV-powheg-pythia8"         : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5up_13TeV-powheg-pythia8"                     : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5down_13TeV-powheg-pythia8"                   : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5down_13TeV-powheg-pythia8"                       : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5up_13TeV-powheg-pythia8"                         : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8"               : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5down_PSweights_13TeV-powheg-pythia8"             : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8"                    : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR1_13TeV-powheg-pythia8"                        : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR2_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR2_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5CR2_13TeV-powheg-pythia8"                    : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5CR2_13TeV-powheg-pythia8"                        : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_erdON_PSweights_13TeV-powheg-pythia8"       : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_erdON_PSweights_13TeV-powheg-pythia8"           : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_erdON_13TeV-powheg-pythia8"                 : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_erdON_13TeV-powheg-pythia8"                     : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_DS_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_DS_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"                    : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_DS_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8"                        : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1695_TuneCP5_PSweights_13TeV-powheg-pythia8"    : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1695_TuneCP5_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1715_TuneCP5_PSweights_13TeV-powheg-pythia8"    : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1715_TuneCP5_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1735_TuneCP5_PSweights_13TeV-powheg-pythia8"    : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1735_TuneCP5_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1755_TuneCP5_PSweights_13TeV-powheg-pythia8"    : xsecDict["tW_nofullyhad"],
                    "ST_tW_antitop_5f_NoFullyHadronicDecays_mtop1755_TuneCP5_13TeV-powheg-pythia8"              : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1695_TuneCP5_PSweights_13TeV-powheg-pythia8"        : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1695_TuneCP5_13TeV-powheg-pythia8"                  : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1715_TuneCP5_PSweights_13TeV-powheg-pythia8"        : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1715_TuneCP5_13TeV-powheg-pythia8"                  : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1735_TuneCP5_PSweights_13TeV-powheg-pythia8"        : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1735_TuneCP5_13TeV-powheg-pythia8"                  : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1755_TuneCP5_PSweights_13TeV-powheg-pythia8"        : xsecDict["tW_nofullyhad"],
                    "ST_tW_top_5f_NoFullyHadronicDecays_mtop1755_TuneCP5_13TeV-powheg-pythia8"                  : xsecDict["tW_nofullyhad"],

                    "ST_tW_top_5f_inclusiveDecays_TuneCP5down_13TeV-powheg-pythia8"                             : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_TuneCP5up_13TeV-powheg-pythia8"                               : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8"                     : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_TuneCP5down_PSweights_13TeV-powheg-pythia8"                   : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5down_13TeV-powheg-pythia8"                         : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5up_13TeV-powheg-pythia8"                           : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5up_PSweights_13TeV-powheg-pythia8"                 : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5down_PSweights_13TeV-powheg-pythia8"               : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_DS_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"                : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_DS_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"                    : xsecDict["tW_inclusive"],
                    "ST_tW_DS_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"                          : xsecDict["tW_inclusive"],
                    "ST_tW_DS_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"                              : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_mtop1695_TuneCP5_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_mtop1715_TuneCP5_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_mtop1735_TuneCP5_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_inclusive"],
                    "ST_tW_antitop_5f_inclusiveDecays_mtop1755_TuneCP5_PSweights_13TeV-powheg-pythia8"          : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_mtop1695_TuneCP5_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_mtop1715_TuneCP5_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_mtop1735_TuneCP5_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_inclusive"],
                    "ST_tW_top_5f_inclusiveDecays_mtop1755_TuneCP5_PSweights_13TeV-powheg-pythia8"              : xsecDict["tW_inclusive"],
}

##### Function definitions
def CheckPathDataset(path):
    ''' Check if the name exists in local folder or in dataset folder '''
    if (os.path.isfile(path)):
        return path
    elif (os.path.isfile(path + '.txt')):
        return path + '.txt'

    path = 'datasets/' + path
    if (os.path.isfile(path)):
        return path
    elif (os.path.isfile(path + '.txt')):
        return path+'.txt'
    return ''


def GuessIsData(path):
    ''' Returns False if the dataset file seems to correspond to mc, True otherwise '''
    name = path.replace('datasets', '')
    if "mc" in name.lower():
        return False
    elif "data" in name.lower():
        return True
    else:
        if 'NANOAOD' in path:
            if 'NANOAODSIM' in path:
                return False
            else:
                return True
    return True


def GuessYear(path):
    thepath = path.lower()
    if   any([el in thepath for el in ["5tev", "5p02"]]): return 5
    elif 'run2018' in thepath: return 2018
    elif 'run2017' in thepath: return 2017
    elif 'run2016' in thepath: return 2016
    elif '2018'    in thepath: return 2018
    elif '2017'    in thepath: return 2017
    elif '2016'    in thepath: return 2016

    raise RuntimeError("FATAL: couldn't guess year from path " + path)
    return


def GetRequestName(d, tn, wa):
    if len(wa + "_" + tn + "_" + "_".join(d.split("/")[:-1])) < 100:
        return wa + "_" + tn + "_" + "_".join(d.split("/")[1:-1])

    elif len((wa + "_" + tn + "_" + d.split("/")[1] + "_XX" + d.split("/")[2][(len(d.split("/")[2]) - (99 - 4 - len(tn) - len(wa) - len(d.split("/")[1]))):])) >= 100:
        return (wa + "_" + tn + "_" + (d.split("/")[1])[:24] + "XX_XX" + d.split("/")[2][(len(d.split("/")[2]) - (99 - 6 - len(tn) - len(wa) - 24)):])

    else:
        return (wa + "_" + tn + "_" + d.split("/")[1] + "_XX" + d.split("/")[2][(len(d.split("/")[2]) - (99 - 4 - len(tn) - len(wa) - len(d.split("/")[1]))):])


def ReadLines(path):
    lines = []
    f = open(path, 'r')
    for line in f:
        line = line.replace(' ', '')
        line = line.replace('\t', '')
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        if line == '': continue
        if line[0] == '#': continue
        if line.find('#') > 0: line = line[:line.find('#')]
        if len(line) <= 1: continue
        lines.append(line)
    return lines


def GetToday():
    return datetime.now.strftime("%Y-%m-%d")


def GetTimeNow():
    now = datetime.now()
    time = str(now.hour) + 'h' + str(now.minute) + 'm' + str(now.second) + 's'
    return time


def GetEra(sampleName, year, isData = True):
    if not isData: return ''
    if isinstance(year, int): year = str(year)
    if len(year) == 2: year = "20%s"%year
    sy = 'Run%s'%(year)
    ls = len(sy)
    find = sampleName.find(sy)
    if find == -1: return ''
    era = sampleName[find+ls:find+ls+1]
    return era


def confirm(message = "Do you wish to continue?"):
    """
    Ask user to enter y(es) or n(o) (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n", "yes", "no"]:
        answer = raw_input(message + " [Y/N]\n").lower()
    return answer[0] == "y"


def CheckExistanceOfFolders(listoftasks):
    listoftaskswcreatedfolder = []
    for tsk in listoftasks:
        if os.path.isdir("./" + tsk[3] + "/crab_" + GetRequestName(tsk[0], tsk[2], tsk[3])):
            listoftaskswcreatedfolder.append(tsk)
    # task := (dataset, dataset_group, year, crab_workarea, output_folder = outputdir + "/" + name)
    return listoftaskswcreatedfolder


def KillAndErase(tsk):
    print "### Task with folder", "crab_" + GetRequestName(tsk[0], tsk[2], tsk[3])
    print "# Killing..."
    os.system("crab kill -d ./{wa}/{fl}".format(wa = tsk[3], fl = "crab_" + GetRequestName(tsk[0], tsk[2], tsk[3])))
    print "# Erasing..."
    os.system("rm -rf ./{wa}/{fl}".format(wa = tsk[3], fl = "crab_" + GetRequestName(tsk[0], tsk[2], tsk[3])))
    return


#def GetAllTheDatasets(listofdgs, listofyears, crab_workarea, output_folder):
    ## task := (dataset, dataset_group, year, crab_workarea, output_folder = outputdir + "/" + name)
    #listofdatasets = []
    #isdata = False

    #if ["All"] == listofdgs:
        #for year in listofyears:
            #tmpdict = GetDictionaryFromJSON(year, True)
            #for dg in tmpdict:
                #for dataset in tmpdict[dg]:
                    #if str(dataset[0]) == "#": continue
                    #listofdatasets.append( (str(dataset), dg, year, crab_workarea, output_folder) )
            #tmpdict = GetDictionaryFromJSON(year, False)
            #for dg in tmpdict:
                #for dataset in tmpdict[dg]:
                    #if str(dataset[0]) == "#": continue
                    #listofdatasets.append( (str(dataset), dg, year, crab_workarea, output_folder) )
    #else:
        #for dg in listofdgs:
            #isdata = IsItData(dg)
            #for year in listofyears:
                #tmpdict = GetDictionaryFromJSON(year, isdata)
                #if dg in tmpdict:
                    #for dataset in tmpdict[dg]:
                        #if str(dataset[0]) == "#": continue
                        #listofdatasets.append( (str(dataset), dg, year, crab_workarea, output_folder) )
    #return listofdatasets


#def GetDictionaryFromJSON(year, isdata):
    #if year.isdigit(): f = ("data" if isdata else "mc") + year + ".json"
    #else:              f = year + ".json"
    #with open("datasets_MINIAOD/" + f , "r") as jfile:
        #return copy.deepcopy(json.load(jfile))


#def IsItData(dg):
    #for datadg in all_data_dataset_groups:
        #if datadg in dg:
            #return True
    #return False


#def GetConfigFileParameters(dataset, dg, y):
    #pars = []
    #cfgdict = {}
    #if y.isdigit():
        #y_ = ("data" if IsItData(dg) else "mc") + y
    #else:
        #y_ = y

    #with open("datasets_MINIAOD/nanoAODv{v}_cfg.json".format(v = nanoAODv), "r") as jfile:
        #cfgdict = copy.deepcopy(json.load(jfile))


    ## Getting datinness
    #if IsItData(dg):
        #pars.append("IsData=True")
    #else:
        #pars.append("IsData=False")

    #if y_ not in cfgdict:
        #raise RuntimeError("ERROR: the information for the year/supergroup {y} could not be found in the JSON configuration file for nanoAOD version {v} while trying to get the parameters for dataset {d} inside dataset group {g}.".format(y = y_, v = nanoAODv, d = dataset, g = dg))

    ## Getting era
    #if isinstance(cfgdict[y_]["era"], dict):
        #if "v1" in cfgdict[y_]["era"] and int(y) == 2017:
            #if "RunIIFall17MiniAODv2" in dataset and not IsItData(dg):
                #pars.append(str("Era=" + cfgdict[y_]["era"]["v2"]))
            #else:
                #pars.append(str("Era=" + cfgdict[y_]["era"]["v1"]))
    #else:
        #pars.append(str("Era=" + cfgdict[y_]["era"]))
    ##print pars
    ##sys.exit()
    ## Getting global tag
    #if not isinstance(cfgdict[y_]["global_tag"], basestring):
        #raise RuntimeError("ERROR: attempted to obtain global tag for dataset {d} inside dataset group {g} for year/supergroup {y} with nanoAOD version {v}, but there are multiple ones implemented in the JSON config. file, and this is not supported in the code.".format(y = y_, v = nanoAODv, d = dataset, g = dg))
    #else:
        #pars.append(str("GlobalTag=" + cfgdict[y_]["global_tag"]))

    #return pars


#configurationCache = {}
def LaunchCRABTask(tsk):
    sampleName, isData, productionTag, year, thexsec, options, thedbs, test, username, pretend, verbose = tsk
    from CRABAPI.RawCommand       import crabCommand
    from CRABClient.UserUtilities import config
    from CRABClient.JobType       import CMSSWConfig

    print "\n# Launching CRAB task for sample {d} that is data {isd}, year {y}, for prod. tag {p} using the DBS {dbs} with xsec {xs}".format(d = sampleName, isd = str(isData), dbs = thedbs, p = productionTag, xs = thexsec, y = year) + ((" and with options " + options) if len(options) else "")
    if test:
        print "\t- This is a test submission! Only THREE (3) files will be processed!"
    #print "\nsyspath:", sys.path
    #print "\ncwd:", os.getcwd()
    #sys.exit()

    outputdir = "/store/user/" + username + "/nanoAOD_postprocessing/" + productionTag
    inFiles   = ['./crab_script.py', '../scripts/haddnano.py', './SlimFileIn.txt', './SlimFileOut.txt']
    lumimask  = ""
    workarea  = "temp_postproc_" + productionTag


    craboptions = "year:" + str(year)
    if options != "":
        craboptions += "," + options
    craboptions += ",datasetname:" + sampleName.split("/")[1]
    era = GetEra(sampleName, year, isData)
    if era != '': craboptions += ',era:%s'%era

    if not isData:
        craboptions += ",isData:0,xsec:" + str(thexsec)
    else:
        craboptions += ",isData:1"

    if (isData):
        # Set as MC... the only way the Count histogram works!! --> So we can compare with the numbers in DAS
        if   year == 2016:
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
            lumiMask = './lumijson/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
            lumijson = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
        elif year == 2017:
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'  # 41.29/fb
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
            lumiMask = './lumijson/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
            #lumijson = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
            lumijson = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
        elif year == 2018:
            #lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
            lumiMask = './lumijson/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
            lumijson = 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
        else:
            raise RuntimeError("FATAL: no lumimask and lumijson set for year " + str(year))

        inFiles.append("./lumijson/" + lumijson)

    if verbose:
        print "\t- outputdir:", outputdir
        print "\t- infiles:",   inFiles
        print "\t- workarea:",  workarea
    config = config()
    def submit(config):
        res = crabCommand('submit', config = config )

    reqnam = GetRequestName(sampleName, GetTimeNow(), productionTag)
    #reqnam  = productionTag + "_" + sampleName[0:min([70, len(sampleName)])].replace("/", "_")
    print "\t- Using as request name:", reqnam

    config.General.requestName  = reqnam
    config.General.workArea     = workarea
    config.General.transferLogs = True

    config.JobType.pluginName  = 'Analysis'
    config.JobType.psetName    = '../crab/PSet.py'
    config.JobType.scriptExe   = './crab_script.sh'
    config.JobType.scriptArgs  = ["theargs=" + craboptions] #### Debe haber un "="
    config.JobType.inputFiles  = inFiles

    #config.JobType.maxMemoryMB = 2500
    config.JobType.allowUndistributedCMSSW = True
    config.JobType.sendPythonFolder = True

    config.Data.inputDBS    = thedbs
    config.Data.splitting   = 'FileBased'
    #config.Data.splitting   = 'Automatic'
    config.Data.unitsPerJob = 1
    config.Data.publication = False
    if test:
        config.Data.totalUnits  = 3
    config.Data.allowNonValidInputDataset = True

    config.Data.outLFNDirBase = outputdir
    config.Data.inputDataset  = sampleName
    config.Data.lumiMask      = lumimask


    #config.Data.outputDatasetTag = productionTag + "_" + sampleName[0:min([70, len(sampleName)])].replace("/", "_") #### TODO: FIXXXXXXXX
    config.Data.outputDatasetTag = sampleName.split("/")[2]  ## fix???


    config.Site.storageSite = 'T2_ES_IFCA'
    #config.Site.storageSite = 'T2_CH_CERN'
    #config.Site.blacklist   = ['T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']
    #config.Site.blacklist   = []
    config.Site.ignoreGlobalBlacklist = True


    #res = crabCommand('submit', config = config)

    if not pretend:
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
        del p

    del config
    #CMSSWConfig.configurationCache.clear() #### NOTE: this is done in order to allow the parallelised CRAB job submission. For further
                                           ## information, please check the code on [1], the commit of [2] and the discussion of [3].
                                           ## [1]: https://github.com/dmwm/CRABClient/blob/master/src/python/CRABClient/JobType/CMSSWConfig.py
                                           ## [2]: https://github.com/dmwm/CRABClient/commit/a50bfc2d1f32093b76ba80956ee6c5bd6d61259e
                                           ## [3]: https://github.com/dmwm/CRABClient/pull/4824
    return
