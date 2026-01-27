# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 12:33:05 2026

Specific functions for plotting related to derivation tables.

Plot derivation tables as heatmaps
Plot relational network as heatmap
Plot Relational Network as Graph Network

@author: mraemaek
"""

# Dependencies

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
import string
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D  # <— for legend proxies

from utils import *

# Some labels 
type_labs = {'Linear': 'Linear Combination: AxB and BxC - Derive AxC',
             'OTM': 'One-to-Many Combination: AxB and AxC - Derive BxC',
             'MTO': 'Many-to-One Combination: AxB and CxB - Derive AxC',
             'sMTO': 'Reversed Linear Combination: AxB and CxA - Derive BxC',}
rel2_x = {'Linear': 'Second Relation - BxC', # second relation for plot x-axis
        'OTM': 'Second Relation - AxC',
        'MTO': 'Second Relation - CxB',
        'sMTO': 'Second Relation - CxA'
        }
shortrels = {'Same as': 'Sa', # (for x-axis and cells)
             'Different from': 'Di',
             'Opposite to': 'Op',
             'More than': 'Mo',
             'Less than': 'Le',
             'Contains': 'Co',
             'Is part of': 'Pa',
             'Before': 'Be',
             'After': 'Af'
    }
long_rels = {'Same as': 'Same as (Sa)', # on y-axis or separate legend?
             'Different from': 'Different from (Di)',
             'Opposite to': 'Opposite to (Op)',
             'More than': 'More than(Mo)',
             'Less than': 'Less than (Le)',
             'Contains': 'Contains (Co)',
             'Is part of': 'Is part of (Pa)',
             'Before': 'Before (Be)',
             'After': 'After (Af)'
    }
# %% createPlotRelLabels - Creates relation labels for plot based on input

def createPlotRelLabels(relations):
    
    shortrels = {}
    longrel = {}
    
    shortrels = {i:i[:2] for i in relations.keys()}
    
    longrels = {i: i + ' (' + shortrels[i] + ')'for i in relations.keys()}
        
    return shortrels, longrels

# %% Plot derivation tables as heatmaps

def plotTablesHeatmap(relations, mutual, combi):
    
    """
    """
    inv_relations = {v: k for k, v in relations.items()}  # invert dict index -> label
    # Plot mutual entailment as heatmap 
    n_rels = len(relations)

    shortrels, longrels = createPlotRelLabels(relations)

    # === Plot ===
    mutual_matrix = np.zeros((2, len(relations)), dtype=int)
    
    # Populate mutual matrix: row 0 = original relations, row 1 = corresponding mutual relations
    for i, rel in enumerate(relations):
        mutual_matrix[0, i] = i  # Original relation index
        mutual_matrix[1, i] = mutual[i]  # Corresponding mutual relation index
    
    labels = np.empty_like(mutual_matrix, dtype=object)  # Create labels matrix
    for row in range(2):
        for col in range(n_rels):
            labels[row, col] = shortrels[inv_relations[mutual_matrix[row, col]]]
    # Create a DataFrame from the matrix
    df = pd.DataFrame(mutual_matrix, index=["Input Relation AxB", "Mutually Entailed Relation BxA"], columns=relations)

    # Create the plot with a dynamic size
    fig, ax = plt.subplots(figsize=(len(relations), 2))  # Adjust width based on the number of relations
    
    sns.heatmap(df, annot=labels, fmt='', cmap='YlGnBu', cbar=False, linewidths=0.5, ax=ax,
                annot_kws={"weight": "bold"}, cbar_kws={'label': 'Mutual Relations'})
    
    # Set title and axes labels
    ax.set_title('Mutual Entailment for User Input', fontsize=14, fontweight='bold')
    ax.set_ylabel('Input Relation AxB', fontsize=12, fontweight='bold')
    ax.set_xlabel('Mutually Entailed Relation BxA', fontsize=12, fontweight='bold')
    
    # Adjust x and y ticks
    plt.xticks(rotation=45, ha='right', fontsize=10, fontweight='bold')
    plt.yticks(rotation=0, fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

    # Plot combinatorial entailment heatmaps for each combination type 
    fig, axs = plt.subplots(2, 2, figsize=(18, 14))  # 2 rows, 2 columns
    axs = axs.flatten()  # Flatten to index as 0,1,2,3
    
    for i, (comb_type, matrix) in enumerate(combi.items()):
        df = pd.DataFrame(matrix)
        df.index = [k for k in relations]
        df.columns = [k for k in relations]
        df.replace(-1, np.nan, inplace=True)
    
        # Abbreviated cell labels
        label_matrix = (
            df.astype(pd.Int64Dtype())
              .apply(lambda col: col.map(inv_relations))
              .apply(lambda col: col.map(shortrels))
        )
    
        ax = axs[i]
        sns.heatmap(
            df,
            annot=label_matrix,
            fmt='',
            cmap='coolwarm',
            cbar=False,
            linewidths=0.5,
            linecolor='lightgray',
            annot_kws={"weight": "bold"},
            ax=ax
        )
    
        ax.set_title(f"{type_labs[comb_type]}",
                     fontweight='bold', fontsize=14, pad=20)
    
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        ax.set_xlabel(rel2_x[comb_type], fontweight='bold', fontsize=12)
        if i % 2 == 0: ax.set_ylabel("First Relation - AxB", fontweight='bold', fontsize=12)
    
        ax.set_xticks(np.arange(len(df.columns))+0.5)
        ax.set_xticklabels([shortrels[r] for r in df.columns], rotation=0, fontweight='bold')
        ax.set_yticks(np.arange(len(df.index))+0.5)
        ax.set_yticklabels([longrels[r] for r in df.index], rotation=0, fontweight='bold')
    
    plt.suptitle('Combinatorially Entailed Relations for All Combinations of Relations',
                 fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
    return


# %%

def plotNetworkHeatmap(baseline, derived, sLabs):
    
    
    """
    Plots (derived) relational network as heatmap.
    
    Args:
        baseline: dict containing instances (tuples, pairs of int) of relations (keys, str)
        derived: dict of same format containing derived relations
        sLabs: list of stimulus labels
    
    """
    
    f, axs = plt.subplots(figsize=(13, 3), ncols=len(derived.keys()))
    
    relTab = createRelationTable(baseline, derived)
    
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
            n_stim = countUniqueStimuli(baseline)
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
    return


# %% determine coordinates of polygon to plot relational network

def polygon_coords(n_nodes, protocol):
    
    """
    Compute the vertices for relational graph network
    
    Args:
        n_nodes: int, number of unique stimuli in network
    """
    radius=n_nodes*45
    center=(n_nodes*50, n_nodes*50)
    
    vertices = []
    # Calculate angle between vertices
    if n_nodes > 3: 
        
        if protocol != 'Linear': # Plot network around the 'One' (center)for OTM/MTO
            angle = 2 * np.pi / (n_nodes-1) 
            vertices.append((center))
            for i in range(n_nodes-1): # skip one for center S
                x = center[0] + radius * np.cos(i * angle) # Calculate polygon coords around center
                y = center[1] + radius * np.sin(i * angle)
                vertices.append((x, y))
        else:
            angle = 2 * np.pi / (n_nodes) 
            for i in range(n_nodes):
                x = center[0] + radius * np.cos(i * angle) 
                y = center[1] + radius * np.sin(i * angle)
                vertices.append((x, y))
                
    else: # regardless of protocol, plot triangle around center
        angle = 2 * np.pi / (n_nodes)
        for i in range(n_nodes):
            x = center[0] + radius * np.cos(i * angle) 
            y = center[1] + radius * np.sin(i * angle)
            vertices.append((x, y))            
    return vertices

# %% Determine label position for graph network (arrow midpoint + offset)

def findLabelPosition(x_start, x_end, y_start, y_end, radius, label_offset):
    
    """
    
    For two points in Cartesian space, calculates the midpoint and azymuth of the 
    arrow drawn between them and adds offset for placing label
    
    Args: 
        x_start: int, x-coord of first point
        x_end: int, x-coord of second point
        y_start: int, y-coord of first point
        y_end: int, y-coord of second point

    returns:
        azymuth_x: int, x-coord of arrow azymuth offset
        aymuth_y: int, y-coord
    """
    # Label the curve, position depending on symmetry of relation
    mid_x, mid_y = (x_start + x_end)/ 2, (y_start + y_end)/ 2# midpoint for positioning
    # make label position function of direction of arrow up/down-left/right
            
        
    dx, dy = x_end - x_start, y_end - y_start # Vector from start to end
    
    distance = np.sqrt(dx**2 + dy**2) # Calculate the distance between start and end points
    # Calculate angle of the line segment for consistent radial offset
    angle = np.arctan2(dy, dx) + np.pi / 2  # Rotate by 90 degrees to get perpendicular

    offset = radius * distance # Offset based on radius
    # Azimuth point for label, shifted by label_offset in the radial direction
    azimuth_x = mid_x - offset * np.cos(angle) *label_offset
    azimuth_y = mid_y - offset * np.sin(angle) *label_offset
    return azimuth_x, azimuth_y
# %% Plot relational network as graph network



def plotRelNetworkGraph(baseline, derived = None, sLabs = None, plotRels = None, 
                        plotTitle = None):
    
    """
    
    """
    
    
    # determine which plotting parameters to allow user to tweak?
    
    relations = cleanRelationLabels(list(baseline.keys()))
    
    if plotRels is None:
        plotRels = ['baseline', 'mutual', 'derived']
    # Do I need to input derived? Want user to also use it in stand-alone case
    # so derive on the spot anyways, should produce same result anyway
    

    # plot parameteres
    
    relColor = 'black'
    mrelColor = '#0072B2' # mutually entailed relations
    crelColor = '#CC79A7' # combinatorially entailed relations
    
    # move to one param later?
    legendCombi = False
    legendBaseline = False # include in legend?
    legendMutual = False
    
    # accessible colors: '#0072B2', '#009E73', '#D55E00', '#CC79A7'
    
    # title (move down?)
    if plotTitle == '' or plotTitle is None: 
        if not 'mutual' in plotRels and 'combi' not in plotRels:
            title = 'Trained Relational Network'
        elif 'mutual' in plotRels and not 'combi' in plotRels:
            title = 'Trained and Mutually Entailed Relational Network'
        else:
            title = 'Trained and Derived Relational Network'

    # graph parameters
    radius = .18 # Determines curvature of lines between stimuli, can tweak to make plot more readable
    # Between .15 and .3 seems to provide best results
    #       "simple, head_length=50, head_width=15, tail_width=5" # Simple arrow growing thinner
    relArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
    drelArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
    label_offset = .55 # Play around with how close labels are plotted to lines
    relLabelFontSize = 50
    sLabelFontSize = 60
    sDotSize = 100

    # Specify training protocol
    protocol = 'OneToMany' # For one-to-many or many-to-one, the 'one' is plotted in the middle
    # Maybe better to let user specify circle or line?
    
    # should be loaded already, but in case not
    from createDerivationTables import createDerivationTables
    from deriveRelationsFromBaseline import deriveRelationsFromBaseline
    # create derivation tables
    mutual, combi, relations = createDerivationTables(list(baseline.keys()))
    # derive relations (or do on the spot while plotting?)
    relTab, derived = deriveRelationsFromBaseline(baseline, sLabs)
    
    n_stim = countUniqueStimuli(baseline)

    vertices = []    
    vertices = polygon_coords(n_stim, protocol)

    # Create a Cartesian grid plot without showing the grid
    figsize = (25,25) # make dependent on n_nodes?
    plt.figure(figsize=figsize)  # Set figure size
    plt.plot([], [])  # Create an empty plot (optional for axes setup)
    plt.xlim(0,  n_stim*100)  # Set x-axis range
    plt.ylim(0,  n_stim*100)  # Set y-axis range

    # Intitialize to ensure network is constructed the same for baseline/derived
    plottedS = dict({}) # init empty dict to avoid double-plotting
    for i in range(n_stim):
        plottedS[sLabs[i]] =  [vertices[len(plottedS.keys())]]
    plottedRels = dict({}) # init empty dict to avoid double-plotting

    if 'baseline' in plotRels:
        # Loop through baseline relations
        for rels, rel_instances in baseline.items():
            for rel in rel_instances:
                for s in range(2):
                    # plot a labeled point on the grid
                    x = plottedS[sLabs[rel[s]]][0][0]
                    y = plottedS[sLabs[rel[s]]][0][1]
                    plt.plot(x, y, 'o', markersize = sDotSize, color = 'grey')  # Plot point
                    plt.text(x, y , sLabs[rel[s]], 
                             fontweight = 'bold', fontsize=sLabelFontSize, ha='center', va = 'center')  # Label next to the point
                # get coords for relation
                x_start, y_start = plottedS[sLabs[rel[0]]][0][0], plottedS[sLabs[rel[0]]][0][1]        
                x_end, y_end = plottedS[sLabs[rel[1]]][0][0], plottedS[sLabs[rel[1]]][0][1]
                # Plot a curved line using FancyArrowPatch 
                baselineArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle= relArrowStyle, color=relColor, linewidth=1.5)
                plt.gca().add_patch(baselineArrow)
                
                # calculate position of label
                azimuth_x, azimuth_y = findLabelPosition(x_start, x_end,
                                                         y_start, y_end,
                                                         radius,
                                                         label_offset)
                plt.text(azimuth_x, azimuth_y, shortrels[rels], color=relColor, 
                         fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
            
    plotted = []
    # Loop through derived relations
    for drels in derived.keys():
        for drel in derived[drels]:
            if not 'baseline' in plotRels: # Plot nodes if no baseline relations plotted 
                for s in range(2):
                    # plot a labeled point on the grid
                    x = plottedS[sLabs[drel[s]]][0][0]
                    y = plottedS[sLabs[drel[s]]][0][1]
                    plt.plot(x, y, 'o', markersize = sDotSize, color = 'grey')  # Plot point
                    plt.text(x, y , sLabs[drel[s]], 
                             fontweight = 'bold', fontsize=sLabelFontSize, ha='center', va = 'center')  # Label next to the point
            # Figure out if derivation is mutual or not?
            # Check whether the mutually entailed relation of the current
            # derived relation (in loop) is one of the baseline relations
            # if so, it is mutually entailed, if not, combinatorially entailed
            if list(relations.keys())[mutual[relations[drels]]] in baseline.keys():
                if (drel[1], drel[0]) in baseline[list(relations.keys())[mutual[relations[drels]]]]:
                    dtype = 'mutual'
                else: dtype = 'combi'
            else: dtype = 'combi' # if mutually entailed relation not in baseline, must be combinatorially entailed
            # get coords for relation
            x_start, y_start = plottedS[sLabs[drel[0]]][0][0], plottedS[sLabs[drel[0]]][0][1]        
            x_end, y_end = plottedS[sLabs[drel[1]]][0][0], plottedS[sLabs[drel[1]]][0][1]
            # Label the curve, position depending on symmetry of relation
            azimuth_x, azimuth_y = findLabelPosition(x_start, x_end, 
                                                     y_start, y_end,
                                                     radius,
                                                     label_offset)                
            
            if 'mutual' in plotRels and dtype == 'mutual': # No duplicates (better to filter in derivation script!!)
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=mrelColor, 
                                        linestyle = ':', linewidth=1)
                plt.gca().add_patch(derivedArrow)
                plt.text(azimuth_x, azimuth_y, shortrels[drels], color=mrelColor, 
                         fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))
            if 'combi' in plotRels and dtype == 'combi':
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=crelColor, 
                                        linestyle = '--', linewidth=1)
                plt.gca().add_patch(derivedArrow)
                plt.text(azimuth_x, azimuth_y, shortrels[drels], color=crelColor, 
                         fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))

    
    legend_handles = []
    if legendBaseline:
        legend_handles.append(Line2D([0],[0], color=relColor, linestyle='-', linewidth=5, label='Baseline'))
    if legendMutual:
        legend_handles.append(Line2D([0],[0], color=mrelColor, linestyle=':', linewidth=5, label='Mutual'))
    if legendCombi:
        legend_handles.append(Line2D([0],[0], color=crelColor, linestyle='--', linewidth=5, label='Combinatorial'))
    if legend_handles:
        plt.legend(handles=legend_handles, loc='best', fontsize=50, frameon=False)

    # title
    if plotTitle: plt.title(title, fontsize=72, fontweight = 'bold')
    
    # Ensure grid is not displayed
    plt.grid(False)
    plt.xticks([])  # Removes x-axis ticks
    plt.yticks([])  # Removes y-axis ticks
    
    # Hide spines (the axis lines)
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    # Display the plot
    plt.show()

    return