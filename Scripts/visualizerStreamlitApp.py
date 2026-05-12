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
from derTables.plotRelNetworkGraph import plotRelNetworkGraph

st.set_page_config(layout="wide")

st.title("Relational Network Graph Visualizer")

st.markdown("""
Visualize trained and derived relational networks.

This app plots:
- baseline relations
- mutually entailed relations
- combinatorially entailed relations

using graph-network visualizations.
""")


# SIDEBAR

st.sidebar.header("Network specification")

n_stim = st.sidebar.slider(
    "Number of stimuli",
    min_value=2,
    max_value=10,
    value=3
)

default_labels = [chr(65+i) for i in range(n_stim)]

label_string = st.sidebar.text_input(
    "Stimulus labels (comma-separated)",
    value=",".join(default_labels)
)

sLabs = [x.strip() for x in label_string.split(",")]

relation_options = [
    "Same as",
    "Different from",
    "More than",
    "Less than",
    "Before",
    "After",
    "Contains",
    "Is part of"
]

selected_relation = st.sidebar.selectbox(
    "Relation type",
    relation_options
)

st.sidebar.markdown("---")
st.sidebar.subheader("Baseline relations")

baseline_pairs = []

for i in range(n_stim - 1):

    c1, c2 = st.sidebar.columns(2)

    with c1:
        s1 = st.selectbox(
            f"Source {i+1}",
            sLabs,
            key=f"s1_{i}"
        )

    with c2:
        s2 = st.selectbox(
            f"Target {i+1}",
            sLabs,
            index=min(i+1, len(sLabs)-1),
            key=f"s2_{i}"
        )

    baseline_pairs.append((sLabs.index(s1), sLabs.index(s2)))

st.sidebar.markdown("---")

plotRels = st.sidebar.multiselect(
    "Relations to display",
    ["baseline", "mutual", "combi"],
    default=["baseline", "mutual", "combi"]
)

plotTitle = st.sidebar.text_input(
    "Plot title",
    value="Relational Network"
)

# BUILD BASELINE DICT

baseline = {
    selected_relation: baseline_pairs
}

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