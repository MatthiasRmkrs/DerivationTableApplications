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
    - 'n_stim': int - the number of unique stimuli in the network (for indexing, can be replaced?)
    - 'sLabs': list of labels for the stimuli (can be longer than n_stim)


TO DO:
    - Plotting errors when only one relation and order of derived /baseline is not same?
    - Could add steps beyond two step?
    - Compute n_unique stim in function here
    - add network plotter
    - Move computation of relTab to end so that order of relations can be controlled
    



"""

# Given a set of stimuli and baseline relations, compute derived relations 

# Dependencies
import numpy as np
import matplotlib.pyplot as plt
from derivationTablesFromSourceRelations import derivationTablesFromSourceRelations
import pdb
# Specify relations
relations = dict({'Same as': 0,
             'Different from': 1,
             'Opposite to': 2,
             'More than': 3,
             'Less than': 4,
             'Contains': 5,
             'Is part of': 6,
             'Before': 7,
             'After': 8})
# Find different solution for the above? E.g., manual input in function, 

# Function to derive relation
def deriveRelationsFromBaseline(baseline, plot, printRels, n_stim, sLabs):
    mutual, combi = derivationTablesFromSourceRelations(relations)
    n_rel = len(baseline.keys())
    derived = dict()
    relTab = np.zeros([n_rel, n_stim, n_stim], dtype = 'int') # Tabular version of dict
    
    for i in range(len(baseline.keys())): # Loop relations
        for j in range(len(list(baseline.values())[i])): # Loop relation instances
            
            # Derive mutual relation first
            source1 = list(baseline.values())[i][j] # Fetch first relation
            relTab[i, source1[0], source1[1]] = 1 # Update table
            rel1Lab = list(baseline.keys())[i] # Get relation label
            # And relation id in predefined dict/lookup table
            rel1 = list(relations.values())[list.index(list(relations.keys()), rel1Lab)]
            
            mrel = mutual[rel1] # Find mutually entailed relation in predefined list
            mrelLab = list(relations.keys())[mrel] # label
            if printRels:
                print('{} is {} {}. \nFrom that, I can derive that {} is {} {}'.format(
                          sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                          sLabs[source1[1]], mrelLab, sLabs[source1[0]]))
                        
            if mrelLab not in derived.keys():
                # If derived relation not in baseline rels, create new key in dict
                derived[mrelLab] = [(source1[1], source1[0])]
                relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim])))
            else: # Find derived relations then append mutually entailed relation
                derived[mrelLab].append((source1[1], source1[0]))
            relTab[list.index(list(derived.keys()), mrelLab), source1[1], source1[0]] = 1 # Update table

            # Derive combinatorially entailed relations using second relation
            for ii in range(len(baseline.keys())): # Loop relations again
                for jj in range(len(list(baseline.values())[ii])): # Loop instances
                    source2 = list(baseline.values())[ii][jj]
                    # Find common element
                    common = -1
                    for sr1 in source1:
                        for sr2 in source2:
                            if sr1 == sr2:
                                common = sr2    
                    
                    if common >= 0 and not (ii == i and jj == j): 
                        # Only combine rels with common element, 
                        # Don't combine identical instances
                            
                        rel2Lab = list(baseline.keys())[ii] # Get relation label
                        # And relation id in source dict/lookup table
                        rel2 = list(relations.values())[list.index(list(relations.keys()), rel2Lab)]

                        # Find combinatorially entailed relation in lookup table
                        # Depends on order of relations and elements (type of training)
                        if tuple.index(source1, common) == 0:
                            if tuple.index(source2, common) == 0: # A-B & A - C (OTM)
                                crel = combi['OTM'][rel1, rel2]

                            else: # A - B & C - A (sort of MTO)
                                crel = combi['sMTO'][rel1, rel2]
                        else:
                            if tuple.index(source2, common) == 0: # A-B & B - C (linear)
                                crel = combi['Linear'][rel1, rel2]
                            else: # A-B & C- B (MTO)
                                crel = combi['MTO'][rel1, rel2]
                        

                        if crel >= 0: # Exclude ill-defined relations
                            crelLab = list(relations.keys())[crel] # label
                            mcrel = mutual[crel] # get mutually entailed from predefined list
                            mcrelLab = list(relations.keys())[mcrel] # label
    
                            if tuple.index(source1, common) == 0: 
                                if tuple.index(source2, common) == 0: # Find second element
                                # One-to-many: A-B & A-C
                                    if printRels: 
                                        print('{} is {} {} \nand {} is {} {}. \
                                              \nFrom that, I can derive that {} is {} {}.'.format(
                                                  sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                                  sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                                  sLabs[source1[1]], crelLab, sLabs[source2[1]]))
                                    if crelLab not in derived.keys(): 
                                        # If derived relation not in baseline rels, create new key in dict
                                        derived[crelLab] = [(source1[1], source2[1])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[crelLab].append((source1[1], source2[1]))
                                    relTab[list.index(list(derived.keys()), crelLab), source1[1], source2[1]] = 1 # Update table
                                    if printRels:
                                        print('\n...And that {} is {} {}.\n\n'.format(
                                                  sLabs[source2[1]], mcrelLab, sLabs[source1[1]]))
                                    if mcrelLab not in derived.keys():
                                        derived[mcrelLab] = [(source2[1], source1[1])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[mcrelLab].append((source2[1], source1[1]))
                                    relTab[list.index(list(derived.keys()), mcrelLab), source2[1], source1[1]] = 1 # Update table
                                else:
                                    if printRels:
                                        print('{} is {} {} \nand {} is {} {}. \
                                              \nFrom that, I can derive that {} is {} {}.'.format(
                                                  sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                                  sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                                  sLabs[source1[1]], crelLab, sLabs[source2[0]]))
                                    if crelLab not in derived.keys():
                                        derived[crelLab] = [(source1[1], source2[0])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[crelLab].append((source1[0], source2[1]))
                                    relTab[list.index(list(derived.keys()), crelLab), source1[1], source2[0]] = 1 # Update table
                                    if printRels:
                                        print('\n...And that {} is {} {}.\n\n'.format(
                                                  sLabs[source2[0]], mcrelLab,sLabs[ source1[1]]))
                                    if mcrelLab not in derived.keys():
                                        derived[mcrelLab] = [(source2[0], source1[1])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[mcrelLab].append((source2[0], source1[1]))
                                    relTab[list.index(list(derived.keys()), mcrelLab), source2[0], source1[1]] = 1 # Update table
                            else: 
                                # --> Derive B-C relation
                                if tuple.index(source2, common) == 0: # Find second element
                                    if printRels:
                                        print('{} is {} {} \nand {} is {} {}. \
                                              \nFrom that, I can derive that {} is {} {}.'.format(
                                                 sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                                  sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                                  sLabs[source1[0]], crelLab, sLabs[source2[1]]))
                                    if crelLab not in derived.keys():
                                        derived[crelLab] = [(source1[0], source2[1])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[crelLab].append((source1[0], source2[1]))
                                    relTab[list.index(list(derived.keys()), crelLab), source1[0], source2[1]] = 1 # Update table
                                    if printRels:
                                        print('And that {} is {} {}.\n\n'.format(
                                                  sLabs[source2[1]], mcrelLab, sLabs[source1[0]]))
                                    if mcrelLab not in derived.keys():
                                        derived[mcrelLab] = [(source2[1], source1[0])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[mcrelLab].append((source2[1], source1[0]))
                                    relTab[list.index(list(derived.keys()), mcrelLab), source2[1], source1[0]] = 1 # Update table        
                                else: # A - B and A - C -> B-C
                                    if printRels:
                                        print('{} is {} {} \nand {} is {} {}. \
                                              \nFrom that, I can derive that {} is {} {}.'.format(
                                                  sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                                  sLabs[source2[0]], rel2Lab, sLabs[source2[1]],
                                                  sLabs[source1[0]], crelLab, sLabs[source2[0]]))
                                    if crelLab not in derived.keys():
                                        derived[crelLab] = [(source1[0], source2[0])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:
                                        derived[crelLab].append((source1[0], source2[0]))
                                    relTab[list.index(list(derived.keys()), crelLab), source1[0], source2[0]] = 1 # Update table
                                    if printRels:
                                        print('\n...And that {} is {} {}\n\n'.format(
                                                  sLabs[source1[0]], mcrelLab, sLabs[source2[0]]))
                                    if mcrelLab not in derived.keys():
                                        derived[mcrelLab] = [(source2[0], source1[0])]
                                        relTab = np.vstack((relTab, np.zeros([1, n_stim, n_stim]))) # Add another relation to table
                                    else:       
                                        derived[mcrelLab].append((source2[0], source1[0]))
                                    relTab[list.index(list(derived.keys()), mcrelLab), source2[0], source1[0]] = 1 # Update table

                        else:
                            if printRels:
                                print('{} is {} {} \nand {} is {} {}. \
                                        \nFrom that, I cannot derive anything...\n\n'.format(
                                            sLabs[source1[0]], rel1Lab, sLabs[source1[1]],
                                            sLabs[source2[0]], rel2Lab, sLabs[source2[1]]))  
                            # Can go beyond two step derivations? Parametrize?
    if plot: # Plot baseline and derived relations as stimulus x stimulus heatmap
        f, axs = plt.subplots(figsize=(13, 3), ncols=len(derived.keys()))
        
        # find labels for stimuli in baseline rels (avoid error #labels > #Ss)
        plot_sLabs = []
        for i in baseline.keys():
            for j in range(len(baseline[i])):
                for s in range(2):
                    if sLabs[baseline[i][j][s]] not in plot_sLabs: 
                        plot_sLabs.append(sLabs[baseline[i][j][s]])
        if len(derived.keys()) > 1:
            for sp in range(len(derived.keys())):
                data = np.array(relTab[sp, :, :], dtype = 'float')
                axs[sp].imshow(data, cmap='RdYlGn', vmin=0,
                                    vmax=1, interpolation='nearest')
                axs[sp].set_title(list(derived.keys())[sp],
                                 fontsize=12, fontweight='bold')
                # f.colorbar(map, ax=axs[sp], extend='both')
                axs[sp].set(xticks=range(n_stim), yticks=range(n_stim))
                axs[sp].set(xticklabels=plot_sLabs, yticklabels=plot_sLabs)
            
                axs[sp].xaxis.tick_top()
                axs[sp].set_xlabel('Stimulus 1', fontweight='bold')
                axs[sp].set_ylabel('Stimulus 2', fontweight='bold')
            
            f.suptitle('Baseline and Derived Relations',
                       x=0.5, y=1.1, fontsize=14, fontweight='bold')
        
        else:
            for sp in range(len(derived.keys())):
                data = np.array(relTab[sp, :, :], dtype = 'float')
                axs.imshow(data, cmap='RdYlGn', vmin=0,
                                    vmax=1, interpolation='nearest')
                axs.set_title(list(derived.keys())[sp],
                                 fontsize=12, fontweight='bold')
                # f.colorbar(map, ax=axs[sp], extend='both')
                axs.set(xticks=range(n_stim), yticks=range(n_stim))
                axs.set(xticklabels=plot_sLabs, yticklabels=plot_sLabs)
            
                axs.xaxis.tick_top()
                axs.set_xlabel('Stimulus 1', fontweight='bold')
                axs.set_ylabel('Stimulus 2', fontweight='bold')
            
            plt.title('Baseline and Derived Relations',
                       x=0.5, y=1.1, fontsize=14, fontweight='bold')
            
        plt.show()
    
    return relTab, derived