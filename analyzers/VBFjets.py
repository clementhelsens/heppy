'''Find the two most forward jets and compute their pseudorapidity difference (used for vbf topologies) (ANALYZER UNDER REVIEW)'''

from heppy.framework.analyzer import Analyzer
import math

class VBFjets(Analyzer):
    '''Computes the pseudorapidity difference in forward jets.
    
    '''
    
    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        if len(jets)<2:
            return # NOT CALCULATING ETA DIFFERENCE IF LESS THAN 2 JETS

        jets_tmp = []
        for ijet, jet in enumerate(jets):
            jets_tmp.append([ijet,jet.eta()])

        eta_ordered_jets=sorted(jets_tmp,key=lambda l:l[1], reverse=True)
 #       fillParticle(self.tree, 'forward_jet1', jets[eta_ordered_jets[0][0]])
        

        setattr(event, self.cfg_ana.forward_jet1, jets[eta_ordered_jets[0][0]])
        setattr(event, self.cfg_ana.forward_jet2, jets[eta_ordered_jets[-1][0]])
        setattr(event, self.cfg_ana.forward_jet_eta_diff, abs(jets[eta_ordered_jets[0][0]].eta()-jets[eta_ordered_jets[-1][0]].eta()))
