# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 17:18:13 2026

Test walkthrough of derivation table functions


@author: mraemaek
"""

# dependencies
from createDerivationTables import createDerivationTables
from deriveRelationsFromBaseline import deriveRelationsFromBaseline
from utils import *
from plot_utils import *


# %% create default derivation tables or specific for user-input list

# If no relations are specified when function is called, tables are by default 
# created for all currently supported relations

plotTables = True
mutual, combi, relations = createDerivationTables(plotTables= True)


# %%

# Function can also take user specific input
relations = ['Same', 'Different', 'Opposite']
mutual, combi, relations = createDerivationTables(relations, plotTables = True)

# %% 
# And will add missing mutually or combinatorially entailed relations
# e.g., if you only specify 'more than', mutually entailed 'less than' is added 

relations = ['More']
mutual, combi, relations = createDerivationTables(relations, plotTables = True)

# Or if you only include opposite, combinatorially entailed sameness 
# (i.e., from combining two opposition relations) is added

relations = ['Opposite']
mutual, combi, relations = createDerivationTables(relations, plotTables = True)

# %% Derive relations from baseline

# Using such derivation tables, user can automatically derive relations from
# a specific set of baseline relations

# For instance, if we provide some stimulus labels, we can recreate the network
# trained by Steele & Hayes, with six baseline relations:
    # A same as B1; A same as C1;
    # A different from B3, A different from C3;
    # A opposite to B2, A opposite to C2
    
sLabs = ['A', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'N1', 'N2']
baseline = dict({'Same as': [(0,1), (0,4)],
             'Different from': [(0,3), (0,6)],
             'Opposite to': [(0,2), (0,5)]})
illustrate = 'print' # print derivations
relTab, derived = deriveRelationsFromBaseline(baseline, sLabs, illustrate)

# %%

# Instead of printing out the derivations, you can plot the network as a heatmap
illustrate = 'heatmap'
relTab, derived = deriveRelationsFromBaseline(baseline, sLabs, illustrate)


# %%

# Alternatively, we can plot the network as a graph

plotRels = ['baseline', 'mutual', 'combi'] # which relations to plot
plotTitle = '' # optional title
sLabs = ['A', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'N1', 'N2']

# Deinfe baseline network
baseline = dict({'Same as': [(0,1), (0, 4)],
                  'Different from': [(0,2), (0,5)], 
                'Opposite to': [(0,3), (0,6)]
             })
illustrate = 'graph'
relTab, derived = deriveRelationsFromBaseline(baseline, sLabs, illustrate)

# plotRelNetworkGraph(baseline, derived, sLabs, plotTitle)

# %% 
# Or we could do a typical  transitive inference task

# But, to do that properly, one needs multi-step derivation

sLabs = ['A', 'B', 'C', 'D', 'E', 'F']
baseline = {'More than': [(0,1), (1,2), (2,3), (3,4), (4,5)]}

relTab, derived = deriveRelationsFromBaseline(baseline, sLabs, illustrate)

# %%


