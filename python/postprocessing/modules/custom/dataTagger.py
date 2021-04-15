from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class dataTagger( Module ):
    def __init__(self, _isd = False):
        self.isd = _isd
        pass

    def beginJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('isData', 'i')

    def endJob(self):
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        self.wrappedOutputTree.fillBranch('isData', self.isd)
        return True


#dataTag = lambda : dataTagger()
