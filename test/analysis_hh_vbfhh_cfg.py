import os
import copy
import heppy.framework.config as cfg
import sys
sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)


from FCChh_samples import pp_vbfhh

pp_vbfhh.splitFactor=50


comp = cfg.Component(
    'example',
     files = ["root://eospublic.cern.ch//eos/fcc/hh/generation/DelphesEvents/v0_0/pp_vbfhh/events90.root"]
)

#to run over all the files on eos (batch)
#selectedComponents = [pp_vbfhh]
#to run only over one file
selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    #gen_particles = 'genParticles',
    #gen_vertices = 'genVertices',

    gen_jets = 'genJets',

    jets = 'jets',
    bTags = 'bTags',
    cTags = 'cTags',
    tauTags = 'tauTags',

    electrons = 'electrons',
    electronITags = 'electronITags',

    muons = 'muons',
    muonITags = 'muonITags',

    photons = 'photons',
    met = 'met',
)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events


#from heppy.analyzers.MyGenAnalyzer import GenAnalyzer
#genana = cfg.Analyzer(
#    GenAnalyzer
#    )



from heppy.analyzers.Selector import Selector
muons = cfg.Analyzer(
    Selector,
    'sel_muons',
    output = 'muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()<20
)


from heppy.analyzers.Selector import Selector
electrons = cfg.Analyzer(
    Selector,
    'sel_electrons',
    output = 'electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()<20
)


jets_30 = cfg.Analyzer(
    Selector,
    'jets_30',
    output = 'jets_30',
    input_objects = 'jets',
    filter_func = lambda jet: jet.pt()>30.
)


from heppy.analyzers.examples.ttbar.BTagging import BTagging
btagging = cfg.Analyzer(
    BTagging,
    'b_jets_30',
    output = 'b_jets_30',
    input_objects = 'jets_30',
    filter_func = lambda jet : jet.tags['bf']>0.
)

from heppy.vbfHHanalysis.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)


from heppy.vbfHHanalysis.vbfHHTreeProducer import vbfHHTreeProducer
gen_tree = cfg.Analyzer(
    vbfHHTreeProducer,
    jets_30 = 'jets_30',
    met = 'met'

)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    jets_30,
    muons,
    electrons,
    btagging,
    selection,
    gen_tree
    ] )

# comp.files.append('example_2.root')
#comp.splitFactor = len(comp.files)  # splitting the component in 2 chunks

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def next():
        loop.process(loop.iEvent+1)

    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0,
                   timeReport=True)
    loop.process(6)
    print loop.event
