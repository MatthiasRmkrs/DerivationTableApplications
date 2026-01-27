# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 12:49:38 2026

Personal functions to improve efficiency and readability.

@author: mraemaek
"""

# %% dependencies

import numpy as np
from itertools import product
import pdb



# %% cleanRelations - Convert input list of 'dirty' relation labels to 'clean' dict

def cleanRelationLabels(relations):
    
    """ 
    Converts 'dirty' input relations list to dict with 'clean' relation labels.
    
    Args: 
        relations: list of input relations
        relVariants: dict with common variants of supported relations
        
    Returns: 
        relations: dict with clean relation labels as keys and zero-based indices 
                    for derivation tables as values
    """
    
    cleanVariants = {'Same as': 'same',
                        'Different from': 'different',
                        'Opposite to': 'opposite',
                        'More than':  "more", 
                        'Bigger than': 'bigger',
                        'Larger than': "larger", 
                        'Faster than': "faster", 
                        'Stronger than': "stronger",
                        'Better than': "better", 
                        'Longer than': "longer", # any comparative relation
                        'Less than': "less", 
                        'Smaller than': "smaller", 
                        'Slower than': "slower", 
                        'Weaker than': "weaker", 
                        'Worse than': "worse", 
                        'Shorter than': "shorter",
                        'Before': 'before',
                        'After': 'after',
                        'Contains': 'contains',
                        'Is part of': 'part of'}

    
    cleanRelations = dict()
    useableRelations = dict()
    rel_id = -1 # init relation index
    for rel in relations: # loop input relations list
        rel_id +=1
        
        for clean, dirty in cleanVariants.items(): # also store a clean version of input
            if dirty in rel.lower(): cleanRelations[clean] = rel_id
            
    return cleanRelations

# %% findGenericRelations - converts specific relations (e.g. taller) to general (more)

def findGeneralRelations(relations):
    default2specific = dict({'Same as': ['same', "equivalent", "identical",
                                    # more?
                                    ],
                        'Different from': ['different', 'non-equivalent', 'non-identical'],
                        'Opposite to': ['opposite'],
                        'More than':  ["more", 'bigger', "larger", "faster", 
                                       "stronger", "better", "longer", # any comparative relation
                                       # 'after', # could add temporal here too, but then need to remove the before/after lists
                                ],
                        'Less than': ["less", "smaller", "slower", "weaker", "worse", "shorter",
                                      # "before",
                                ],
                        'Before': ['Before', 'before', 'is before'],
                        'After': ['After', 'after', 'is after'],
                        'Contains': ['contains', 'includes', 'Includes'],
                        'Is part of': ['part of', 
                                       'example', # is an example of ...
                                       'type' # is a type of ...
                                       ]
                        })
    defaultRelations = {}
    rel_id = -1
    for rel in relations.keys(): # loop input relations
        rel_id +=1
        for defaults, variants in default2specific.items(): # find the correct gerenal relational pattern
            for variant in variants:
                if variant in rel.lower(): 
                    # create a new label to store in new dict, with general relation
                    # accounting for multiple instances of same general pattern
                    relLab = str(defaults) + ' - ' + str(rel)
                    defaultRelations[relLab] = rel_id
    return defaultRelations
# %% completeRelations - complete list of input relations with missing derived relations

def completeRelations(relations, assymetrical):
    """
    For a given set (list) of input relations, checks whether the derived 
    relations are also included. If not, this will lead to indexing problems, 
    so add them to the list before creating derivation tables.
    
    Args: 
        relations: list, strings representing relations
        assymetrical: dict, input relations as keys, mutually entailed relation
                        as values.
                        
    Returns:
        relations: dict
    """
    updatedRels = dict()
    for i in relations.keys():
        updatedRels[i] = len(list(updatedRels.keys())) # add input relations
        if i in assymetrical:  # find mutually entailed relation in assymetrical dict
            mutlab = assymetrical[i] # get label for mutual
            if assymetrical[i] not in relations.keys(): # check if mutually entailed relation is in 
                updatedRels[assymetrical[i]] = len(list(updatedRels.keys())) # if not, add it
                # (i.e., mutually entailed of the now newly added relation, 
                # otherwise dimensions don't match)
                
    relations = updatedRels # update dict
    
    # in the exceptional case that only opposition relations are included in input, 
    # and not equivalence, add equivalence to 'relations' dict so combinatorial 
    # entailment of opposition relations can be done
    if 'Opposite to' in relations.keys() and 'Same as' not in relations.keys():
        relations['Same as'] = len(relations.keys()) # add 'Same as'
    
    return relations

# %% relLabsForPremises - similar to above, convert rel Labs for premises in syllogistic problem

def relLabsForPremises(relations):
    """
    # convert input labels to ones that can be used in premises
    """
    premiseVariants = {'the same as': 'same',
                        'different from': 'different',
                        'opposite to': 'opposite',
                        'more than':  "more", 
                        'bigger than': 'bigger',
                        'larger than': "larger", 
                        'faster than': "faster", 
                        'stronger than': "stronger",
                        'better than': "better", 
                        'longer than': "longer", # any comparative relation
                        'less than': "less", 
                        'smaller than': "smaller", 
                        'slower than': "slower", 
                        'weaker than': "weaker", 
                        'worse than': "worse", 
                        'shorter than': "shorter",
                        'before': 'before',
                        'after': 'after',
                        'contains': 'contains',
                        'part of': 'part of'}
    useableRelations = []
    rel_id = -1 # init relation index
    for rel in relations: # loop input relations
        rel_id +=1
        for useable, inputs in premiseVariants.items():
            if inputs in rel.lower(): useableRelations.append(useable)
    
    return useableRelations

# %% findCommon - Find common relata in combination of two relations

def findCommon(source1, source2):
    """ 
    Finds the common relata in two input relations.
    
    Args:
        source1 - tuple containing two indices for related stimuli
        source2 - 
        
    Returns:
        common: index of the common stimulus, returns -1 if no common element
    """
    
    # Find common element
    common = -1
    for sr1 in source1:
        for sr2 in source2:
            if sr1 == sr2:
                common = sr2  
                
    return common
    
    
# %% deriveCombi - Find combinatorially entailed relation for a pair of relations

def deriveCombi(source1, source2, common, rel1, rel2, combi):
    """
    
    Uses derivation tables to derive the combinatorially entailed relation for
    combination of two provided relations.
    Derivation depends on combination of relations, and of the position of the
    common element (i.e., the order of relata -> combination type: linear, OTM, MTO, sMTO)
    
    Args:
        source1: tuple containing indices of two related stimuli
        source2: tuple containing indices of second pair of related stimuli
        common: index of the stimulus that is common between source1 and source2
        rel1:
        rel2:
        
    Returns:
        crel: int - the index of the combinatorially entailed relation in the
                    derivation tables
        source12: tuple, pair of stimuli related by derived relation
    """
    
    if tuple.index(source1, common) == 0:
        if tuple.index(source2, common) == 0: # A-B & A - C (OTM)
            crel = combi['OTM'][rel1, rel2]
            source12 = (source1[1], source2[1])

        else: # A - B & C - A (sort of MTO)
            crel = combi['sMTO'][rel1, rel2]
            source12 = (source1[1], source2[0])
    else:
        if tuple.index(source2, common) == 0: # A-B & B - C (linear)
            crel = combi['Linear'][rel1, rel2]
            source12 = (source1[0], source2[1])
        else: # A-B & C- B (MTO)
            crel = combi['MTO'][rel1, rel2]
            source12 = (source1[0], source2[0])

    return crel, source12
    
# %% determineProtocol - determine combination protocol (linear, reversed linear, OTM, MTO)

def determineProtocol(source1, source2, common):
    """
    Determines the protocol (linear, reversed linear)
    
    Args:
        source1: tuple containing indexes of two related stimuli
        source2: tuple containing indexes of second pair of related stimuli
        common: index of the common element in both relations (findCommon function output)
    """
    # check each relation to find location of common element & protocol
    if tuple.index(source1, common) == 0:
        if tuple.index(source2, common) == 0: # AxB and AxC
            protocol = 'OTM' # One-to-many
        else: # AxB and CxA
            protocol = 'sMTO'
    else: 
        if tuple.index(source2, common) == 0: # AxB and BxC
            protocol = 'Linear'
        else: # AxB and CxB
            protocol = 'MTO'
    return protocol

# %% countUniqueStimuli - Find number of unique stimuli in 'baseline' network

def countUniqueStimuli(baseline):
    
    """
    For a given set of baseline relations, finds the number of unique stimuli 
    that make up the relational network.
    
    Args:
        baseline: a dict with relation labels as keys, and a list of tuples 
        (stimulus pairs) that represent the different instances of that relation
        
    Returns:
        n_stim: int, the number of unique stimuli in the network
    
    """
    
    unique = []
    for i,j in baseline.items():
        for jj in j:
            for stim in jj:
                if stim not in unique: unique.append(stim)
    n_stim = len(unique)
    return n_stim

# %% createRelationTable - Create relTab for heatmap plot of relational network

def createRelationTable(baseline, derived=None):
    
    # Get dimensions to initialize table
    unique_rels = []
    for base in baseline.keys():
        if base not in unique_rels: unique_rels.append(base)
        
    if derived is not None:
        for der in derived.keys():
            if der not in unique_rels: unique_rels.append(der)
    n_rel = len(unique_rels) # number of unique relations
    relations = cleanRelationLabels(unique_rels) # get relations dict
    n_stim = countUniqueStimuli(baseline)  # find number of unique stimuli
    relTab = np.zeros([n_rel, n_stim, n_stim], dtype = 'int') # Tabular version of dict
    
    for rel, instances in baseline.items():
        rel_id = relations[rel]
        for instance in instances:
            relTab[rel_id, instance[0], instance[1]] = 1
    if derived is not None:
        for rel, instances in derived.items():
            rel_id = relations[rel]
            for instance in instances:
                relTab[rel_id, instance[0], instance[1]] = 1
                
    return relTab

# %% find all unique combinations of a set of relations for a given number of premises

def findAllRelPremCombinations(relations, p):
    
    """
    For a given set of relations, finds all combinations of those relations that 
    can go in a given number of premises, using itertools product.
    
    Args:
        Relations: dict, relations as keys, int indices as values
        n_p: the number of premises (repetitions)
    Returns:
        p_rels: dict, number of premises as keys, list of lists with combinations
                of relations as values
    """
    
    
    rel_list = list(relations.keys())
    
    p_rels = {
        str(n): [list(tup) for tup in product(rel_list, repeat=n)]
        for n in range(1, int(p) + 1)
    }
    return p_rels


# %% Find new (unique) stimulus labels for a given syllogistic problem in loop

def findUniqueStimuli(relations, sLabs, p, n_rep, rep, r, r2=None, r3 = None, r4=None, r5 = None):
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

def findIncorrectRelation(relations, correctRel):
    notRels = []
    if len(relations.keys()) == 1:
        allRels = ['the same as', 'different from', 'opposite to', 
                   'more than', 'less than', 
                   # 'part of', 'contains', 'before', 'after'
                   ]
    else:
        allRels = list(relations.keys())
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
    if corLab == "contains":
        conc= "Does {} contain {}?". format(source12[0], source12[1])
    else:
        conc = "Is {} {} {}?". format(source12[0], corLab, source12[1])

    return conc

# %%

def createTOFConclusion(tofs, corLab, func, cfuncprompts, funcs):
    
    
    if corLab in ['Same as', 'Different from', 'opposite to']:
        conc = "Does {} {} '{}'?".format(tofs, cfuncprompts[corLab][func], funcs[corLab][func])
    elif corLab in ['more than', 'less than', 'before', 'after']:
        conc = "Is {} {} '{}'?".format(tofs, cfuncprompts[corLab][func], funcs[corLab][func])
    else: pdb.set_trace()
    return conc

# %% create analogy prompt conclusion

def createAnalogyConclusion(stim):
    
    conc = "Is {} to {} the same as {} to {}?". format(stim[0], stim[1], stim[1], stim[2])
    
    return

# %% createMCconclusion - create multiple choice response options


def createMCconclusion(n_opt, corDerLab, d_pair, rels, relations, relpremVoc, derivation, mutual):
    corDer= relations[list(relpremVoc.keys())[list.index(list(relpremVoc.values()), corDerLab)]]
    
    prompt_answers = {} # map response options to correct response
    conc = [] # store response options
    correct = [] # store correct responses
    
    # correct derivation
    correct_conc = "{} is {} {}.".format(d_pair[0], corDerLab, d_pair[1]) # create conclusion
    prompt_answers[correct_conc] = 'Yes' # add to dict
    
    # incorrect derivation
    incorDerLab = findIncorrectRelation(relations, corDerLab) # find incorrect derived relation
    incorDerLab = relpremVoc[incorDerLab]    
    incorrect_conc = "{} is {} {}.".format(d_pair[0], incorDerLab, d_pair[1]) # create conclusion
    prompt_answers[incorrect_conc] = 'No' # add to dict
    
    if derivation == 'Combinatorial': # can include correct and incorrect mutually entailed CE
        d_revpair = [d_pair[1], d_pair[0]] # reverse stimulus pair
        derRev = mutual[corDer] # find mutually entailed relation
        derRevLab = relpremVoc[list(relations.keys())[derRev]] # get label
        correct_rev_conc = "{} is {} {}.".format(d_revpair[0], derRevLab, d_revpair[1]) # create conclusion
        prompt_answers[correct_rev_conc] = 'Yes' # add to dict
        
        # incorrect mutually entailed of CE
        incorDerRevLab = findIncorrectRelation(relations, derRevLab) # find incorrect derived relation
        incorDerRevLab = relpremVoc[incorDerRevLab]
        incorrect_rev_conc = "{} is {} {}.".format(d_revpair[0], incorDerRevLab, d_revpair[1]) # create conclusion
        prompt_answers[incorrect_rev_conc] = 'No' # add to dict
        
    all_true_conc = 'All other options are TRUE.'
    all_false_conc = 'All other options are FALSE.'
    IDK_conc = "I don't know."
    prompt_answers[all_true_conc] = '' # add to dict
    prompt_answers[all_false_conc] = '' # add to dict
    
    # randomly select user-specified number of response options 
    temp_conc = np.random.choice(list(prompt_answers.keys()), n_opt, replace = False)
    
    temp_correct = []
    # determine whether all TRUE/FALSE, if included
    for i in temp_conc:
        if not (i == all_true_conc or i == all_false_conc):
            temp_correct.append(prompt_answers[i])
            
    if all_true_conc in temp_conc:
        if 'No' in temp_correct: prompt_answers[all_true_conc] = 'No' # update dict
        else: prompt_answers[all_true_conc] = 'Yes' # update dict
    elif all_false_conc in temp_conc: 
        if 'Yes' in temp_correct: prompt_answers[all_false_conc] = 'No'  # update dict
        else: prompt_answers[all_false_conc] = 'Yes'  # update dict
    
    # find correct responses to each included response option
    for i in temp_conc:
        correct.append(prompt_answers[i]) # update final 'correct' list in correct order
    
    # add numbering to response options
    for i in range(len(temp_conc)):
        conc.append('\n{}. {}'.format(i+1, temp_conc[i]))
    
    return conc, correct