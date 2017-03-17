from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('At least 4 jets')
        self.counters['cut_flow'].register('At least 6 jets')
        self.counters['cut_flow'].register('At least 2 b-jet')

    def process(self, event):
        self.counters['cut_flow'].inc('All events')
        
        #select events with at least 4 jets
        if len(event.jets_30)<4:
            return False
        self.counters['cut_flow'].inc('At least 4 jets')

        #select events with at least 6 jets
        if len(event.jets_30)<6:
            return False
        self.counters['cut_flow'].inc('At least 4 jets')

        #select events with at least 1 b-jet
        if len(event.b_jets_30)<2:
            return False
        self.counters['cut_flow'].inc('At least 2 b-jet')
            
        return True
