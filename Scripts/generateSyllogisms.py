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
    - Relations to use in premises dict:
        - Keys: labels for relations that will be used in premises like 'A is *label* B'
                    e.g., 'the same as', 'different from', 'larger than', ...
        - values: numbers starting from 0, used as indices
    - n_type_premises: Number of premises and types of problem in a dict:
        - Keys: numbers 1 to 5 for different number of premises
        - Values: list with different options for problem, choose from:
            - 'irrelevant': add irrelevant premise to problem
            - 'addMutualCE': test reversal of combinatorially entailed relation
            - ...
    - sLabs: list of labels (non-words or other) for stimulus set
    - n_rep: number of repetitions of each trial (type)


######
TODO:
    - Check whether function works with other relations (it should?)
    - Add test for mutual of CE if requested
    - Rather than storing exact premises, store relations involved
        -> Could be interesting to assess differences 
        (seems mainly opposition is a problem)
    - Ultimately add clause to generate random nonwords if not provided?
    - This version is linear training, could allow user to define and specify 
        different training protocols (Linear, One-to-many, many-to-one)? 
        Many different options when there are more than 2 premises...
    - Add analogy: "Is rel1 the same as rel 2"
    - Add deictics? (also involves 'if I were you and you were me', ...; WHY?)
    ...
    - Add multiple functions?
        -> Would require no changes to derivation function, just some coding of
            the mappings of derived function transformations?
        -> What is the benefit? Not really transformation of function anyway?
            -> Could add separate test where a function is attached to the 
                relations, "is ... the same value as ...?"
                Only need to make sure labels are compatible across relations,
                or specify them?

@author: mraemaek

"""


import pdb


# def generateSyllogism(max_p, incorrect, irrelevant, sLabs, n_rep, relations = None):
def generateSyllogism(n_type_premises, n_rep, sLabs, printTrials, relations = None):
    
    # Dependencies
    import numpy as np
    from derivationTablesFromSourceRelations import derivationTablesFromSourceRelations
    from deriveRelationsFromBaseline import deriveRelationsFromBaseline
    
    if relations is None: # If no relations were specified
        relations = dict({'Same as': 0,
                     'Different from': 1,
                     'Opposite to': 2,
                     # 'More': 3,
                     # 'Less': 4,
                     # 'Contains': 5,
                     # 'Is part of': 6
                     })
        # Not sure how to choose the default? Generic same-diff-oppo or transitive inference?
        # Could add functionality to provide n_rel and select random number of relations?
        
    # Create transitivity tables for relations in task
    mutual, combi = derivationTablesFromSourceRelations(relations)
    
    # Initialize before looping trials
    trial_data = dict({'id': [], 'Premises': [], 'Relations': [], 'Prompt': [], 
                       'Correct': [], 'Type': [], 'n_p':[]})
    t =0
    rels = []
    stim = []
    for p in list(n_type_premises.keys()):
    # for p in range(max_p):
        # select the relation first 
        match p: 
# %% 1 relational premise reversal (vary correct/incorrect prompt; + irrelevant premise)
            case '1': 
                for r in range(len(list(relations.keys()))):
                    rel = list(relations.keys())[r]
                    for rep in range(n_rep):
                        t +=1                        
                        if len(relations.keys()) == 1 or n_rep == 1: # new Ss every relation
                            t_id = 2*rep + 2*r # 2 stimuli per problem
                        else: # new stimuli each repetition
                            t_id = 2*rep # 2 S's per problem
                        # Adapt index to avoidindexing errors
                        if t_id+3 >= len(sLabs): # If more S's needed than labeled in list, loop through list
                            loop = int(np.round(t_id/len(sLabs)))
                            t_id -= loop*len(sLabs) # cycle back through list
                        stim = [sLabs[t_id], sLabs[t_id+1]]
                            
                        premise = "{} is {} {}.".format(stim[0], rel, stim[1])
                        corMut = mutual[r] # Find mutual relation
                        corMutLab = list(relations.keys())[corMut] # label
                        
                        # Compile prompt from premise + reversal query 
                        prompt = "{} Is {} {} {}?". format(premise, stim[1], corMutLab, stim[0])
                        trial_data['id'].append(t) # Store data
                        trial_data['Premises'].append(premise)
                        trial_data['Relations'].append([rel])
                        trial_data['Prompt'].append(prompt)
                        trial_data['Correct'].append('Yes') # note: Always correct if specified like this
                        trial_data['Type'].append('Regular')
                        trial_data['n_p'].append('1')
                        # Incorrect query variant
                        t += 1
                        # Find incorrect relation examples
                        notRels = []
                        if len(relations.keys()) == 1:
                            allRels = ['the same as', 'different from', 'opposite to', 
                                       'more than', 'less than', 
                                       # 'part of', 'contains', 'before', 'after'
                                       ]
                        else:
                            allRels = list(relations.keys())
                        for ir in range(len(allRels)):
                            if corMutLab == 'different from':
                                if not allRels[ir] in ['opposite to', 'different from']:
                                    notRels.append(allRels[ir])
                            elif corMutLab == 'opposite to':
                                if not list(allRels)[ir] in ['opposite to', 'different from']:
                                    notRels.append(allRels[ir])
                            else:
                                if not allRels[ir] == corMutLab:
                                    notRels.append(allRels[ir])
                        incorMutLab = np.random.choice(notRels)
                        # Build prompt
                        prompt = "{} Is {} {} {}?".format(premise, stim[1], incorMutLab, stim[0])
                        trial_data['id'].append(t) # Store data
                        trial_data['Premises'].append(premise)
                        trial_data['Relations'].append([rel])
                        trial_data['Prompt'].append(prompt)
                        trial_data['Correct'].append('No')
                        trial_data['Type'].append('Incorrect')
                        trial_data['n_p'].append('1')
                        if 'irrelevant' in n_type_premises['1']:
                            t += 1
                            # Find irrelevant S to add premise
                            half = len(sLabs)/2
                            if t_id < half:
                                irr_id = np.random.randint(half+1, len(sLabs))
                            else:
                                irr_id = np.random.randint(0,half-1)
                            irrRel = np.random.choice(list(relations.keys()))
                            irrS = sLabs[irr_id]
                            # Randomize order of relata in irrelevant premise
                            if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                            else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                            prompt = "{} {} Is {} {} {}?".format(premise, irrPremise,
                                                                 stim[1], corMutLab, stim[0])
                                
                            premise = premise + ' ' + irrPremise
                            trial_data['id'].append(t)
                            trial_data['Premises'].append(premise)
                            trial_data['Relations'].append([rel])
                            trial_data['Prompt'].append(prompt)
                            trial_data['Correct'].append('Yes')
                            trial_data['Type'].append('Irrelevant')
                            trial_data['n_p'].append('1')
                            # Incorrect query variant
                            t += 1
                            # Find irrelevant S to add premise
                            half = len(sLabs)/2
                            if t_id < half: # to avoid indexing issues
                                irr_id = np.random.randint(half+1, len(sLabs))
                            else:
                                irr_id = np.random.randint(0,half-1)
                            irrRel = np.random.choice(list(relations.keys())) # select random releation
                            irrS = sLabs[irr_id]
                            # Randomize order of relata in irrelevant premise
                            if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                            else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                            prompt = "{} {} Is {} {} {}?".format(premise, irrPremise,
                                                                 stim[1], incorMutLab, stim[0])
                            trial_data['id'].append(t) # Store data
                            trial_data['Premises'].append(premise)
                            trial_data['Relations'].append([rel])
                            trial_data['Prompt'].append(prompt)
                            trial_data['Correct'].append('No')
                            trial_data['Type'].append('Irrelevant')
                            trial_data['n_p'].append('1')
# %% 2-premise syllogism, test transitive inference (+irrelevant)
            case '2':
                premises = [] 
                for r1 in range(len(list(relations.keys()))):
                    for r2 in range(len(list(relations.keys()))):
                        rels = [list(relations.keys())[r1], list(relations.keys())[r2]]
                        for rep in range(n_rep):
                            t += 1
                            if len(relations.keys()) == 1 or n_rep == 1: # new Ss every relation
                                t_id = 3*rep + 3*r1 +3*r2 # 3 Stimuli per problem
                            else: # new stimuli each repetition
                                t_id = 3*rep # 3 S's per problem
                            # Adapt index to avoidindexing errors
                            if t_id+2 >= len(sLabs): # If more S's needed than labeled in list, loop through list
                                loop = int(np.round(t_id/len(sLabs)))
                                t_id -= loop*len(sLabs) # cycle back through list
                            # Get stimuli in list
                            stim = [sLabs[t_id], sLabs[t_id+1], sLabs[t_id+2]]
                            
                            # Build premises using stimuli (linear)
                            premise1 = "{} is {} {}.".format(stim[0], rels[0], stim[1])
                            source1 = [stim[0], stim[1]]
                            premise2 = "{} is {} {}.".format(stim[1], rels[1], stim[2])
                            source2 = [stim[1], stim[2]]
                            premises = [premise1, premise2]
                            # Get derived relations from tables
                            corMut1 = mutual[r1] # Find mutual relation
                            corMut2 = mutual[r2]
                            # Note that testing the mutual relations in this context 
                            # is equivalent to the 1-premise reversal + irrelevant case
                            # Find common
                            for sr1 in range(len(source1)):
                                for sr2 in range(len(source1)):
                                    if source1[sr1] == source2[sr2]:
                                        common = source2[sr2]
                            if list.index(source1, common) == 0:
                                if list.index(source2, common) == 0: # A-B & A - C (OTM)
                                    corCombi = combi['OTM'][r1, r2]
                                    source12 = [stim[1], stim[2]]

                                else: # A - B & C - A (sort of MTO)
                                    corCombi = combi['sMTO'][r1, r2]
                                    source12 = [stim[1], stim[2]]
                            else:
                                if list.index(source2, common) == 0: # A-B & B - C (linear)
                                    # pdb.set_trace()
                                    corCombi = combi['Linear'][r1, r2]
                                    source12 = [stim[0], stim[2]]
                                else: # A-B & C- B (MTO)
                                    corCombi = combi['MTO'][r1, r2]
                                    source12 = [stim[0], stim[2]]
                                        
                            corMut1Lab = list(relations.keys())[corMut1] # labels
                            corMut2Lab = list(relations.keys())[corMut2]
                            corCombiLab = list(relations.keys())[corCombi] 
                            if corCombi >= 0: # Only include well-defined derivations
                                # Compile prompt from premise + query
                                prompt = "{} {} Is {} {} {}?". format(premise1, 
                                                                   premise2, 
                                                                   stim[2], corCombiLab, stim[0])
                                trial_data['id'].append(t)
                                trial_data['Premises'].append(premises)
                                trial_data['Relations'].append(rels)
                                trial_data['Prompt'].append(prompt)
                                trial_data['Correct'].append('Yes') # Always correct if specified like this
                                trial_data['Type'].append('Regular')
                                trial_data['n_p'].append('2')
                                
                                ## ADD REVERSE PROMPT FOR  2<= premises
                                # Mutually entailed of CE
                                
                                # Incorrect query variant
                                t += 1
                                # Find incorrect relation examples
                                notRels = []
                                if len(relations.keys()) == 1:
                                    allRels = ['the same as', 'different from', 'opposite to', 
                                               'more than', 'less than', 
                                               # 'part of', 'contains', 'before', 'after'
                                               ]
                                else:
                                    allRels = list(relations.keys())
                                for ir in range(len(allRels)):
                                    if corMutLab == 'different from':
                                        if not allRels[ir] in ['opposite to', 'different from']:
                                            notRels.append(allRels[ir])
                                    elif corMutLab == 'opposite to':
                                        if not list(allRels)[ir] in ['opposite to', 'different from']:
                                            notRels.append(allRels[ir])
                                    else:
                                        if not allRels[ir] == corMutLab:
                                            notRels.append(allRels[ir])
                                incorCombiLab = np.random.choice(notRels)
                                
                                prompt = "{} {} Is {} {} {}?".format(premise1,
                                                                  premise2,
                                                                  stim[2], incorCombiLab, stim[0])
                                    
                                trial_data['id'].append(t)
                                trial_data['Premises'].append(premises)
                                trial_data['Relations'].append(rels)
                                trial_data['Prompt'].append(prompt)
                                trial_data['Correct'].append('No')
                                trial_data['Type'].append('Incorrect')
                                trial_data['n_p'].append('2')
                                if 'irrelevant' in n_type_premises['2']:
                                    t += 1
                                    # Find irrelevant S to add premise
                                    half = len(sLabs)/2
                                    if t_id < half:
                                        irr_id = np.random.randint(half+1, len(sLabs))
                                    else:
                                        irr_id = np.random.randint(0,half-1)
                                    irrRel = np.random.choice(list(relations.keys()))
                                    irrS = sLabs[irr_id]
                                    # Randomize order of relata in irrelevant premise
                                    if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                    else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                    prompt = "{} {} {} Is {} {} {}?".format(premise1, premise2, irrPremise,
                                                                      stim[2], corCombiLab, stim[0])
                                    # Store trial data
                                    premises.append(irrPremise)
                                    trial_data['id'].append(t) 
                                    trial_data['Premises'].append(premises)
                                    trial_data['Relations'].append([rels])
                                    trial_data['Prompt'].append(prompt)
                                    trial_data['Correct'].append('Yes')
                                    trial_data['Type'].append('Irrelevant')
                                    trial_data['n_p'].append('2')
                                    
                                    # Incorrect query variant
                                    t += 1
                                    # Find irrelevant S to add premise
                                    half = len(sLabs)/2
                                    if t_id < half: # to avoid indexing issues
                                        irr_id = np.random.randint(half+1, len(sLabs))
                                    else:
                                        irr_id = np.random.randint(0,half-1)
                                    irrRel = np.random.choice(list(relations.keys())) # select random releation
                                    irrS = sLabs[irr_id]
                                    # Randomize order of relata in irrelevant premise
                                    if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                    else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                    prompt = "{} {} {} Is {} {} {}?".format(premise1,premise2, irrPremise, 
                                                                      stim[2], incorCombiLab, stim[0])
                                    trial_data['id'].append(t) # Store data
                                    trial_data['Premises'].append(premises)
                                    trial_data['Relations'].append([rels])
                                    trial_data['Prompt'].append(prompt)
                                    trial_data['Correct'].append('No')
                                    trial_data['Type'].append('Irrelevant')
                                    trial_data['n_p'].append('2')
# %% 4-term reasoning in three premises (+irrelevant)                
            case '3': 
                premises = [] 
                for r1 in range(len(list(relations.keys()))):
                    for r2 in range(len(list(relations.keys()))):
                        for r3 in range(len(list(relations.keys()))):
                            rels = [list(relations.keys())[r1], 
                                    list(relations.keys())[r2],
                                    list(relations.keys())[r3]]
                            for rep in range(n_rep):
                                t +=1                                
                                if len(relations.keys()) == 1 or n_rep == 1: # new Ss every relation
                                    t_id = 4*rep + 4*r1 +4*r2+4*r3 # 4 stimuli per problem
                                else: # new stimuli each repetition
                                    t_id = 4*rep # 4 S's per problem
                                # Adapt index to avoidindexing errors
                                if t_id+3 >= len(sLabs): # If more S's needed than labeled in list, loop through list
                                    loop = int(np.round(t_id/len(sLabs)))
                                    t_id -= loop*len(sLabs) # cycle back through list
                                stim = [sLabs[t_id], sLabs[t_id+1], sLabs[t_id+2], sLabs[t_id+3]]
                                premise1 = "{} is {} {}.".format(stim[0], rels[0], stim[1])
                                source1 = [stim[0], stim[1]]
                                premise2 = "{} is {} {}.".format(stim[1], rels[1], stim[2])
                                source2 = [stim[1], stim[2]]
                                premise3 = "{} is {} {}.".format(stim[2], rels[2], stim[3])
                                source3 = [stim[2], stim[3]]
                                premises = [premise1, premise2, premise3]
                                ##########
                                # Here is where the more intricate part starts  
                                # stepwise derivation works (be it somewhat cumbersome)
                                
                                # Derivation
                                # Find common element in first two premises (if any)
                                for sr1 in range(len(source1)):
                                    for sr2 in range(len(source1)):
                                        if source1[sr1] == source2[sr2]:
                                            common = source2[sr2]
                                # Determine training schedule and derive
                                if list.index(source1, common) == 0:
                                    if list.index(source2, common) == 0: # A-B & A - C (OTM)
                                        combi12 = combi['OTM'][r1, r2]
                                        source12 = [stim[1], stim[2]]
                                    else: # A - B & C - A (sort of MTO)
                                        combi12 = combi['sMTO'][r1, r2]
                                        source12 = [stim[1], stim[2]]
                                else:
                                    if list.index(source2, common) == 0: # A-B & B - C (linear)
                                        # pdb.set_trace()
                                        combi12 = combi['Linear'][r1, r2]
                                        source12 = [stim[0], stim[2]]
                                    else: # A-B & C- B (MTO)
                                        combi12 = combi['MTO'][r1, r2]
                                        source12 = [stim[0], stim[2]]                            
                                # Then find common element between derived relation and third premise
                                if combi12 >= 0: # can only derive from well-defined relation
                                    for sr1 in range(len(source12)):
                                        for sr2 in range(len(source3)):
                                            if source12[sr1] == source3[sr2]:
                                                common = source3[sr2]
                                    if list.index(source12, common) == 0:
                                        if list.index(source3, common) == 0: # A-B & A - C (OTM)
                                            combi123 = combi['OTM'][combi12, r3]
                                            der3 = [source12[0], source3[1]]
                                        else: # A - B & C - A (sort of MTO)
                                            combi123 = combi['sMTO'][combi12, r3]
                                            der3 = [source12[1], source3[0]]
                                    else:
                                        if list.index(source3, common) == 0: # A-B & B - C (linear)
                                            combi123 = combi['Linear'][combi12, r3]
                                            der3 = [source12[0], source3[1]]
                                        else: # A-B & C- B (MTO)
                                            combi123 = combi['MTO'][combi12, r3]
                                            der3 = [source12[0], source3[0]]  
                                else: 
                                     combi123 = -1 # Deri ation from ill-defined relation will be ill-defined
                                if combi123 >= 0: # Only include defined relations
                                    t+=1    
                                    corMut1 = mutual[r1] # Find mutual relation
                                    corMut1Lab = list(relations.keys())[corMut1] # label
                                    corMut2 = mutual[r2] # Find mutual relation
                                    corMut2Lab = list(relations.keys())[corMut2] # label
                                    corMut3 = mutual[r1] # Find mutual relation
                                    corMut3Lab = list(relations.keys())[corMut3] # label
                                    corCombiLab = list(relations.keys())[combi123] 
                                    # Compile prompt from premise + query
                                    prompt = "{} {} {} Is {} {} {}?". format(premise1, 
                                                                       premise2,
                                                                       premise3,
                                                                       der3[0], corCombiLab, der3[1])
                                    trial_data['id'].append(t)
                                    trial_data['Premises'].append(premises)
                                    trial_data['Relations'].append(rels)
                                    trial_data['Prompt'].append(prompt)
                                    trial_data['Correct'].append('Yes') # Always correct if specified like this
                                    trial_data['Type'].append('Regular')
                                    trial_data['n_p'].append('3')
                                    
                                    ## ADD REVERSE PROMPT FOR  2<= premises
                                    
                                    # Incorrect query variant
                                    t += 1
                                    # Find incorrect relation examples
                                    notRels = []
                                    if len(relations.keys()) == 1:
                                        allRels = ['the same as', 'different from', 'opposite to', 
                                                   'more than', 'less than', 
                                                   # 'part of', 'contains', 'before', 'after'
                                                   ]
                                    else:
                                        allRels = list(relations.keys())
                                    for ir in range(len(allRels)):
                                        if corMutLab == 'different from':
                                            if not allRels[ir] in ['opposite to', 'different from']:
                                                notRels.append(allRels[ir])
                                        elif corMutLab == 'opposite to':
                                            if not list(allRels)[ir] in ['opposite to', 'different from']:
                                                notRels.append(allRels[ir])
                                        else:
                                            if not allRels[ir] == corMutLab:
                                                notRels.append(allRels[ir])
                                    incorCombiLab = np.random.choice(notRels)
                                    
                                    prompt = "{} {} {} Is {} {} {}?".format(premise1,
                                                                      premise2,
                                                                      premise3,
                                                                      der3[0], incorCombiLab, der3[1])
                                    trial_data['id'].append(t)
                                    trial_data['Relations'].append(rels)
                                    trial_data['Prompt'].append(prompt)
                                    trial_data['Correct'].append('No')
                                    trial_data['Type'].append('Incorrect')
                                    trial_data['n_p'].append('3')
                                    if 'irrelevant' in n_type_premises['3']:
                                        t += 1
                                        # Find irrelevant S to add premise
                                        half = len(sLabs)/2
                                        if t_id < half:
                                            irr_id = np.random.randint(half+1, len(sLabs))
                                        else:
                                            irr_id = np.random.randint(0,half-1)
                                        irrRel = np.random.choice(list(relations.keys()))
                                        irrS = sLabs[irr_id]
                                        # Randomize order of relata in irrelevant premise
                                        if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                        else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                        prompt = "{} {} {} {} Is {} {} {}?".format(premise1,
                                                                          premise2,
                                                                          premise3,
                                                                          irrPremise,
                                                                          der3[0], corCombiLab, der3[1])
                                        # Store trial data
                                        premises.append(irrPremise)
                                        trial_data['id'].append(t) 
                                        trial_data['Premises'].append(premises)
                                        trial_data['Relations'].append([rels])
                                        trial_data['Prompt'].append(prompt)
                                        trial_data['Correct'].append('Yes')
                                        trial_data['Type'].append('Irrelevant')
                                        trial_data['n_p'].append('3')
                                        
                                        # incorrect query variant
                                        t += 1
                                        # Find irrelevant S to add premise
                                        half = len(sLabs)/2
                                        if t_id < half: # to avoid indexing issues
                                            irr_id = np.random.randint(half+1, len(sLabs))
                                        else:
                                            irr_id = np.random.randint(0,half-1)
                                        irrRel = np.random.choice(list(relations.keys())) # select random releation
                                        irrS = sLabs[irr_id]
                                        # Randomize order of relata in irrelevant premise
                                        if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                        else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                        prompt = "{} {} {} {} Is {} {} {}?".format(premise1,
                                                                          premise2,
                                                                          premise3,
                                                                          irrPremise,
                                                                          der3[0], incorCombiLab, der3[1])
                                        trial_data['id'].append(t) # Store data
                                        trial_data['Premises'].append(premises)
                                        trial_data['Relations'].append([rels])
                                        trial_data['Prompt'].append(prompt)
                                        trial_data['Correct'].append('No')
                                        trial_data['Type'].append('Irrelevant')
                                        trial_data['n_p'].append('3')
# %% Five-term reasoning - four presmises (+ irrelevant)    
            case '4':
                premises = [] 
                for r1 in range(len(list(relations.keys()))):
                    for r2 in range(len(list(relations.keys()))):
                        for r3 in range(len(list(relations.keys()))):
                            for r4 in range(len(list(relations.keys()))):
                                rels = [list(relations.keys())[r1], 
                                        list(relations.keys())[r2],
                                        list(relations.keys())[r3],
                                        list(relations.keys())[r4]]
                                for rep in range(n_rep):
                                    t +=1
                                    if len(relations.keys()) == 1 or n_rep == 1: # new Ss every relation
                                        t_id = 5*rep + 5*r1 +5*r2+5*r3+5*r4 # 5 stimuli per problem
                                    else: # new stimuli each repetition
                                        t_id = 5*rep # 5 S's per problem
                                    # Adapt index to avoidindexing errors
                                    if t_id+4 >= len(sLabs): # If more S's needed than labeled in list, loop through list
                                        loop = int(np.round(t_id/len(sLabs)))
                                        t_id -= loop*len(sLabs) # cycle back through list
                                    # Get stimuli
                                    stim = [sLabs[t_id], sLabs[t_id+1], sLabs[t_id+2],
                                            sLabs[t_id+3], sLabs[t_id+4]]
                                    # Build premises
                                    premise1 = "{} is {} {}.".format(stim[0], rels[0], stim[1])
                                    source1 = [stim[0], stim[1]]
                                    premise2 = "{} is {} {}.".format(stim[1], rels[1], stim[2])
                                    source2 = [stim[1], stim[2]]
                                    premise3 = "{} is {} {}.".format(stim[2], rels[2], stim[3])
                                    source3 = [stim[2], stim[3]]
                                    premise4 = "{} is {} {}.".format(stim[3], rels[3], stim[4])
                                    source4 = [stim[3], stim[4]]
                                    premises = [premise1, premise2, premise3, premise4]

                                    # Derivation using custom algorithm
                                    # Find common element in first two premises (if any)
                                    for sr1 in range(len(source1)):
                                        for sr2 in range(len(source1)):
                                            if source1[sr1] == source2[sr2]:
                                                common = source2[sr2]
                                    if list.index(source1, common) == 0:
                                        if list.index(source2, common) == 0: # A-B & A - C (OTM)
                                            combi12 = combi['OTM'][r1, r2]
                                            source12 = [stim[1], stim[2]]
                                        else: # A - B & C - A (sort of MTO)
                                            combi12 = combi['sMTO'][r1, r2]
                                            source12 = [stim[1], stim[2]]
                                    else:
                                        if list.index(source2, common) == 0: # A-B & B - C (linear)
                                            # pdb.set_trace()
                                            combi12 = combi['Linear'][r1, r2]
                                            source12 = [stim[0], stim[2]]
                                        else: # A-B & C- B (MTO)
                                            combi12 = combi['MTO'][r1, r2]
                                            source12 = [stim[0], stim[2]]                            
                                    # Then find common element between derived relation and third premise
                                    if combi12 >= 0:
                                        for sr1 in range(len(source12)):
                                            for sr2 in range(len(source3)):
                                                if source12[sr1] == source3[sr2]:
                                                    common = source3[sr2]
                                        if list.index(source12, common) == 0:
                                            if list.index(source3, common) == 0: # A-B & A - C (OTM)
                                                combi123 = combi['OTM'][combi12, r3]
                                                der3 = [source12[0], source3[1]]
                                            else: # A - B & C - A (sort of MTO)
                                                combi123 = combi['sMTO'][combi12, r3]
                                                der3 = [source12[1], source3[0]]
                                        else:
                                            if list.index(source3, common) == 0: # A-B & B - C (linear)
                                                combi123 = combi['Linear'][combi12, r3]
                                                der3 = [source12[0], source3[1]]
                                            else: # A-B & C- B (MTO)
                                                combi123 = combi['MTO'][combi12, r3]
                                                der3 = [source12[0], source3[0]]  
                                    # And again for the third
                                    if combi123 >= 0: # Only derive from properly defined relations
                                        for sr1 in range(len(der3)):
                                            for sr2 in range(len(source4)):
                                                if der3[sr1] == source4[sr2]:
                                                    common = source4[sr2]
                                        if list.index(der3, common) == 0:
                                            if list.index(source4, common) == 0: # A-B & A - C (OTM)
                                                combi1234 = combi['OTM'][combi123, r4]
                                                der4 = [der3[0], source4[1]]
                                            else: # A - B & C - A (sort of MTO)
                                                combi1234 = combi['sMTO'][combi123, r4]
                                                der4 = [der3[1], source4[0]]
                                        else:
                                            if list.index(source3, common) == 0: # A-B & B - C (linear)
                                                combi1234 = combi['Linear'][combi123, r4]
                                                der4 = [der3[0], source4[1]]
                                            else: # A-B & C- B (MTO)
                                                combi1234 = combi['MTO'][combi123, r4]
                                                der4 = [der3[0], source4[0]]  
                                    else: 
                                         combi1234 = -1 # Derivation from ill-defined relation is ill-defined
                                    # Get derived relations and labels from function lists
                                    corMut1 = mutual[r1] # Find mutual relation
                                    corMut1Lab = list(relations.keys())[corMut1] # label
                                    corMut2 = mutual[r2] # Find mutual relation
                                    corMut2Lab = list(relations.keys())[corMut2] # label
                                    corMut3 = mutual[r3] # Find mutual relation
                                    corMut3Lab = list(relations.keys())[corMut3] # label
                                    corMut4 = mutual[r4] # Find mutual relation
                                    corMut4Lab = list(relations.keys())[corMut4] # label
                                    corCombiLab = list(relations.keys())[combi1234] 
                                    if combi1234 >= 0: # Only include defined relations
                                        # Compile prompt from premise + query
                                        prompt = "{} {} {} {} Is {} {} {}?". format(premise1, 
                                                                           premise2,
                                                                           premise3,
                                                                           premise4, 
                                                                           der4[0], corCombiLab, der4[1])
                                        trial_data['id'].append(t)
                                        trial_data['Premises'].append(premises)
                                        trial_data['Relations'].append(rels)
                                        trial_data['Prompt'].append(prompt)
                                        trial_data['Correct'].append('Yes') # Always correct if specified like this
                                        trial_data['Type'].append('Regular')
                                        trial_data['n_p'].append('4')
                                        
                                        ## ADD REVERSE PROMPT FOR  2<= premises
                                        
                                        # Incorrect query variant
                                        t += 1
                                        # Find incorrect relation examples
                                        notRels = []
                                        if len(relations.keys()) == 1:
                                            allRels = ['the same as', 'different from', 'opposite to', 
                                                       'more than', 'less than', 
                                                       # 'part of', 'contains', 'before', 'after'
                                                       ]
                                        else:
                                            allRels = list(relations.keys())
                                        for ir in range(len(allRels)):
                                            if corMutLab == 'different from':
                                                if not allRels[ir] in ['opposite to', 'different from']:
                                                    notRels.append(allRels[ir])
                                            elif corMutLab == 'opposite to':
                                                if not list(allRels)[ir] in ['opposite to', 'different from']:
                                                    notRels.append(allRels[ir])
                                            else:
                                                if not allRels[ir] == corMutLab:
                                                    notRels.append(allRels[ir])
                                        incorCombiLab = np.random.choice(notRels)
                                        # Build prompt
                                        prompt = "{} {} {} {} Is {} {} {}?". format(premise1, 
                                                                           premise2,
                                                                           premise3,
                                                                           premise4, 
                                                                           der4[0], incorCombiLab, der4[1])
                                        # Store trial data
                                        trial_data['id'].append(t) 
                                        trial_data['Relations'].append(rels)
                                        trial_data['Prompt'].append(prompt)
                                        trial_data['Correct'].append('No')
                                        trial_data['Type'].append('Incorrect')
                                        trial_data['n_p'].append('4')
                                        if 'irrelevant' in n_type_premises['4']:
                                            t += 1
                                            # Find irrelevant S to add premise
                                            half = len(sLabs)/2
                                            if t_id < half: irr_id = np.random.randint(half+1, len(sLabs))
                                            else: irr_id = np.random.randint(0,half-1)
                                            irrRel = np.random.choice(list(relations.keys())) # randomly select relation
                                            irrS = sLabs[irr_id] # label
                                            # Randomize order of relata in irrelevant premise
                                            if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                            else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                            prompt = "{} {} {} {} {} Is {} {} {}?".format(premise1,
                                                                              premise2,
                                                                              premise3,
                                                                              premise4,
                                                                              irrPremise,
                                                                              der4[0], corCombiLab, der4[1])
                                            # Store trial data
                                            premises.append(irrPremise)
                                            trial_data['id'].append(t) 
                                            trial_data['Premises'].append(premises)
                                            trial_data['Relations'].append([rels])
                                            trial_data['Prompt'].append(prompt)
                                            trial_data['Correct'].append('Yes')
                                            trial_data['Type'].append('Irrelevant')
                                            trial_data['n_p'].append('4')
                                            
                                            # Incorrect query version
                                            t += 1
                                            # Find irrelevant S to add premise
                                            half = len(sLabs)/2
                                            if t_id < half: # to avoid indexing issues
                                                irr_id = np.random.randint(half+1, len(sLabs))
                                            else:
                                                irr_id = np.random.randint(0,half-1)
                                            irrRel = np.random.choice(list(relations.keys())) # select random releation
                                            irrS = sLabs[irr_id]
                                            # Randomize order of relata in irrelevant premise
                                            if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                            else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                            prompt = "{} {} {} {} {} Is {} {} {}?".format(premise1,
                                                                              premise2,
                                                                              premise3,
                                                                              premise4,
                                                                              irrPremise,
                                                                              der4[0], incorCombiLab, der4[1])
                                            trial_data['id'].append(t) # Store data
                                            trial_data['Premises'].append(premises)
                                            trial_data['Relations'].append([rels])
                                            trial_data['Prompt'].append(prompt)
                                            trial_data['Correct'].append('No')
                                            trial_data['Type'].append('Irrelevant')
                                            trial_data['n_p'].append('4')
# %% 6-term reasoning - five premises (+irrelevant)
            case '5':
                premises = [] 
                for r1 in range(len(list(relations.keys()))):
                    for r2 in range(len(list(relations.keys()))):
                        for r3 in range(len(list(relations.keys()))):
                            for r4 in range(len(list(relations.keys()))):
                                for r5 in range(len(list(relations.keys()))):
                                    rels = [list(relations.keys())[r1], 
                                            list(relations.keys())[r2],
                                            list(relations.keys())[r3],
                                            list(relations.keys())[r4],
                                            list(relations.keys())[r5]]
                                    for rep in range(n_rep):
                                        t +=1
                                        if len(relations.keys()) == 1 or n_rep == 1: # new Ss every relation
                                            t_id = 6*rep + 6*r1 +6*r2+6*r3+6*r4 +6*r5 # 5 stimuli per problem
                                        else: # new stimuli each repetition
                                            t_id = 6*rep # 6 S's per problem
                                        # Adapt index to avoidindexing errors
                                        if t_id+5 >= len(sLabs): # If more S's needed than labeled in list, loop through list
                                            loop = int(np.round(t_id/len(sLabs)))
                                            t_id -= loop*len(sLabs) # cycle back through list
                                        # Get stimuli
                                        stim = [sLabs[t_id], sLabs[t_id+1], sLabs[t_id+2],
                                                sLabs[t_id+3], sLabs[t_id+4], sLabs[t_id+5]]
                                        # Build premises
                                        premise1 = "{} is {} {}.".format(stim[0], rels[0], stim[1])
                                        source1 = [stim[0], stim[1]]
                                        premise2 = "{} is {} {}.".format(stim[1], rels[1], stim[2])
                                        source2 = [stim[1], stim[2]]
                                        premise3 = "{} is {} {}.".format(stim[2], rels[2], stim[3])
                                        source3 = [stim[2], stim[3]]
                                        premise4 = "{} is {} {}.".format(stim[3], rels[3], stim[4])
                                        source4 = [stim[3], stim[4]]
                                        premise5 = "{} is {} {}.".format(stim[4], rels[3], stim[5])
                                        source5 = [stim[4], stim[5]]
                                        premises = [premise1, premise2, premise3, premise4, premise5]
    
                                        # Derivation using custom algorithm
                                        # Find common element in first two premises (if any)
                                        for sr1 in range(len(source1)):
                                            for sr2 in range(len(source1)):
                                                if source1[sr1] == source2[sr2]:
                                                    common = source2[sr2]
                                        if list.index(source1, common) == 0:
                                            if list.index(source2, common) == 0: # A-B & A - C (OTM)
                                                combi12 = combi['OTM'][r1, r2]
                                                source12 = [stim[1], stim[2]]
                                            else: # A - B & C - A (sort of MTO)
                                                combi12 = combi['sMTO'][r1, r2]
                                                source12 = [stim[1], stim[2]]
                                        else:
                                            if list.index(source2, common) == 0: # A-B & B - C (linear)
                                                # pdb.set_trace()
                                                combi12 = combi['Linear'][r1, r2]
                                                source12 = [stim[0], stim[2]]
                                            else: # A-B & C- B (MTO)
                                                combi12 = combi['MTO'][r1, r2]
                                                source12 = [stim[0], stim[2]]                            
                                        # Then find common element between derived relation and third premise
                                        if combi12 >= 0:
                                            for sr1 in range(len(source12)):
                                                for sr2 in range(len(source3)):
                                                    if source12[sr1] == source3[sr2]:
                                                        common = source3[sr2]
                                            if list.index(source12, common) == 0:
                                                if list.index(source3, common) == 0: # A-B & A - C (OTM)
                                                    combi123 = combi['OTM'][combi12, r3]
                                                    der3 = [source12[0], source3[1]]
                                                else: # A - B & C - A (sort of MTO)
                                                    combi123 = combi['sMTO'][combi12, r3]
                                                    der3 = [source12[1], source3[0]]
                                            else:
                                                if list.index(source3, common) == 0: # A-B & B - C (linear)
                                                    combi123 = combi['Linear'][combi12, r3]
                                                    der3 = [source12[0], source3[1]]
                                                else: # A-B & C- B (MTO)
                                                    combi123 = combi['MTO'][combi12, r3]
                                                    der3 = [source12[0], source3[0]]  
                                        # And again for the third
                                        if combi123 >= 0: # Only derive from properly defined relations
                                            for sr1 in range(len(der3)):
                                                for sr2 in range(len(source4)):
                                                    if der3[sr1] == source4[sr2]:
                                                        common = source4[sr2]
                                            if list.index(der3, common) == 0:
                                                if list.index(source4, common) == 0: # A-B & A - C (OTM)
                                                    combi1234 = combi['OTM'][combi123, r4]
                                                    der4 = [der3[0], source4[1]]
                                                else: # A - B & C - A (sort of MTO)
                                                    combi1234 = combi['sMTO'][combi123, r4]
                                                    der4 = [der3[1], source4[0]]
                                            else:
                                                if list.index(source3, common) == 0: # A-B & B - C (linear)
                                                    combi1234 = combi['Linear'][combi123, r4]
                                                    der4 = [der3[0], source4[1]]
                                                else: # A-B & C- B (MTO)
                                                    combi1234 = combi['MTO'][combi123, r4]
                                                    der4 = [der3[0], source4[0]]  
                                        # And again for the fourth
                                        if combi1234 >= 0: # Only derive from properly defined relations
                                            for sr1 in range(len(der3)):
                                                for sr2 in range(len(source4)):
                                                    if der4[sr1] == source5[sr2]:
                                                        common = source5[sr2]
                                            if list.index(der4, common) == 0:
                                                if list.index(source5, common) == 0: # A-B & A - C (OTM)
                                                    combi12345 = combi['OTM'][combi1234, r5]
                                                    der5 = [der4[0], source5[1]]
                                                else: # A - B & C - A (sort of MTO)
                                                    combi12345 = combi['sMTO'][combi1234, r5]
                                                    der5 = [der4[1], source5[0]]
                                            else:
                                                if list.index(source3, common) == 0: # A-B & B - C (linear)
                                                    combi12345 = combi['Linear'][combi1234, r5]
                                                    der5 = [der4[0], source5[1]]
                                                else: # A-B & C- B (MTO)
                                                    combi12345 = combi['MTO'][combi1234, r5]
                                                    der5 = [der4[0], source5[0]]       
                                        else: 
                                             combi1234 = -1 # Derivation from ill-defined relation is ill-defined
                                        # Get derived relations and labels from function lists
                                        corMut1 = mutual[r1] # Find mutual relation
                                        corMut1Lab = list(relations.keys())[corMut1] # label
                                        corMut2 = mutual[r2] # Find mutual relation
                                        corMut2Lab = list(relations.keys())[corMut2] # label
                                        corMut3 = mutual[r3] # Find mutual relation
                                        corMut3Lab = list(relations.keys())[corMut3] # label
                                        corMut4 = mutual[r4] # Find mutual relation
                                        corMut4Lab = list(relations.keys())[corMut4] # label
                                        corMut4 = mutual[r4] # Find mutual relation
                                        corMut4Lab = list(relations.keys())[corMut4] # label
                                        corCombiLab = list(relations.keys())[combi12345] 
                                        if combi12345 >= 0: # Only include defined relations
                                            # Compile prompt from premise + query
                                            prompt = "{} {} {} {} Is {} {} {}?". format(premise1, 
                                                                               premise2,
                                                                               premise3,
                                                                               premise4, 
                                                                               premise5,
                                                                               der5[0], corCombiLab, der5[1])
                                            trial_data['id'].append(t)
                                            trial_data['Premises'].append(premises)
                                            trial_data['Relations'].append(rels)
                                            trial_data['Prompt'].append(prompt)
                                            trial_data['Correct'].append('Yes') # Always correct if specified like this
                                            trial_data['Type'].append('Regular')
                                            trial_data['n_p'].append('4')
                                            
                                            ## ADD REVERSE PROMPT FOR  2<= premises
                                            
                                            # Incorrect query variant
                                            t += 1
                                            # Find incorrect relation examples
                                            notRels = []
                                            if len(relations.keys()) == 1:
                                                allRels = ['the same as', 'different from', 'opposite to', 
                                                           'more than', 'less than', 
                                                           # 'part of', 'contains', 'before', 'after'
                                                           ]
                                            else:
                                                allRels = list(relations.keys())
                                            for ir in range(len(allRels)):
                                                if corMutLab == 'different from':
                                                    if not allRels[ir] in ['opposite to', 'different from']:
                                                        notRels.append(allRels[ir])
                                                elif corMutLab == 'opposite to':
                                                    if not list(allRels)[ir] in ['opposite to', 'different from']:
                                                        notRels.append(allRels[ir])
                                                else:
                                                    if not allRels[ir] == corMutLab:
                                                        notRels.append(allRels[ir])
                                            incorCombiLab = np.random.choice(notRels)
                                            # Build prompt
                                            prompt = "{} {} {} {} {} Is {} {} {}?". format(premise1, 
                                                                               premise2,
                                                                               premise3,
                                                                               premise4, 
                                                                               premise5, 
                                                                               der5[0], incorCombiLab, der5[1])
                                            # Store trial data
                                            trial_data['id'].append(t) 
                                            trial_data['Relations'].append(rels)
                                            trial_data['Prompt'].append(prompt)
                                            trial_data['Correct'].append('No')
                                            trial_data['Type'].append('Incorrect')
                                            trial_data['n_p'].append('5')
                                            if 'irrelevant' in n_type_premises['5']:
                                                t += 1
                                                # Find irrelevant S to add premise
                                                half = len(sLabs)/2
                                                if t_id < half: irr_id = np.random.randint(half+1, len(sLabs))
                                                else: irr_id = np.random.randint(0,half-1)
                                                irrRel = np.random.choice(list(relations.keys())) # randomly select relation
                                                irrS = sLabs[irr_id] # label
                                                # Randomize order of relata in irrelevant premise
                                                if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                                else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                                prompt = "{} {} {} {} {} {} Is {} {} {}?".format(premise1,
                                                                                  premise2,
                                                                                  premise3,
                                                                                  premise4,
                                                                                  premise5,
                                                                                  irrPremise,
                                                                                  der5[0], corCombiLab, der5[1])
                                                # Store trial data
                                                premises.append(irrPremise)
                                                trial_data['id'].append(t) 
                                                trial_data['Premises'].append(premises)
                                                trial_data['Relations'].append([rels])
                                                trial_data['Prompt'].append(prompt)
                                                trial_data['Correct'].append('Yes')
                                                trial_data['Type'].append('Irrelevant')
                                                trial_data['n_p'].append('5')
                                                
                                                # Incorrect query version
                                                t += 1
                                                # Find irrelevant S to add premise
                                                half = len(sLabs)/2
                                                if t_id < half: # to avoid indexing issues
                                                    irr_id = np.random.randint(half+1, len(sLabs))
                                                else:
                                                    irr_id = np.random.randint(0,half-1)
                                                irrRel = np.random.choice(list(relations.keys())) # select random releation
                                                irrS = sLabs[irr_id]
                                                # Randomize order of relata in irrelevant premise
                                                if t%2==0: irrPremise = "{} is {} {}.".format(stim[0], irrRel, irrS)
                                                else: irrPremise = "{} is {} {}.".format(irrS, irrRel, stim[1])
                                                prompt = "{} {} {} {} {} {} Is {} {} {}?".format(premise1,
                                                                                  premise2,
                                                                                  premise3,
                                                                                  premise4,
                                                                                  premise5,
                                                                                  irrPremise,
                                                                                  der5[0], incorCombiLab, der5[1])
                                                trial_data['id'].append(t) # Store data
                                                trial_data['Premises'].append(premises)
                                                trial_data['Relations'].append([rels])
                                                trial_data['Prompt'].append(prompt)
                                                trial_data['Correct'].append('No')
                                                trial_data['Type'].append('Irrelevant')
                                                trial_data['n_p'].append('5')
    if printTrials:
        for t in range(len(trial_data['id'])):
            print("Trial {}: {}. {}".format(t+1, trial_data['Prompt'][t], trial_data['Correct'][t]))
            
    return trial_data
