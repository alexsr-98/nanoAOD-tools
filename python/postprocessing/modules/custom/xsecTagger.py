from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class xsecTagger( Module ):
    def __init__(self, xsec):
        self._xsec = xsec

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if self._xsec:
            self.wrappedOutputTree = wrappedOutputTree
            self.wrappedOutputTree.branch('xsec', 'F')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        if self._xsec:
            self.wrappedOutputTree.fillBranch('xsec', self._xsec)
        return True


xsecTag = lambda : xsecTagger()
