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

Users can optionally choose to specify the derived relations as well, instead of
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
    "Is part of"
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
        "Check this box to manually specify derived relations (similar to baseline above)."
        "If not checked, derived relations will be computed automatically "
        "from the baseline relations."
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
                f"Number of derived stimulus pairs for '{relation}'",
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
- Specify the number of stimuli in the network, their labels and the types of relations in the network
- Specify the number of instances of each relation and specify which stimuli are related (optionally also define derived relations in same way)
- Specify the layout you want for the network (circular, degree-based, hierarchical, ...), which relations to plot and other plot settings.
- Press the 'Generate Network Graph' to create the plot and download it. 
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

