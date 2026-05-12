# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:40:28 2026

@author: mraemaek
"""

import streamlit as st
import pandas as pd
import numpy as np
import ast

from derTables.generateTrials import generateTrials

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MTS Trial Generator",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("MTS Trial Generator")

st.markdown("""
Generate matching-to-sample (MTS) training and testing trials
from relational networks.

This app allows you to:
- define baseline relations
- optionally define derived relations
- generate baseline and derived test trials
- preview/export generated tasks
""")

# =========================================================
# SIDEBAR — GENERAL SETTINGS
# =========================================================

st.sidebar.header("General settings")

preset = st.sidebar.selectbox(
    "Preset",
    ["Manual", "SH91", "TransitiveInference"],
    help="Use predefined relational structures or specify your own manually."
)

n_baseline = st.sidebar.number_input(
    "Baseline repetitions",
    min_value=1,
    max_value=100,
    value=2,
    help="Number of repetitions for each baseline trial."
)

n_test = st.sidebar.number_input(
    "Test repetitions",
    min_value=1,
    max_value=100,
    value=2,
    help="Number of repetitions for each derived/test trial."
)

n_comp = st.sidebar.selectbox(
    "Number of comparison stimuli",
    [2, 3],
    index=1,
    help="Number of comparison options shown on each trial."
)

# =========================================================
# STIMULUS SETTINGS
# =========================================================

st.sidebar.header("Stimulus settings")

n_stim = st.sidebar.slider(
    "Number of stimuli",
    min_value=2,
    max_value=20,
    value=5
)

default_labels = [chr(65+i) for i in range(n_stim)]

label_string = st.sidebar.text_input(
    "Stimulus labels (comma-separated)",
    value=",".join(default_labels)
)

sLabs = [x.strip() for x in label_string.split(",")]

# =========================================================
# BASELINE RELATIONS
# =========================================================

st.sidebar.header("Baseline relations")

relation_options = [
    "Same as",
    "Different from",
    "Opposite to",
    "More Than",
    "Less Than"
]

n_relations = st.sidebar.number_input(
    "Number of relation types",
    min_value=1,
    max_value=10,
    value=1
)

baseline = {}

for r in range(n_relations):

    st.sidebar.markdown(f"### Relation set {r+1}")

    rel_type = st.sidebar.selectbox(
        f"Relation type {r+1}",
        relation_options,
        key=f"reltype_{r}"
    )

    n_pairs = st.sidebar.number_input(
        f"Number of pairs for {rel_type}",
        min_value=1,
        max_value=30,
        value=2,
        key=f"npairs_{r}"
    )

    rel_pairs = []

    for i in range(n_pairs):

        c1, c2 = st.sidebar.columns(2)

        with c1:

            s1 = st.selectbox(
                f"Source {r}_{i}",
                sLabs,
                key=f"s1_{r}_{i}"
            )

        with c2:

            s2 = st.selectbox(
                f"Target {r}_{i}",
                sLabs,
                index=min(i+1, len(sLabs)-1),
                key=f"s2_{r}_{i}"
            )

        rel_pairs.append(
            (sLabs.index(s1), sLabs.index(s2))
        )

    baseline[rel_type] = rel_pairs

# =========================================================
# OPTIONAL DERIVED DICTIONARY
# =========================================================

st.sidebar.header("Derived relations")

derived_mode = st.sidebar.selectbox(
    "Derived relation mode",
    ["Auto-compute", "Manual dictionary"]
)

derived = None

if derived_mode == "Manual dictionary":

    st.sidebar.markdown("""
Example:

{
    "Same as": [(1,0)],
    "Opposite to": [(2,3)]
}
""")

    derived_text = st.sidebar.text_area(
        "Derived dictionary",
        height=200
    )

    if derived_text.strip():

        try:

            derived = ast.literal_eval(derived_text)

        except Exception:

            st.sidebar.error("Could not parse dictionary.")

# =========================================================
# SHOW CURRENT CONFIGURATION
# =========================================================

with st.expander("Current baseline dictionary"):

    st.json(baseline)

if derived is not None:

    with st.expander("Current derived dictionary"):

        st.json(derived)

# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button("Generate trials"):

    try:

        # =================================================
        # GENERATE TRIALS
        # =================================================

        trial_data = generateTrials(
            baseline=baseline,
            n_baseline=n_baseline,
            preset=preset,
            n_test=n_test,
            n_comp=n_comp,
            derived=derived,
            printTrials=False,
            sLabs=sLabs
        )

        # =================================================
        # CREATE DATAFRAME
        # =================================================

        df = pd.DataFrame({
            "Trial ID": trial_data["tID"],
            "Type": trial_data["type"],
            "Relation": trial_data["relation"],
            "Sample": trial_data["sample"],
            "Cue": trial_data["cue"],
            "Comparisons": [
                list(x) for x in trial_data["comparisons"]
            ],
            "Correct": trial_data["correct"],
            "Label": trial_data["label"]
        })

        # =================================================
        # ADD HUMAN-READABLE LABELS
        # =================================================

        df["Sample Label"] = df["Sample"].apply(
            lambda x: sLabs[x]
        )

        df["Correct Label"] = df["Correct"].apply(
            lambda x: sLabs[x]
        )

        df["Comparison Labels"] = df["Comparisons"].apply(
            lambda comps: [sLabs[c] for c in comps]
        )

        # =================================================
        # SUMMARY
        # =================================================

        st.success(f"{len(df)} trials generated.")

        st.subheader("Trial summary")

        c1, c2 = st.columns(2)

        with c1:

            st.write("Trial types")

            st.dataframe(
                df["Type"].value_counts()
            )

        with c2:

            st.write("Relations")

            st.dataframe(
                df["Relation"].value_counts()
            )

        # =================================================
        # PREVIEW
        # =================================================

        st.subheader("Trial preview")

        st.dataframe(df)

        # =================================================
        # EXAMPLE TRIAL
        # =================================================

        st.subheader("Example trial")

        ex = df.iloc[0]

        st.markdown(f"""
### {ex['Type']}

- **Sample stimulus:** {ex['Sample Label']}
- **Relation cue:** {ex['Relation']}
- **Comparison stimuli:** {", ".join(ex['Comparison Labels'])}
- **Correct comparison:** {ex['Correct Label']}
""")

        # =================================================
        # DOWNLOAD
        # =================================================

        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            data=csv,
            file_name="mts_trials.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(f"Error: {e}")

# =========================================================
# DOCUMENTATION
# =========================================================

with st.expander("What are baseline and derived relations?"):

    st.markdown("""
### Baseline relations
Directly trained relations.

Example:

{
    "More Than": [(0,1), (1,2)]
}

### Derived relations
Relations inferred from the baseline network.

From the example above:

(0,2)

can be derived.
""")

with st.expander("Trial structure"):

    st.markdown("""
Each generated trial contains:
- sample stimulus
- relation cue
- comparison stimuli
- correct comparison
- trial type
""")

with st.expander("Presets"):

    st.markdown("""
### Manual
User-defined relational network.

### SH91
Steele & Hayes (1991)-style setup.

### TransitiveInference
Linear transitive inference network.
""")
