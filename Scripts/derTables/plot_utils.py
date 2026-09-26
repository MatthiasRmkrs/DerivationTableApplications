# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 12:33:05 2026

Specific functions for plotting related to derivation tables.

Defines the following functions:
    plotTablesHeatmap - Plot derivation tables as heatmaps
    plotNetworkHeatmap - Plot relational network (baseline + derived) as heatmap
    plotRelNetworkGraph - Plot Relational Network as Graph Network
    + some further minor functions that support the above


TO DO:
    - graph network plotter legend and selective relations
        -> not easy to allow customization within deriveRelations
        -> Only if plot function is used separately? Specify what to plot, 
            and then automatically include in legend?
    - createPlotRelLabels can be more robust by checking whether new label already
        exists? avoid problems for relations that start with same letters?
        
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
import networkx as nx # Graph network

from derTables.utils_tables import (createRelationTable, 
                   countUniqueStimuli, 
                   cleanRelationLabels)

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
    
    """
    Creates 'short' labels for relations to use in plots (e.g., label vertices in 
    graph network or cells in heatmap). Just converts to first two letters of the label.
    
    Args: 
        relations: dict containing relation labels as keys and tuples of stimulus pairs as values
            typically output of createDerivationTables (already converted, hence dict not list)
        
    """
    
    shortrels = {}
    longrel = {}
    
    shortrels = {i:i[:2] for i in relations.keys()}
    
    longrels = {i: i + ' (' + shortrels[i] + ')'for i in relations.keys()}
        
    return shortrels, longrels

# %% Plot derivation tables as heatmaps

def plotTablesHeatmap(relations, mutual, combi):
    
    """
    Plots derivation tables, created by 'createDerivationTables' as heatmaps,
    both for mutual and combinatorial entailment.
    
    Args:
        relations: dict, relations as keys, tuples of stimulus indices as values
                 output by createDerivationTables
        mutual: list that contains the (indices) of the relations that are mutually 
                entailed by those provided in input
                output by createDerivationTables
        combi:  a dict containing four arrays, one for each way two relations can be combined,
             each containing the combinatorially entailed relations (indices)
             for all possible combinations of the relations provided in input
             output by createDerivationTables
            
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
    ax.set_xticks([])
    # Adjust x and y ticks
    # plt.xticks(rotation=45, ha='right', fontsize=10, fontweight='bold')
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


# %% plotNetworkHeatmap - plot network of baseline and derived relations as heatmaps

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

# %% Helpers for graph network plotter

def build_layout_graph(baseline, sLabs, derived=None, include_derived=False):
    """
    Build a NetworkX directed graph from baseline and optionally derived relations.
    Nodes are stimulus labels. Edges are directed relations.
    """

    G = nx.DiGraph()

    for lab in sLabs:
        G.add_node(lab)

    for rel_name, rel_instances in baseline.items():
        for i, j in rel_instances:
            G.add_edge(
                sLabs[i],
                sLabs[j],
                relation=rel_name,
                kind="baseline"
            )

    if include_derived and derived is not None:
        for rel_name, rel_instances in derived.items():
            for i, j in rel_instances:
                G.add_edge(
                    sLabs[i],
                    sLabs[j],
                    relation=rel_name,
                    kind="derived"
                )

    return G


def degree_layout(G, scale=100):
    """
    Places the most connected node in the center and all other nodes around it.
    Good for one-to-many and many-to-one networks.
    """

    if G.number_of_nodes() == 0:
        return {}

    degrees = dict(G.degree())
    center_node = max(degrees, key=degrees.get)

    other_nodes = [node for node in G.nodes if node != center_node]

    pos = {
        center_node: (0.0, 0.0)
    }

    n = len(other_nodes)

    if n == 0:
        return pos

    for k, node in enumerate(other_nodes):
        angle = 2 * np.pi * k / n
        pos[node] = (
            scale * np.cos(angle),
            scale * np.sin(angle)
        )

    return pos


def hierarchical_layout(G, scale=100):
    """
    Places nodes in directed layers.
    Good for ordered or chain-like relations, such as:
    A > B > C > D
    """

    try:
        generations = list(nx.topological_generations(G))
    except nx.NetworkXUnfeasible:
        # Graph contains a cycle, so hierarchy is not well-defined.
        return nx.spring_layout(G, scale=scale, seed=123)

    pos = {}

    for x_level, generation in enumerate(generations):
        generation = list(generation)
        n = len(generation)

        for y_index, node in enumerate(generation):
            y = y_index - (n - 1) / 2

            pos[node] = (
                x_level * scale,
                -y * scale
            )

    return pos


def normalize_positions(pos, scale=100, margin=50):
    """
    Converts any NetworkX-style position dictionary into positive plotting
    coordinates with a margin around the graph.
    """

    if not pos:
        return {}

    xs = [xy[0] for xy in pos.values()]
    ys = [xy[1] for xy in pos.values()]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max(max_x - min_x, 1e-9)
    height = max(max_y - min_y, 1e-9)

    normalized = {}

    for node, (x, y) in pos.items():
        new_x = margin + ((x - min_x) / width) * scale
        new_y = margin + ((y - min_y) / height) * scale

        normalized[node] = (float(new_x), float(new_y))

    return normalized


def compute_stimulus_layout(
    baseline,
    sLabs,
    derived=None,
    layout="auto",
    positions=None,
    include_derived=False,
    scale=1000,
    margin=100
):
    """
    Computes stimulus coordinates for plotting.

    layout options:
    - 'auto'
    - 'circle'
    - 'spring'
    - 'degree'
    - 'hierarchical'
    - 'manual'
    """

    if sLabs is None:
        raise ValueError("sLabs must be provided to compute stimulus layout.")

    if layout == "manual":
        if positions is None:
            raise ValueError(
                "layout='manual' requires a positions dictionary."
            )

        # Allow either:
        # positions = {"A": (x, y), "B": (x, y)}
        # or:
        # positions = {0: (x, y), 1: (x, y)}
        converted_positions = {}

        for i, lab in enumerate(sLabs):
            if lab in positions:
                converted_positions[lab] = positions[lab]
            elif i in positions:
                converted_positions[lab] = positions[i]
            else:
                raise ValueError(
                    f"No manual position provided for stimulus '{lab}'."
                )

        return converted_positions

    G = build_layout_graph(
        baseline=baseline,
        sLabs=sLabs,
        derived=derived,
        include_derived=include_derived
    )

    n_stim = len(sLabs)

    if layout == "auto":
        degrees = dict(G.degree())
        max_degree = max(degrees.values()) if degrees else 0
        n_edges = G.number_of_edges()

        density = nx.density(G.to_undirected()) if n_stim > 1 else 0

        is_chain_like = (
            n_edges >= max(n_stim - 1, 1)
            and sum(d <= 2 for d in degrees.values()) >= max(n_stim - 1, 1)
        )

        has_hub = max_degree >= max(3, n_stim // 2)

        if n_stim <= 5:
            selected_layout = "circle"
        elif has_hub:
            selected_layout = "degree"
        elif is_chain_like:
            selected_layout = "hierarchical"
        elif density > 0.35:
            selected_layout = "spring"
        else:
            selected_layout = "spring"

    else:
        selected_layout = layout

    if selected_layout == "circle":
        pos = nx.circular_layout(G, scale=scale)

    elif selected_layout == "spring":
        pos = nx.spring_layout(
            G,
            scale=scale,
            seed=123
        )

    elif selected_layout == "degree":
        pos = degree_layout(G, scale=scale)

    elif selected_layout == "hierarchical":
        pos = hierarchical_layout(G, scale=scale)

    else:
        raise ValueError(
            f"Unknown layout '{layout}'. "
            "Choose from 'auto', 'circle', 'spring', 'degree', "
            "'hierarchical', or 'manual'."
        )

    return normalize_positions(
        pos,
        scale=scale,
        margin=margin
    )
# %% Plot relational network as graph network

def plotRelNetworkGraph(baseline, 
                        derived = None, 
                        sLabs = None, 
                        plotRels = None, 
                        plotTitle = None, 
                        layout = 'auto', 
                        positions = None,
                        includeDerivedInLayout = False,
                        relation_colors = None,
                        labels = False,
                        radius = .18,
                        label_offset = .55,
                        fontSize = 50,
                        sDotSize = 100,
                        legend = None,
                        ):
    
    """
    Plots a network of (baseline and derived) relations as a graph network
    
    Args:
        baseline: dict - baseline relation labels as keys, list of tuples 
                    (stimulus pairs) that represent instances of that 
                    relation as the value for each key
        derived: optional, dict - derived relations, can be output of 
                deriveRelationsFromBaseline function, is not provided, will be
                computed using said function
        sLabs: optional, list of str representing stimulus labels (for plotting)
        plotRels: list of str, which relations to include in plot
                choose from 'baseline', 'mutual', 'combi'. Default is all types.
        plotTitle: optional str to serve as plot title.
        layout: choose from: 
                'auto': function creates network structure based on relations
                'circle': circular polygon, good for small networks
                'spring': 
                'degree': for one-to-many or many-to-one, highly connecte stimuli central in network
                'hierarchical': for ordered relations
                'manual'
                
        
    """
    # Plot parameteres    
    if plotRels is None:
        plotRels = ['baseline', 'mutual', 'combi']
    

    if legend is None:
        legend = ["Relation type", "Relation colors"]
    
    
    # mrelColor = '#0072B2' # mutually entailed relations
    # crelColor = '#CC79A7' # combinatorially entailed relations
    # accessible colors: 

    # graph parameters
    # radius = .18 # Determines curvature of lines between stimuli, can tweak to make plot more readable
    # Between .15 and .3 seems to provide best results
    #       "simple, head_length=50, head_width=15, tail_width=5" # Simple arrow growing thinner
    # relArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
    # drelArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
    relArrowStyle = "-|>"
    drelArrowStyle = "-|>"
    
    # label_offset = .55 # Play around with how close labels are plotted to lines
    relLabelFontSize = fontSize
    sLabelFontSize = fontSize
    # sDotSize = 100

    # create derivation tables and derive from baseline if needed
    relations = cleanRelationLabels(list(baseline.keys()))  # clean input relation labels 
    # should be loaded already, but in case not
    
    
    from derTables.createDerivationTables import createDerivationTables
    from derTables.deriveRelationsFromBaseline import deriveRelationsFromBaseline
    
    mutual, combi, relations = createDerivationTables(list(baseline.keys()))
    # derive relations (or do on the spot while plotting?)
    relTab, derived = deriveRelationsFromBaseline(baseline, sLabs)
    
    default_relation_colors = [
        "#E69F00",  # orange
        "#56B4E9",  # sky blue
        "#009E73",  # bluish green
        "#F0E442",  # yellow
        "#0072B2",  # blue
        "#D55E00",  # vermillion
        "#CC79A7",  # reddish purple
        "#000000",  # black
    ]
    
    if derived is None:
        derived_for_colors = {}
    else:
        derived_for_colors = derived
    
    all_relation_labels = list(dict.fromkeys(
        list(baseline.keys()) + list(derived_for_colors.keys())
    ))
    
    if relation_colors is None:
        relation_colors = {
            rel_label: default_relation_colors[i % len(default_relation_colors)]
            for i, rel_label in enumerate(all_relation_labels)
        }
    else:
        # Add fallback colors for any relations missing from the supplied dictionary
        for i, rel_label in enumerate(all_relation_labels):
            if rel_label not in relation_colors:
                relation_colors[rel_label] = default_relation_colors[i % len(default_relation_colors)]
        
    # Determine stimulus positions in graph
    n_stim = len(sLabs)
    
    layout_positions = compute_stimulus_layout(
        baseline=baseline,
        derived=derived,
        sLabs=sLabs,
        layout=layout,
        positions=positions,
        include_derived=includeDerivedInLayout,
        scale=max(700, n_stim * 150),
        margin=150
    )
    
    # Create a Cartesian grid plot without showing the grid
    figsize = (25, 25)
    plt.figure(figsize=figsize)
    plt.plot([], [])
    
    # Use dynamic plot limits based on computed coordinates
    xs = [xy[0] for xy in layout_positions.values()]
    ys = [xy[1] for xy in layout_positions.values()]
    
    x_margin = max(100, (max(xs) - min(xs)) * 0.15)
    y_margin = max(100, (max(ys) - min(ys)) * 0.15)
    
    plt.xlim(min(xs) - x_margin, max(xs) + x_margin)
    plt.ylim(min(ys) - y_margin, max(ys) + y_margin)
    
    # Initialize to ensure network is constructed the same for baseline/derived
    plottedS = {
        lab: [layout_positions[lab]]
        for lab in sLabs
    }
    
    plottedRels = dict({})

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
                
                currentColor = relation_colors[rels]
                baselineArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle= relArrowStyle, color=currentColor, linewidth=5)
                plt.gca().add_patch(baselineArrow)
                
                # calculate position of label
                azimuth_x, azimuth_y = findLabelPosition(x_start, x_end,
                                                         y_start, y_end,
                                                         radius,
                                                         label_offset)
                if labels:
                    plt.text(azimuth_x, azimuth_y, shortrels[rels], color=currentColor, 
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
            currentColor = relation_colors[drels]
            if 'mutual' in plotRels and dtype == 'mutual': # No duplicates (better to filter in derivation script!!)
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=currentColor, 
                                        linestyle = ':', linewidth=5)
                plt.gca().add_patch(derivedArrow)
                if labels:
                    plt.text(azimuth_x, azimuth_y, shortrels[drels], color=currentColor, 
                         fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))
            if 'combi' in plotRels and dtype == 'combi':
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=currentColor, 
                                        linestyle = '--', linewidth=5)
                plt.gca().add_patch(derivedArrow)
                if labels:
                    plt.text(azimuth_x, azimuth_y, shortrels[drels], color=currentColor, 
                             fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))

    
    if legend:

        ax = plt.gca()
    
        # Legend 1: relation class / derivation type by line style
        if "Relation type" in legend:
    
            type_legend_handles = []
    
            if 'baseline' in plotRels:
                type_legend_handles.append(
                    Line2D(
                        [0], [0],
                        color='black',
                        linestyle='-',
                        linewidth=5,
                        label='Baseline'
                    )
                )
    
            if 'mutual' in plotRels:
                type_legend_handles.append(
                    Line2D(
                        [0], [0],
                        color='black',
                        linestyle=':',
                        linewidth=5,
                        label='Mutual'
                    )
                )
    
            if 'combi' in plotRels:
                type_legend_handles.append(
                    Line2D(
                        [0], [0],
                        color='black',
                        linestyle='--',
                        linewidth=5,
                        label='Combinatorial'
                    )
                )
    
            if type_legend_handles:
                type_legend = ax.legend(
                    handles=type_legend_handles,
                    title="Relation type",
                    loc="upper left",
                    fontsize=35,
                    title_fontsize=40,
                    frameon=False
                )
    
                ax.add_artist(type_legend)
    
        # Legend 2: specific relation labels by color
        if "Relation colors" in legend:
    
            relation_legend_handles = []
    
            for rel_label in all_relation_labels:
                relation_legend_handles.append(
                    Line2D(
                        [0], [0],
                        color=relation_colors[rel_label],
                        linestyle='-',
                        linewidth=5,
                        label=rel_label
                    )
                )
    
            if relation_legend_handles:
                ax.legend(
                    handles=relation_legend_handles,
                    title="Relation",
                    loc="upper right",
                    fontsize=35,
                    title_fontsize=40,
                    frameon=False
                )

    # title
    if plotTitle == '' or plotTitle is None: 
        if not 'mutual' in plotRels and 'combi' not in plotRels:
            title = 'Trained Relational Network'
        elif 'mutual' in plotRels and not 'combi' in plotRels:
            title = 'Trained and Mutually Entailed Relational Network'
        else:
            title = 'Trained and Derived Relational Network'
    else:
        title = plotTitle
    plt.title(title, fontsize=72, fontweight = 'bold')
    
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