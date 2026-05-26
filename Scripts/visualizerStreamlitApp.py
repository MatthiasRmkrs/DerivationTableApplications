# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:27:23 2026

Streamlit app for relational network visualizer

@author: mraemaek
"""

import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

# IMPORT FUNCTION
from derTables.plot_utils import plotRelNetworkGraph
# from derTables.createDerivationTables import createDerivationTables

st.set_page_config(layout="wide")

st.title("Relational Network Graph Visualizer")

st.markdown("""
Visualize a relational network as a graph network.

Users can specify:
- baseline relations
- optional derived relations (mutually entailed and combinatorially entailed relations, can also be automatically derived)


Workflow:
- Select the number of stimuli in the network and give them desired labels
- Select the relations to include in the network
- Specify baseline relations (two stimuli connected by a relation you selected)


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
    help = "Specifiy the title for the plot, if any."
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
            based on network density (more connected stimuli centered).'degree' ..."
)
    
relColor = st.sidebar.text_input("Baseline Relation Color",
                                 value = 'black',
                                 help = "Color of baseline relation arrows.")
mrelColor = st.sidebar.color_picker("Mutually Entailed Relation Color", 
                                  value = '#0072B2',
                                  help = "Color of arrows for mutually entailed relations.")
crelColor = st.sidebar.text_input("Combinatorially Entailed Relation Color",
                                  value = '#CC79A7',
                                  help = "Color of arrows for combinatorially entailed relations.")


radius = st.Sidebar.slider('Arrow Radius',
                           min_value = 0, max_value = .5, step = .01, value = .18,
                           help = "Determines curvature of lines between stimuli.")
    # #       "simple, head_length=50, head_width=15, tail_width=5" # Simple arrow growing thinner
    # relArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
    # drelArrowStyle = "fancy, head_length=100, head_width=25, tail_width=7" # Pointed arrow growing thinner
    # label_offset = .55 # Play around with how close labels are plotted to lines
    # relLabelFontSize = 50
    # sLabelFontSize = 60
    # sDotSize = 100

###########
# GENERATE

if st.button("Generate network graph"):
    try:
        fig = plt.figure(figsize=(12,12))

        plotRelNetworkGraph(
            baseline=baseline,
            sLabs=sLabs,
            plotRels=plotRels,
            plotTitle=plotTitle
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

# INFORMATION

with st.expander("What do the relation types mean?"):

    st.markdown("""
- **baseline** → directly trained relations  
- **mutual** → mutually entailed relations  
- **combi** → combinatorially entailed relations  
""")

with st.expander("Example"):

    st.markdown("""
Example baseline:

- A more than B
- B more than C

Derived:
- A more than C (combinatorial)
- B less than A (mutual)
""")