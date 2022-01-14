from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT as r

class calculateVariatedElePt( Module ):
    def __init__(self, isd):
        self._thestr  = "scale" if isd else "sigma"

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch("Electron_" + self._thestr + "Up_pt"  , 'F', lenVar = "nElectron")
        self.wrappedOutputTree.branch("Electron_" + self._thestr + "Down_pt", 'F', lenVar = "nElectron")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, ev):
        outup = []; outdn = [];
        for iE in range(ev.nElectron):
            tmpelec = r.TLorentzVector()
            tmpelec.SetPtEtaPhiM(ev.Electron_pt[iE], ev.Electron_eta[iE], ev.Electron_phi[iE], ev.Electron_mass[iE])
            outup.append(r.TMath.Sqrt( (tmpelec.E() + getattr(ev, "Electron_dE" + self._thestr + "Up")[iE] )**2   - tmpelec.Pz()**2))
            outdn.append(r.TMath.Sqrt( (tmpelec.E() + getattr(ev, "Electron_dE" + self._thestr + "Down")[iE] )**2 - tmpelec.Pz()**2))

        self.wrappedOutputTree.fillBranch("Electron_" + self._thestr + "Up_pt"  , outup)
        self.wrappedOutputTree.fillBranch("Electron_" + self._thestr + "Down_pt", outdn)
        return True
