# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:38:11 2026

Newer version of function that generates symmetry and transitivity tables for 
given set of relations.
Tables can then be used for automatic derivation, task generation, etc..

Changes relative to old version:
    - Just takes a list as input, not dict (more user-friendly?)
    - Can take individual items from paired relations and complete the pair
        (e.g., if only 'more than' included in input, output will include
         both more than and less than)
    - Made code robust against variable inputs (e.g., same not included, so not index 0)
    - Added plotting functionality
    
Input:
    - 'Relations': (optional) list of strings specifying to-be-included relations 
        All supported relations are included if no input is provided
        Currently supports:
            - Same as
            - Different from
            - Opposite to
            - More than & Less than
            - Contains & Is part of
            - Before & After
    
Output:
    - mutual: 
        list that contains the (indices) of the relations that are mutually 
        entailed by those provided in input
        e.g., [0, 1, 2]
        
        
    - combi: 
        a dict containing four arrays, one for each way two relations can be combined,
        each containing the combinatorially entailed relations (indices)
        for all possible combinations of the relations provided in input
        e.g., [0, 1, 2;
               1, -1, -1;
               2, -1, 0]
        
TO DO:
    - Account for entailed relations not included in input
        (e.g., sameness if only opposition included)
    - Add more relations
        e.g. other relations that follow same type of derivations 
    - Add shorter relation-labels for plot
    - subplots for combi heatmap -> one instead of four
        
@author: mraemaek
"""

# Dependencies
import numpy as np
from utils import *
from plot_utils import *
import pandas as pd
import pdb


def createDerivationTables(relations=None, *, plotTables=False):
    # Define different types of relations (mutual entailment)
    symmetrical = ['Same as', 'Different from', 'Opposite to']
    assymetrical = dict({'More than': 'Less than',
                            'Less than': 'More than',
                            'Bigger than': 'Smaller than',
                            'Larger than': 'Smaller than', 
                            'Faster than': "Slower than", 
                            'Stronger than': "Weaker than",
                            'Better than': "Worse than", 
                            'Longer than': "Shorter than",
                            'Smaller than': 'Larger than', 
                            'Slower than': "Faster than", 
                            'Weaker than': "Stronger than", 
                            'Worse than': "Better than", 
                            'Shorter than': "Longer than",
                            'Contains': 'Is part of',
                            'Is part of': 'Contains',
                            'Before': 'After',
                            'After': 'Before',
                            'Here': 'There', # Not sure about the deictics?
                            'There': 'Here',
                            'Now': 'Then',
                            'Then': 'Now'})
    
    compatible = {'Same as': [], # anything really
                 'Different from': ['Same as', 'Different from', 'Opposite to'],
                 'Opposite to': ['Same as', 'Different from', 'Opposite to'],
                 'More than': ['Less than', 'More than'],
                'Less than': ['Less than', 'More than'],
                'Bigger than': ['Bigger than', 'Smaller than'],
                'Larger than': ['Larger than', 'Smaller than'], 
                'Faster than': ['Faster than', "Slower than"], 
                'Stronger than': ['Stronger than', "Weaker than"],
                'Better than': ['Better than', "Worse than"], 
                'Longer than': ["Shorter than", 'Longer than'],
                'Smaller than': ['Larger than', 'Smaller than'],
                'Slower than': ["Faster than", 'Slower than'],
                'Weaker than': ["Stronger than",'Weaker than'] ,
                'Worse than': ["Better than", 'Worse than'],
                'Shorter than': ["Longer than",'Shorter than'],
                'Contains': ['Is part of', 'Contains'],
                'Is part of': ['Contains', 'Is part of'],
                'Before': ['After', 'Before'],
                'After': ['Before', 'After'], 
        }
    if relations is None:
        # If no source relations are specified, use default list 
        # (default = all currently supported relations)
        cleanRelations = dict({'Same as': 0,
                     'Different from': 1,
                     'Opposite to': 2,
                     'More than': 3,
                     'Less than': 4,
                     'Contains': 5,
                     'Is part of': 6,
                     'Before': 7,
                     'After': 8
                     }) 
        relations =  dict({'Same as - Same as': 0,
                     'Different from - Different from': 1,
                     'Opposite to - Opposite to': 2,
                     'More than - More than': 3,
                     'Less than - Less than': 4,
                     'Contains - Contains': 5,
                     'Is part of - Is part of': 6,
                     'Before - Before': 7,
                     'After - After': 8
                     }) # immediately put into dict
        # And insert default mutually entailed relations
        mutual = [0, 1, 2, 4, 3, 6, 5, 8, 7]

    else:
        # if (a list of) relations is specified, clean labels
        cleanRelations = cleanRelationLabels(relations)
        
        # add missing mutually or combinatorially entailed relations
        cleanRelations = completeRelations(cleanRelations, assymetrical)
        
        # convert to clean default relational pattern labels for derivation table rules
        relations = findGeneralRelations(cleanRelations)
        

    # Create list of mutually entailed relations based on input (or default)
    mutual = []
    for i in relations.keys():
        if ' -' in i:
            relLab = i[i.index('- ')+2:]
        else: relLab = i
        if relLab in symmetrical:  # Check whether relation is symmetrical
            mutual.append(relations[i]) # add index to list
        else:  # If not, find mutually entailed relation in assymetrical dict
            mutlab = assymetrical[relLab] # get label for mutual
            mutual.append(cleanRelations[mutlab])  # add index to list
    
    # Specify combinatorially entailed relations for all combinations of input rels
    # Four possible orders of relata in combination of two relations (with common element)
    combi = dict({'Linear': np.zeros([len(relations), len(relations)], dtype = 'int'),
                'sMTO': np.zeros([len(relations), len(relations)], dtype = 'int'),
                'OTM': np.zeros([len(relations), len(relations)], dtype = 'int'),
                'MTO': np.zeros([len(relations), len(relations)], dtype = 'int')
                })
    
    for i in combi.keys(): # loop possible combinations
        for r1lab, rel1 in relations.items():
            for r2lab, rel2 in relations.items(): # loop relationss
                # if rel1 == 1 and rel2 == 1: pdb.set_trace()
                # if rel1 == 2 and rel2 == 2: pdb.set_trace()
                cleanR1 = r1lab[r1lab.index('- ')+ 2:]
                cleanR2 = r2lab[r2lab.index('- ')+2:]
                if not ('Same as' in cleanR1 or 'Same as' in cleanR2) and \
                    cleanR1 not in compatible[cleanR2]: # 'Same' is compatible with anything
                        # exclude incompatible combinations
                        combi['Linear'][rel1, rel2] = -1 
                        combi['OTM'][rel1, rel2] = -1 
                        combi['MTO'][rel1, rel2] = -1 
                        combi['sMTO'][rel1, rel2] = -1   
                else: 
                    if rel1 == rel2: 
                        # If two identical relations are combined, some special cases
                        if 'Different from' in r1lab:
                            # Two difference relations combined always result in 
                            # ill-defined derived relation
                            combi['Linear'][rel1, rel2] = -1 
                            combi['OTM'][rel1, rel2] = -1 
                            combi['MTO'][rel1, rel2] = -1 
                            combi['sMTO'][rel1, rel2] = -1                         
                        elif 'Opposite to' in r1lab: 
                            # Two opposition relations combined result in derived equivalence
                            combi['Linear'][rel1, rel2] = relations['Same as - Same as']
                            combi['OTM'][rel1, rel2] = relations['Same as - Same as']
                            combi['MTO'][rel1, rel2] = relations['Same as - Same as']
                            combi['sMTO'][rel1, rel2] = relations['Same as - Same as']
                        elif 'Same as' in r1lab:
                            # Two sameness relations alwasy produce more sameness
                            combi['Linear'][rel1, rel2] = relations['Same as - Same as']
                            combi['OTM'][rel1, rel2] = relations['Same as - Same as']
                            combi['MTO'][rel1, rel2] = relations['Same as - Same as']
                            combi['sMTO'][rel1, rel2] = relations['Same as - Same as']
                        else: 
                            # If two other, assymmetrical relations are combined,
                            # derivation depends on order
                            combi['Linear'][rel1, rel2] = rel1
                            combi['OTM'][rel1, rel2] = -1
                            combi['MTO'][rel1, rel2] = -1
                            combi['sMTO'][rel1, rel2] = mutual[rel1] # reverse linear
                    else: 
                        # If two non-identical relations are combined, derivations depend 
                        # on the particular relation involved and on the order of relata
                        if i == 'OTM': # One-to-many (AxB and AxC)
                            if 'Same as' in r1lab: 
                                # If AxB is equivalence, BxC (derived) is same relation as AxC
                                combi[i][rel1, rel2] = rel2
                            elif 'Same as' in r2lab:
                                # If AxC is 'same', BxC (derived) is same relation
                                # as AxB if symmetrical, otherwise BxC is the 
                                # mutually entailed relation of AxB
                                if cleanR1 in assymetrical.keys():
                                    combi[i][rel1, rel2] = mutual[rel1]
                                else:
                                    combi[i][rel1, rel2] = rel1
                            else: # If neither relation is 'same'
                                # and if relation AxB is the mutually entailed 
                                # relation of AxC (e.g., A more than B, A less than C)
                                # then BxC is the second relation (B less than C)
                                if mutual[rel1] == rel2: 
                                    combi[i][rel1, rel2] = rel2
                                else: # otherwise it is (always) ill-defined
                                    combi[i][rel1, rel2] = -1
                        if i == 'MTO': # Many-to-one (AxB and CxB -> derive AxC)
                            # note that this is the reverse logic of OTM
                            if 'Same as' in r1lab: 
                                if cleanR1 in assymetrical.keys():
                                    # If AxB is equivalence, AxC (derived) is mutual of CxB
                                    # for assymmetrical relations
                                    combi[i][rel1, rel2] = mutual[rel2]
                                else: # AxC is the same as CxB for symmetrical relations
                                    combi[i][rel1, rel2] = rel2
                            elif 'Same as' in r2lab:
                                # If CxB is 'same', AxC (derived) is same as AxB
                                combi[i][rel1, rel2] = rel1
                            else: # if neither is 'same'
                                # and if relation AxB is the mutually entailed 
                                # relation of CxB (e.g., A more than B, C less than B)
                                # then AxC is the first relation (A more than C)
                                if mutual[rel1] == rel2: # for 2 assymetrical mutually entailed relations (in a pair, e.g., more and less), combination depends on order
                                    combi['MTO'][rel1, rel2] = rel1
                                else: # else, it is ill-defined
                                    combi['MTO'][rel1, rel2] = -1
                        if i == 'sMTO': # reversed linear combination (AxB and CxA -> derive BxC)
                            if 'Same as' in r1lab: # If AxB is 'same'
                                if cleanR2 in assymetrical.keys():
                                    # for assymmetrical relations, derived BxC is mutual of AxB
                                    combi[i][rel1, rel2] = mutual[rel2]
                                else: # for symmetrical relations, it is same as AxB
                                    combi[i][rel1, rel2] = rel2
                            elif 'Same as'in r2lab: # If CxA is 'same'
                                if cleanR1 in assymetrical.keys():
                                    combi[i][rel1, rel2] = mutual[rel1]
                                else: # for symmetrical relations, it is same as AxB
                                    combi[i][rel1, rel2] = rel1    
                            else: # if neither relation is 'same', derived will always be ill-defined
                                combi[i][rel1, rel2] = -1
                        if i == 'Linear': # linear combination (AxB and BxC -> derive AxC)
                            # if either relation is 'same', derived relation always
                            # defaults to the other relation
                            if 'Same as'in r1lab: 
                                combi[i][rel1, rel2] = rel2
                            elif 'Same as' in r2lab:
                                combi[i][rel1, rel2] = rel1
                            else:
                                combi[i][rel1, rel2] = -1
    if plotTables: # Plot derivation tables as heatmaps
        plotTablesHeatmap(cleanRelations, mutual, combi)
        # use clean input labels for plot

    return mutual, combi, cleanRelations # return clean, og input relations

