# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 04:47:43 2024

Script to plot a relational network as a graph (kind of) on a grid

Mainly need to specify a baseline network (dict as in other applications)
    Can then choose to plot baseline and/or mutually and/or combinatorially
    derived relations
        At the moment, linear protocol plotted as polygon, whearas OTM/MTO are 
        plotted with 'one' S in the center of the polygon 
        (except 2- or 3-nod)
    Can adapt plot characteristics (e.g., node and arrow styles, fonts, title)
TODO:
    - clean up
    - how to decide on network shape, based on input?
        - option to choose line vs polygpn?
    - labels rotated to match arrow?
            or rather change arrow labels to symbols with legend
    - get user-specified input and general notebook outlined

    
    
@author: mraemaek
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
import string
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D  # <— for legend proxies

from derivationTablesFromSourceRelations import derivationTablesFromSourceRelations
from deriveRelationsFromBaseline import deriveRelationsFromBaseline

# plot parameteres
radius = .18 # Determines curvature of lines between stimuli, can tweak to make plot more readable
# Between .15 and .3 seems to provide best results
plotBaseline = True
relColor = 'black'
legendBaseline = False # include in legend?

plotMutual = False
mrelColor = '#0072B2'
legendMutual = False

plotCombinatorial = False
crelColor = '#CC79A7'
legendCombi = False

# accessible colors: '#0072B2', '#009E73', '#D55E00', '#CC79A7'

plotTitle = False
if plotTitle: title = 'Trained Relational Network'


#       "simple, head_length=50, head_width=15, tail_width=5" # Simple arrow growing thinner
relArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
drelArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
label_offset = .55 # Play around with how close labels are plotted to lines
relLabelFontSize = 50
sLabelFontSize = 60
sDotSize = 100

figsize = (25,25)

# Specify training protocol
protocol = 'OneToMany' # For one-to-many or many-to-one, the 'one' is plotted in the middle

# Define default relations
relations = dict({'Same as': 0,
             'Different from': 1,
             'Opposite to': 2,
             'More than': 3,
             'Less than': 4,
             'Contains': 5,
             'Is part of': 6,
             'Before': 7,
             'After': 8})
mutual, combi = derivationTablesFromSourceRelations(relations)
# Deinfe baseline network
baseline = dict({'Same as': [(0,1), (0, 4)],
                  'Different from': [(0,2), (0,5)], 
                'Opposite to': [(0,3), (0,6)]
             })

# for model manuscript figure
lmap = {'Same as': 'S', 'Different from': 'D', 'Opposite to': 'O'}
def pretty_label(name: str) -> str:
    return lmap.get(name, name)


# derive relations (or do on the spot while plotting?)
plot = False
printRels = False
unique = []
for rels in baseline.keys():
    for rel in baseline[rels]: 
        for s in rel: 
            if s not in unique: unique.append(s)
n_stim = len(unique) 
sLabs = ['A1', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'D3']
relTab, derived = deriveRelationsFromBaseline(baseline, plot, printRels, n_stim, sLabs)

vertices = []
def polygon_coords(n_nodes, radius=n_stim*45, center=(n_stim*50, n_stim*50)):
    # Compute the vertices
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

vertices = polygon_coords(n_stim)


# Create a Cartesian grid plot without showing the grid
plt.figure(figsize=figsize)  # Set figure size
plt.plot([], [])  # Create an empty plot (optional for axes setup)
plt.xlim(0,  n_stim*100)  # Set x-axis range
plt.ylim(0,  n_stim*100)  # Set y-axis range


# Intitialize to ensure network is constructed the same for baseline/derived
plottedS = dict({})
for i in range(n_stim):
    plottedS[sLabs[i]] =  [vertices[len(plottedS.keys())]]
plottedRels = dict({})

if plotBaseline:
    # Loop through baseline relations
    for rels in baseline.keys():
        for rel in baseline[rels]:
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
            # pdb.set_trace()
            baselineArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                    connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                    arrowstyle= relArrowStyle, color=relColor, linewidth=1.5)
            plt.gca().add_patch(baselineArrow)
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
            plt.text(azimuth_x, azimuth_y, pretty_label(rels), color=relColor, 
                     fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
        
plotted = []
# Loop through derived relations
for drels in derived.keys():
    for drel in derived[drels]:
        if drel not in baseline[drels]: # account for derivation of baseline relations, don't include
            if not plotBaseline: # Plot nodes if no baseline relations plotted 
                for s in range(2):
                    # plot a labeled point on the grid
                    x = plottedS[sLabs[drel[s]]][0][0]
                    y = plottedS[sLabs[drel[s]]][0][1]
                    plt.plot(x, y, 'o', markersize = sDotSize, color = 'grey')  # Plot point
                    plt.text(x, y , sLabs[drel[s]], 
                             fontweight = 'bold', fontsize=sLabelFontSize, ha='center', va = 'center')  # Label next to the point
            # Figure out if derivation is mutual or not?
            if list(relations.keys())[mutual[relations[drels]]] in baseline.keys():
                if (drel[1], drel[0]) in baseline[list(relations.keys())[mutual[relations[drels]]]]:
                    type = 'mutual'
                else: type = 'combi'
            # get coords for relation
            x_start, y_start = plottedS[sLabs[drel[0]]][0][0], plottedS[sLabs[drel[0]]][0][1]        
            x_end, y_end = plottedS[sLabs[drel[1]]][0][0], plottedS[sLabs[drel[1]]][0][1]
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
            
            
            # if x_start != x_end and y_start != y_end: # no self relations (filtered out?)
            if plotMutual and type == 'mutual': # No duplicates (better to filter in derivation script!!)
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=mrelColor, 
                                        linestyle = ':', linewidth=1)
                plt.gca().add_patch(derivedArrow)
                plt.text(azimuth_x, azimuth_y, pretty_label(drels), color=mrelColor, 
                         fontsize=relLabelFontSize, ha='center', fontweight = 'bold')
                plotted.append((drel))
            if plotCombinatorial and type == 'combi':
                # Plot a curved line using FancyArrowPatch 
                derivedArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                        arrowstyle=drelArrowStyle, color=crelColor, 
                                        linestyle = '--', linewidth=1)
                plt.gca().add_patch(derivedArrow)
                plt.text(azimuth_x, azimuth_y, pretty_label(drels), color=crelColor, 
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
# %%
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Initialize the graph
G = nx.DiGraph()  # Directed graph for relationships

# Define relations and stimuli
relations = {
    "Same as": 0,
    "Different from": 1,
    "Opposite to": 2,
    "More than": 3,
    "Less than": 4,
    "Contains": 5,
    "Is part of": 6,
    "Before": 7,
    "After": 8,
}
# Optional to have relation-specific colors (get better colors tho)
relColors = False
if relColors:
    rel_colors = {
        "Less than": "blue",
        "More than": "green",
        "Same as": "yellow",
        "Different from": "red",
        "Opposite to": "yellow",
        "Contains": "orange",
        "Is part of": "brown",
        "Before": "cyan",
        "After": "pink",
    }

# Define baseline network
baseline = {
    "Same as": [(0, 1), (0, 4)],
    # "More than": [(0, 2), (0, 5)],
    "Less than": [(0, 2), (0, 3)]
}
plot = False
printRels = False
unique = []
for rels in baseline.keys():
    for rel in baseline[rels]: 
        for s in rel: 
            if s not in unique: unique.append(s)
n_stim = len(unique) 
relTab, derived = deriveRelationsFromBaseline(baseline, plot, printRels, n_stim, sLabs)

# Define labels for stimuli
sLabs = ["A", "B1", "B2", "B3", "C1", "C2", "C3", "N"]
label_offset = 1
edge_colors = []
edge_styles = []
# Add nodes and edges for baseline relations
for rel, pairs in baseline.items():
    for src, tgt in pairs:
        G.add_node(sLabs[src])  # Add source node
        G.add_node(sLabs[tgt])  # Add target node
        G.add_edge(sLabs[src], sLabs[tgt], relation=rel)  # Add edge with relation label
        if relColors:
            edge_colors.append(rel_colors[rel])
        else:
            edge_colors.append(relColor)
        # edge_styles.append("-")

for rel, pairs in derived.items():
    for src, tgt in pairs:
        G.add_node(sLabs[src])  # Add source node
        G.add_node(sLabs[tgt])  # Add target node
        G.add_edge(sLabs[src], sLabs[tgt], relation=rel)  # Add edge with relation label
        if relColors:
            edge_colors.append(rel_colors[rel])
            
        else:
            edge_colors.append(drelColor)
        # edge_styles.append(":")
# Use a circular layout for node positions
pos = nx.circular_layout(G)

# Plot the graph
plt.figure(figsize=(10, 10), dpi=100)  # Lower DPI to reduce pixel dimensions

# Draw nodes with labels
nx.draw_networkx_nodes(G, pos, node_size=800, node_color="lightgrey")
nx.draw_networkx_labels(G, pos, font_size=14, font_weight="bold")



# # Draw edges with labels
nx.draw_networkx_edges(G, pos, arrowstyle="simple, tail_width = .1, head_width = .4, head_length = 1",
                        # style = edge_styles,
                        arrowsize=20, edge_color=edge_colors, connectionstyle="arc3,rad=0.3")
edge_labels = nx.get_edge_attributes(G, "relation")
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=12)

# Alternatively draw labels on the curves, to adress assymetrical relations
i = 0
for (src, tgt, data) in G.edges(data=True):
    i +=1 
    # Get source and target positions
    x1, y1 = pos[src]
    x2, y2 = pos[tgt]

    # Calculate midpoint
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    mid_x, mid_y = (x_start + x_end)/ 2, (y_start + y_end)/ 2# midpoint for positioning
    # make label position function of direction of arrow up/down-left/right       
    dx, dy = x_end - x_start, y_end - y_start # Vector from start to end
    distance = np.sqrt(dx**2 + dy**2) # Calculate the distance between start and end points
    # Calculate angle of the line segment for consistent radial offset
    angle = np.arctan2(dy, dx) + np.pi / 2  # Rotate by 90 degrees to get perpendicular
    offset = radius * distance # Offset for curve/label based on radius
    # Azimuth point for label, shifted by label_offset in the radial direction
    azimuth_x = mid_x - offset * np.cos(angle) *label_offset
    azimuth_y = mid_y - offset * np.sin(angle) *label_offset
    # Draw the label
    plt.text(
        azimuth_x,
        azimuth_y,
        data["relation"],
        fontsize=12,
        color=edge_colors[i],
        ha="center",
        va="center",
    )

# Set plot title
plt.title("Relational Network Graph", fontsize=24, fontweight="bold")

# Hide axes
plt.axis("off")

# Show the plot
plt.show()

# %%
for rels in range(len(list((baseline.keys())))):
    for rel in list(baseline.values())[rels]:
        brelLab = list(baseline.keys())[rels] # label for arrow
        brel = relations[brelLab] # get correct index for derivation tables
        for s in range(2):
            # First plot dot if new stimulus
            if not sLabs[rel[s]] in plottedS.keys():
                plottedS[sLabs[rel[s]]] = [vertices[len(plottedS.keys())]] 
                # plot a labeled point on the grid
                x = plottedS[sLabs[rel[s]]][0][0]
                y = plottedS[sLabs[rel[s]]][0][1]
                plt.plot(x, y, 'o', markersize = 25, color = 'grey')  # Plot point
                plt.text(x, y , sLabs[rel[s]], 
                         fontweight = 'bold', fontsize=14, ha='center', va = 'center')  # Label next to the point
                if s: # store coords for plotting
                    x_end, y_end = x, y
                else: 
                    x_start, y_start = x, y
        
        
        # Plot a curved line using FancyArrowPatch 
        baselineArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                connectionstyle="arc3,rad={}".format(radius),  # Controls the curvature
                                arrowstyle="->", color="black", linewidth=1.5)
        plt.gca().add_patch(baselineArrow)
        # Label the curve, position depending on symmetry of relation
        mid_x, mid_y = (x_start + x_end)/ 2, (y_start + y_end)/ 2# midpoint for positioning
        # make label position function of direction of arrow up/down-left/right
                
        if brelLab not in ['Same as', 'Different from', 'Opposite to']:            
            
            dx, dy = x_end - x_start, y_end - y_start # Vector from start to end
            
            distance = np.sqrt(dx**2 + dy**2) # Calculate the distance between start and end points
            # Calculate angle of the line segment for consistent radial offset
            angle = np.arctan2(dy, dx) + np.pi / 2  # Rotate by 90 degrees to get perpendicular
    
            offset = radius * distance # Offset based on radius
            # Azimuth point for label, shifted by label_offset in the radial direction
            azimuth_x = mid_x - offset * np.cos(angle) *.75
            azimuth_y = mid_y - offset * np.sin(angle) *.75
            plt.text(azimuth_x, azimuth_y, brelLab, color=relColor, 
                     fontsize=8, ha='center', fontweight = 'bold')
        else:
            plt.text(mid_x , mid_y , brelLab, color=relColor, 
                     fontsize=8, ha='center', fontweight = 'bold')
        
        # update tracker dict
        if brelLab not in plottedRels.keys(): plottedRels[brelLab] = [rel]
        else: plottedRels[brelLab].append(rel)
        
        # Add arrow for mutually entailed relation (for now, ultimately just loop derived dict)
        mut = mutual[relations[brelLab]] # get derived relation from table
        mrelLab = list(relations.keys())[mut] # label for arrow plot
        mutualArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                connectionstyle="arc3,rad=-{}".format(radius),  # Controls the curvature
                                arrowstyle="<-", color=drelColor, linestyle = ':',linewidth=1.5 )
        plt.gca().add_patch(mutualArrow)
        # Label the mutual curve only if assymetric (i.e., derived rel != baseline rel)
        if brelLab not in ['Same as', 'Different from', 'Opposite to']:    
            # Calculate azimuth point in the other direction- midpoint offset by perpendicular vector
            azimuth_x = mid_x + offset * np.cos(angle) *.75
            azimuth_y = mid_y + offset * np.sin(angle) *.75
            plt.text(azimuth_x, azimuth_y, mrelLab, # label
                     color=drelColor, fontsize=8, ha='center',
                     fontweight = 'bold')   
        # Find a second relation in plotted relations to combinatorially entail
        for rels2 in range(len(plottedRels.keys())):
            brel2lab = list(plottedRels.keys())[rels2] # label for arrow plot
            brel2 = relations[brel2lab] # get correct index for derivation tables
            for rel2 in plottedRels[brel2lab]: 
                
                # Find common and determine combination protocol
                for sr1 in range(len(rel)):
                    for sr2 in range(len(rel)):
                        if rel[sr1] == rel2[sr2]:
                            common = rel2[sr2]
                if tuple.index(rel, common) == 0:
                    if tuple.index(rel, common) == 0: # A-B & A - C (OTM)
                        com = combi['OTM'][brel, brel2]
                        ce_relata = [rel[1], rel2[1]]

                    else: # A - B & C - A (sort of MTO)
                        com = combi['sMTO'][brel, brel2]
                        ce_relata = [rel[1], rel2[0]]
                else:
                    if tuple.index(rel2, common) == 0: # A-B & B - C (linear)
                        # pdb.set_trace()
                        com = combi['Linear'][brel, brel2]
                        ce_relata = [rel[0], rel2[1]]
                    else: # A-B & C- B (MTO)
                        com = combi['MTO'][brel, brel2]
                        ce_relata = [rel[0], rel2[0]]
                
                # Then derive
                # NOTE: again this works for now, but in case of large 
                # networks essentially requires entire function be recreated.....
                if com >= 0 and (ce_relata[0], ce_relata[1]) not in plottedRels[brel2lab]: # only plot well-defined relations
                    mcom = mutual[com] #  mutual of combinatorially entailed 
                    crelLab = list(relations.keys())[com] # label
                    mcrelLab = list(relations.keys())[mcom] # label
                    
                    # fetch coords for Ss in entailed relation
                    s1, s2 = plottedS[sLabs[ce_relata[0]]][0], plottedS[sLabs[ce_relata[1]]][0]
                    x_start, x_end, y_start, y_end = s1[0], s2[0], s1[1], s2[1]
                    mid_x, mid_y = (x_start + x_end) / 2, (y_start + y_end) / 2 # midpoint for labels
                    
                    # Note: combinatorially entailed relations labels always plotted on curve (to avoid overlap)
                    dx, dy = x_end - x_start, y_end - y_start # Vector from start to end
                    distance = np.sqrt(dx**2 + dy**2) # Calculate the distance between start and end points
                    # Calculate angle of the line segment for consistent radial offset
                    angle = np.arctan2(dy, dx) + np.pi / 2  # Rotate by 90 degrees to get perpendicular
            
                    offset = radius * distance # Offset based on radius
                    # Azimuth point for label, shifted by label_offset in the radial direction
                    azimuth_x = mid_x - offset * np.cos(angle) *.75
                    azimuth_y = mid_y - offset * np.sin(angle) *.75
                    
                    combiArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                            connectionstyle="arc3,rad={}".format(radius),  
                                            arrowstyle="<-", color= drelColor, linestyle = ':',linewidth=1.5 )
                    plt.gca().add_patch(combiArrow)

                    pdb.set_trace()
                    
                    plt.text(azimuth_x , azimuth_y, crelLab, #label
                              color=drelColor, fontsize=8, ha='center', fontweight = 'bold')

                    pdb.set_trace()
                    mcombiArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                            connectionstyle="arc3,rad=-{}".format(radius),  
                                            arrowstyle="<-", color=drelColor, linestyle = ':',linewidth=1.5 )
                    plt.gca().add_patch(mcombiArrow)

                    pdb.set_trace()

                    # mutual relation label offset in other direction
                    azimuth_x = mid_x + offset * np.cos(angle) *.75
                    azimuth_y = mid_y + offset * np.sin(angle) *.75
                    plt.text(azimuth_x, azimuth_y, mcrelLab, #label
                              color=drelColor, fontsize=8, ha='center', fontweight = 'bold')  

                    pdb.set_trace()

           
                        
            # elif len(plottedRels.keys()) >= 2:
            #     # If only one instance of the current relation plotted, check others
            #     for rels2 in range(len(list(plottedRels.keys()))):
            #         if not rels == rels2: # skip baseline relation
            #             brel2lab = list(plottedRels.keys())[rels2] # label for arrow plot                        
            #             brel2 = relations[brel2lab] # get correct index for derivation tables
            #             for rel2 in list(plottedRels.values())[rels2]: 
            #                 # Loop through list backwards
            #                 if not rel == rel2:
            #                     # Find common and determine combination protocol
            #                     for sr1 in range(len(rel)):
            #                         for sr2 in range(len(rel)):
            #                             if rel[sr1] == rel2[sr2]:
            #                                 common = rel2[sr2]
            #                     if tuple.index(rel, common) == 0:
            #                         if tuple.index(rel, common) == 0: # A-B & A - C (OTM)
            #                             com = combi['OTM'][brel, brel2]
            #                             ce_relata = [rel[1], rel2[1]]

            #                         else: # A - B & C - A (sort of MTO)
            #                             com = combi['sMTO'][brel, brel2]
            #                             ce_relata = [rel[1], rel2[1]]
            #                     else:
            #                         if tuple.index(rel2, common) == 0: # A-B & B - C (linear)
            #                             # pdb.set_trace()
            #                             com = combi['Linear'][brel, brel2]
            #                             ce_relata = [rel[0], rel2[1]]
            #                         else: # A-B & C- B (MTO)
            #                             com = combi['MTO'][brel, brel2]
            #                             ce_relata = [rel[0], rel2[1]]
                            
            #                 if com >= 0: # only plot well-defined relations
            #                     mcom = mutual[com] #  mutual of combinatorially entailed 
            #                     crelLab = list(relations.keys())[com] # label
            #                     mcrelLab = list(relations.keys())[mcom] # label
                                
            #                     # need to fetch coords for correct SS
            #                     # pdb.set_trace()
            #                     s1, s2 = plottedS[sLabs[ce_relata[0]]][0], plottedS[sLabs[ce_relata[1]]][0]
            #                     x_start, x_end, y_start, y_end = s1[0], s2[0], s1[1], s2[1]
            #                     if brelLab not in ['Same as', 'Different from', 'Opposite to']:            
            #                         if x_start < x_end and y_start < y_end: # curve trends towards higher x and y (top right)
            #                             #  curve bends clockwise -> print on bottom right of midpoint
            #                             nudge_x, nudge_y = 3, -3
            #                         elif x_start < x_end and y_start >= y_end: # curve trends towards bottom right
            #                             nudge_x, nudge_y = -3, -3 # print bottom left of mid
            #                         elif x_start >= x_end and y_start < y_end: # curve trends towards top left
            #                             nudge_x, nudge_y = 3,3 # print top right of mid
            #                         else: nudge_x, nudge_y = -3, 3 # curve trends bottom left, print top left
                                
            #                     mid_x, mid_y = (x_start + x_end) / 2, (y_start + y_end) / 2 # midpoint for labels
                                
            #                     combiArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
            #                                             connectionstyle="arc3,rad=.3",  
            #                                             arrowstyle="<-", color="black", linestyle = ':',linewidth=1.5 )
            #                     plt.gca().add_patch(combiArrow)
                                
            #                     # Label position dependent on symmetry
            #                     if crelLab not in ['Same as', 'Different from', 'Opposite to']: 
            #                         plt.text(mid_x + nudge_x, mid_y + nudge_y, crelLab, #label
            #                                  color="black", fontsize=8, ha='center', fontweight = 'bold')   
            #                     else: # no nudge for symmetric relations
            #                         plt.text(mid_x , mid_y, crelLab, #label
            #                                  color="black", fontsize=8, ha='center', fontweight = 'bold')
                                    
            #                     mcombiArrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
            #                                             connectionstyle="arc3,rad=.3",  
            #                                             arrowstyle="<-", color="black", linestyle = ':',linewidth=1.5 )
            #                     plt.gca().add_patch(combiArrow)
            #                     # plot mutual label only if not symmetrical
            #                     if crelLab not in ['Same as', 'Different from', 'Opposite to']: 
            #                         plt.text(mid_x - nudge_x, mid_y - nudge_y , mcrelLab, #label
            #                                  color="black", fontsize=8, ha='center', fontweight = 'bold')  
            #         pdb.set_trace()
                   
# Set labels and title (optional)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Cartesian Plot Without Grid')

# Ensure grid is not displayed
plt.grid(False)

# Display the plot
plt.show()

