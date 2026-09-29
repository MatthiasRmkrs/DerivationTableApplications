# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:10:17 2026

@author: mraemaek
"""

# dependencies
import numpy as np
from itertools import product, combinations
import pdb

# %% relLabsForPremises - similar to above, convert rel Labs for premises in syllogistic problem

def relLabsForPremises(relations):
    """
    Convert relation labels to wording that can be used in premises.

    Args:
        relations: list of relation labels (str)

    Returns:
        list of premise-compatible relation labels
    """

    premiseVariants = {
        'Same as': 'the same as',
        'Different from': 'different from',
        'Opposite to': 'opposite to',
        'More than': 'more than',
        'Bigger than': 'bigger than',
        'Larger than': 'larger than',
        'Faster than': 'faster than',
        'Stronger than': 'stronger than',
        'Better than': 'better than',
        'Longer than': 'longer than',
        'Less than': 'less than',
        'Smaller than': 'smaller than',
        'Slower than': 'slower than',
        'Weaker than': 'weaker than',
        'Worse than': 'worse than',
        'Shorter than': 'shorter than',
        'Before': 'before',
        'After': 'after',
        'Contains': 'contains',
        'Is part of': 'part of',
        'Left of': 'to the left of',
        'Right of': 'to the right of',
        'In front': 'in front of',
        'Behind': 'behind',
        'Above': 'above',
        'Below': 'below',
        'Heavier than': 'heavier than',
        'Lighter than': 'lighter than',
        'Older than': 'older than',
        'Younger than': 'younger than',
        'Wider than': 'wider than',
        'Narrower than': 'narrower than',
        'Louder than': 'louder than',
        'Quieter than': 'quieter than',
        'Farther than': 'farther than',
        'Closer than': 'closer than',
        'Higher than': 'higher than',
        'Lower than': 'lower than',
        'Earlier than': 'earlier than',
        'Later than': 'later than',
        'North of': 'north of',
        'South of': 'south of',
        'Taller than': 'taller than',
        'Not as tall as': 'not as tall as',
    }

    useableRelations = []

    for rel in relations:
        if rel not in premiseVariants:
            raise ValueError(
                f"Relation '{rel}' is not defined in premiseVariants."
            )

        useableRelations.append(
            premiseVariants[rel]
        )

    return useableRelations

# %% find all unique combinations of a set of relations for a given number of premises

def findAllRelPremCombinations(relations, p):
    """
    For a given set of relations, find all ordered combinations of relations
    that can occur together in problems with 1..p premises.

    Only combinations containing mutually compatible relations are retained.

    Args:
        relations: dict
            Relation labels as keys and integer indices as values.
        p: int or str
            Maximum number of premises.

    Returns:
        p_rels: dict
            Number of premises as string keys and lists of compatible
            relation combinations as values.
    """

    compatible = {
        'Same as': [],  # treated as compatible with everything below

        'Different from': ['Same as', 'Different from', 'Opposite to'],
        'Opposite to': ['Same as', 'Different from', 'Opposite to'],

        'More than': ['Less than', 'More than'],
        'Less than': ['Less than', 'More than'],

        'Larger than': ['Larger than', 'Smaller than'],
        'Smaller than': ['Larger than', 'Smaller than'],

        'Faster than': ['Faster than', 'Slower than'],
        'Slower than': ['Faster than', 'Slower than'],

        'Stronger than': ['Stronger than', 'Weaker than'],
        'Weaker than': ['Stronger than', 'Weaker than'],

        'Better than': ['Better than', 'Worse than'],
        'Worse than': ['Better than', 'Worse than'],

        'Longer than': ['Longer than', 'Shorter than'],
        'Shorter than': ['Longer than', 'Shorter than'],

        'Contains': ['Contains', 'Is part of'],
        'Is part of': ['Contains', 'Is part of'],

        'Before': ['Before', 'After'],
        'After': ['Before', 'After'],

        'Left of': ['Left of', 'Right of'],
        'Right of': ['Left of', 'Right of'],

        'In front': ['In front', 'Behind'],
        'Behind': ['In front', 'Behind'],

        'Above': ['Above', 'Below'],
        'Below': ['Above', 'Below'],

        'Heavier than': ['Heavier than', 'Lighter than'],
        'Lighter than': ['Heavier than', 'Lighter than'],

        'Older than': ['Older than', 'Younger than'],
        'Younger than': ['Older than', 'Younger than'],

        'Wider than': ['Wider than', 'Narrower than'],
        'Narrower than': ['Wider than', 'Narrower than'],

        'Louder than': ['Louder than', 'Quieter than'],
        'Quieter than': ['Louder than', 'Quieter than'],

        'Farther than': ['Farther than', 'Closer than'],
        'Closer than': ['Farther than', 'Closer than'],

        'Higher than': ['Higher than', 'Lower than'],
        'Lower than': ['Higher than', 'Lower than'],

        'Earlier than': ['Earlier than', 'Later than'],
        'Later than': ['Earlier than', 'Later than'],

        'North of': ['North of', 'South of'],
        'South of': ['North of', 'South of'],

        'Taller than': ['Taller than', 'Not as tall as'],
        'Not as tall as': ['Taller than', 'Not as tall as']
    }

    rel_list = list(relations.keys())

    def are_compatible(rel1, rel2):
        """Return True if two relation labels can occur in the same problem."""

        # Coordination can combine with any relation
        if rel1 == 'Same as' or rel2 == 'Same as':
            return True

        # Require compatibility to be defined in both directions
        return (
            rel2 in compatible.get(rel1, [])
            and rel1 in compatible.get(rel2, [])
        )

    def valid_combination(rel_combination):
        """Check pairwise compatibility of all relations in a combination."""

        return all(
            are_compatible(rel1, rel2)
            for rel1, rel2 in combinations(rel_combination, 2)
        )

    p_rels = {}

    for n in range(1, int(p) + 1):

        all_combinations = product(rel_list, repeat=n)

        p_rels[str(n)] = [
            list(rel_combination)
            for rel_combination in all_combinations
            if valid_combination(rel_combination)
        ]

    return p_rels


# %% Find new (unique) stimulus labels for a given syllogistic problem in loop

def findUniqueStimuli(relations, sLabs, p, n_rep, rep, r, r2=None, r3 = None, r4=None, r5 = None):
    """
    Finds unique stimulus labels to put in new iteration of syllogistic reasoning problem.
    
    Args:
        relations: dict, maps relation labels to indices
        sLabs: list of str, stimulus labels
        p: str, number of premises
        n_rep: int, number of repetitions for each problem
        r: index for relation one
        r2: index for relation 2
        ...
        
    Returns:
        stim: list of str, unique stimulus labels for this problem
        t_id: index of the first stimulus label (in sLabs) in current problem
        
    """
    p = int(p)
    if len(relations.keys()) == 1 or n_rep == 1: # new Ss every relation
        if p == 1:
            t_id = (p+1)*rep + (p+1)*r # 2 stimuli per problem
        elif p == 2:
            t_id = (p+1)*rep + (p+1)*r + (p+1)*r2 # 3 stimuli per problem
        elif p == 3:
            t_id = (p+1)*rep + (p+1)*r + (p+1)*r2 + (p+1)*r3 # 4 stimuli per problem
        elif p == 4:
            t_id = (p+1)*rep + (p+1)*r + (p+1)*r2 + (p+1)*r3 + (p+1)*r4 # 5 stimuli per problem
        else: t_id = (p+1)*rep + (p+1)*r + (p+1)*r2 + (p+1)*r3 + (p+1)*r4 + (p+1)*r5 # 6 stimuli per problem
    else: # new stimuli each repetition
        t_id = (p+1)*rep # 2 S's per problem
    
    # Adapt index to avoidindexing errors
    if t_id+p >= len(sLabs): # If more S's needed than labeled in list, loop through list
        loop = int(np.round(t_id/len(sLabs)))
        t_id -= loop*len(sLabs) # cycle back through list
    stim = []
        
    for i in range(p+1):
        stim.append(sLabs[t_id+i])
    
    return stim, t_id
# %% Find an incorrect relation

def findIncorrectRelation(relations, relpremVoc, correctRel):
    notRels = []
    if len(relations.keys()) == 1:
        allRels = ['the same as', 'different from', 'opposite to', 
                   'more than', 'less than', 
                   # 'part of', 'contains', 'before', 'after'
                   ]
    else:
        allRels = []
        for i in relations.keys():
            allRels.append(relpremVoc[i]) 
    for ir in range(len(allRels)):
        if correctRel == 'different from':
            if not allRels[ir] in ['opposite to', 'different from']:
                notRels.append(allRels[ir])
        elif correctRel == 'opposite to':
            if not list(allRels)[ir] in ['opposite to', 'different from']:
                notRels.append(allRels[ir])
        else:
            if not allRels[ir] == correctRel:
                notRels.append(allRels[ir])
    incorLab = np.random.choice(notRels)
    return incorLab

# %% Find irrelevant stimuli and relation to include in syllogistic problem

def findIrrelevant(relations, sLabs, t_id):
    """
    Finds an irrelevant relation and stimulus to include in syllogistic problem.
    
    Args:
        relations: dict, maps relation labels to indices
        sLabs: list of str, stimulus labels
        t_id: int, index of current stimulus labels
        
    """
    # Find irrelevant S to add premise
    half = len(sLabs)/2
    if t_id < half:
        irr_id = np.random.randint(half+1, len(sLabs))
    else:
        irr_id = np.random.randint(0,half-1)
    irrRel = np.random.choice(list(relations.keys()))
    irrS = sLabs[irr_id]
    
    return irrRel, irrS

# %% formatPremise - helper function to create premises

def formatPremise(a, rel, b):
    """
    Formats premise based on relation.
    
    Args: 
        a: str, stimulus label 1
        rel: str, relation label
        b: str, stimulus label 2
        
    Returns: formatted premise
    """
    return f"{a} {rel} {b}." if rel == "contains" else f"{a} is {rel} {b}."

# %% Create relational premises for syllogistic reasoning problem

def createPremises(rels, stim, protocol):
    
    """
    For given level of complexity (number of premises) and combination 
    protocol (linear, OTM, MTO, reversed linear), create premises for syllogistic 
    relational reasoning problems from input stimuli and rels.
    
    Args:
        rels: list of str, labels for the relations to put in premises
        stim: list of str, labels for to-be-related stimuli, not yet ordered
        protocol: str, the combination protocol ('Linear', 'OTM', 'MTO', 'revLinear')
    
    Returns:
        premises: list of strings containing premises
        sources: list of tuples containing related stimulus pairs for each premise
    
    """
    n_p = len(rels) # determine number of premises from number of rels
    if protocol == 'Linear': # linear combination AB, BC, CD, ...
        premises = [
            formatPremise(stim[i], rels[i], stim[i+1])
            for i in range(n_p)
            ]
        # also store source stimulus pairs for each relation
        sources = [(stim[i], stim[i+1]) for i in range(n_p)] 
        
    elif protocol == 'OTM': # one-to-many AB, AC, AD, ...
        premises = [
            formatPremise(stim[0], rels[i], stim[i+1])
            for i in range(n_p)
            ]
        sources = [(stim[0], stim[i]) for i in range(1, len(stim))]
    elif protocol == 'MTO': # many-to-one BA, CA, DA, ...
        premises = [
            formatPremise(stim[i+1], rels[i], stim[0])
            for i in range(n_p)
            ]
        sources = [(stim[i], stim[0]) for i in range(1, len(stim))]
    elif protocol == 'revLinear':
        premises = [
            formatPremise(
                stim[0] if i == 0 else stim[i+1],
                rels[i],
                stim[1] if i == 0 else stim[i-1]
            )
            for i in range(n_p)
            ]   
        sources = [
            (stim[0], stim[1]) if i == 0 else (stim[i+1], stim[i-1])
            for i in range(n_p)
            ]
    else:
        raise ValueError("Unknown protocol")

    return premises, sources

# %% Create problem conclusion given relation label and stimulus pair

def createConclusion(source12, corLab):
    
    """
    Formats conclusion for regular syllogistic reasoning problem
    
    Args:
        source12: list of int, pair of (derived) related stimulus indices
        corLab: str, label of derived relation
        
    Returns: 
        conc: str, conclusion prompt
    """
    if corLab == "contains":
        conc= "Does {} contain {}?". format(source12[0], source12[1])
    else:
        conc = "Is {} {} {}?". format(source12[0], corLab, source12[1])

    return conc

# %%

def createTOFConclusion(tofs, corLab, func, cfuncprompts, funcs):
    """
    Formats conclusion for transformation of function syllogistic reasoning problem
    
    Args:
        tofs: str, label for the stimulus that has derived function
        corLab: str, label of derived relation
        func: int, index of the related function label
        cfuncprompts: dict, maps relations to function 'verbs'
        funcs: dict, maps relations to functions
        
    Returns: 
        conc: str, conclusion prompt
    """
    
    if corLab in ['Same as', 'Different from', 'opposite to']:
        conc = "Does {} {} '{}'?".format(tofs, cfuncprompts[corLab][func], funcs[corLab][func])
    elif corLab in ['more than', 'less than', 'before', 'after']:
        conc = "Is {} {} '{}'?".format(tofs, cfuncprompts[corLab][func], funcs[corLab][func])
    else: pdb.set_trace()
    return conc

# %% create analogy prompt conclusion

def createAnalogyConclusion(stim):
    """
    Formats conclusion for analogy syllogistic reasoning problem
    
    Args:
        stim: list of str, three stilmuli related in two premises
        
    Returns: 
        conc: str, conclusion prompt
    """
    conc = "Is {} to {} the same as {} to {}?". format(stim[0], stim[1], stim[1], stim[2])
    
    return

# %% determine_taskPremise - choose task premise (select TRUE/FALSE) for MC problems

def determine_taskPremise(selectTF):
    if selectTF:
        taskPremise = np.random.choice(["Select all TRUE statements.",
                                         "Select all FALSE statements."])
    else:
        taskPremise = 'Select the TRUE statement from the options below.'
    return taskPremise

# %% convert_selecttf - convert 'correct' list for MC problems based on task premise
def _convert_selecttf(corr_list, output, selectTF, taskPremise):
    
    """ 
    Convert 'correct' list for labjs output data and printing
    """
    if selectTF:
        if output == 'csv':
            out = [1 if x == "Yes" else 0 for x in corr_list] # default select TRUE
            if taskPremise == "Select all FALSE statements.":
                out = [1 - x for x in out] # convert if task is to select false
            out = ['select' if x == 1 else 'no select' for x in out] # convert
            printOut = out
        elif output == 'labjs':
            out = [1 if x == "Yes" else 0 for x in corr_list] # default select TRUE
            if taskPremise == "Select all FALSE statements.":
                out = [1 - x for x in out] # convert if task is to select false
            printOut = ['select' if x == 1 else 'no select' for x in out] # convert
        elif output == 'LLMstudy':
            out = ""
            cor_ids = []
            if taskPremise == 'Select all TRUE statements.':
                for i in range(len(corr_list)):
                    if corr_list[i] == 'Yes': cor_ids.append(i+1)
                if len(cor_ids) == 2:
                    out = f"Option {cor_ids[0]} and Option {cor_ids[1]}"
                    printOut = f"Option {cor_ids[0]} and Option {cor_ids[1]} are TRUE."
                elif len(cor_ids) == 1:
                    out = f"Option {cor_ids[0]}"
                    printOut = f"Option {cor_ids[0]} is TRUE."
            else:
                for i in range(len(corr_list)):
                    if corr_list[i] == 'No': cor_ids.append(i+1)
                if len(cor_ids) == 2:
                    out = f"Option {cor_ids[0]} and Option {cor_ids[1]}"
                    printOut = f"Option {cor_ids[0]} and Option {cor_ids[1]} are FALSE."
                elif len(cor_ids) == 1:
                    out = f"Option {cor_ids[0]}"
                    printOut = f"Option {cor_ids[0]} is FALSE."
    else:
        if output == 'csv':
            out = [1 if x == "Yes" else 0 for x in corr_list] # default select TRUE
            printOut = ['select' if x == 1 else 'no select' for x in out] # convert
        elif output == 'labjs':
            out = [1 if x == "Yes" else 0 for x in corr_list] # default select TRUE
            printOut = ['select' if x == 1 else 'no select' for x in out]
        elif output == 'LLMstudy':
            cor_id = list.index(corr_list, 'Yes')
            out = f"Option {cor_id+1}"
            printOut = f"Option {cor_id+1} is TRUE."
    return out, printOut
# %% createMCconclusion - create multiple choice response options


def createMCconclusion(n_opt, corDerLab, d_pair, rels, relations, relpremVoc, 
                       derivation, mutual, selectTF, illDefined = False):
    
    """
    Formats conclusions for multiple choice syllogistic reasoning problem
    
    Args:
        n_opt: int, number of response options
        corDerLab: str, label of derived relation
        d_pair: list of str, labels of derived related stimuli
        rels: list of str, labels of relations in premises
        relations: dict, maps relations to indices
        relpremVoc: dict, maps adapted relation labvels to indices
        derivation: str, 'mutual' or 'combinatorial'
        mutual: list of int, indices for mutually entailed relations of relations
        
    Returns: 
        conc: list of str, number multiple choice conclusion prompts
        correct: list of str, 'yes' or 'no' for each conclusion
    """
    corDer= relations[list(relpremVoc.keys())[list.index(list(relpremVoc.values()), corDerLab)]]
    
    prompt_answers = {} # map response options to correct response
    conc = [] # store response options
    correct = [] # store correct responses
    
    # correct derivation
    correct_conc = "{} is {} {}.".format(d_pair[0], corDerLab, d_pair[1]) # create conclusion
    prompt_answers[correct_conc] = 'Yes' # add to dict
    
    # incorrect derivation
    incorDerLab = str(findIncorrectRelation(relations, relpremVoc, corDerLab)) # find incorrect derived relation
    
    incorrect_conc = "{} is {} {}.".format(d_pair[0], incorDerLab, d_pair[1]) # create conclusion
    prompt_answers[incorrect_conc] = 'No' # add to dict
    if derivation == 'Combinatorial':
        # if derivation == 'Combinatorial': # can include correct and incorrect mutually entailed CE
        d_revpair = [d_pair[1], d_pair[0]] # reverse stimulus pair
        derRev = mutual[corDer] # find mutually entailed relation
        derRevLab = relpremVoc[list(relations.keys())[derRev]] # get label
        correct_rev_conc = "{} is {} {}.".format(d_revpair[0], derRevLab, d_revpair[1]) # create conclusion
        prompt_answers[correct_rev_conc] = 'Yes' # add to dict
        
        # incorrect mutually entailed of CE
        incorDerRevLab = findIncorrectRelation(relations, relpremVoc, derRevLab) # find incorrect derived relation
        incorrect_rev_conc = "{} is {} {}.".format(d_revpair[0], incorDerRevLab, d_revpair[1]) # create conclusion
        prompt_answers[incorrect_rev_conc] = 'No' # add to dict
    IDK_conc = f"I need more information to derive the relation between {d_pair[1]} and {d_pair[0]}."
    if illDefined: 
        prompt_answers[IDK_conc] = 'Yes'
    else:
        prompt_answers[IDK_conc] = 'No'
    # randomly select user-specified number of response options and determine which are correct
    if selectTF:
        if not illDefined:
            temp_conc = np.random.choice(list(prompt_answers.keys()), n_opt, replace = False)
            for i in temp_conc:
                correct.append(prompt_answers[i])
        else: 
            raise ValueError("'It is better not to include ill-defined problems with\
                              the 'selectTF' option on!")
    else: # only one correct conclusion
        if illDefined:
            temp_conc = np.random.choice(list(prompt_answers.keys()), n_opt-1, replace = False)
            temp_conc = np.concatenate([temp_conc, [IDK_conc]])
            np.random.shuffle(temp_conc)
            for i in temp_conc:
                if i == IDK_conc:
                    correct.append('Yes')
                else: correct.append('No')
        else:
            if derivation == 'Mutual':
                if n_opt -1 > 2: n_draw = 2 
                else: n_draw = n_opt-1
                temp_conc = np.random.choice([incorrect_conc, IDK_conc], n_draw, replace = False)
                temp_conc = np.concatenate([temp_conc, [correct_conc]])
                np.random.shuffle(temp_conc)
            else:
                if n_opt -1 > 3: n_draw = 2 
                else: n_draw = n_opt-1
                temp_conc = np.random.choice([incorrect_conc, incorrect_rev_conc, IDK_conc], n_draw, replace = False)
                temp_conc = np.concatenate([temp_conc, [np.random.choice([correct_conc, correct_rev_conc])]])
                np.random.shuffle(temp_conc)
            for i in temp_conc:
                correct.append(prompt_answers[i])    
    # add numbering to response options
    for i in range(len(temp_conc)):
        conc.append('\n{}. {}'.format(i+1, temp_conc[i]))
        
    return conc, correct

