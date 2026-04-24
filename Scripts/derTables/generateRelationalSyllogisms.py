# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 11:22:22 2024

Script that generates a syllogistic relational reasoning task.
Very similar to generateMTS:
    - Takes a number of specified relations (that the task involves) to derive
        transitivity tables
        -> The labels specified in this dict will serve as the 'cue' in syllogism
    - Uses input relations and task parameters to create syllogisms
    
Input: 
    - Relations: list - labels for relations that will be used in premises like 'A is *label* B'
                    e.g., 'the same as', 'different from', 'larger than', ...
    - premises_types: Number of premises and types of problem in a dict:
        - Keys: numbers 1 to 5 for different number of premises (could in principle do more)
        - Values: list with different options for problem, choose from:
            - 'Incorrect'
            - 'Irrelevant': add irrelevant premise to problem
            - 'addMutualCE': test reversal of combinatorially entailed relation
            - 'Analogy': only for two premises, adds problem that prompts analogical 
                        comparison of two relations
            - ...
    - n_rep: number of repetitions of each trial (type)
    - relata: str - determines what stimuli to use as relate, if not defined by user
    - sLabs = None: optional list of stimulus labels (non-words, names, letters) 
    - functions = None, dict containing functions to use in function transformation problems
        Keys: 
    - testToF = False: Boolean, set to True to also test transformations of function
    - printTrials = False, Boolean - print out problems as illustration 
    - randomizePremises = False, Boolean - Randomize premise order?
    - includeIllDefined = False, Booelan - also include ill-defined problems?


######
TODO:
    - ADD multiple choice setting
        -> figure out inputs, which types to include, efficiently update trial data, 
        ...
    - This version is linear training, could allow user to define and specify 
        different training protocols (Linear, One-to-many, many-to-one)? 
        Many different options when there are more than 2 premises...
    - Add other types of ToF
        -> What is the benefit? Not really transformation of function anyway?
            -> Could add separate test where a function is attached to the 
                relations, "is ... the same value as ...?"
                Only need to make sure labels are compatible across relations,
                or specify them?

@author: mraemaek

"""


import pdb

# Dependencies
import numpy as np
import pandas as pd
from derTables.createDerivationTables import createDerivationTables # create derivation tables for input relations
from derTables.deriveRelationsFromBaseline import deriveRelationsFromBaseline # auto-derive relations
from derTables.utils_tables import (findCommon, deriveCombi) # derivation tables helpers
from derTables.utils_syllogisms import (findAllRelPremCombinations, # syllogistic problem formatiing helpers
                              relLabsForPremises,
                              findUniqueStimuli,
                              findIncorrectRelation,
                              findIrrelevant,
                              createConclusion,
                              createPremises,
                              formatPremise,
                              createAnalogyConclusion,
                              createMCconclusion,
                              createTOFConclusion,
                              determine_taskPremise,
                              _convert_selecttf
                              )


# Some default stimulus labels (non-words, names, alfanumerics) to use in problems
alphanumerics = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 
                 'N1', 'O1', 'P1', 'Q1', 'R1', 'S1', 'T1', 'U1', 'V1', 'W1', 'X1', 'Y1', 'Z1',
                 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 
                 'N2', 'O2', 'P2', 'Q2', 'R2', 'S2', 'T2', 'U2', 'V2', 'W2', 'X2', 'Y2', 'Z2']

nonwords = ['GUK', 'WEK', 'MAK', 'POK', 'MUL', "WUL", 'POM', "ERT", "ZET", "KUB",
             "BAH", "REB", "FER", "ARV", "BUL", "MOL", "CUZ", "VAP", "GEB", "LIR",
             "JIL", "KIR", "ERP", "BIR", "RAL", "BUR", "MOR", "BAU", "PIL", "ERK",
             "DEB", "ABE", "OPI", "ARP", "LOM", "BIR", "GUR", "RUG", "NIT", 'WIL',
             "REG", "ZEP", "TOR", "TAM", "BUR", "POL", "NOP", "FES", "TUR", "BIL", 
             "MAV", "DOJ", "SAH", "SEG", "DIJ", "LIS", "MIP", "DEP", "FON", "QUG",
             "AZE", "ERI", "KOT", "MAJ", "VOR", "XIL", "POR", "WIL", "CET", "FUB",
             "ZEV", "GIB", "LUN", "VOT", "SIH", "ZOP", "BES", "JEX", "LIM", "PED",
             "BUR", "FIK", "MEV", "DOS", "LOM", "TER", "PUX", "ALO", "IME", "MOP",
             "VIT", "POQ", "XIM", "WOM", "DOR", "AZO", "ELA", "MIL", "POR", "SER",
             "DET", "ITO", "VIO", "MOL", "DIF", "ERD", "TRO", "IBO", "DOA", "MIP"] 

names = ['Bart', 'John', 'Elsa', 'Mark', 'Jane', 'Phillip', 'Jake', 'Lisa', 'Ella',
         'Sam', 'Chris', 'Joe', 'Megan', 'Archie', 'Charlie', 'Macie', 'Grace', 'Jack',
         'Mike', 'Fiona', 'Ellie', 'Jim', 'Ben', 'Jacob', 'Mary', 'Casper', 'Jon',
         'Micheal', 'Fred', 'Ivan', 'Tim', 'Bella', 'Blake', 'Amber', 'Josh',
         'Nick', 'Jake', 'Maria', 'Chelsea', 'Frank', 'James', 'Jamie', 'Melissa']

def generateSyllogism(relations, premises_types, n_rep, relata, protocol, *, sLabs = None, 
                      functions = None, n_opt = None, testToF = False,
                      printTrials = False, randomizePremises = False,
                      selectTF = False, includeIllDefined = False, output = 'csv'):
    
    if protocol is None:
        protocol = 'Linear' # linear combination by default
    if sLabs is None:
        if relata == 'nonwords': sLabs = nonwords
        elif relata == 'names': sLabs = names
        elif relata == 'alphanumerics': sLabs = alphanumerics
    
    # specify vocabulary to translate default relation labels to ones that fit in premises
    relpremVoc = {'Same as': 'the same as',
                    'Different from': 'different from',
                    'Opposite to': 'opposite to',
                    'More than': 'more than',
                    'Less than': 'less than',
                    'Contains': 'contains',
                    'Before': 'before',
                    'After': 'after',
                    'Is part of': 'is part of',
                    'Left of': 'to the left of',
                    'Right of': 'to the right of',
                    'In front': 'in front of',
                    'Behind': 'behind'
                      }

    # Create transitivity tables for relations in task
    mutual, combi, relations = createDerivationTables(relations)
    # Initialize before looping trials
    trial_data = dict({'id': [], 'Premises': [], 'Relations': [], 'Prompt': [],
                       'Correct': [], 'printCorrect': [], 'Type': [], 'n_p': []})
    t = 0
    rels = []  # init to store current problem relation(s) and stimuli
    stim = []
    rows = []  # for data storage

    for p, var in premises_types.items():  # loop levels of complexity and variants                                          
        premises = [] # init new set of premises
        p_rels = findAllRelPremCombinations(relations, p) # find all combinations of relations for N premises
        for rels in p_rels[p]:# then loop over those
            r_ids = []
            for i in rels: # fetch relation indices (for derivation tables)
                r_ids.append(relations[i])
            useableRelations = relLabsForPremises(rels)
            

            for rep in range(n_rep): # loop problem repetitions (unique stimuli)
                t += 1  # update trial id
                if p == '1':
                    stim, t_id = findUniqueStimuli(
                        relations, sLabs, p, n_rep, rep, r_ids[0])
                elif p == '2':
                    stim, t_id = findUniqueStimuli(
                        relations, sLabs, p, n_rep, rep, r_ids[0], r_ids[1])
                elif p == '3':
                    stim, t_id = findUniqueStimuli(
                        relations, sLabs, p, n_rep, rep, r_ids[0], r_ids[1], r_ids[2])
                elif p == '4':
                    stim, t_id = findUniqueStimuli(
                        relations, sLabs, p, n_rep, rep, r_ids[0], r_ids[1], r_ids[2], r_ids[3])
                elif p == '5':
                    stim, t_id = findUniqueStimuli(
                        relations, sLabs, p, n_rep, rep, r_ids[0], r_ids[1], r_ids[2], r_ids[3], r_ids[4])
                
                # Build premises using stimuli (linear)
                # establish function for first related S
                if testToF and rels[0] not in ['part of', 'contains']:
                    if functions != None:
                        crelfuncs = functions['crelfuncs']
                        cfuncprompts = functions['cfuncprompts']
                        funcs = functions['funcs']
                    if rep >= len(crelfuncs[rels[0]]):  # control index
                        loop = int(
                            np.round(rep/len(crelfuncs[rels[0]])))
                        # cycle back through list
                        func = rep - loop*len(crelfuncs[rels[0]])
                    else:
                        func = rep
                    fPremise = "{} {} '{}'.".format(
                        stim[0], crelfuncs[rels[0]][func], funcs[rels[0]][func])
                premises, sources = createPremises(useableRelations, stim, protocol)
                
                # derive relation
                if p == '1': # mutual entailment
                    corDer = mutual[r_ids[0]] # Find mutual relation
                    d_pair = [stim[1], stim[0]]
                    derivation = 'Mutual'
                else:                    
                    derivation = 'Combinatorial'
                if p == '2':
                    common = findCommon(sources[0], sources[1]) # Find common
                    corDer, d_pair = deriveCombi(
                        sources[0], sources[1], common, r_ids[0], r_ids[1], combi)
                if p == '3':
                    common = findCommon(sources[0], sources[1]) # Find common
                    corDer, d_pair = deriveCombi(
                        sources[0], sources[1], common, r_ids[0], r_ids[1], combi)
                    common = findCommon(d_pair, sources[2]) # Find common
                    corDer, d_pair = deriveCombi(
                        d_pair, sources[2], common, corDer, r_ids[2], combi)
                if p == '4':
                    common = findCommon(sources[0], sources[1]) # Find common
                    corDer, d_pair = deriveCombi(
                        sources[0], sources[1], common, r_ids[0], r_ids[1], combi)
                    common = findCommon(d_pair, sources[2]) # Find common
                    corDer, d_pair = deriveCombi(
                        d_pair, sources[2], common, corDer, r_ids[2], combi)
                    common = findCommon(d_pair, sources[3]) # Find common
                    corDer, d_pair = deriveCombi(
                        d_pair, sources[3], common, corDer, r_ids[3], combi)
                if p == '5':
                    common = findCommon(sources[0], sources[1]) # Find common
                    corDer, d_pair = deriveCombi(
                        sources[0], sources[1], common, r_ids[0], r_ids[1], combi)
                    common = findCommon(d_pair, sources[2]) # Find common
                    corDer, d_pair = deriveCombi(
                        d_pair, sources[2], common, corDer, r_ids[2], combi)
                    common = findCommon(d_pair, sources[3]) # Find common
                    corDer, d_pair = deriveCombi(
                        d_pair, sources[3], common, corDer, r_ids[3], combi)
                    common = findCommon(d_pair, sources[4]) # Find common
                    corDer, d_pair = deriveCombi(
                        d_pair, sources[4],common,  corDer, r_ids[4], combi)
                corDerLab = relpremVoc[list(relations.keys())[corDer]]
    
                if n_opt == 1:
                    if corDer >= 0: # well-defined derivations
                   
                        # Regular 2-premise problem: Compile prompt from premise + query
                        p_premises = premises.copy()
                        if randomizePremises:  # randomize premise order
                            p_premises = np.random.permutation(p_premises)  
                        conc = createConclusion(d_pair, corDerLab)
                        prompt = "{} {}".format(" ".join(p_premises), conc)
                        rows.append({'id': t, 'Premises': p_premises,
                                     'Relations': rels, 'Prompt': prompt,
                                     'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                     'Derivation': derivation, 'Type': 'Regular'})
    
                        ## Transformation of function 
                        # -> func prompt reversed, requires reversed relation
                        # e.g., A is worth  €5, A is more than B, B is more than C, is C less than €5?
                        # corDer woould be A more than C, so need the reverse
                        # for mutual, use the original relation: A = 5, A more than B, is B less than 5? 
                        derRev = mutual[corDer]
                        derRevLab = list(relations.keys())[derRev]
                        
                        tofS = stim[-1] # function always queried for last stimulus in row
                        if testToF and rels[0] not in ['part of', 'contains']:
                            t += 1  # update trial index
                            p_premises = premises.copy()
                            p_premises.insert(0, fPremise)  # function premise first
                            if randomizePremises: # randomize premise order
                                p_premises = np.random.permutation(p_premises)  
                            conc = createTOFConclusion(tofS, derRevLab, func, cfuncprompts, funcs)
                            prompt = "{} {}".format(" ".join(p_premises), conc)
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                         'Derivation': derivation + ' ToF', 'Type': 'Regular'})
                            
                        if 'mutualCE' in var: # Mutually entailed of CE for 2<= premises
                            t += 1 # update trial index
                            p_premises = premises.copy()
                            if randomizePremises:  # randomize premise order
                                p_premises = np.random.permutation(p_premises) 
                            
                            d_revpair = [d_pair[1], d_pair[0]]
                            conc = createConclusion(d_revpair, derRevLab)
                            prompt = '{} {}'.format(" ".join(p_premises), conc)
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                         'Derivation': 'Mutual Combinatorial', 'Type': 'Regular'})
    
                        if 'Incorrect' in var:  # Incorrect query variant
                            t += 1  # update trial index
                            # Find incorrect relation examples
                            incorDerLab = findIncorrectRelation(relations, relpremVoc,corDerLab)
                            p_premises = premises.copy()
                            if randomizePremises:  # randomize premise order
                                p_premises = np.random.permutation(p_premises)  
                            conc = createConclusion(d_pair, incorDerLab)
                            prompt = '{} {}'.format(" ".join(p_premises), conc)
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                         'Derivation': derivation, 'Type': 'Incorrect'})
    
                            # Transformation of function
                            if testToF and rels[0] not in ['part of', 'contains']:
                                t += 1 # update trial index
                                # find mutually entailed relation of (incorrect) CE (cfunc prompt reversed)
                                incorDer = list(relations.keys()).index(str(incorDerLab))
                                incorDerRev = mutual[incorDer]
                                incorDerRevLab = list(relations.keys())[incorDerRev]
                                p_premises = premises.copy()
                                p_premises.insert(0, fPremise) 
                                if randomizePremises: # randomize premise order
                                    p_premises = np.random.permutation(premises.append(fPremise))
                                conc = createTOFConclusion(tofS, incorDerRevLab, func, cfuncprompts, funcs)
                                prompt = '{} {}'.format(" ".join(p_premises), conc)
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                             'Derivation': derivation + ' ToF', 'Type': 'Incorrect'})                            
                                
                            if 'mutualCE' in var: # Incorrect prompt - 2 premises
                                # incorrect mutual of combinatorially entailed relation
                                t += 1 # update trial id
                                incorDerRevLab = findIncorrectRelation(relations,relpremVoc,derRevLab)
                                p_premises = premises.copy()
                                if randomizePremises: # randomize premise order
                                    p_premises = np.random.permutation(p_premises)
                                conc = createConclusion(d_revpair, incorDerRevLab)
                                prompt = '{} {}'.format(" ".join(p_premises), conc)
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                             'Derivation': 'Mutual Combinatorial', 'Type': 'Incorrect'})
                            
                        # Analogy prompt: 2 premises, compare relations
                        if 'Analogy' in var:  # not in relations list, separate setting
                            t += 1 # update trial id
                            p_premises = premises.copy()
                            if randomizePremises: # randomize premise order
                                p_premises = np.random.permutation(p_premises) 
                            if rels[0] == rels[1]:
                                prompt = "{} Is {} to {} the same as {} to {}?".format(" ".join(p_premises),
                                                                                        stim[0], stim[1], stim[1], stim[2])
                            else: 
                                prompt = "{} Is {} to {} different from {} to {}?".format(" ".join(p_premises),
                                                                                        stim[0], stim[1], stim[1], stim[2])
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                         'Derivation': 'Analogy', 'Type': 'Regular'})
                            
                            if 'Incorrect' in var:  # Incorrect analogy prompt:
                                t += 1
                                p_premises = premises.copy()
                                if randomizePremises: # randomize premise order
                                    p_premises = np.random.permutation(p_premises)  
                                if rels[0] == rels[1]:
                                    prompt = "{} Is {} to {} different from {} to {}?".format(" ".join(p_premises),
                                                                                            stim[0], stim[1], stim[1], stim[2])
                                else: 
                                    prompt = "{} Is {} to {} the same as {} to {}?".format(" ".join(p_premises),                                                       stim[0], stim[1], stim[1], stim[2])
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                             'Derivation': 'Analogy', 'Type': 'Incorrect'})
                                
                        if 'Irrelevant' in var:
                            t += 1
                            irrRel, irrS = findIrrelevant(relations, sLabs, t_id) # Find irrelevant S to add premise
                            if t % 2 == 0: # Randomize order of relata in irrelevant premise
                                irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                            else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                            p_premises = premises.copy()
                            p_premises.append(irrPremise)
                            if randomizePremises: # randomize premise order
                                p_premises = np.random.permutation(p_premises)
                            conc = createConclusion(d_pair, corDerLab)
                            prompt = "{} {}".format(" ".join(p_premises), conc)
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                         'Derivation': derivation, 'Type': 'Irrelevant'})  # Store trial data
    
                            # Transformation of function
                            if testToF and rels[0] not in ['part of', 'contains']:
                                t += 1 # update trial index
                                p_premises = premises.copy()
                                p_premises.insert(0, fPremise)
                                p_premises = p_premises.append(irrPremise)
                                if randomizePremises:# randomize premise order 
                                    p_premises = np.random.permutation(p_premises)  
                                conc = createTOFConclusion(tofS, derRevLab, func, cfuncprompts, funcs)
                                prompt = "{} {}".format(" ".join(p_premises), conc)
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                             'Derivation': derivation + ' ToF', 'Type': 'Irrelevant'})
    
                            if 'mutualCE' in var: # Irrelevant premise - query Mutual of CE
                                t += 1 # update trial id
                                p_premises = premises.copy()
                                p_premises.append(irrPremise)
                                if randomizePremises:
                                    p_premises = np.random.permutation(p_premises)
                                conc = createConclusion(d_revpair, derRevLab)
                                prompt = "{} {}".format(" ".join(p_premises), conc)
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                             'Derivation': 'Mutual Combinatorial', 'Type': 'Irrelevant'})
    
                            if "Incorrect" in var:  # Incorrect irrlevant query variant
                                t += 1
                                # Find irrelevant S to add premise
                                irrRel, irrS = findIrrelevant(relations, sLabs, t_id)
                                p_premises = premises.copy()
                                p_premises.append(irrPremise)
                                if randomizePremises:
                                    p_premises = np.random.permutation(p_premises)
                                conc = createConclusion(d_pair, incorDerLab)
                                prompt = "{} {}".format(" ".join(p_premises), conc)
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                             'Derivation': derivation, 'Type': 'Irrelevant Incorrect'})
    
                                # Transformation of function (irrelevant incorrect)
                                if testToF and rels[0] not in ['part of', 'contains']:
                                    t += 1 # update trial index
                                    p_premises = premises.copy()
                                    p_premises.insert(0, fPremise)
                                    if randomizePremises: # randomize premise order
                                        p_premises = np.random.permutation(p_premises)
                                    conc = createTOFConclusion(d_pair, incorDerRevLab, func, cfuncprompts, funcs)
                                    prompt = "{} {}".format(" ".join(p_premises), conc)
                                    rows.append({'id': t, 'Premises': p_premises,
                                                 'Relations': rels, 'Prompt': prompt,
                                                 'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                                 'Derivation': derivation + ' ToF', 'Type': 'Irrelevant Incorrect'})
    
                                if 'mutualCE' in var: # Incorrect irrelevant - Mutual entailment of (incorrect) CE
                                    t += 1
                                    # find irrelevant stimulus and relation
                                    irrRel, irrS = findIrrelevant(relations, sLabs, t_id)
                                    p_premises = premises.copy()
                                    p_premises.append(irrPremise)
                                    if randomizePremises:
                                        p_premises = np.random.permutation(p_premises)
                                    conc = createConclusion(d_revpair, incorDerRevLab)
                                    prompt = "{} {}".format(" ".join(p_premises), conc)
                                    rows.append({'id': t, 'Premises': p_premises,
                                                 'Relations': rels, 'Prompt': prompt,
                                                 'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                                 'Derivation': 'Mutual Combinatorial', 'Type': 'Irrelevant Incorrect'})
    
                            # Analogy with irrelevant premise
                            if 'Analogy' in var:  # not in relations list, separate setting
                                t += 1 # update trial id
                                p_premises = premises.copy()
                                p_premises.append(irrPremise)
                                if randomizePremises:
                                    p_premises = np.random.permutation(p_premises)
                                if rels[0] == rels[1]:
                                    prompt = "{} Is {} to {} the same as {} to {}?".format(" ".join(p_premises),
                                                                                            stim[0], stim[1], stim[1], stim[2])
                                else: 
                                    prompt = "{} Is {} to {} different from {} to {}?".format(" ".join(p_premises),
                                                                                              stim[0], stim[1], stim[1], stim[2])
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': 'Yes', 'printCorrect': 'Yes', 'n_p': p,
                                             'Derivation': 'Analogy', 'Type': 'Irrelevant'})
    
                                if 'Incorrect' in var: # Irrelevant premise + Incorrect analogy prompt
                                    t += 1 # update trial id
                                    p_premises = premises.copy()
                                    p_premises.append(irrPremise)
                                    if randomizePremises: # randomize premise order
                                        p_premises = np.random.permutation(p_premises)                                    
                                    if rels[0] == rels[1]:
                                        prompt = "{} Is {} to {} different from {} to {}?".format(" ".join(p_premises),
                                                                                                stim[0], stim[1], stim[1], stim[2])
                                    else: 
                                        prompt = "{} Is {} to {} the same as {} to {}?".format(" ".join(p_premises),
                                                                                                  stim[0], stim[1], stim[1], stim[2])
                                    rows.append({'id': t, 'Premises': p_premises,
                                                 'Relations': rels, 'Prompt': prompt,
                                                 'Correct': 'No', 'printCorrect': 'No', 'n_p': p,
                                                 'Derivation': 'Analogy', 'Type': 'Irrelevant Incorrect'})
                    else: # can't derive relation with certainty for this combination
                        if includeIllDefined: # onnly include if specified by user
                            der_rel = np.random.choice(
                                rels, 1) #pick random relation to prompt
                            # only include 'regular' problem variant and irrelevant premise?
                            t += 1
                            corDerLab = relpremVoc[der_rel[0]]
                            
                            p_premises = premises.copy()
                            if randomizePremises:  # randomize premise order
                                p_premises = np.random.permutation(p_premises)  
                            conc = createConclusion(d_pair, corDerLab)
                            prompt = "{} {}".format(" ".join(p_premises), conc)
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': "I cannot know", 'printCorrect': "I cannot know", 'n_p': p,
                                         'Derivation': derivation, 'Type': 'Ill-defined'})
                            
                            if 'Irrelevant 'in var:  # add irrelevant premise
                                t += 1
                                irrRel, irrS = findIrrelevant(relations, sLabs, t_id) # Find irrelevant S to add premise
                                if t % 2 == 0: # Randomize order of relata in irrelevant premise
                                    irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                p_premises = premises.copy()
                                p_premises.append(irrPremise)
                                if randomizePremises: # randomize premise order
                                    p_premises = np.random.permutation(p_premises)
                                conc = createConclusion(d_pair, corDerLab)
                                prompt = "{} {}".format(" ".join(p_premises), conc)
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': "I cannot know", 'printCorrect': "I cannot know", 'n_p': p,
                                             'Derivation': derivation, 'Type': 'Ill-defined Irrelevant'}) 
                else: # multiple choice
                    if corDer >= 0:
                        # determine task instruction (select TRUE/FALSE)
                        
                        taskPremise = determine_taskPremise(selectTF)
                        # regular problem type
                        t +=1
                        p_premises = premises.copy()
                        if randomizePremises:  # randomize premise order
                            p_premises = np.random.permutation(p_premises)
                        conc, correct = createMCconclusion(n_opt, corDerLab, d_pair, 
                                                           rels, relations, relpremVoc,
                                                           derivation, mutual,
                                                           selectTF, illDefined = False)
                        correct, printCorrect = _convert_selecttf(correct, output, selectTF, taskPremise)
                        
                        prompt = "{} {} {}".format(" ".join(p_premises), 
                                                       taskPremise,
                                                       " ".join(conc))
                        rows.append({'id': t, 'Premises': p_premises,
                                     'Relations': rels, 'Prompt': prompt,
                                     'Correct': correct, 'printCorrect': printCorrect, 'n_p': p,
                                     'Derivation': derivation, 'Type': 'Regular'}) 
                        if 'Irrelevant' in var: # Irrelevant variant
                            t += 1
                            irrRel, irrS = findIrrelevant(relations, sLabs, t_id) # Find irrelevant S to add premise
                            if t % 2 == 0: # Randomize order of relata in irrelevant premise
                                irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                            else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                            p_premises = premises.copy()
                            p_premises.append(irrPremise)
                            if randomizePremises: # randomize premise order
                                p_premises = np.random.permutation(p_premises)
                            conc, correct = createMCconclusion(n_opt, corDerLab, d_pair, 
                                                               rels, relations, relpremVoc,
                                                               derivation, mutual,
                                                               selectTF, illDefined = False)  
                            taskPremise = determine_taskPremise(selectTF)
                            correct, printCorrect = _convert_selecttf(correct, output, selectTF, taskPremise)
                            
                            prompt = "{} {} {}".format(" ".join(p_premises), 
                                                           taskPremise,
                                                           " ".join(conc))
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': correct, 'printCorrect': printCorrect, 'n_p': p,
                                         'Derivation': derivation, 'Type': 'Irrelevant'}) 
                    else: # ill-defined problems
                        if includeIllDefined: # onnly include if specified by user
                        
                            der_rel = np.random.choice(rels, 1) # pick a random relation to prompt
                            # only include 'regular' problem variant and irrelevant premise (?)
                            t += 1
                            corDerLab = relpremVoc[der_rel[0]]
                            
                            p_premises = premises.copy()
                            if randomizePremises:  # randomize premise order
                                p_premises = np.random.permutation(p_premises)  
                            conc, correct = createMCconclusion(n_opt, corDerLab, d_pair, 
                                                               rels, relations, relpremVoc,
                                                               derivation, mutual,
                                                               selectTF, illDefined = True)  
                            taskPremise = determine_taskPremise(selectTF)
                            correct, printCorrect = _convert_selecttf(correct, output, selectTF, taskPremise)
                            prompt = "{} {} {}".format(" ".join(p_premises), 
                                                           taskPremise,
                                                           " ".join(conc))
                            rows.append({'id': t, 'Premises': p_premises,
                                         'Relations': rels, 'Prompt': prompt,
                                         'Correct': correct, 'printCorrect': printCorrect, 'n_p': p,
                                         'Derivation': derivation, 'Type': 'Ill-defined'})
                            
                            if 'Irrelevant 'in var:  # add irrelevant premise
                                t += 1
                                irrRel, irrS = findIrrelevant(relations, sLabs, t_id) # Find irrelevant S to add premise
                                if t % 2 == 0: # Randomize order of relata in irrelevant premise
                                    irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                p_premises = premises.copy()
                                p_premises.append(irrPremise)
                                if randomizePremises: # randomize premise order
                                    p_premises = np.random.permutation(p_premises)
                                conc, correct = createMCconclusion(n_opt, corDerLab, d_pair, 
                                                                   rels, relations,  relpremVoc,
                                                                   derivation, mutual,
                                                                   selectTF, illDefined = True)  
                                taskPremise = determine_taskPremise(selectTF)
                                correct, printCorrect = _convert_selecttf(correct, output, selectTF, taskPremise)
                                prompt = "{} {} {}".format(" ".join(p_premises), 
                                                               taskPremise,
                                                               " ".join(conc))
                                rows.append({'id': t, 'Premises': p_premises,
                                             'Relations': rels, 'Prompt': prompt,
                                             'Correct': correct, 'printCorrect': printCorrect, 'n_p': p,
                                             'Derivation': derivation, 'Type': 'Ill-defined Irrelevant'}) 
    trial_data = pd.DataFrame(rows) # create dataframe

    if printTrials:
        for t in range(len(trial_data['id'])):
            print("Trial {} ({} - {}): {} \nCorrect: {}".format(
                t+1, trial_data['Derivation'][t], trial_data['Type'][t],
                trial_data['Prompt'][t], trial_data['printCorrect'][t]))

    return trial_data


 # %% test function

# crelfuncs = dict({'Same as': ['has the same meaning as'],
#                   'Different from': ['has the same meaning as'],
#                   # 'opposite to': ['has the same meaning as'],
#                   # 'more t7han': ['is worth', 'means'],
#                   # 'less than': ['is worth', 'means'],
#                   # 'before': ['is at'],
#                   # 'after': ['is at']
#                       })

# cfuncprompts = dict({'Same as': ['have the same meaning as'],
#                   'Different from': ['have a different meaning than'],
#                   # 'opposite to': ['have the opposite meaning of'],
#                   # 'more than': ['worth more than', 'more than'],
#                   # 'less than': ['worth less than', 'less than'],
#                   # 'before': ['before', 'before'],
#                   # 'after': ['after', 'after']
#                       })

# funcs = dict({'Same as': ['cat', 'yes', 'water', 'mom', 'dog',
#                               'bear', 'no', 'fire', 'dad', 'cow'], 
#                   'Different from':['cat', 'yes', 'water', 'mom', 'dog',
#                                     'bear', 'no', 'fire', 'dad', 'cow'],
#                   # 'opposite to': ['cat', 'yes', 'water', 'mom', 'dog',
#                   #                 'bear', 'no', 'fire', 'dad', 'cow'],
#                   # 'more than': ['€5', 'four', '€1', 'ten', '$20',
#                   #               '€3', 'six', '£11', 'two', '$50'],
#                   # 'less than': ['€5', 'four', '€1', 'ten', '$20',
#                   #               '€3', 'six', '£11', 'two', '$50'],
#                   # 'before': ['5pm', '4pm', '3am', 'noon', '11am', 
#                   #            '9pm', 'midnight', '10am', '7am', 'sunrise'],
#                   # 'after': ['5pm', '4pm', '3am', 'noon', '11am', '9pm',
#                   #           '9pm', 'midnight', '10am', '7am', 'sunrise'],
#                   })

# premises_types = {
#                    '1': ['Incorrect', 'Irrelevant'],
#                    '2': ['Incorrect', 'Irrelevant'],
#                    # '3': [],
#                    # '4': ['Incorrect', 'Irrelevant'],
#                    # '5': ['Incorrect', 'Irrelevant']
#                    }
# relations = ['same', 'different']
# # functions = {'crelfuncs': crelfuncs, # for transformation of function
# #                   'cfuncprompts': cfuncprompts,
# #                   'funcs': funcs}
# relata = 'nonwords' # choose between nonwords, names, alfanumerics or custom?
# # sLabs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
# n_rep = 1
# protocol = 'Linear' # note that OTM and MTO only work for 2 premisew
# trial_data = generateSyllogism(relations, premises_types, n_rep, relata, protocol, n_opt = 3,
#                                printTrials = True, selectTF = False,
#                                includeIllDefined=True, output = 'LLMstudy')