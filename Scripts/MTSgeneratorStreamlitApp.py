# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:40:28 2026

@author: mraemaek
"""

import streamlit as st
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from io import BytesIO

from derTables.GenerateMTS_wip import generateTrials
from derTables.plot_utils import plotRelNetworkGraph
from derTables.utils_mts import *

st.set_page_config(
    page_title="MTS Trial Generator",
    layout="wide"
)

# INFO

st.title("MTS Trial Generator")

st.markdown("""
Generate matching-to-sample (MTS) training and testing trials
for user-specified relational networks.

This app allows you to:
- define baseline relations
- optionally define derived relations
- generate baseline and derived test trials
- preview/export generated tasks
""")

# SIDEBAR — GENERAL SETTINGS

st.sidebar.header("Network Specification")

use_preset = st.sidebar.checkbox(
    "Relational Network Preset",
    value=False,
    help=(
        "Check this box if you want to use a preset relational network to create the MTS procedure for. "
        "If not checked, you will have to manually specify the network. "
        "Currently supported presets are the Steele and Hayes (1991) procedure and a typical transitive inference task (but more will be added)."
    )
)

if use_preset:
    preset_category = st.sidebar.selectbox(
        "Preset category",
        [
            "Stimulus Equivalence",
            "RFT",
            "Other"
        ]
    )
    
    if preset_category == 'Stimulus Equivalence':
        preset = st.sidebar.selectbox(
        "Preset",
        [
            "Custom Equivalence",
            "Equivalence Linear vs OTM 5-member",
            "Equivalence Linear vs MTO 5-member",
            "Equivalence OTM vs MTO 5-member"],
                help="Select Equivalence protocol or Custom Equivalence to define # classes, # members and training structure."
            )
    elif preset_category == 'RFT':
        
        preset = st.sidebar.selectbox(
        "Preset",
        [
            "Steele&Hayes91",
            "RFT Comparison More-Less",
            "RFT Temporal Before-After",
            "RFT Hierarchical Contains-PartOf",
            "RFT Same-Opposite",
            "RFT Same-Different"],
            help="Select MTS protocol. Steele&Hayes91 replicates seminal procedure by Steele and Hayes (1991). "
        )
            
    else: 
        preset = st.sidebar.selectbox(
        "Preset",
        [
            "TransitiveInference",
            "Identity Matching",
            "Arbitrary Conditional Discrimination"
        ],
            help="Select predefined MTS protocol. Transitive inference allows for specifying number of nodes. Identity matching is simple identity matching task. Arbitrary Conditional discriminations trains arbitrary relations."
        )
    

    
    # Default: fixed presets are handled by generateTrials()
    generator_preset = preset
    baseline = None
    derived = None
    sLabs = None


    # =====================================================
    # CUSTOM EQUIVALENCE
    # =====================================================

    if preset == "Custom Equivalence":

        st.sidebar.subheader("Equivalence settings")

        n_classes = st.sidebar.number_input(
            "Number of classes",
            min_value=1,
            max_value=10,
            value=2,
            step=1
        )

        n_members = st.sidebar.number_input(
            "Members per class",
            min_value=2,
            max_value=10,
            value=4,
            step=1
        )

        equivalence_protocol = st.sidebar.selectbox(
            "Training protocol",
            ["Linear", "OTM", "MTO"],
            format_func=lambda x: {
                "Linear": "Linear series",
                "OTM": "One-to-many (OTM)",
                "MTO": "Many-to-one (MTO)"
            }[x]
        )

        baseline, sLabs = create_equivalence_network(
            n_classes=n_classes,
            n_members=n_members,
            protocol=equivalence_protocol
        )

        derived = None

        # Send dynamically generated network through Manual branch
        generator_preset = "Manual"


    # =====================================================
    # STEELE & HAYES
    # =====================================================

    elif preset == "Steele&Hayes91":

        sLabs = [
            "A",
            "B1", "B2", "B3",
            "C1", "C2", "C3",
            "N1", "N2"
        ]

        baseline = None

        derived = st.sidebar.selectbox(
            "Derived relations",
            ["All", "Relnet"],
            help=(
                "Select which derived relations to test. "
                "'All' creates trials for all possible derivations. "
                "'Relnet' only creates trials for the selected "
                "Steele & Hayes relational network."
            )
        )


    # =====================================================
    # TRANSITIVE INFERENCE
    # =====================================================

    elif preset == "TransitiveInference":

        n_stim = st.sidebar.slider(
            "Number of stimuli",
            min_value=3,
            max_value=15,
            value=5,
            help="Number of stimuli in the transitive inference chain."
        )

        sLabs = [
            chr(65 + i)
            for i in range(n_stim)
        ]

        baseline = None
        derived = None


    # =====================================================
    # ALL OTHER FIXED PRESETS
    # =====================================================

    else:

        # Their baseline, derived relations and labels
        # are created inside generateTrials().
        baseline = None
        derived = None
        sLabs = None


else:

    preset = "Manual"
    generator_preset = "Manual"
    
    
if preset == "Manual":
    
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
        
st.sidebar.markdown("---")
st.sidebar.subheader("Network Visualization")

visualize = st.sidebar.checkbox(
    "Visualize Relational Network",
    value=False,
    help=(
        "Check this box if you want to visualize the relational network as a graph network. "
        "If checked, the baseline (trained) relations and derived (tested) relations for which you are generating the MTS procedure will be plotted as two graphs. "
    )
)

st.sidebar.markdown("---")
st.sidebar.subheader("Procedure Settings")

n_baseline = st.sidebar.number_input(
    "Baseline Trial Repetitions",
    min_value=1,
    max_value=100,
    value=10,
    help="Number times each baseline trial is repeated."
)

n_test = st.sidebar.number_input(
    "Test Trial Repetitions",
    min_value=1,
    max_value=100,
    value=1,
    help="Number of repetitions for each derived relational responding/test trial."
)

n_comp = st.sidebar.selectbox(
    "Number of comparison stimuli",
    [2, 3],
    index=1,
    help="Number of comparison options shown on each trial."
)


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
            preset=generator_preset,
            n_test=n_test,
            n_comp=n_comp,
            derived=derived,
            printTrials=False,
            sLabs=sLabs
        )
        if trial_data["extra_stimuli"]:

            st.warning(
                "Insufficient unrelated stimuli were available to create all "
                f"{n_comp}-comparison trials. The following neutral comparison "
                "stimuli were added automatically: "
                + ", ".join(trial_data["extra_stimuli"])
            )
        # Use the final stimulus list returned by generateTrials
        sLabs = trial_data["sLabs"]
        baseline = trial_data['baseline']
        derived = trial_data['derived']
        
        # =================================================
        # VISUALIZATION
        #=================================================
        if visualize:
                try:
                    fig = plt.figure(figsize=(12,12))

                    plotRelNetworkGraph(
                        baseline=baseline,
                        sLabs=sLabs,
                        plotRels=['baseline'],
                        plotTitle='Trained Relations',
                        layout = 'auto',
                        includeDerivedInLayout = False,
                        relation_colors = None,
                        labels = False,
                        radius = .3,
                        label_offset= .2,
                        fontSize = 60,
                        sDotSize = 100,
                        legend = ['Relation type']
                    )

                    st.pyplot(plt.gcf())

                    # DOWNLOAD BUTTON
                    buf = BytesIO()
                    plt.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)

                    st.download_button(
                        "Download PNG",
                        data=buf,
                        file_name="trained_network.png",
                        mime="image/png"
                    )

                    st.success("Graph generated successfully.")

                    plotRelNetworkGraph(
                        baseline=baseline,
                        derived = derived,
                        sLabs=sLabs,
                        plotRels=['mutual', 'combi'],
                        plotTitle='Tested Derived Relations',
                        layout = 'auto',
                        includeDerivedInLayout = False,
                        relation_colors = None,
                        labels = False,
                        radius = .3,
                        label_offset= .2,
                        fontSize = 60,
                        sDotSize = 100,
                        legend = ['Relation colors']
                    )

                    st.pyplot(plt.gcf())

                    # DOWNLOAD BUTTON
                    buf = BytesIO()
                    plt.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)

                    st.download_button(
                        "Download PNG",
                        data=buf,
                        file_name="test_network.png",
                        mime="image/png"
                    )

                    st.success("Graph generated successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")

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
