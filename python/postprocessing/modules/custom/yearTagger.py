from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class yearTagger( Module ):
    def __init__(self, year):
        self._year = year

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('year', 'I')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        self.wrappedOutputTree.fillBranch('year', self._year)
        return True


yearTag = lambda : yearTagger()
