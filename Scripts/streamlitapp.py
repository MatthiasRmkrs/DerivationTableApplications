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


# -------------------------
# UI
# -------------------------
st.sidebar.header("Task settings")

relations = st.sidebar.multiselect(
    "Relations",
    ['Same as', 
     'Different from',
     'Opposite to',
    'More than', 'Less than',
    'Larger than', 'Smaller than', 
    'Faster than',  'Slower than', 
    'Stronger than','Weaker than',
    'Better than', 'Worse than', 
    'Longer than', 'Shorter than',
    'Before', 'After', 
    'Contains','Is part of', 
    'Left of','Right of',
    'In front', 'Behind',
    'Heavier than','Lighter than',
    'Older than','Younger than',
    'Wider than','Narrower than',
    'Louder than','Quieter than',
    'Farther than','Closer than',
    'Higher than','Lower than',
    'Earlier than','Later than',
    'North of','South of',
    'Taller than', 'Not as tall as'
    ],
    default=["Same as", "Different from"],
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
            key=f"variants_{p}",
            help = """ See explainer for examples.
        - **Incorrect**: conclusion is false  
        - **Irrelevant**: adds unrelated premise  
        - **Analogy**: compares relations (only for 2 premises)  
        - **mutualCE**: tests reversed combinatorial entailment  
        """
        )
        
        if selected:  # only include if something selected
            premises_types[str(p)] = selected
            

n_rep = st.sidebar.number_input("Repetitions", 1, 50, 1,
                                help = """
                                Set how many repetitions to create for each 
                                unique problem (relations, premises and type).
                                Each repetition will include novel stimuli.
                                """)

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
    help = """'Linear' presents premises as 'A related to B; B related to C, ...'.
            'OTM' presents premises as 'A related to B, A related to C, ...'.
            'MTO' presents premises as 'A related to B, C related to B, ...'.
            'revLinear' presentspremises as 'A related to B, C related to A'.
            Note that OTM and MTO are only relevant for 2-premise problems."""
            
)

n_opt = st.sidebar.selectbox(
    "Number of Response Options",
    [1, 2, 3, 4],
    index=2,
    help = """Number of response options. If set to 1, problem premises are 
        followed by one conclusion (forced choice). If set to more than 1, 
        multiple choice problems will be created."""
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
if relata in ["names", "nonwords", "alphanumerics"]:
    syllogism_sLabs = None

if st.button("Generate task"):
    try:
        df = generateSyllogism(
            relations=relations,
            premises_types=premises_types,
            n_rep=n_rep,
            relata=relata,
            protocol=protocol,
            n_opt=n_opt,
            randomizePremises=randomize,
        )
    
    except Exception as e:
        st.exception(e)
        st.stop()
        
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
    
    with st.expander("How to use this app?"):
        st.markdown("""
                    
        This app allows you to generate syllogistic reasoning tasks with content and
        parameters of your choice.
        
        First, select the relations you want to make up the premises from the drop-down menu.
        The function underneath the app ensures that only compatible relations 
        (e.g., stronger than and weaker than, but not longer than) are combined in a given problem.
        
        Then, specify the number of premises you want problems to made up of. 
        You can vary the number of premises from 1 to 5 by checking the boxes.
        
        Next, for each level of complexity, you will have to specify which problem 
        variants (see explainer below) you want to include, by selecting them from 
        the drop-down menu. If none are selected, only 'regular' problems are included.
        
        Finally, you can manipulate a number of procedural aspects:
            - The number of repetitions of each unique problem type (each repetition using new stimuli)
            - The type of stimuli to use in the problems (names, nonwords, alphanumerics)
            - The number of response options. Set to 1 for forced choice problems,
                or >1 for multiple-choice problems.
            - Include ill-defined problems (problems for which no relation can reliably be derived)
            - Randomise premise order (default is linear: A related to B, B related to C, ...)
        
        

    """)
    with st.expander("What are the problem variants."):
        st.markdown("""
                    
                A regular problem presents a number of premises and a conclusion 
                that can be derived from those premises, e.g.:
                    
                    Jack is stronger than Jane, Jane is stronger than Ellie.
                    Is stronger than Ellie?
                
                
                'Incorrect' problems present a conclusion that cannot be derived 
                from the premises, allowing you to balance the number of yes/no responses.
                For example:
                    
                    Jack is stronger than Jane, Jane is stronger than Ellie. 
                    Is Ellie stronger than Jack?
                    
                'Irrelevant' problems add an extra premise to the problem, which is not 
                required to make the derivation allowing one to judge the conclusion.
                For example:
                    
                    Jack is stronger than Jane, Jane is stronger than Ellie. 
                    Ellie is weaker than Mark.
                    Is Jack stronger than Ellie?
                    
                    Note that if both 'incorrect' and 'irrelevant' problems are included, 
                    a problem variant with both an irrlevant premise and an incorrect 
                    conclusion will also be created.
                
                'mutual CE' will also include problem variants that assess the reversal 
                of the transitively derived relation.
                For example:
                    Given premises "Jack is stronger than Jane. Jane is stronger than Ellie."
                    A 'regular' conclusion would be 'Is Jack stronger than Ellie?'
                    And the 'mutual CE' conclusion would be 'Is Ellie weaker than Jack?'
                    
                'Analogy' problems present two premises and then prompt a comparison 
                of the two relations in the premises. For example,
                
                Jack is stronger than Jane, Jane is stronger than Ellie. 
                Is Jack related to Jane in the same way that Jane is related to Ellie?
                
    """)
    
    with st.expander("How to use this output"):
        st.markdown("""
    The downloaded CSV contains:
    - **Premises**: list of premises per trial  
    - **Prompt**: full text shown to participant (including conclusion and response options)
    - **Correct**: correct response  
    - **Type**: trial type (e.g., Incorrect, Irrelevant, ...)
    - 
    
    You can import this into:
    - PsychoPy
    - jsPsych
    - Empirica
    - custom experiments
    """)