# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 12:49:38 2026

Personal functions to improve efficiency and readability of the derivation
tables and their applications.

@author: mraemaek
"""

# %% dependencies

import numpy as np
import pdb
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple


# %% cleanRelations - Convert input list of 'dirty' relation labels to 'clean' dict

def cleanRelationLabels(relations):
    
    """ 
    Converts 'dirty' input relations list to dict with 'clean' relation labels.
    
    Args: 
        relations: list of input relations
        relVariants: dict with common variants of supported relations
        
    Returns: 
        relations: dict with clean relation labels as keys and zero-based indices 
                    for derivation tables as values
    """
    
    cleanVariants = {'Same as': 'same',
                        'Different from': 'different',
                        'Opposite to': 'opposite',
                        'More than':  "more", 
                        'Bigger than': 'bigger',
                        'Larger than': "larger", 
                        'Faster than': "faster", 
                        'Stronger than': "stronger",
                        'Better than': "better", 
                        'Longer than': "longer", # any comparative relation
                        'Less than': "less", 
                        'Smaller than': "smaller", 
                        'Slower than': "slower", 
                        'Weaker than': "weaker", 
                        'Worse than': "worse", 
                        'Shorter than': "shorter",
                        'Before': 'before',
                        'After': 'after',
                        'Contains': 'contains',
                        'Is part of': 'part', 
                        'Left of': 'left',
                        'Right of': 'right',
                        'In front': 'front',
                        'Behind': 'behind'} 

    
    cleanRelations = dict()
    useableRelations = dict()
    rel_id = -1 # init relation index
    for rel in relations: # loop input relations list
        rel_id +=1
        
        for clean, dirty in cleanVariants.items(): # also store a clean version of input
            if dirty in rel.lower(): cleanRelations[clean] = rel_id
            
    return cleanRelations

# %% findGenericRelations - converts specific relations (e.g. taller) to general (more)

def findGeneralRelations(relations):
    
    """
    For a given list of input relations, finds the general patterns that they 
    are instances of. E.g., 'taller' is an instance of 'more than'.
    
    Args:
        relations: dict, relation labels as keys, tuples of stimulus indices as values
        
    Returns:
        defaultRelations: dict with same information as input 'relations',
        but now with relation labels (keys) adapted to specify the general patterns,
        so they can be used for derivation downstream.
        
    """
    default2specific = dict({'Same as': ['same', "equivalent", "identical",
                                    # more?
                                    ],
                        'Different from': ['different', 'non-equivalent', 'non-identical'],
                        'Opposite to': ['opposite'],
                        'More than':  ["more", 'bigger', "larger", "faster", 
                                       "stronger", "better", "longer", # any comparative relation
                                       'right', 'in front'
                                       # 'after', # could add temporal here too, but then need to remove the before/after lists
                                ],
                        'Less than': ["less", "smaller", "slower", "weaker", "worse", "shorter",
                                      'left', 'behind'
                                      # "before",
                                      
                                ],
                        'Before': ['Before', 'before', 'is before'],
                        'After': ['After', 'after', 'is after'],
                        'Contains': ['contains', 'includes', 'Includes'],
                        'Is part of': ['part of', 
                                       'example', # is an example of ...
                                       'type' # is a type of ...
                                       ]
                        })
    defaultRelations = {}
    rel_id = -1
    for rel in relations.keys(): # loop input relations
        rel_id +=1
        for defaults, variants in default2specific.items(): # find the correct gerenal relational pattern
            for variant in variants:
                if variant in rel.lower(): 
                    # create a new label to store in new dict, with general relation
                    # accounting for multiple instances of same general pattern
                    relLab = str(defaults) + ' - ' + str(rel)
                    defaultRelations[relLab] = rel_id
    return defaultRelations
# %% completeRelations - complete list of input relations with missing derived relations

def completeRelations(relations, assymetrical):
    """
    For a given set (list) of input relations, checks whether the derived 
    relations are also included. If not, this will lead to indexing problems, 
    so add them to the list before creating derivation tables.
    
    Args: 
        relations: list, strings representing relations
        assymetrical: dict, input relations as keys, mutually entailed relation
                        as values.
                        
    Returns:
        relations: dict
    """
    updatedRels = dict()
    for i in relations.keys():
        updatedRels[i] = len(list(updatedRels.keys())) # add input relations
        if i in assymetrical:  # find mutually entailed relation in assymetrical dict
            mutlab = assymetrical[i] # get label for mutual
            if assymetrical[i] not in relations.keys(): # check if mutually entailed relation is in 
                updatedRels[assymetrical[i]] = len(list(updatedRels.keys())) # if not, add it
                # (i.e., mutually entailed of the now newly added relation, 
                # otherwise dimensions don't match)
                
    relations = updatedRels # update dict
    
    # in the exceptional case that only opposition relations are included in input, 
    # and not equivalence, add equivalence to 'relations' dict so combinatorial 
    # entailment of opposition relations can be done
    if 'Opposite to' in relations.keys() and 'Same as' not in relations.keys():
        relations['Same as'] = len(relations.keys()) # add 'Same as'
    
    return relations



# %% findCommon - Find common relata in combination of two relations

def findCommon(source1, source2):
    """ 
    Finds the common relata in two input relations.
    
    Args:
        source1 - tuple containing two indices for related stimuli
        source2 - 
        
    Returns:
        common: index of the common stimulus, returns -1 if no common element
    """
    
    # Find common element
    common = -1
    for sr1 in source1:
        for sr2 in source2:
            if sr1 == sr2:
                common = sr2  
                
    return common
    
    
# %% deriveCombi - Find combinatorially entailed relation for a pair of relations

def deriveCombi(source1, source2, common, rel1, rel2, combi):
    """
    
    Uses derivation tables to derive the combinatorially entailed relation for
    combination of two provided relations.
    Derivation depends on combination of relations, and of the position of the
    common element (i.e., the order of relata -> combination type: linear, OTM, MTO, sMTO)
    
    Args:
        source1: tuple containing indices of two related stimuli
        source2: tuple containing indices of second pair of related stimuli
        common: index of the stimulus that is common between source1 and source2
        rel1:
        rel2:
        
    Returns:
        crel: int - the index of the combinatorially entailed relation in the
                    derivation tables
        source12: tuple, pair of stimuli related by derived relation
    """
    
    if tuple.index(source1, common) == 0:
        if tuple.index(source2, common) == 0: # A-B & A - C (OTM)
            crel = combi['OTM'][rel1, rel2]
            source12 = (source1[1], source2[1])

        else: # A - B & C - A (sort of MTO)
            crel = combi['sMTO'][rel1, rel2]
            source12 = (source1[1], source2[0])
    else:
        if tuple.index(source2, common) == 0: # A-B & B - C (linear)
            crel = combi['Linear'][rel1, rel2]
            source12 = (source1[0], source2[1])
        else: # A-B & C- B (MTO)
            crel = combi['MTO'][rel1, rel2]
            source12 = (source1[0], source2[0])

    return crel, source12
    
# %% determineProtocol - determine combination protocol (linear, reversed linear, OTM, MTO)

def determineProtocol(source1, source2, common):
    """
    Determines the protocol (linear, reversed linear)
    
    Args:
        source1: tuple containing indexes of two related stimuli
        source2: tuple containing indexes of second pair of related stimuli
        common: index of the common element in both relations (findCommon function output)
    """
    # check each relation to find location of common element & protocol
    if tuple.index(source1, common) == 0:
        if tuple.index(source2, common) == 0: # AxB and AxC
            protocol = 'OTM' # One-to-many
        else: # AxB and CxA
            protocol = 'sMTO'
    else: 
        if tuple.index(source2, common) == 0: # AxB and BxC
            protocol = 'Linear'
        else: # AxB and CxB
            protocol = 'MTO'
    return protocol

# %% countUniqueStimuli - Find number of unique stimuli in 'baseline' network

def countUniqueStimuli(baseline):
    
    """
    For a given set of baseline relations, finds the number of unique stimuli 
    that make up the relational network.
    
    Args:
        baseline: a dict with relation labels as keys, and a list of tuples 
        (stimulus pairs) that represent the different instances of that relation
        
    Returns:
        n_stim: int, the number of unique stimuli in the network
    
    """
    
    unique = []
    for i,j in baseline.items():
        for jj in j:
            for stim in jj:
                if stim not in unique: unique.append(stim)
    n_stim = len(unique)
    return n_stim

# %% createRelationTable - Create relTab for heatmap plot of relational network

def createRelationTable(baseline, derived=None):
    """
    Creates an array that represents a relational network input by the user.
    Used for plotting network as a heatmap.
    
    Args:
        baseline: dict, keys are relation labels, values are list of tuples 
                        that represent pairs of related stimluli
        derived: optional similar dict of derived relations
    Returns: 
        relTab: numpy array of dimensions relations x stimuli x stimuli, 
            where value of 1 represents that those stimuli are related, and a
            value 0 represents not related.
    """
    # Get dimensions to initialize table
    unique_rels = []
    for base in baseline.keys():
        if base not in unique_rels: unique_rels.append(base)
        
    if derived is not None:
        for der in derived.keys():
            if der not in unique_rels: unique_rels.append(der)
    n_rel = len(unique_rels) # number of unique relations
    relations = cleanRelationLabels(unique_rels) # get relations dict
    n_stim = countUniqueStimuli(baseline)  # find number of unique stimuli
    relTab = np.zeros([n_rel, n_stim, n_stim], dtype = 'int') # Tabular version of dict
    
    for rel, instances in baseline.items():
        rel_id = relations[rel]
        for instance in instances:
            relTab[rel_id, instance[0], instance[1]] = 1
    if derived is not None:
        for rel, instances in derived.items():
            rel_id = relations[rel]
            for instance in instances:
                relTab[rel_id, instance[0], instance[1]] = 1
                
    return relTab

