# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:12:50 2024

@author: mraemaek

Function that derives all entailed relations from a given set of baseline relations

Uses transitivity tables which can be constructed using another function.

Prameters:
    - 'baseline': a dict containting tuples that represent the relata for 
                    baseline relations to derive from, the relation 
                    e.g., dict({'Same as':[(0, 1)]; 'Different from': [0, 2]})
    - 'plot': True/False - option to plot relations as stimulus-by-stimulus 
                            heatmap for each relation (replace with network plotter)
    - 'printRels': True/False -  to print out the 'reasoning steps' involved in the process
    - 'sLabs': list of labels for the stimuli (can be longer than n_stim)


TO DO:
    - Plotting errors when only one relation and order of derived /baseline is not same?
        FIXED
    - Proper testing with all kinds of relations


    - add network plotter
    



"""

# Given a set of stimuli and baseline relations, compute derived relations 

# Dependencies
import numpy as np
import matplotlib.pyplot as plt
# from derivationTablesFromSourceRelations import derivationTablesFromSourceRelations
from createDerivationTables import createDerivationTables # to create derivation tables for input relations
from utils import * # helper functions
from plot_utils import *
import pdb


def deriveRelationsFromBaseline(baseline, sLabs = None, illustrate = None):
    
    
    if sLabs is None or len(sLabs) == 0 : # use default labels if not specified by user
        sLabs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    # fetch relations from baseline dict input
    relations = cleanRelationLabels(list(baseline.keys()))
    mutual, combi, relations = createDerivationTables(list(baseline.keys()))
    relation_list = list(relations.keys())
    derived = dict() # initialize dict for derived relations
    for i in relations.keys():
        derived[i] = [] # ensure same order  & all relations accounted for
    
    for rel1Lab, source1_instances in baseline.items(): # Loop relations
        rel1 = relations[rel1Lab]
        for source1 in source1_instances: # Loop specific relation instances

            # Find mutually entailed relation in predefined list
            mrel = mutual[rel1] 
            mrelLab = list(relations.keys())[mrel] # label
            
            if illustrate == 'printRels': # For illustration, print baseline relation, then derived
                print('{} is {} {}. \nFrom that, I can derive that {} is {} {}'.format(
                          sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                          sLabs[source1[1]], mrelLab, sLabs[source1[0]]))
                        
            # if mrelLab not in derived.keys():
            #     # If derived relation not in baseline rels, create new key in dict
            #     derived[mrelLab] = [(source1[1], source1[0])]
            #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim])))
            # else: # Find derived relation andappend mutually entailed relation
            derived[mrelLab].append((source1[1], source1[0]))
            
            # # Update table (for visuals)
            # relTab[rel1, source1[0], source1[1]] = 1 
            # relTab[mrel, source1[1], source1[0]] = 1 

            # Loop relations again to get second relation for combinatorial entailment 
            for rel2Lab, source2_instances in baseline.items():
                rel2 = relations[rel2Lab]
                for source2 in source2_instances:
                    # Find common element between relations (to determine protococ and derivation)
                    common = findCommon(source1, source2)

                    if common >= 0 and not (source1 == source2): 
                        # Can only derive if non-identical relations have common element

                        # Find combinatorially entailed relation in lookup table
                        # Depends on order of relations and elements (type of training)
                        crel, source12 = deriveCombi(source1, source2, common, rel1, rel2, combi)
                        
                        if crel >= 0: # Exclude ill-defined relations
                            crelLab = relation_list[crel] # label
                            mcrel = mutual[crel] # get mutually entailed from predefined list
                            mcrelLab = relation_list[mcrel] # label
                            
                            # determine protocol
                            protocol = determineProtocol(source1, source2, common)
    
                            if protocol == 'OTM':# One-to-many: A-B & A-C
                                if illustrate == 'print':# illustration: print baseline relations + combinatorial entailment
                                    print('{} is {} {} \nand {} is {} {}. \
                                          \nFrom that, I can derive that {} is {} {}.'.format(
                                              sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                              sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                              sLabs[source1[1]], crelLab, sLabs[source2[1]]))
                                # if crelLab not in derived.keys(): 
                                #     # If derived relation not in baseline rels, create new key in dict
                                #     derived[crelLab] = [(source1[1], source2[1])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source1[1], source2[1]) in derived[crelLab] \
                                    and source1[1] != source2[1]:  # Filter duplicates and reflexive relations
                                    derived[crelLab].append((source1[1], source2[1]))
                                if illustrate == 'print':
                                    print('\n...And that {} is {} {}.\n\n'.format(
                                              sLabs[source2[1]], mcrelLab, sLabs[source1[1]]))
                                # if mcrelLab not in derived.keys():
                                #     derived[mcrelLab] = [(source2[1], source1[1])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source2[1], source1[1]) in derived[mcrelLab]\
                                    and source2[1] != source1[1]:  # Filter duplicates and reflexive relations
                                    derived[mcrelLab].append((source2[1], source1[1]))
                            elif protocol == 'sMTO':
                                if illustrate == 'print':
                                    print('{} is {} {} \nand {} is {} {}. \
                                          \nFrom that, I can derive that {} is {} {}.'.format(
                                              sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                              sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                              sLabs[source1[1]], crelLab, sLabs[source2[0]]))
                                # if crelLab not in derived.keys():
                                #     derived[crelLab] = [(source1[1], source2[0])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source1[0], source2[1]) in derived[crelLab]\
                                    and source1[0] != source2[1]:  # Filter duplicates and reflexive relations
                                    derived[crelLab].append((source1[0], source2[1]))
                                if illustrate == 'print':
                                    print('\n...And that {} is {} {}.\n\n'.format(
                                              sLabs[source2[0]], mcrelLab,sLabs[ source1[1]]))
                                # if mcrelLab not in derived.keys():
                                #     derived[mcrelLab] = [(source2[0], source1[1])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source2[0], source1[1]) in derived[mcrelLab]\
                                    and source2[0] != source1[1]:  # Filter duplicates and reflexive relations
                                    derived[mcrelLab].append((source2[0], source1[1]))
                            elif protocol == 'Linear': # AxB and BxC -> derive A-C
                                if illustrate == 'print':
                                    print('{} is {} {} \nand {} is {} {}. \
                                          \nFrom that, I can derive that {} is {} {}.'.format(
                                             sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                              sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                              sLabs[source1[0]], crelLab, sLabs[source2[1]]))
                                # if crelLab not in derived.keys():
                                #     derived[crelLab] = [(source1[0], source2[1])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source1[0], source2[1]) in derived[crelLab]\
                                    and source1[0] != source2[1]:  # Filter duplicates and reflexive relations
                                    derived[crelLab].append((source1[0], source2[1]))
                                if illustrate == 'print':
                                    print('And that {} is {} {}.\n\n'.format(
                                              sLabs[source2[1]], mcrelLab, sLabs[source1[0]]))
                                # if mcrelLab not in derived.keys():
                                #     derived[mcrelLab] = [(source2[1], source1[0])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source2[1], source1[0]) in derived[mcrelLab]\
                                    and source2[1] != source1[0]:  # Filter duplicates and reflexive relations
                                    derived[mcrelLab].append((source2[1], source1[0]))
                            else: # sMTO:  A - B and A - C -> B-C
                                if illustrate == 'print':
                                    print('{} is {} {} \nand {} is {} {}. \
                                          \nFrom that, I can derive that {} is {} {}.'.format(
                                              sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                              sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                              sLabs[source1[0]], crelLab, sLabs[source2[0]]))
                                # if crelLab not in derived.keys():
                                #     derived[crelLab] = [(source1[0], source2[0])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:
                                if not (source1[0], source2[0]) in derived[crelLab]\
                                    and source1[0] != source2[0]:  # Filter duplicates and reflexive relations
                                    derived[crelLab].append((source1[0], source2[0]))
                                if illustrate == 'print':
                                    print('\n...And that {} is {} {}\n\n'.format(
                                              sLabs[source1[0]], mcrelLab, sLabs[source2[0]]))
                                # if mcrelLab not in derived.keys():
                                #     derived[mcrelLab] = [(source2[0], source1[0])]
                                #     relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                # else:       
                                if not (source2[0], source1[0]) in derived[mcrelLab]\
                                    and source2[0] != source1[0]:  # Filter duplicates and reflexive relations
                                    derived[mcrelLab].append((source2[0], source1[0]))

                        else:
                            if illustrate == 'print':
                                print('{} is {} {} \nand {} is {} {}. \
                                        \nFrom that, I cannot derive anything...\n\n'.format(
                                            sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                            sLabs[source2[0]], rel2Lab, sLabs[source2[1]]))  
                            # Can go beyond two step derivations? Parametrize?
                            # Probably have to for things like transitive inference
    
    # create table for heatmap illustration of relational network 
    relTab = createRelationTable(baseline, derived)
    
    if illustrate == 'heatmap': 
        # Plot baseline and derived relations as stimulus x stimulus heatmap   
        plotNetworkHeatmap(baseline, derived, sLabs)
    if illustrate == 'graph':
        plotRels = ['baseline', 'mutual', 'combi']
        plotTitle = ''
        plotRelNetworkGraph(baseline, derived, sLabs, plotRels)
    return relTab, derived
