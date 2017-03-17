from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *

from ROOT import TFile

class vbfHHTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(vbfHHTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        bookParticle(self.tree, 'jet1')
        bookParticle(self.tree, 'jet2')
        bookParticle(self.tree, 'jet3')
        bookParticle(self.tree, 'jet4')
        bookParticle(self.tree, 'jet5')
        bookParticle(self.tree, 'jet6')
        bookParticle(self.tree, 'jet7')
        bookParticle(self.tree, 'jet8')
        bookMet(self.tree, 'met')

    def process(self, event):
        self.tree.reset()
 
        jets = getattr(event, self.cfg_ana.jets_30)
        if len(jets)<3:
            return # NOT FILLING THE TREE IF LESS THAN 4 JETS
        for ijet, jet in enumerate(jets):
            if ijet==8:
                break
            fillParticle(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)

        met = getattr(event, self.cfg_ana.met)
        fillMet(self.tree, 'met', met)
        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
