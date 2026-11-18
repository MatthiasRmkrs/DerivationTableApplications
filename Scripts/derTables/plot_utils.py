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


from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.gridspec import GridSpec

def plotTablesHeatmap(
    relations,
    mutual,
    combi,
    save_path=None,
    palette="YlGnBu"
):
    """
    Create a five-panel manuscript figure displaying mutual
    and combinatorial entailment tables.

    A: Mutual entailment (full-width top panel)
    B-E: Four combinatorial entailment configurations

    All panels use the same categorical color mapping.

    Parameters
    ----------
    relations : dict
        Relation labels mapped to integer indices.
    mutual : array-like
        Mutually entailed relation index for each relation.
    combi : dict
        Four combinatorial entailment matrices.
    save_path : str or Path, optional
        Base filename for exporting PNG and PDF.
    palette : str
        Seaborn categorical palette.
    """

    n_rels = len(relations)

    inv_relations = {v: k for k, v in relations.items()}
    shortrels, longrels = createPlotRelLabels(relations)

    # -----------------------------------------------------
    # Shared categorical colormap
    # -----------------------------------------------------

    colors = sns.color_palette(
        palette,
        n_colors=n_rels
    )

    cmap = ListedColormap(colors)
    cmap.set_bad("lightgray")

    norm = BoundaryNorm(
        np.arange(-0.5, n_rels + 0.5, 1),
        ncolors=n_rels
    )

    # -----------------------------------------------------
    # Figure layout
    # -----------------------------------------------------

    fig = plt.figure(figsize=(15, 15))

    gs = GridSpec(
        3, 2,
        figure=fig,
        height_ratios=[0.55, 1.5, 1.5],
        hspace=0.45,
        wspace=0.35
    )

    ax_mutual = fig.add_subplot(gs[0, :])

    axes_combi = [
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1]),
        fig.add_subplot(gs[2, 0]),
        fig.add_subplot(gs[2, 1])
    ]

    # =====================================================
    # A. Mutual entailment
    # =====================================================

    mutual_matrix = np.zeros(
        (2, n_rels),
        dtype=int
    )

    for i in range(n_rels):
        mutual_matrix[0, i] = relations[list(relations)[i]]
        mutual_matrix[1, i] = mutual[i]

    mutual_labels = np.empty(
        mutual_matrix.shape,
        dtype=object
    )

    for row in range(2):
        for col in range(n_rels):

            rel_idx = mutual_matrix[row, col]

            mutual_labels[row, col] = (
                shortrels[inv_relations[rel_idx]]
                if rel_idx >= 0 else ""
            )

    mutual_df = pd.DataFrame(
        mutual_matrix,
        index=[
            "Original relation (AxB)",
            "Bidirectional relation (BxA)"
        ],
        columns=list(relations)
    ).replace(-1, np.nan)

    sns.heatmap(
        mutual_df,
        annot=mutual_labels,
        fmt="",
        cmap=cmap,
        norm=norm,
        cbar=False,
        linewidths=0.7,
        linecolor="white",
        annot_kws={
            "weight": "bold",
            "fontsize": 11
        },
        ax=ax_mutual
    )

    ax_mutual.set_title(
        "A. Bidirectional Relations",
        fontweight="bold",
        fontsize=14,
        pad=14
    )

    ax_mutual.set_xticks(
        np.arange(n_rels) + 0.5
    )

    ax_mutual.set_xticklabels(
        [shortrels[r] for r in relations],
        rotation=0,
        fontweight="bold"
    )

    ax_mutual.tick_params(
        axis="y",
        rotation=0,
        length=0
    )

    # =====================================================
    # B-E. Combinatorial entailment
    # =====================================================

    panel_letters = ["B", "C", "D", "E"]

    for i, (comb_type, matrix) in enumerate(combi.items()):

        if i >= 4:
            break

        ax = axes_combi[i]

        df = pd.DataFrame(
            matrix,
            index=list(relations),
            columns=list(relations)
        ).replace(-1, np.nan)

        # Annotation matrix
        annotations = np.empty(
            df.shape,
            dtype=object
        )
        
        
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):

                value = df.iloc[row, col]

                if pd.isna(value):
                    annotations[row, col] = ""
                else:
                    annotations[row, col] = (
                        shortrels[inv_relations[int(value)]]
                    )

        sns.heatmap(
            df,
            annot=annotations,
            fmt="",
            cmap=cmap,
            norm=norm,
            cbar=False,
            linewidths=0.5,
            linecolor="white",
            square=True,
            annot_kws={
                "weight": "bold",
                "fontsize": 10
            },
            ax=ax
        )

        ax.set_title(
            f"{panel_letters[i]}. {type_labs[comb_type]}",
            fontweight="bold",
            fontsize=13,
            pad=16
        )

        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        ax.set_xlabel(
            rel2_x[comb_type],
            fontweight="bold",
            fontsize=11
        )

        if i % 2 == 0:
            ax.set_ylabel(
                "First relation (AxB)",
                fontweight="bold",
                fontsize=11
            )

        ax.set_xticks(
            np.arange(n_rels) + 0.5
        )
        ax.set_xticklabels(
            [shortrels[r] for r in relations],
            rotation=0,
            fontweight="bold"
        )

        ax.set_yticks(
            np.arange(n_rels) + 0.5
        )
        ax.set_yticklabels(
            [longrels[r] for r in relations],
            rotation=0
        )

        ax.tick_params(length=0)
    
    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    if save_path is not None:

        from pathlib import Path

        save_path = Path(save_path)

        fig.savefig(
            save_path.with_suffix(".png"),
            dpi=300,
            bbox_inches="tight"
        )

        fig.savefig(
            save_path.with_suffix(".pdf"),
            bbox_inches="tight"
        )

    plt.show()

    return fig



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


def degree_layout(G, scale=100, class_spacing=2.5):
    """
    Arrange each disconnected component as a star/polygon.

    For each component:
    - The highest-degree node is placed centrally.
    - Remaining nodes are evenly distributed around it.
    - Components are arranged horizontally.

    Works with multiple classes of different sizes.
    """

    if G.number_of_nodes() == 0:
        return {}

    # Identify independent classes/components
    components = list(nx.connected_components(G.to_undirected()))

    pos = {}

    # Position each class separately
    for ci, component in enumerate(components):

        subG = G.subgraph(component)

        # Determine central node within this class
        degrees = dict(subG.degree())
        center_node = max(degrees, key=degrees.get)

        other_nodes = [
            node for node in subG.nodes
            if node != center_node
        ]

        n = len(other_nodes)

        # Horizontal position of class center
        cx = ci * scale * class_spacing
        cy = 0

        pos[center_node] = (cx, cy)

        # Arrange remaining stimuli around their class center
        for k, node in enumerate(other_nodes):

            angle = 2 * np.pi * k / max(n, 1)

            pos[node] = (
                cx + scale * np.cos(angle),
                cy + scale * np.sin(angle)
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


def linear_series_layout(baseline, sLabs, spacing=250, row_spacing=380, margin=150):
    """Place independent baseline chains on parallel horizontal rows.

    Isolated nodes (e.g. a test-only second class when using the wrong baseline)
    are grouped into one horizontal row in stimulus-label order rather than
    becoming separate vertical single-node rows. Use the actual task baseline
    for semantically meaningful chain ordering.
    """
    G = nx.Graph()
    G.add_nodes_from(sLabs)
    for pairs in baseline.values():
        for source, target in pairs:
            G.add_edge(sLabs[int(source)], sLabs[int(target)])

    order = {label: index for index, label in enumerate(sLabs)}
    components = list(nx.connected_components(G))
    chains, isolated = [], []
    for component in components:
        subgraph = G.subgraph(component)
        if len(component) == 1:
            isolated.extend(component)
            continue
        if any(degree > 2 for _, degree in subgraph.degree()):
            raise ValueError("layout='line' requires unbranched baseline chains; "
                             "try 'hierarchical' or 'degree' instead.")
        ends = [node for node, degree in subgraph.degree() if degree == 1]
        if len(ends) != 2:
            raise ValueError("layout='line' requires acyclic baseline chains.")
        current = min(ends, key=order.get)
        previous = None
        chain = []
        while current is not None:
            chain.append(current)
            neighbors = [node for node in subgraph.neighbors(current)
                         if node != previous]
            previous, current = current, (neighbors[0] if neighbors else None)
        chains.append(chain)
    if isolated:
        chains.append(sorted(isolated, key=order.get))
    chains.sort(key=lambda chain: min(order[node] for node in chain))
    return {node: (float(margin + col * spacing),
                   float(margin - row * row_spacing))
            for row, chain in enumerate(chains)
            for col, node in enumerate(chain)}


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
    - 'line' (one or more independent baseline chains)
    - 'manual'
    """

    if sLabs is None:
        raise ValueError("sLabs must be provided to compute stimulus layout.")

    if layout == "line":
        # Use BASELINE edges, not derived links, to preserve chain order.
        # Use fixed spacing rather than normalization, so separate chains
        # remain parallel and nodes are evenly separated.
        return linear_series_layout(baseline, sLabs, margin=margin)

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
            "'hierarchical', 'line', or 'manual'."
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
    relArrowStyle = "-|>,head_length=20.0,head_width=5"
    drelArrowStyle = "-|>,head_length=20,head_width=5"
    
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
    if derived is None:
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
        
    shortrels, _ = createPlotRelLabels(
        dict.fromkeys(list(baseline.keys()) + list(derived.keys()))
    )

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
    
    # Leave dedicated space on the right for BOTH legends, outside the axes.
    if layout == 'line':
        n_rows = len(set(y for x, y in layout_positions.values()))
        figsize = (17, max(4.5, 2.3 * n_rows + 1.5))
    else:
        figsize = (25, 25)
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=.055, right=.74, top=.82, bottom=.12)
    if layout == 'line':
        # Old defaults were sized for a 25-inch square figure.
        if fontSize == 50:
            relLabelFontSize = sLabelFontSize = 16
        if sDotSize == 100:
            sDotSize = 34
        arrow_shrink, arrow_width = 17, 2.2
    else:
        arrow_shrink, arrow_width = 40, 5

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
    # Track relation labels actually drawn, preserving first-seen order.
    plotted_relation_labels = dict.fromkeys([])

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
                                        arrowstyle= relArrowStyle, color=currentColor,
                                        shrinkA=arrow_shrink,shrinkB=arrow_shrink,linewidth=arrow_width)
                plt.gca().add_patch(baselineArrow)
                plotted_relation_labels[rels] = None
                
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
                                        linestyle = ':', shrinkA=arrow_shrink, shrinkB=arrow_shrink, linewidth=arrow_width)
                plt.gca().add_patch(derivedArrow)
                plotted_relation_labels[drels] = None
                if labels:
                    plt.text(azimuth_x, azimuth_y, shortrels[drels], color=currentColor, 
                         fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))
            if 'combi' in plotRels and dtype == 'combi':
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=currentColor, 
                                        linestyle = '--', shrinkA=arrow_shrink,shrinkB=arrow_shrink, linewidth=arrow_width)
                plt.gca().add_patch(derivedArrow)
                plotted_relation_labels[drels] = None
                if labels:
                    plt.text(azimuth_x, azimuth_y, shortrels[drels], color=currentColor, 
                             fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))

    
    if legend:
        type_handles = []
        for kind, linestyle, caption in (
            ('baseline', '-', 'Baseline'),
            ('mutual', ':', 'Mutual'),
            ('combi', '--', 'Combinatorial')
        ):
            if kind in plotRels:
                type_handles.append(Line2D([0], [0], color='black',
                                           linestyle=linestyle, linewidth=2.5,
                                           label=caption))

        color_handles = [
            Line2D([0], [0], color=relation_colors[name], linewidth=2.5,
                   label=name)
            for name in plotted_relation_labels
        ]
        legend_font = 12 if layout == 'line' else 20
        if 'Relation type' in legend and type_handles:
            first = fig.legend(handles=type_handles, title='Relation type',
                               loc='upper left', bbox_to_anchor=(.77, .79),
                               fontsize=legend_font, title_fontsize=legend_font + 1,
                               frameon=False)
        if 'Relation colors' in legend and color_handles:
            fig.legend(handles=color_handles, title='Relation',
                       loc='upper left', bbox_to_anchor=(.77, .44),
                       fontsize=legend_font, title_fontsize=legend_font + 1,
                       frameon=False)

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
    fig.suptitle(title, fontsize=(19 if layout == 'line' else 34), fontweight='bold', y=.96)
    
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