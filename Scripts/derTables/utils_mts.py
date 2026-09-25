# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:15:57 2026

Helper functions for MTS Generator

- find comparison stimulus options
- select specified number of comparison stimuli



@author: mraemaek
"""

# dependencies
import numpy as np
from itertools import combinations

# %% Find comparison stimulus options (not related to sample)

def findComparisonOptions(sLabs, relTab, rel, source):
    options = [] # init 

    for i in range(len(sLabs)):
        if i < len(relTab[rel, source[0], :]):
            if not relTab[rel, source[0], i] and not relTab[rel, i, source[0]]:
                if i != source[0]: options = [*options, i]
                
                # !!! ADD Clause for no opposite/comparative comparisons if difference relation

        else: # stimuli not included in relations
            options = [*options, i]
    
    # # Find comparison stimuli (other than correct): given sample and cue, find unrelated S
    # rels = relTab[rel, source[0], :] != 1 # Find non-rels in table

    
    # for o in range(len(rels)): # Loop stimuli
    #     if rels[o]: 
    #         if not o == source[0]: # Select and add to option list if valid
    #             options = [*options, o] # Store possible comparison index
    
    return options

# %% add comparison stimuli for trial


def add_comparison_sets(unique_cmps, scc, source, options, n_comp):
    """
    Generate all valid comparison sets for an MTS trial.

    Parameters
    ----------
    unique_cmps : dict
        Dictionary in which comparison sets are stored.
    scc : tuple
        Key identifying the sample-cue-correct comparison combination.
    source : tuple
        Relation pair (sample, correct comparison).
    options : list
        Candidate incorrect comparison stimuli.
    n_comp : int
        Total number of comparison stimuli on the trial,
        including the correct comparison.
    """

    # Remove sample and correct comparison from distractor pool
    valid_options = [
        option for option in options
        if option not in source
    ]

    if len(valid_options) < n_comp - 1:
        raise ValueError(
            f"Not enough valid comparison stimuli for n_comp={n_comp}. "
            f"Need {n_comp - 1} distractors, but only "
            f"{len(valid_options)} are available."
        )

    for distractors in combinations(valid_options, n_comp - 1):

        comparison_set = [
            source[1],      # correct comparison
            *distractors    # incorrect comparisons
        ]

        unique_cmps[scc].append(comparison_set)
        
# %% join comparison stimulus labels for printing

def format_comparisons(comparisons, sLabs):
    """
    Convert comparison stimulus indices into a readable string.

    Examples:
        [1, 2]       -> "B or C"
        [1, 2, 3]    -> "B, C or D"
        [1, 2, 3, 4] -> "B, C, D or E"
    """

    labels = [sLabs[c] for c in comparisons]

    if len(labels) == 1:
        return labels[0]

    if len(labels) == 2:
        return f"{labels[0]} or {labels[1]}"

    return ", ".join(labels[:-1]) + f" or {labels[-1]}"

# %% print MTS trial for debugging

def print_mts_trial(trial_data, idx, trial_number, trial_name, sLabs, relations):

    comparisons = format_comparisons(
        trial_data["comparisons"][idx],
        sLabs
    )

    print(
        f"\n{trial_name} Trial {trial_number} "
        f"(#{trial_data['tID'][idx]}, {trial_data['type'][idx]}): "
        f"Sample stimulus {sLabs[trial_data['sample'][idx]]} is "
        f"{list(relations.keys())[trial_data['cue'][idx]]} "
        f"{comparisons}? "
        f"\n\nCorrect answer is "
        f"{sLabs[trial_data['correct'][idx]]}!"
    )