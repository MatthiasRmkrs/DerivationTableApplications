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

def findComparisonOptions(sLabs, relTab, rel, relLab, relations, source):
    options = [] # init 

    for i in range(len(sLabs)):
        if i < len(relTab[rel, source[0], :]):
            if not relTab[rel, source[0], i] and not relTab[rel, i, source[0]]:
                if i != source[0]: 
                    if relLab == 'Different from' and 'Opposite to' in relations.keys():
                        if not relTab[relations['Opposite to'], source[0], i] and not relTab[relations['Opposite to'], i, source[0]]:
                            options = [*options, i]
                    else:
                        options = [*options, i]

        else: # stimuli not included in relations
            options = [*options, i]
    
    
    
    return options

# %% add comparison stimuli for trial


from itertools import combinations
import warnings


def add_comparison_sets(
    unique_cmps,
    scc,
    source,
    options,
    n_comp,
    sLabs
):
    """
    Generate all valid comparison sets for an MTS trial.

    If there are insufficient unrelated stimuli to serve as distractors,
    additional neutral stimuli (XTR1, XTR2, ...) are created automatically.

    Extra stimuli are appended to sLabs and can occur as comparison stimuli,
    but are not part of the relational network.

    Returns
    -------
    added_stimuli : list
        Labels of any extra stimuli that were created.
    """

    n_distractors = n_comp - 1

    # Remove sample and correct comparison from distractor pool
    valid_options = [
        option for option in options
        if option not in source
    ]

    added_stimuli = []

    # -------------------------------------------------------
    # Add extra neutral stimuli if necessary
    # -------------------------------------------------------

    n_missing = n_distractors - len(valid_options)

    if n_missing > 0:

        for _ in range(n_missing):

            # Find the first unused XTR label
            xtr_number = 1

            while f"XTR{xtr_number}" in sLabs:
                xtr_number += 1

            xtr_label = f"XTR{xtr_number}"

            # Add label to stimulus list
            sLabs.append(xtr_label)

            # Its index is its new position in sLabs
            xtr_index = len(sLabs) - 1

            # Make it available as an incorrect comparison
            valid_options.append(xtr_index)

            added_stimuli.append(xtr_label)

        warnings.warn(
            f"Not enough unrelated comparison stimuli were available for "
            f"n_comp={n_comp}. Added {n_missing} extra neutral stimulus/stimuli: "
            f"{', '.join(added_stimuli)}."
        )

    # -------------------------------------------------------
    # Generate comparison sets
    # -------------------------------------------------------

    for distractors in combinations(
        valid_options,
        n_distractors
    ):

        comparison_set = [
            source[1],       # correct comparison
            *distractors     # incorrect comparisons
        ]

        unique_cmps[scc].append(comparison_set)

    return added_stimuli
        
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
    
# %% helper to generate preset equivalence protocol

def create_equivalence_network(
    n_classes,
    n_members,
    protocol
):
    """
    Create an equivalence-training network.

    Parameters
    ----------
    n_classes : int
        Number of equivalence classes.

    n_members : int
        Number of members per class.

    protocol : str
        Training structure:
        'Linear', 'OTM', or 'MTO'.

    Returns
    -------
    baseline : dict
        Baseline Same-as relations.

    sLabs : list
        Stimulus labels.
    """

    baseline = {
        "Same as": []
    }

    sLabs = []

    # -----------------------------------------------------
    # Create labels
    # -----------------------------------------------------

    # Member labels: A, B, C, D, ...
    member_labels = [
        chr(65 + i)
        for i in range(n_members)
    ]

    # Store indices per class
    classes = []

    for class_id in range(1, n_classes + 1):

        class_indices = []

        for member in member_labels:

            label = f"{member}{class_id}"

            sLabs.append(label)

            class_indices.append(
                len(sLabs) - 1
            )

        classes.append(class_indices)

    # -----------------------------------------------------
    # Create baseline structure
    # -----------------------------------------------------

    for class_indices in classes:

        if protocol == "Linear":

            # A -> B -> C -> D ...
            for i in range(len(class_indices) - 1):

                baseline["Same as"].append(
                    (
                        class_indices[i],
                        class_indices[i + 1]
                    )
                )

        elif protocol == "OTM":

            # A -> B
            # A -> C
            # A -> D
            anchor = class_indices[0]

            for target in class_indices[1:]:

                baseline["Same as"].append(
                    (anchor, target)
                )

        elif protocol == "MTO":

            # B -> A
            # C -> A
            # D -> A
            anchor = class_indices[0]

            for source in class_indices[1:]:

                baseline["Same as"].append(
                    (source, anchor)
                )

        else:

            raise ValueError(
                "protocol must be "
                "'Linear', 'OTM', or 'MTO'."
            )

    return baseline, sLabs