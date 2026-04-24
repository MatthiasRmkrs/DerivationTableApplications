# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:25:16 2026

@author: mraemaek
"""

import streamlit as st
import pandas as pd

# import your function
from derTables.generateRelationalSyllogisms import generateSyllogism

st.title("Relational Syllogism Task Generator")

st.markdown("""
Create custom syllogistic reasoning tasks based on relational frame theory.

**Workflow:**
1. Choose relations and task structure in the sidebar
2. Click *Generate task*
3. Preview and download your trials as CSV
""")


# -------------------------
# UI
# -------------------------
st.sidebar.header("Task settings")

relations = st.sidebar.multiselect(
    "Relations",
    ["same", "different", "opposite", "more than", "less than"],
    default=["same", "different"],
    help="Choose which relational cues will be used in syllogism \
        premises (e.g., 'A is more than B'). Note that for problems with \
        multiple premises, only compatible relations will be combined in one problem."
)

st.sidebar.header("Premise structure")

variant_options = ["Incorrect", "Irrelevant", "Analogy", "mutualCE"]

premises_types = {}

for p in range(1, 6):
    use_level = st.sidebar.checkbox(f"Include {p}-premise problems", value=(p <= 2))
    
    if use_level:
        selected = st.sidebar.multiselect(
            f"Variants for {p} premises",
            variant_options,
            default=["Incorrect", "Irrelevant"],
            key=f"variants_{p}"
        )
        
        if selected:  # only include if something selected
            premises_types[str(p)] = selected
            
with st.expander("What are problem variants?"):
    st.markdown("""
- **Incorrect**: conclusion is false  
- **Irrelevant**: adds unrelated premise  
- **Analogy**: compares relations (only for 2 premises)  
- **mutualCE**: tests reversed combinatorial entailment  
""")

n_rep = st.sidebar.number_input("Repetitions", 1, 50, 1)

relata = st.sidebar.selectbox(
    "Stimulus type",
    ["nonwords", "names", "alphanumerics"],
    help = "Choose which type of stimuli to use as relata. \
        \n'Non-words' are randomly generated three-letter non-words, \
        similar to those used in the Relational Abilities Index (e.g., 'CUG is the same as BOP').\
        \n'Names' are randomly selected names of people like those used \
        in traditional n-term relational reasoning tasks (e.g. 'Tim is taller than Becca').\
        \n'Alphanumerics' are combinations of letters and numbers."
)

protocol = st.sidebar.selectbox(
    "Protocol",
    ["Linear", "OTM", "MTO", "revLinear"],
    help = ""
)

n_opt = st.sidebar.selectbox(
    "Number of Response Options",
    [1, 2, 3, 4],
    index=2,
    help = "Number of response options. If set to 1, problem premises are \
        followed by one conclusion, and function generates a unique problem \
        for each type you specified in input."
)

include_ill = st.sidebar.checkbox("Include ill-defined problems",
                                  help = "If checked, function also includes problems \
                                      for which the prompted conclusion cannot be derived \
                                          with certainty (e.g., 'CUG is different from WUG. \
                                        WUG is different from POM. Is POM different from CUG?'")
randomize = st.sidebar.checkbox("Randomize premise order",
                                help = "If not checked, premises are ordered by default \
                                    (mostly relevant for linear protocol, e.g., A is the \
                                     same as B, B is the same as C, C is different from D.).\
                                        If checked, premise order is randomized.")


# -------------------------
# Generate
# -------------------------
if st.button("Generate task"):
    df = generateSyllogism(
        relations=relations,
        premises_types=premises_types,
        n_rep=n_rep,
        relata=relata,
        protocol=protocol,
        n_opt=n_opt,
        includeIllDefined=include_ill,
        randomizePremises=randomize,
    )

    st.success(f"Generated {len(df)} trials")
    
    st.subheader("Task summary")

    st.write(f"Total trials: {len(df)}")
    
    st.write("Trial types:")
    st.write(df["Type"].value_counts())
    
    st.write("Premise levels:")
    st.write(df["n_p"].value_counts())
    
    if len(df) > 1000:
        st.warning("⚠️ Large task generated. This may be difficult to run experimentally.")
    
    if len(df) > 0:
        st.subheader("Example trial")
    
        example = df.iloc[0]
    
        st.markdown(f"""
                **Premises:**  
                {" ".join(example["Premises"])}
                
                **Prompt:**  
                {example["Prompt"]}
                
                **Correct answer:**  
                {example["printCorrect"]}
                """)

    st.dataframe(df.head(20))

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name="syllogism_task.csv",
        mime="text/csv"
    )
    with st.expander("How to use this output"):
        st.markdown("""
    The downloaded CSV contains:
    - **Premises**: list of premises per trial  
    - **Prompt**: full text shown to participant  
    - **Correct**: correct response  
    - **Type**: trial type (e.g., Incorrect, Irrelevant)  
    
    You can import this into:
    - PsychoPy
    - jsPsych
    - Empirica
    - custom experiments
    """)