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
from deriveRelationsFromBaseline import deriveRelationsFromBaseline
from derivationTablesFromSourceRelations import derivationTablesFromSourceRelations

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
            # if n_rel == 1: # catch labeling error WIP ()
            #     if len(s_mp) > len(srel_mp)+n_comps:
            #         print('Warning Please add more stimuli to serve as comparison stimuli!')
            #         pdb.set_trace()
            plot = False
            printRels = False
            if sLabs is None:
                sLabs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                         'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 
                         'W', 'X', 'Y', 'Z'] # Default to fall back on
            if derived is None or derived == 'All':
                relTab, derived = deriveRelationsFromBaseline(baseline, plot, 
                                                       printRels, n_stim, sLabs)
            else:
                relTab, derived = deriveRelationsFromBaseline(baseline, plot, 
                                                       printRels, n_stim, sLabs)
            
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
        case 'SH91': # Steele & Hayes set-up
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
            unique = [] # find number of unique stimuli for array dimensions
            for i in baseline.keys(): 
                for j in baseline[i]: 
                    for s in j: 
                        if s not in unique: unique.append(s)
            n_stim = len(unique)
            if derived is None or derived == 'All':
                relTab, derived = deriveRelationsFromBaseline(baseline, plot, 
                                                      printRels, n_stim, sLabs)                
            elif derived == 'Relnet':
                relTab, derived_all = deriveRelationsFromBaseline(baseline, plot, 
                                                      printRels, n_stim, sLabs)  
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
        case 'TransitiveInference':
            baseline = dict({'More Than': []})
            for i in range(n_stim):
                baseline['More Than'].append((i, i+1))  
            
            if derived is None: # Test all derived relations is not specified
                relTab, derived = deriveRelationsFromBaseline(baseline, plot, 
                                                      printRels, n_stim, sLabs)
            elif derived == 'nonAdjacent':
                derived = dict({'More Than': [(0,2), (0,3), (0,4), (1,3), (1,4), (2, 4)]})
            
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
                     "type": np.empty(nt_b + nt_t, dtype=object)}
    
    relations = dict({}) # Create relations dict (for creating and indexing tables)
    for i in range(len(baseline.keys())): relations[list(baseline.keys())[i]] = i   
    mutual, combi = derivationTablesFromSourceRelations(relations)
    # First create all unique trials (i.e., different configurations of comparison stimuli)
    unique_scs = [] # init to store unique baseline relations
    unique_cmps = dict() # init to store unique comparison sets
    tr = -1 # counter
    for i in range(len(list(baseline.keys()))):
        for j in range(len(list(baseline.values())[i])):
            
            source = (list(baseline.values())[i][j]) # Store current relation
            relLab = list(baseline.keys())[i] # relation label
            rel = list.index(list(relations.keys()), relLab) # find index
            # Find comparison stimuli (other than correct): given sample and cue, find unrelated S
            rels = relTab[rel, source[0], :] != 1 # Find non-rels in table
            options = [] # init 
            for o in range(len(rels)): # Loop stimuli
                if rels[o]: 
                    if not o == source[0]: # Select and add to option list if valid
                        options = [*options, o] # Store possible comparison index
            
            scc = (source[0], rel, source[1]) # Create tuple to index trial info 
            unique_scs.append([source[0], rel, source[1]]) # Store this trial
            if scc not in list(unique_cmps.keys()):
                unique_cmps[scc] = []
            
            if n_comp == 2:
                for c2 in range(len(options)): # find a second comparison
                    if not options[c2] in source: # exclude two identical comparisons
                        unique_cmps[scc].append([source[1], options[c2]])
            if n_comp == 3:
                for c2 in range(len(options)-1): # Find second comparison
                    for c3 in range(len(options[c2:])): # Find third comparison
                        if c3 == 0: # account for zero-indexing to get second S from list
                            unique_cmps[scc].append([source[1], options[c2], options[c2+c3+1]])
                        else:
                            unique_cmps[scc].append([source[1], options[c2], options[c2+c3]])
            # Can add more comparison stimuli, but not needed for now?
                
            # !!! ADD Clause for no opposite/comparative comparisons if difference relation
            
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
            options = []
            for o in range(len(rels)): # Loop stimuli
                if rels[o]: 
                    if not o == source[0]: # Only store valid
                        options = [*options, o] # Store possible comparison index
#            pdb.set_trace()
            scc = (source[0], rel, source[1])
            unique_scs.append([source[0], rel, source[1]])
            
            if scc not in list(unique_cmps.keys()):
                # Create novel key for source relation if not yet in trial list
                unique_cmps[scc] = []
            if n_comp == 2:
                for c2 in range(len(options)): # find a second comparison
                    if not options[c2] in source: # exclude two identical comparisons
                        unique_cmps[scc].append([source[1], options[c2]])
            if n_comp == 3:
                for c2 in range(len(options)-1): # Find second comparison
                    for c3 in range(len(options[c2:])): # Find third comparison
                        if c3 == 0: # account for zero-indexing to get second S from list
                            unique_cmps[scc].append([source[1], options[c2], options[c2+c3+1]])
                        else:
                            unique_cmps[scc].append([source[1], options[c2], options[c2+c3]])

            # Can add more comparison stimuli, but not needed for now?
                

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
            mrel = list(relations.keys())[mutual[list.index(list(relations.keys()),trial_data['relation'][tr])]]
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
        # Print trials (for now assuming 3 comparison stimuli)
        for b in range(nt_b): # Loop baseline trials
            if n_comp == 2: # find a better solution so any number is accounted for!!
                print('\n Training Trial {} (#{}, {}): Sample stimulus {} is {} {} or {}? \n\nCorrect answer is {}!'.format(
                        b+1, trial_data['tID'][b], trial_data['type'][b],
                        sLabs[trial_data['sample'][b]], 
                        list(relations.keys())[trial_data['cue'][b]],
                        sLabs[trial_data['comparisons'][b][0]],
                        sLabs[trial_data['comparisons'][b][1]],
                        sLabs[trial_data['correct'][b]]))
            elif n_comp == 3:
                print('\n Training Trial {} (#{}, {}): Sample stimulus {} is {} {}, {} or {}? \n\nCorrect answer is {}!'.format(
                        b+1, trial_data['tID'][b], trial_data['type'][b],
                        sLabs[trial_data['sample'][b]], 
                        list(relations.keys())[trial_data['cue'][b]],
                        sLabs[trial_data['comparisons'][b][0]],
                        sLabs[trial_data['comparisons'][b][1]],
                        sLabs[trial_data['comparisons'][b][2]],
                        sLabs[trial_data['correct'][b]]))
            
        for t in range(nt_t): # Loop trials
            if n_comp == 2:
                print('\n Test Trial {} (#{}, {}): Sample stimulus {} is {} {} or {}? \n\nCorrect answer is {}!'.format(
                        t+1, trial_data['tID'][nt_b+t], trial_data['type'][nt_b+t],
                        sLabs[trial_data['sample'][nt_b+t]], 
                        list(relations.keys())[trial_data['cue'][nt_b+t]],
                        sLabs[trial_data['comparisons'][nt_b+t][0]],
                        sLabs[trial_data['comparisons'][nt_b+t][1]],
                        sLabs[trial_data['correct'][nt_b+t]]))
            elif n_comp == 3:
                print('\n Test Trial {} (#{}, {}): Sample stimulus {} is {} {}, {} or {}? \n\nCorrect answer is {}!'.format(
                        t+1, trial_data['tID'][nt_b+t], trial_data['type'][nt_b+t],
                        sLabs[trial_data['sample'][nt_b+t]], 
                        list(relations.keys())[trial_data['cue'][nt_b+t]],
                        sLabs[trial_data['comparisons'][nt_b+t][0]],
                        sLabs[trial_data['comparisons'][nt_b+t][1]],
                        sLabs[trial_data['comparisons'][nt_b+t][2]],
                        sLabs[trial_data['correct'][nt_b+t]]))

    return trial_data


