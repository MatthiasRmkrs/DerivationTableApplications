# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:27:23 2026

Streamlit app for relational network visualizer

@author: mraemaek
"""

import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import inspect

# IMPORT FUNCTION
from derTables.plot_utils import plotRelNetworkGraph


st.set_page_config(layout="wide")

st.title("Relational Network Graph Visualizer")

st.markdown("""
This app helps you visualize a relational network of your choosing as a directed graph network.

Simplest use-case is for users to specify a set of baseline relations, the function 
will then automatically compute all relations that can be derived from those baseline 
relations, and plot the full network as a labeled graph network.

Users can optionally choose to manually specify the derived relations as well, instead of
automatically deriving all relations.

Users can specify the layout of the network (circular, degree-based, linear, etc.)
and tweak various other plot settings (colors, labels, ...).

Hover over the question marks in the sidebar for more information.

""")


# SIDEBAR

st.sidebar.header("Network Specification")

n_stim = st.sidebar.slider(
    "Number of stimuli",
    min_value=2,
    max_value=15,
    value=0,
    help = "Specify the number of stimuli in the relational network."
)

default_labels = [chr(65+i) for i in range(n_stim)]

label_string = st.sidebar.text_input(
    "Stimulus labels (comma-separated)",
    value=",".join(default_labels),
    help = "Provide as many labels as the number of stimuli you want to include in the network, spearated by commas"
)

sLabs = [x.strip() for x in label_string.split(",")]

relation_options = [
    "Same as",
    "Different from",
    "Opposite to",
    "More than",
    "Less than",
    "Before",
    "After",
    "Contains",
    "Is part of",
    'Bigger than',
    'Smaller than',
    'Larger than',
    'Smaller than', 
    'Faster than',
    "Slower than", 
    'Stronger than',
    "Weaker than",
    'Better than',
    "Worse than", 
    'Longer than',
    "Shorter than",
    'Left of',
    'Right of',
    'In front',
    'Behind',
    'Above',
    'Below',
]

selected_relations = st.sidebar.multiselect(
    "Relations",
    relation_options,
    help = "Select all relations you want to include in the network. \
        You will be able to specify stimulus-pairs for each relation below."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Baseline relations")

baseline = {}

if selected_relations and len(sLabs) == n_stim:

    for relation in selected_relations:

        st.sidebar.markdown(f"### {relation}")

        n_pairs = st.sidebar.number_input(
            f"Number of '{relation}' relations",
            min_value=0,
            max_value=50,
            value=1,
            step=1,
            key=f"n_pairs_{relation}"
        )

        relation_pairs = []

        for i in range(n_pairs):

            c1, c2 = st.sidebar.columns(2)

            with c1:
                s1 = st.selectbox(
                    f"{relation}: source {i + 1}",
                    sLabs,
                    key=f"{relation}_s1_{i}"
                )

            with c2:
                default_target_index = min(i + 1, len(sLabs) - 1)

                s2 = st.selectbox(
                    f"{relation}: target {i + 1}",
                    sLabs,
                    index=default_target_index,
                    key=f"{relation}_s2_{i}"
                )

            relation_pairs.append(
                (sLabs.index(s1), sLabs.index(s2))
            )

        baseline[relation] = relation_pairs

else:
    if not selected_relations:
        st.sidebar.info("Select at least one relation type to include in the network.")
    if len(sLabs) != n_stim:
        st.sidebar.info("Define the stimulus labels before defining pairs.")

st.sidebar.markdown("---")
st.sidebar.subheader("Derived relations")

manual_derived = st.sidebar.checkbox(
    "Manually define derived relations",
    value=False,
    help=(
        "Check this box to manually specify derived relations (similar to baseline relations above)."
        "If not checked, derived relations will be computed automatically from the baseline relations."
    )
)

derived = None

if manual_derived:

    derived = {}

    derived_relations = st.sidebar.multiselect(
        "Derived relation types",
        relation_options,
        default=[],
        help="Select which relation types occur as derived relations."
    )

    if derived_relations and len(sLabs) == n_stim:

        for relation in derived_relations:

            st.sidebar.markdown(f"### Derived: {relation}")

            n_derived_pairs = st.sidebar.number_input(
                f"Number of '{relation}' relations",
                min_value=0,
                max_value=100,
                value=1,
                step=1,
                key=f"n_derived_pairs_{relation}"
            )

            derived_pairs = []

            for i in range(n_derived_pairs):

                c1, c2 = st.sidebar.columns(2)

                with c1:
                    s1 = st.selectbox(
                        f"Derived {relation}: source {i + 1}",
                        sLabs,
                        key=f"derived_{relation}_s1_{i}"
                    )

                with c2:
                    default_target_index = min(i + 1, len(sLabs) - 1)

                    s2 = st.selectbox(
                        f"Derived {relation}: target {i + 1}",
                        sLabs,
                        index=default_target_index,
                        key=f"derived_{relation}_s2_{i}"
                    )

                derived_pairs.append(
                    (sLabs.index(s1), sLabs.index(s2))
                )

            derived[relation] = derived_pairs

    else:
        if not derived_relations:
            st.sidebar.info("Select at least one derived relation type.")
        if len(sLabs) != n_stim:
            st.sidebar.info("Fix the stimulus labels before defining derived pairs.")
        
        
# Plot settings
st.sidebar.markdown("---")
st.sidebar.subheader("Plot Settings")


plotRels = st.sidebar.multiselect(
    "Relations to display",
    ["baseline", "mutual", "combi"],
    default=["baseline", "mutual", "combi"],
    help = "Select which relations to plot. To create separate plots for baseline and derived network, first generate plot with only baseline, then with only derived relations."
)

plotTitle = st.sidebar.text_input(
    "Plot title",
    value="Relational Network",
    help = "Specifiy the title for the plot, if any. If left empty, no title will be plotted"
)

layout = st.sidebar.selectbox(
    "Stimulus layout",
    [
        "auto",
        "circle",
        "spring",
        "degree",
        "hierarchical",
        "manual"
    ],
    index=0,
    help = "Determine the layout for the network. 'Auto' will adapt based on the specified network. \
        'circle' draws network as a circular polygon, works well for small networks. 'spring' adapts\
            based on network density (more connected stimuli near each other, network spread out to avoid overlap). \
                'degree' places highly connected nodes in centre. 'Hierarchical' orders node on a directed line."
)

# relation colors
st.sidebar.subheader("Relation colors")

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

# Make sure derived is at least an empty dictionary
if derived is None:
    derived_for_colors = {}
else:
    derived_for_colors = derived

all_relation_labels = list(dict.fromkeys(
    list(baseline.keys()) + list(derived_for_colors.keys())
))

relation_colors = {}

for i, rel_label in enumerate(all_relation_labels):

    default_color = default_relation_colors[i % len(default_relation_colors)]

    relation_colors[rel_label] = st.sidebar.color_picker(
        f"Color for '{rel_label}'",
        value=default_color,
        key=f"color_{rel_label}",
        help=f"Color used for all '{rel_label}' arrows."
    )

radius = st.sidebar.slider('Arrow Radius',
                           min_value = .0, max_value = .5, step = .01, value = .18,
                           help = "Determines curvature of lines between stimuli.")

labels = st.sidebar.checkbox(
    "Plot labels",
    value=False,
    help="Show abbreviated relation labels for arrows in the graph."
)

label_offset = st.sidebar.slider('Relation Label Offset',
                           min_value = .0, max_value = 1.0, step = .01, value = .55,
                           help = "Determines offset of label relative to arrows. Can be adapted to improve readability.")

fontSize = st.sidebar.slider('Fontsize',
                           min_value = 10, max_value = 100, step = 1, value = 60,
                           help = "Determines fontsize for relation and stimulus labels.")

sDotSize = st.sidebar.slider('Stimulus Node Size',
                           min_value = 0, max_value = 150, step = 1, value = 100,
                           help = "Determines fontsize for relation and stimulus labels.")

legend = st.sidebar.multiselect(
    "Legends to plot",
    ["Relation type", "Relation colors"],
    default=["Relation type", "Relation colors"],
    help=(
        "Choose which legends to show. "
        "'Relation type' explains solid/dotted/dashed arrows for baseline and derived relations. "
        "'Relation colors' explains which color belongs to each unique relation (same, different, ...)."
        "Deselect both to display NO legend."
    )
)

# INFORMATION

with st.expander("How to use the function?"):

    st.markdown("""
- Specify the number of stimuli in the network and provide their labels 
- Select the types of relations in the network, the number of instances of each relation and the pairs of related stimuli (optionally also define derived relations in same way)
- Specify the layout you want for the network (circular, degree-based, hierarchical, ...), which relations to plot and other plot settings.
- Press the 'Generate Network Graph' to create the plot and download it. 
""")

with st.expander("What are baseline and derived relations?"):

    st.markdown("""
### Baseline relations
Directly trained relations.

Example: A is more than B and B is more than C

### Derived relations
Relations inferred from the baseline network, by reversal or transitivity.

From the example above: B is less than A and A is more than C
can be derived.
""")

with st.expander("Example use"):

    st.markdown("""
Say we wanted to illustrate a basic version of the relational network trained in the seminal Steele and Hayes (1991) study.
The basic network involved seven stimuli arranged in a one-to-many protocol, so select 7 stimuli and give them labels A1, B1, B2, B3, C1, C2, C3.
Steele and Hayes trained sameness, difference and opposition relations, so select those.

Then, we specify two sameness relations (A1-B1 and A1-C1), two difference relations (A1-B2 and A1-C2) and two opposition relations (A1-B3 and A1-C3).

If no derived relations are specified, the function will comoute all possible derived relations from baseline network and plot them.

Given the one-to-many structure, let's choose a degree-based layout and create a separate plot for the baseline (only 'baseline' in relations to display) and derived relations ('mutual' and 'combi' in relations to display).
""")

with st.expander("Graph layouts"):

    st.markdown("""
### Graph layouts

The graph visualizer supports several ways of positioning stimuli in the relational network, under 'stimulus layout'.  
Changing the layout only changes the **visual arrangement of the stimuli**; it does not change the underlying baseline or derived relations.

#### Auto
Automatically selects a suitable layout based on the structure of the relational network.

This is generally a good default when you do not have a specific visualization in mind.

#### Degree
Positions stimuli according to their **degree**, that is, the number of relations in which each stimulus participates.

Stimuli with many connections tend to occupy more central positions, whereas stimuli with fewer connections are placed more peripherally.

This layout can be useful for:
- identifying highly connected or central stimuli
- visualizing one-to-many or many-to-one structures
- comparing the connectivity of different nodes

#### Circular
Places all stimuli evenly around a circle.

This gives every stimulus an equal visual position and is useful when:
- the relational network has no obvious hierarchy
- comparing several equivalence classes
- you want to avoid implying that one stimulus is more central than another

For highly connected networks, however, relations may cross through the centre of the graph.

#### Spring
Uses a force-directed layout.

Stimuli are treated as if connected by springs:
- related stimuli attract each other
- stimuli are simultaneously pushed apart

The resulting layout tends to place strongly interconnected stimuli close together.

This can be useful for:
- larger relational networks
- identifying clusters or equivalence classes
- exploring the overall structure of a network

The exact positions may vary somewhat between networks.

#### Spectral
Positions stimuli using the mathematical structure of the graph's connectivity matrix.

It can reveal clusters and structural divisions within larger networks, although the resulting arrangement is sometimes less intuitive than circular or spring layouts.

This layout is mainly useful for exploratory visualization of more complex networks.

#### Shell
Arranges stimuli in concentric circles or *shells*.

This can be useful when the network contains:
- central and peripheral stimuli
- multiple levels of relational structure
- groups that can naturally be represented at different distances from the centre

#### Grid
Places stimuli at regularly spaced positions on a grid.

Unlike force-directed layouts, the positions do not depend strongly on the relational structure.

This is useful when:
- a predictable and orderly layout is preferred
- comparing several graphs using similar stimulus sets
- visual clarity is more important than representing network topology spatially

#### Polygon
Places stimuli at evenly spaced positions around a regular polygon.

For example:
- 3 stimuli → triangle
- 4 stimuli → square
- 5 stimuli → pentagon

This is especially useful for small relational networks because the arrangement is symmetrical and easy to interpret.

---

### Baseline versus derived relations in the layout

The **Include derived relations in layout** option determines whether derived relations influence the positioning of the stimuli.

- **Off:** stimulus positions are determined only from the baseline/trained network.
- **On:** both baseline and derived relations influence the layout.

Keeping this option off is often useful when comparing trained and derived relational networks, because the stimulus positions remain based on the original training structure.

---

### Which layout should I use?

There is no single best layout. Different layouts emphasize different properties of the same relational network.

A useful starting point is:

- **Auto** — general use
- **Degree** — highlight highly connected stimuli
- **Circular / Polygon** — small or symmetrical networks
- **Spring** — larger or more complex networks
- **Shell** — hierarchical or centre–periphery structures
- **Grid** — consistent layouts across graphs
- **Spectral** — exploratory analysis of network structure

Because layout only affects stimulus positions, it can be useful to inspect the same network using several layouts.
""")

###########
# GENERATE

if st.button("Generate network graph"):
    try:
        fig = plt.figure(figsize=(12,12))

        plotRelNetworkGraph(
            baseline=baseline,
            sLabs=sLabs,
            plotRels=plotRels,
            plotTitle=plotTitle,
            layout = layout,
            includeDerivedInLayout = False,
            relation_colors = relation_colors,
            labels = labels,
            radius = radius,
            label_offset= label_offset,
            fontSize = fontSize,
            sDotSize = sDotSize,
            legend = legend
        )

        st.pyplot(plt.gcf())

        # DOWNLOAD BUTTON
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)

        st.download_button(
            "Download PNG",
            data=buf,
            file_name="relational_network.png",
            mime="image/png"
        )

        st.success("Graph generated successfully.")

    except Exception as e:
        st.error(f"Error: {e}")

