# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:01:49 2024

Function that generates symmetry and transitivity table 
    Requires a dict containing source relations as input

@author: mraemaek
"""

# Dependencies
import numpy as np
import pdb

def derivationTablesFromSourceRelations(relations=None):
    
    if relations is None:
        # If no source relations are specified, use default list
        relations = dict({'Same as': 0,
                     'Different from': 1,
                     'Opposite to': 2,
                     'More than': 3,
                     'Less than': 4,
                     'Contains': 5,
                     'Is part of': 6,
                     'Before': 7,
                     'After': 8})
        # And insert default mutually entailed relations
        mutual = [0, 1, 2, 4, 3, 6, 5, 8, 7]
    
    else:
        
        # Also specify variations of relations
        same = ['same', 'same as', "the same as", "is equivalent to"]
        different = ['different', 'different from',"different from"]
        opposite = ['opposite', 'opposite to', 'opposite to']
        more = ["more than", "more", "is more", "is more than", 
                # 'bigger than', "larger", "faster", "stronger", "better",
                # 'after', 'then', # again ??
                ]
        less = ["less than","is less than", "less", 
                # "slower", "weaker", "smaller", "smaller than", # ?? Is rly 'more negative'
                # "before",
                ]
        before = ['Before', 'before', 'is before']
        after = ['After', 'after', 'is after']
        contains = ['Contains', 'contains']
        partof = ['Is part of', 'is part of', 'Part of', 'part of']
        
        # Define different types of relations
        symmetrical = ['Same as', 'Different from', 'Opposite to']
        assymetrical = dict({'More': 'Less',
                             'More than': 'Less than',
                             'Less': 'More',
                             'Less than': 'More than',
                             'Contains': 'Is part of',
                             'Is part of': 'Contains',
                             'Before': 'After',
                             'After': 'Before',
                             'Here': 'There', # Not sure about the deictics?
                             'There': 'Here',
                             'Now': 'Then',
                             'Then': 'Now'})
        # Set default relation labels for compatibility
        relationsClean = dict()
        
        # Update labels/keys to default 
        for i in range(len(list(relations.keys()))):
            # pdb.set_trace()
            if list(relations.keys())[i].lower() in same:
                relationsClean["Same as"] = i
            elif list(relations.keys())[i].lower() in different:
                relationsClean["Different from"] = i
            elif list(relations.keys())[i].lower() in opposite:
                relationsClean["Opposite to"] = i
            elif list(relations.keys())[i].lower() in more:
                relationsClean["More than"] = i
            elif list(relations.keys())[i].lower() in less:
                relationsClean["Less than"] = i
            elif list(relations.keys())[i].lower() in contains:
                relationsClean["Contains"] = i
            elif list(relations.keys())[i].lower() in partof:
                relationsClean["Is part of"] = i
            elif list(relations.keys())[i].lower() in before:
                relationsClean["Before"] = i
            elif list(relations.keys())[i].lower() in after:
                relationsClean["After"] = i
# Need to do the others still
        relations = relationsClean
        
        mutual = []
        for i in range(len(list(relations.keys()))):
            if list(relations.keys())[i] in symmetrical:
                mutual.append(relations[list(relations.keys())[i]]) # add index to list
            else:
                # Find index of relation in assym list
                r = list.index(list(assymetrical.keys()), list(relations.keys())[i])
                rlab = list(assymetrical.values())[r]
                mutual.append(relations[rlab]) # Add to list

    
    # Specify combinatorial relations
    combi = {'Linear': np.zeros([len(relations), len(relations)], dtype = 'int'),
                 'OTM': np.zeros([len(relations), len(relations)], dtype = 'int'),
                 'MTO': np.zeros([len(relations), len(relations)], dtype = 'int'),
                 'sMTO': np.zeros([len(relations), len(relations)], dtype = 'int')}

    
    for i in range(len(combi.keys())):
        for rel1 in range(len(relations.keys())):
            for rel2 in range(len(relations.keys())):
                if rel1 == rel2:
                    if list(relations.keys())[rel1] == 'Different from':
                        # Difference relations combined are ill -defined
                        combi['Linear'][rel1, rel2] = -1 
                        combi['OTM'][rel1, rel2] = -1 
                        combi['MTO'][rel1, rel2] = -1 
                        combi['MTO'][rel1, rel2] = -1                         
                    elif list(relations.keys())[rel1] == 'Opposite to':
                        # Opposition relations combine to equialence
                        combi['Linear'][rel1, rel2] = 0
                        combi['OTM'][rel1, rel2] = 0
                        combi['MTO'][rel1, rel2] = 0
                        combi['sMTO'][rel1, rel2] = 0
                    elif list(relations.keys())[rel1] == 'Same as':
                        # Difference relations combined are ill -defined
                        combi['Linear'][rel1, rel2] = 0
                        combi['OTM'][rel1, rel2] = 0
                        combi['MTO'][rel1, rel2] = 0
                        combi['sMTO'][rel1, rel2] = 0
                    else: # Other relations 
                        combi['Linear'][rel1, rel2] = rel1
                        combi['OTM'][rel1, rel2] = -1
                        combi['MTO'][rel1, rel2] = -1
                        combi['sMTO'][rel1, rel2] = mutual[rel1]

                if list(combi.keys())[i] == 'OTM': # Specific cases
                    if not rel1 == rel2:
                        if rel1 == 0: # If one of the relations is equivalence,
                            combi['OTM'][rel1, rel2] = rel2
                        elif rel2 == 0:
                            if not list(relations.keys())[rel1] in ['Same as', 'Different from', 'Opposite to']:
                                combi['OTM'][rel1, rel2] = mutual[rel1]
                            else:
                                combi['OTM'][rel1, rel2] = rel1
                        else:
                            combi['OTM'][rel1, rel2] = -1
                            if not (list(relations.keys())[rel1] in ['Same as', 'Different from', 'Opposite to']):
                                if not(list(relations.keys())[rel2] in ['Same as', 'Different from', 'Opposite to']):
                                    if rel1 - rel2 == 1:
                                        combi['OTM'][rel1, rel2] = rel2
                                    elif rel2 - rel1 == 1: 
                                        combi['OTM'][rel1, rel2] = rel2
                                    else:
                                        combi['OTM'][rel1, rel2] = -1

                if list(combi.keys())[i] == 'MTO':
                    if not rel1 == rel2:
                        if rel1 == 0: # If one of the relations is equivalence,
                            if not list(relations.keys())[rel1] in ['Same as', 'Different from', 'Opposite to']:
                                combi['MTO'][rel1, rel2] = mutual[rel2]
                            else:
                                combi['MTO'][rel1, rel2] = rel2
                        elif rel2 == 0:
                            combi['MTO'][rel1, rel2] = rel1
    
                        else:
                            combi['MTO'][rel1, rel2] = -1
                            if not (list(relations.keys())[rel1] in ['Same as', 'Different from', 'Opposite to']):
                                if not(list(relations.keys())[rel2] in ['Same as', 'Different from', 'Opposite to']):
                                    if rel1 - rel2 == 1:
                                        combi['MTO'][rel1, rel2] = rel1
                                    elif rel2 - rel1 == 1: 
                                        combi['MTO'][rel1, rel2] = rel1
                                    else:
                                        combi['MTO'][rel1, rel2] = -1
                if list(combi.keys())[i] == 'sMTO':
                    if not rel1 == rel2:
                        if 0 in (rel1, rel2): # If one of the relations is equivalence,
                            if not list(relations.keys())[rel1] in ['Same as', 'Different from', 'Opposite to']:
                                combi['sMTO'][rel1, rel2] = mutual[rel1]
                                combi['sMTO'][rel2, rel1] = mutual[rel1]
                            else:
                                combi['sMTO'][rel1, rel2] = rel1    
                                combi['sMTO'][rel2, rel1] = rel1

                        else:
                            combi['sMTO'][rel1, rel2] = -1
                if list(combi.keys())[i] == 'Linear':
                    if not rel1 == rel2:
                        if rel1 == 0: # If one of the relations is equivalence,
                            # The derived relation defaults to the other relation
                            combi['Linear'][rel1, rel2] = rel2
                        elif rel2 == 0:
                            combi['Linear'][rel1, rel2] = rel1
                        else:
                            combi['Linear'][rel1, rel2] = -1

    return mutual, combi

# %%

relations = dict({'Same as': 0,
             'Different from': 1,
             'Opposite to': 2,
             'More than': 3,
             'Less than': 4,
             'Contains': 5,
             'Is part of': 6,
             'Before': 7,
             'After': 8})
derivationTablesFromSourceRelations(relations)
