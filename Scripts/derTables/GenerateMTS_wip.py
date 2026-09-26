# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:56:53 2023

MTS Trial procedure generator for model training and testing

Function generates a dict containing trial information, based on some settings
input by the user: 
    - baseline - a dict containing baseline relations (keys) to be trained between
        stimulus-pairs (tuples: e.g., (0, 1))
    - preset - for specific cases, like Steele & Hayes or transitive inference,
            default settings are defined
    - n_baseline and n_test - number of repetitions for all baseline and test trials7
    - n_comp - number of comparison stimuli presented on a trial
    - (optional) derived - a dict or string preset containing the derived 
                            relations to be tested
    - (optional) Slabs - list of stimulus labels for printing, 
                        if not provided, default alphanumerics used
    

1) Function first checks provided relations and/or preset, relying on 
    derivation tables to compute all possible derived relations that can be tested,
    (if no 'derived' dict is provided)
2)  loop through baseline relations for n_baseline iterations (of each relation)
    and, given a cue, sample and correct comparison stimulus, find n_comp-1 other 
    (incorrect) comparison stimuli to complete the trail, store trial data
3) Loop through derived relations (n_test iterations) and do the same


Outputted:
    dict containing fields 'tID' (trial index), 'type' (baseline, mutual, combinatorial),
    'cue' (index for contextual cue), 'sample' (index for sample stimulus),
    'comparisons' (list of indices for comparison stimuli), 
    'correct' (index of correct comparison), 'label' (string label for trial)
    


####
TODO - Function would ideally allow to:
    - Manipulate procedural parameters:
        - Number of stimuli, cues, functions, classes/sets,
        set size/derivation/nodal distance
        - Training schedule: one-to-many, many-to-one, linear
        - More complex derivations
        
####
@author: mraemaek
"""

#%% Import dependencies

import numpy as np
import pdb
from derTables.deriveRelationsFromBaseline import deriveRelationsFromBaseline
from derTables.createDerivationTables import createDerivationTables
from derTables.utils_tables import *
from derTables.utils_mts import findComparisonOptions, add_comparison_sets, print_mts_trial, format_comparisons


#%% Generate MTS function workflow
# Create random trials based on set of baseline relations and task parameters
# Loop relations and derived relations, find comparison stimuli that are not related


def generateTrials(baseline, n_baseline, preset, n_test, n_comp, 
                   derived = None, printTrials = None, sLabs = None):
    # First check is specific preset was requested 
    match preset: # Specify additional information for S&H91, transitive inference, ...
        case 'Manual':
            # n_cues = len(np.unique(trial_data["cue"])) # could also be n_rels
            # n_rel = len(np.unique(trial_data["cue"])) 
            unique = [] # find number of unique stimuli for array dimensions
            allRels = []
            for i in baseline.keys(): 
                allRels.append(i)
                for j in baseline[i]: 
                    for s in j: 
                        if s not in unique: unique.append(s)
            n_stim = len(unique)

            if sLabs is None:
                sLabs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                         'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 
                         'W', 'X', 'Y', 'Z'] # Default to fall back on
            relTab, all_derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
            
            if derived is None or derived == "All":
                derived = all_derived
            
            
        # case 'Random':  # Create a list of generic stimulus labels to represent stimuli
        #     alf = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        #            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        #     s_mp = {} # Initializa Stimulus label dict
        #     n_a = 1
        #     for i in range(n_nodes):
        #         if i % 26 == 0: #· Account for multiple trips around the alfabet
        #             n_a += 1
        #         s_mp[alf[i]*n_a] = int(i)
        #         if n_func == 1:
        #             # Stimulus features label to index mapping (used for feature-level array?)
        #             f_mp = {"Reward": 0}
        #             for s in range(n_nodes):
        #                 fs_mp[0]
                        
        #     # Also by default pick first stim in list as sample 
        #     o2m_Samp = s_mp[0]    
        
            
            
        case 'TransitiveInference': # transitive inference task in MTS
            if sLabs is None: sLabs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
            baseline = dict({'More than': []})
            for i in range(len(sLabs)-1):
                baseline['More than'].append((i, i+1))  
            n_stim = countUniqueStimuli(baseline)
            relTab,  all_derived = deriveRelationsFromBaseline(baseline, sLabs)
            derived = dict({'More than': [(0,2), (0,3), (0,4), (1,3), (1,4), (2, 4)]})
            allRels = ['More than', 'Less than']
            n_comp = 2
            
        
        # ============================================================
        # STIMULUS EQUIVALENCE PRESETS
        # ============================================================
    
        case 'Equivalence 2 3-member Linear':
            # Two 3-member equivalence classes
            #
            # Class 1: A1 -> B1 -> C1
            # Class 2: A2 -> B2 -> C2
    
            sLabs = [
                'A1', 'B1', 'C1',
                'A2', 'B2', 'C2'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1), (1, 2),   # class 1
                    (3, 4), (4, 5)    # class 2
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
    
    
        case 'Equivalence 2 3-member OTM':
            # Two 3-member equivalence classes
            # One-to-many training
            #
            # Class 1: A1 -> B1, A1 -> C1
            # Class 2: A2 -> B2, A2 -> C2
    
            sLabs = [
                'A1', 'B1', 'C1',
                'A2', 'B2', 'C2'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1), (0, 2),   # class 1
                    (3, 4), (3, 5)    # class 2
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
    
    
        case 'Equivalence 2 3-member MTO':
            # Two 3-member equivalence classes
            # Many-to-one training
            #
            # Class 1: B1 -> A1, C1 -> A1
            # Class 2: B2 -> A2, C2 -> A2
    
            sLabs = [
                'A1', 'B1', 'C1',
                'A2', 'B2', 'C2'
            ]
    
            baseline = {
                'Same as': [
                    (1, 0), (2, 0),   # class 1
                    (4, 3), (5, 3)    # class 2
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
    
    
        case 'Equivalence 2 4-member Linear':
            # Two 4-member equivalence classes
            #
            # A1 -> B1 -> C1 -> D1
            # A2 -> B2 -> C2 -> D2
    
            sLabs = [
                'A1', 'B1', 'C1', 'D1',
                'A2', 'B2', 'C2', 'D2'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1), (1, 2), (2, 3),
                    (4, 5), (5, 6), (6, 7)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
    
    
        case 'Equivalence 2 4-member OTM':
            # Two 4-member equivalence classes
            # One-to-many training
    
            sLabs = [
                'A1', 'B1', 'C1', 'D1',
                'A2', 'B2', 'C2', 'D2'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1), (0, 2), (0, 3),
                    (4, 5), (4, 6), (4, 7)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
    
    
        case 'Equivalence 2 4-member MTO':
            # Two 4-member equivalence classes
            # Many-to-one training
    
            sLabs = [
                'A1', 'B1', 'C1', 'D1',
                'A2', 'B2', 'C2', 'D2'
            ]
    
            baseline = {
                'Same as': [
                    (1, 0), (2, 0), (3, 0),
                    (5, 4), (6, 4), (7, 4)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
        

        case 'Equivalence 3 4-member MTO':
            sLabs = [
                'A1', 'B1', 'C1', 'D1',
                'A2', 'B2', 'C2', 'D2',
                'A1', 'B3', 'C3', 'D3',
                'A4', 'B4', 'C4', 'D4']
            baseline = {'Same as': [(0,1), (0, 2), (0, 3), # class 1
                                    (4,5), (4,6), (4,7),    # class 2
                                    (8, 9), (8, 10), (8,11) # class 3
                                    ]}
            relTab, derived = deriveRelationsFromBaseline(baseline, sLabs)
            allRels = ["Same as"]
        case 'Equivalence 3 4-member OTM':
            # Three 4-member equivalence classes
            # One-to-many training
    
            sLabs = [
                'A1', 'B1', 'C1', 'D1',
                'A2', 'B2', 'C2', 'D2',
                'A3', 'B3', 'C3', 'D3'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1), (0, 2), (0, 3),
                    (4, 5), (4, 6), (4, 7),
                    (8, 9), (8, 10), (8, 11)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = ['Same as']
    
        case 'Equivalence Linear vs OTM 5-member':
            sLabs = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5']
            baseline = {'Same as': [(0,1), (1, 2), (2, 3), (3,4), # class 1 linear
                                    (5,6), (5,7), (5, 8), (5, 9),  # class 2 OTM
                                    ]}
            relTab, derived = deriveRelationsFromBaseline(baseline, sLabs)
            allRels = ["Same as"]
        case 'Equivalence Linear vs MTO 5-member':

            sLabs = [
                'A1', 'B1', 'C1', 'D1', 'E1',
                'A2', 'B2', 'C2', 'D2', 'E2'
            ]
        
            baseline = {
                'Same as': [
        
                    # Class 1 — linear
                    (0, 1),
                    (1, 2),
                    (2, 3),
                    (3, 4),
        
                    # Class 2 — many-to-one
                    (6, 5),
                    (7, 5),
                    (8, 5),
                    (9, 5)
                ]
            }
        
            n_stim = countUniqueStimuli(baseline)
        
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
        
            allRels = ['Same as']
        case 'Equivalence OTM vs MTO 5-member class':

            sLabs = [
                'A1', 'B1', 'C1', 'D1', 'E1',
                'A2', 'B2', 'C2', 'D2', 'E2'
            ]
        
            baseline = {
                'Same as': [
        
                    # Class 1 — one-to-many
                    (0, 1),
                    (0, 2),
                    (0, 3),
                    (0, 4),
        
                    # Class 2 — many-to-one
                    (6, 5),
                    (7, 5),
                    (8, 5),
                    (9, 5)
                ]
            }
        
            n_stim = countUniqueStimuli(baseline)
        
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
        
            allRels = ['Same as']
        
    
        # ============================================================
        # RFT PRESETS
        # ============================================================
        case 'Steele&Hayes91': # Steele & Hayes set-up
            # Predefined relations/trials
            sLabs = ['A', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'N1', 'N2']
            allRels = ["Same", "Different", "Opposite"] # To be continued
            mRelLabs = ['[S]B1-A', '[S]C1-A', '[O]B3-A', '[O]C3-A']  # Labels for printing
            
            cRelLabs = ['[O]B3-B1', '[O]C3-C1', '[S]B1-C1', '[O]B1-C3',
                        '[S]C3-B3', '[O]B3-C1']
            plot = False
            printRels = False
            baseline = dict({'Same as': [(0,1), (0,4)],
                         'Different from': [(0,3), (0,6)],
                         'Opposite to': [(0,2), (0,5)]})
            n_stim = countUniqueStimuli(baseline)
            if derived is None or derived == 'All':
                relTab, derived = deriveRelationsFromBaseline(baseline, sLabs)                
            elif derived == 'Relnet':
                relTab, derived_all = deriveRelationsFromBaseline(baseline, sLabs)  
                derived = dict({'Same as': [(1,0), (4, 0), (1,4), (4,1), (2,5), (5,2)],
                               'Different from': [(3,0), (6,0), (1, 3), (3, 1), (3, 4), (4, 3), 
                                               (1, 6), (6, 1), (6, 4), (4, 6)],
                               'Opposite to': [(2,0), (5, 0), (1,2), (2, 1), (5, 1), 
                                                  (1, 5), (5, 4), (4, 5), (2, 4), (4, 2)]
                               })
                # if exclusionTest: ## ADD test trials
                #     derived = dict({'Same as': [(1,0), (4, 0), (1,4), (4,1), (3,6), (6,3)],
                #                    'Opposite to': [(2,0), (5, 0), (1,2), (2, 1), (5, 1), 
                #                                       (1, 5), (5, 4), (4, 5), (2, 4), (4, 2)],
                #                    'Different from': [(3,0), (6,0), (1, 3), (3, 1), (3, 4), (4, 3), 
                #                                    (1, 6), (6, 1), (6, 4), (4, 6)]})
            relations = dict({'Same as': 0,
                              'Different from': 1,
                              'Opposite to': 2})
        case 'RFT Comparison More-Less':
            # Comparative relational frame
            #
            # A > B > C > D > E
            #
            # Mutual entailment:
            # B < A, C < B, ...
            #
            # Combinatorial entailment:
            # A > C, A > D, A > E, ...
    
            if sLabs is None:
                sLabs = ['A', 'B', 'C', 'D', 'E']
    
            baseline = {
                'More than': []
            }
    
            for i in range(len(sLabs) - 1):
                baseline['More than'].append(
                    (i, i + 1)
                )
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = [
                'More than',
                'Less than'
            ]
    
    
        case 'RFT Temporal Before-After':
            # Temporal relational frame
            #
            # A before B
            # B before C
            # C before D
            # D before E
    
            if sLabs is None:
                sLabs = ['A', 'B', 'C', 'D', 'E']
    
            baseline = {
                'Before': []
            }
    
            for i in range(len(sLabs) - 1):
                baseline['Before'].append(
                    (i, i + 1)
                )
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = [
                'Before',
                'After'
            ]
    
    
        case 'RFT Hierarchical Contains-PartOf':
            # Hierarchical / containment frame
            #
            # A contains B
            # B contains C
            # C contains D
            #
            # Derivable:
            # A contains C
            # A contains D
            # B contains D
            #
            # and reciprocal "Is part of" relations
    
            if sLabs is None:
                sLabs = ['A', 'B', 'C', 'D']
    
            baseline = {
                'Contains': []
            }
    
            for i in range(len(sLabs) - 1):
                baseline['Contains'].append(
                    (i, i + 1)
                )
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = [
                'Contains',
                'Is part of'
            ]
    
    
        case 'RFT Same-Opposite':
            # Mixed coordination/opposition network
            #
            # A same B
            # B opposite C
            # C same D
            #
            # Tests composition of different relation types
    
            sLabs = [
                'A', 'B', 'C', 'D'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1),
                    (2, 3)
                ],
                'Opposite to': [
                    (1, 2)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = [
                'Same',
                'Opposite'
            ]
    
    
        case 'RFT Same-Different':
            # Mixed coordination/distinction network
            #
            # A same B
            # B different C
            # C same D
    
            sLabs = [
                'A', 'B', 'C', 'D'
            ]
    
            baseline = {
                'Same as': [
                    (0, 1),
                    (2, 3)
                ],
                'Different from': [
                    (1, 2)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            allRels = [
                'Same',
                'Different'
            ]
    
    
        # ============================================================
        # BASIC CONDITIONAL DISCRIMINATION PRESETS
        # ============================================================
    
        case 'Identity Matching':
            # Simple identity matching-to-sample
            #
            # A -> A
            # B -> B
            # C -> C
            # D -> D
            #
            # These are training relations rather than an equivalence
            # derivation procedure.
    
            sLabs = [
                'A', 'B', 'C', 'D'
            ]
    
            baseline = {
                'Same as': [
                    (0, 0),
                    (1, 1),
                    (2, 2),
                    (3, 3)
                ]
            }
    
            n_stim = len(sLabs)
    
            # Construct relation table but do not create derived tests
            relTab, all_derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            derived = {
                'Same as': []
            }
    
            allRels = [
                'Same as'
            ]
    
    
        case 'Arbitrary Conditional Discrimination':
            # Basic arbitrary matching-to-sample
            #
            # A1 -> B1
            # A2 -> B2
            # A3 -> B3
            # A4 -> B4
            #
            # No derived relations are tested by default.
    
            sLabs = [
                'A1', 'A2', 'A3', 'A4',
                'B1', 'B2', 'B3', 'B4'
            ]
    
            baseline = {
                'Same as': [
                    (0, 4),
                    (1, 5),
                    (2, 6),
                    (3, 7)
                ]
            }
    
            n_stim = countUniqueStimuli(baseline)
    
            relTab, all_derived = deriveRelationsFromBaseline(
                baseline,
                sLabs
            )
    
            # Conditional discrimination only:
            # don't automatically test equivalence
            derived = {
                'Same as': []
            }
    
            allRels = [
                'Same as'
            ]
            
    # initialize dicts for storing trial info
    nt_b, nt_t = 0,0
    for i in baseline.keys():
        for j in baseline[i]:
            nt_b += 1
    for i in derived.keys():
        for j in derived[i]:
            nt_t += 1
    nt_b *= n_baseline # Multiply by number of iterations
    nt_t *= n_test
    trial_data = {"relation": np.empty(nt_b + nt_t, dtype=object), # still needed?
                     "cue": np.zeros(nt_b+nt_t, dtype=int),
                     "sample": np.zeros(nt_b+nt_t, dtype=int),
                     "comparisons": np.zeros([nt_b+nt_t, n_comp], dtype=int),
                     "correct": np.zeros(nt_b+nt_t, dtype=int),
                     'tID': np.zeros(nt_b+nt_t, dtype=int),
                     'label': np.empty(nt_b + nt_t, dtype=object),
                     "type": np.empty(nt_b + nt_t, dtype=object),
                     "extra_stimuli": [],
                     "sLabs": sLabs,
                     'baseline': {},
                     'derived': {}
                     }
    extra_stimuli = []
    
    # create derivation tables
    relations = dict({}) # Create relations dict (for creating and indexing tables)
    for i in range(len(baseline.keys())): relations[list(baseline.keys())[i]] = i   
    mutual, combi, cleanRelations = createDerivationTables(relations)
    # First create all unique trials (i.e., different configurations of comparison stimuli)
    unique_scs = [] # init to store unique baseline relations
    unique_cmps = dict() # init to store unique comparison sets
    tr = -1 # counter
    for i in range(len(list(baseline.keys()))):
        for j in range(len(list(baseline.values())[i])):
            
            source = (list(baseline.values())[i][j]) # Store current relation
            relLab = list(baseline.keys())[i] # relation label
            rel = list.index(list(relations.keys()), relLab) # find index
            
            # Find comparison stimulus options
            options = findComparisonOptions(sLabs, relTab, rel, relLab, relations, source)
            
            scc = (source[0], rel, source[1]) # Create tuple to index trial info 
            unique_scs.append([source[0], rel, source[1]]) # Store this trial
            if scc not in list(unique_cmps.keys()):
                unique_cmps[scc] = []
           
            # add comparison stimuli
            new_extra_stimuli  = add_comparison_sets(
                unique_cmps=unique_cmps,
                scc=scc,
                source=source,
                options=options,
                n_comp=n_comp,
                sLabs=sLabs
            )
            for stim in new_extra_stimuli:
                if stim not in extra_stimuli:
                    extra_stimuli.append(stim)   
            
    # Then create trial list by looping over baseline relations, storing trial data,
    # And randomly choosing comparison stimuli
    for t in range(n_baseline): # Loop number of trials per relation
        for r in range(len(list(unique_cmps.keys()))): # Loop relations
            tr += 1
            trial_data['sample'][tr] = unique_scs[r][0] # Store sample
            trial_data['cue'][tr] = unique_scs[r][1] # Store cue index
            trial_data['relation'][tr] = list(baseline.keys())[unique_scs[r][1]] # Store relation
            # Randomly choose a set of comparison stimuli 
            scc = (unique_scs[r][0],unique_scs[r][1], unique_scs[r][2])
            cmp = np.random.choice(np.linspace(0, len(unique_cmps[scc])-1, len(unique_cmps[scc]), dtype = 'int'))
            trial_data['comparisons'][tr] = np.random.permutation(unique_cmps[scc][cmp])
            trial_data['correct'][tr] = unique_scs[r][2] # Correct comparison stored last in sample-cue-comparison list
            trial_data['type'][tr] = 'Baseline'
            trial_data['tID'][tr] = r
            trial_data['label'][tr] = '{} [{}] {} - {}'.format(trial_data['type'][tr],
                                                                allRels[trial_data['cue'][tr]],
                                                                sLabs[trial_data['sample'][tr]],
                                                                sLabs[trial_data['correct'][tr]])
    n_uni_base = len(unique_scs)
    # Do the same for test trials, based on derived relations
    unique_scs = [] # init to store unique baseline relations
    unique_cmps = dict() # init to store unique comparison sets
    for i in range(len(list(derived.keys()))): # loop relations
        for j in range(len(list(derived.values())[i])): # loop instances
            
            source = (list(derived.values())[i][j]) # Store current relation
            relLab = list(derived.keys())[i] # relation label
            rel = list.index(list(relations.keys()), relLab) # find index
            
            # Find comparison stimuli (oter than correct): given sample and cue, find unrelated S
            rels = relTab[rel, source[0], :] != 1 # Find unrelated stimuli
            options = findComparisonOptions(sLabs, relTab, rel, relLab, relations, source)
            scc = (source[0], rel, source[1])
            unique_scs.append([source[0], rel, source[1]])
            
            if scc not in list(unique_cmps.keys()):
                # Create novel key for source relation if not yet in trial list
                unique_cmps[scc] = []
                
            # add comparison stimuli
            new_extra_stimuli  = add_comparison_sets(
                unique_cmps=unique_cmps,
                scc=scc,
                source=source,
                options=options,
                n_comp=n_comp,
                sLabs=sLabs
            )
            for stim in new_extra_stimuli:
                if stim not in extra_stimuli:
                    extra_stimuli.append(stim)

    # Then create trial list by looping over test relations, storing trial data,
    # And randomly choosing comparison stimuli from created set
    for t in range(n_test): # Loop number of trials per derived relation
        for r in range(len(list(unique_cmps.keys()))): # Loop relations
            tr += 1
            trial_data['sample'][tr] = unique_scs[r][0] # Store sample
            trial_data['cue'][tr] = unique_scs[r][1] # Store cue
            trial_data['relation'][tr] = list(derived.keys())[unique_scs[r][1]] # Store cue
            # Randomly choose a set of comparison stimuli 
            scc = (unique_scs[r][0],unique_scs[r][1], unique_scs[r][2])

            cmp = np.random.choice(np.linspace(0, len(unique_cmps[scc])-1, len(unique_cmps[scc]), dtype = 'int'))
            trial_data['comparisons'][tr] = np.random.permutation(unique_cmps[scc][cmp])
            trial_data['correct'][tr] = unique_scs[r][2] # Correct comparison stored last in sample-cue-comparison list  
            # Check if mutually entailed relation is in baseline set,
            mrel = list(cleanRelations.keys())[mutual[relations[trial_data['relation'][tr]]]]
            if mrel in baseline.keys(): # always?
                if (trial_data['correct'][tr], trial_data['sample'][tr]) in baseline[mrel]:
                    trial_data['type'][tr] = 'Mutually entailed'                
                else: # if not, this is combi trial
                    trial_data['type'][tr] = 'Combinatorially entailed'
            trial_data['tID'][tr] = n_uni_base + r
            trial_data['label'][tr] = '{} [{}] {} - {}'.format(trial_data['type'][tr],
                                                                allRels[trial_data['cue'][tr]],
                                                                sLabs[trial_data['sample'][tr]],
                                                                 sLabs[trial_data['correct'][tr]])
    if printTrials:
        # Print baseline/training trials
        for b in range(nt_b):
        
            print_mts_trial(
                trial_data=trial_data,
                idx=b,
                trial_number=b + 1,
                trial_name="Training",
                sLabs=sLabs,
                relations=relations
            )
        
        # Print test trials
        for t in range(nt_t):
        
            idx = nt_b + t
        
            print_mts_trial(
                trial_data=trial_data,
                idx=idx,
                trial_number=t + 1,
                trial_name="Test",
                sLabs=sLabs,
                relations=relations
            )
        
    trial_data["sLabs"] = sLabs
    trial_data["extra_stimuli"] = extra_stimuli
    trial_data["baseline"] = baseline
    trial_data["derived"] = derived
    return trial_data


