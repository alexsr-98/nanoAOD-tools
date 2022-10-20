from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class datasetNamer( Module ):
    def __init__(self, thedat):
        self.dat    = [ord(x) for x in thedat]
        self.lendat = len(self.dat)
        pass

    def beginJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('nDatasetName','i')
        self.wrappedOutputTree.branch('DatasetName_name', 'b', lenVar='nDatasetName')

    def endJob(self):
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        self.wrappedOutputTree.fillBranch('nDatasetName',     self.lendat)
        self.wrappedOutputTree.fillBranch('DatasetName_name', self.dat)
        return True


datasetName = lambda : datasetNamer()
