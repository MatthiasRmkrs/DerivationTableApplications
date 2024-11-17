# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:43:52 2024

Function to create syllogistic problems that target deictic reasoning:
    - interpersonal relations: I-YOU distinction
    - Spatial relations: HERE-THERE distinction
    - Temporal relations: NOW-THEN distinction
    
Building on McHugh protocol (McHugh et al., 2004) and the deictic framing
subset of the RAI, typically two premises are presented along with two questions.
Some trials include a reversal of the premises (e.g., 'if now was then & then was now').


Novel relative to the above tasks is that multiple instances of the three categories 
of relations are included (i.e., I think that, believe that, ....)


TO DO:
    - Later if need be combined spat/temp-iP relations
    - Update/add RAI++ MC format:
        - three or four statements, can be T/F, prompt is to select all T/F
        - 
@author: mraemaek
"""

def generateDeicticSyllogisms(relations, n_reps, reversal, irrelevant, forcedChoice, printTrials):
    #dependencies
    import numpy as np
    import pdb
    
    # Initialise dict and counters
    trial_data = dict({'id': [], 'premises': [], 'domain': [], 'prompt': [],
                       'correct': [], 'type': [], 'problem': []})
    
    t = -1
    problem = -1
    for rel in list(relations.keys()): # Lopp deictic relations specified in input
        match rel:
# %% Interpersonal 'thinking' relations
# Premise: "I think A and you think B" -> Qs: "Do I/you think A/B?", "What do I/you think?"?

            case 'interpersonal-thinking':
                if reversal:
                    reversalPremise = 'If I were you and you were me;'  # always the same
                if irrelevant:  # Specifcy some irrelevant premises
                    irrActions = ['You are wearing a red shirt', 'I am wearing a red shirt',
                                  'You are playing chess.', 'I am playing chess.',
                                  'You are playing outside.', 'I am playing outside.',
                                  'You are drinking a coke.', 'I am drinking a coke.',
                                  'You are feeding the cat.', 'I am feeding the cat.',
                                  'You are playing videogames.', 'I am playing videogames.', 
                                  'You are reading a book.', 'I am reading a book.',
                                  'You are cleaning','I am cleaning', 
                                  'You are cooking', 'I am cooking',
                                  'You are playing football', 'I am playing football', 
                                  'You are watching television', 'I am watching television', 
                                  'You are reading a magazine', 'I am reading a magazine',
                                  'You are sitting on a red chair.', 'I am sitting on a red chair.', 
                                  'You are sitting on a blue chair.', 'I am sitting on a blue chair.', 
                                  'You are sitting on a black chair.', 'I am sitting on a black chair.'
                                  ]
            
                thinking = relations[rel][0] # in case the lists are unnamed in input
                thoughts = relations[rel][1]
    
                for ip in range(len(thinking)):  # loop specified synonyms for 'thinking'
                    prompts = []  # init list
                    types = []  # init list
                    responses = []  # init list
                    for r in range(n_reps):
                        problem += 1
                        if len(thinking) == 1:
                            t_id = 2*r
                            if t_id >= len(thoughts):
                                loop = int(np.round(t_id/len(thoughts)))
                                t_id -= loop*len(thoughts) # cycle back through list
                        elif len(thinking) > 1:
                            t_id = 2*r + 2*(ip+r)
                            if t_id >= len(thoughts):
                                loop = int(np.round(t_id/len(thoughts)))
                                t_id -= loop*len(thoughts) # cycle back through list
                        # Build problem premises, randomize I-You order
                        iyou = np.random.permutation(['I', 'you'])
                        iyou[0] = iyou[0][0].upper() + iyou[0][1:] # capitalize prompt
                        premise1 = '{} {} {}'.format(iyou[0],
                                                     thinking[ip],
                                                     thoughts[t_id])
                        premise2 = '{} {} {}.'.format(iyou[1],
                                                      thinking[ip],
                                                      thoughts[t_id+1])
                        
                        if 'You' in iyou:  # Account for caps in queries
                            iyou[list.index(list(iyou), 'You')] = 'you'
                        # Build queries depending on response format:
                        if forcedChoice:  # forced choice queries e.g. 'Do I think A?'
                            # Balance correct/incorrect queries
                            if problem % 4 == 0:  # both queries correct
                                query1 = 'Do {} {} {}?'.format(iyou[0], thinking[ip],
                                                               thoughts[t_id])
                                query2 = 'Do {} {} {}?'.format(iyou[1], thinking[ip],
                                                               thoughts[t_id + 1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2Correct'.format(problem+1))
                                responses.append(['yes', 'yes'])
                                # problem, id, premises, domain stored at end of loop
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal + Irrelevant -noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                            elif problem % 4 == 1:  # First query incorrect
                                query1 = 'Do {} {} {}?'.format(iyou[1], thinking[ip],
                                                               thoughts[t_id + 1])
                                query2 = 'Do {} {} {}?'.format(iyou[0], thinking[ip],
                                                               thoughts[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 1stCorrect'.format(problem+1))
                                responses.append(['yes', 'no'])
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id+1])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal + Irrelevant - 2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                            elif problem % 4 == 2:  # Second query incorrect
                                query1 = 'Do {} {} {}?'.format(iyou[0], thinking[ip],
                                                               thoughts[t_id + 1])
                                query2 = 'Do {} {} {}?'.format(iyou[1], thinking[ip],
                                                               thoughts[t_id + 1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2ndCorrect'.format(problem+1))
                                responses.append(['no', 'yes'])
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id+1])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal + Irrelevant - 1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                            elif problem % 4 == 3:  # Both incorrect
                                query1 = 'Do {} {} {}?'.format(iyou[1], thinking[ip],
                                                               thoughts[t_id])
                                query2 = 'Do {} {} {}?'.format(iyou[0], thinking[ip],
                                                               thoughts[t_id + 1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - NoCorrect'.format(problem+1))
                                responses.append(['no', 'no'])
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal + Irrelevant - 2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], thinking[ip],
                                                                   thoughts[t_id])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], thinking[ip],
                                                                   thoughts[t_id + 1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                        else:  # open format questions
                            query1 = 'What do {} {}?'.format(iyou[0], thinking[ip])
                            query2 = 'What do {} {}?'.format(iyou[1], thinking[ip])
                            prompt = '{} and {} {} {}'.format(
                                premise1, premise2, query1, query2)
                            prompts.append(prompt)
                            types.append('Problem {} - Open Format'.format(problem+1))
                            responses.append([thoughts[t_id], thoughts[t_id+1]])
                            if irrelevant:
                                irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     irrPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Irrelevant-Open Format'.format(problem+1))
                                responses.append(['no', 'yes'])
                            if reversal and irrelevant:
                                query1 = 'What would {} {}?'.format(iyou[0], thinking[ip])
                                query2 = 'What would {} {}?'.format(iyou[1], thinking[ip])
                                irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                        irrPremise,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal+Irrelevant-Open Format'.format(problem+1))
                                responses.append(['yes', 'yes'])
                            if reversal:
                                query1 = 'What would {} {}?'.format(iyou[0], thinking[ip])
                                query2 = 'What would {} {}?'.format(iyou[1], thinking[ip])
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal - Open Format'.format(problem+1))
                                responses.append([thoughts[t_id+1], thoughts[t_id]])
                    for i in range(len(prompts)): # update trial data after iterations of problem
                        if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                            if i % 4 == 0:  # four versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            elif i %4 == 1:  # first irrelevant
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise])
                            elif i %4 == 2:  # then both
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise, reversalPremise])
                            elif i %4 == 3:  # then reversal only
                                trial_data['premises'].append(
                                    [premise1, premise2, reversalPremise])
                        if irrelevant or reversal:
                            if i % 2 == 0:  # two versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            else:  # reversal trials
                                if irrelevant:
                                    trial_data['premises'].append(
                                        [premise1, premise2, irrPremise])
                                else:
                                    trial_data['premises'].append(
                                        [premise1, premise2, reversalPremise])
                                    
                        trial_data['prompt'].append(prompts[i])
                        trial_data['domain'].append('IP-Thought')
                        trial_data['type'].append(types[i])
                        trial_data['correct'].append(responses[i])
                        
# %% Interpersonal 'feeling' relations
# Premise: "I feel A and you feel B" -> Qs: "Do I/you feel A/B?", "What do I/you feel?"?    
            case 'interpersonal-feeling':  # Separate sets for 'feel' (or synonyms)
                if reversal:
                    reversalPremise = 'If I were you and you were me;'  # always the same
                if irrelevant: # Specifcy some irrelevant premises
                    irrActions = ['You are wearing a red shirt', 'I am wearing a red shirt',
                                  'You are playing chess.', 'I am playing chess.',
                                  'You are playing outside.', 'I am playing outside.',
                                  'You are drinking a coke.', 'I am drinking a coke.',
                                  'You are feeding the cat.', 'I am feeding the cat.',
                                  'You are playing videogames.', 'I am playing videogames.', 
                                  'You are reading a book.', 'I am reading a book.',
                                  'You are cleaning','I am cleaning', 
                                  'You are cooking', 'I am cooking',
                                  'You are playing football', 'I am playing football', 
                                  'You are watching television', 'I am watching television', 
                                  'You are reading a magazine', 'I am reading a magazine',
                                  'You are sitting on a red chair.', 'I am sitting on a red chair.', 
                                  'You are sitting on a blue chair.', 'I am sitting on a blue chair.', 
                                  'You are sitting on a black chair.', 'I am sitting on a black chair.'
                                  ]
                # in case the lists are unnamed in input
                feeling = relations[rel][0]
                feelings = relations[rel][1]
    
                for f in range(len(feeling)):  # loop specified synonyms for 'thinking'
                    prompts = []
                    types = []
                    responses = []
                    for r in range(n_reps):
                        problem += 1
                        if len(feeling) == 1:
                            t_id = 2*r
                            if t_id >= len(feelings):
                                loop = int(np.round(t_id/len(feelings)))
                                t_id -= loop*len(feelings) # cycle back through list
                        elif len(feeling) > 1:
                            t_id = 2*r + 2*(f+r)
                            if t_id >= len(feelings):
                                loop = int(np.round(t_id/len(feelings)))
                                t_id -= loop*len(feelings) # cycle back through list
                        # Build problem premises, randomize I-You order
                        iyou = np.random.permutation(['I', 'you'])
                        iyou[0] = iyou[0][0].upper() + iyou[0][1:] # capitalize prompt
                        premise1 = '{} {} {}'.format(iyou[0],
                                                     feeling[f],
                                                     feelings[t_id])
                        premise2 = '{} {} {}.'.format(iyou[1],
                                                      feeling[f],
                                                      feelings[t_id+1])
                        
                        if 'You' in iyou: # Account for caps in queries
                            iyou[list.index(list(iyou), 'You')] = 'you'
                        # Build queries depending on response format:
                        if forcedChoice:  # forced choice queries e.g. 'Do I think A?'
                            # Both correct (want to make this more efficient)
                            if problem % 4 == 0:
                                query1 = 'Do {} {} {}?'.format(iyou[0], feeling[f],
                                                               feelings[t_id])
                                query2 = 'Do {} {} {}?'.format(iyou[1], feeling[f],
                                                               feelings[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2Correct'.format(problem+1))
                                responses.append(['yes', 'yes'])
                                # problem, id, premises, domain stored at end of loop
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id ])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id +1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id ])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id +1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                            elif problem % 4 == 1:  # First query incorrect
                                query1 = 'Do {} {} {}?'.format(iyou[1], feeling[f],
                                                               feelings[t_id +1])
                                query2 = 'Do {} {} {}?'.format(iyou[0], feeling[f],
                                                               feelings[t_id +1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 1stCorrect'.format(problem+1))
                                responses.append(['yes', 'no'])
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id +1])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id +1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id +1])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id +1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                            elif problem % 4 == 2:  # Second query incorrect
                                query1 = 'Do {} {} {}?'.format(iyou[0], feeling[f],
                                                               feelings[t_id+1])
                                query2 = 'Do {} {} {}?'.format(iyou[1], feeling[f],
                                                               feelings[t_id +1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2ndCorrect'.format(problem+1))
                                responses.append(['no', 'yes'])
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id +1])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id +1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id +1])
                                    query2 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id +1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                            elif problem % 4 == 3:  # Both incorrect
                                query1 = 'Do {} {} {}?'.format(iyou[1], feeling[f],
                                                               feelings[t_id])
                                query2 = 'Do {} {} {}?'.format(iyou[0], feeling[f],
                                                               feelings[t_id +1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - NoCorrect'.format(problem+1))
                                responses.append(['no', 'no'])
                                if irrelevant:
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-NoCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id ])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id +1])
                                    irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal:
                                    query1 = 'Would {} {} {}?'.format(iyou[1], feeling[f],
                                                                   feelings[t_id])
                                    query2 = 'Would {} {} {}?'.format(iyou[0], feeling[f],
                                                                   feelings[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                        else:  # open format questions
                            if 'You' in iyou: # Account for caps in queries
                                iyou[list.index(list(iyou), 'You')] == 'you'
                            query1 = 'What do {} {}?'.format(iyou[0], feeling[f])
                            query2 = 'What do {} {}?'.format(iyou[1], feeling[f])
                            prompt = '{} and {} {} {}'.format(
                                premise1, premise2, query1, query2)
                            prompts.append(prompt)
                            types.append('Problem {} - Open Format'.format(problem+1))
                            responses.append([feelings[t_id], feelings[t_id+1]])
                            if irrelevant:
                                irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     irrPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Irrelevant-NoCorrect'.format(problem+1))
                                responses.append([feelings[t_id], feelings[t_id+1]])
                            if reversal and irrelevant:
                                query1 = 'What would {} {}?'.format(iyou[0], feeling[f])
                                query2 = 'What would {} {}?'.format(iyou[1], feeling[f])
                                irrPremise = irrActions[np.random.randint(0,len(irrActions))]
                                prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                        irrPremise,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal+Irrelevant-2Correct'.format(problem+1))
                                responses.append([feelings[t_id+1], feelings[t_id]])
                            if reversal:
                                query1 = 'What would {} {}?'.format(iyou[0], feeling[f])
                                query2 = 'What would {} {}?'.format(iyou[1], feeling[f])
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal'.format(problem+1))
                                responses.append([feelings[t_id+1], feelings[t_id]])
                    for i in range(len(prompts)): # update trial data after iterations of problem
                        if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                            if i % 4 == 0:  # four versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            elif i %4 == 1:  # first both
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise, reversalPremise])
                            elif i %4 == 2:  # then reversal only
                                trial_data['premises'].append(
                                    [premise1, premise2, reversalPremise])
                            elif i %4 == 3:  # then irrelevant only
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise])
                        if irrelevant or reversal:
                            if i % 2 == 0:  # two versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            else:  # reversal trials
                                if irrelevant:
                                    trial_data['premises'].append(
                                        [premise1, premise2, irrPremise])
                                else:
                                    trial_data['premises'].append(
                                        [premise1, premise2, reversalPremise])
                        trial_data['prompt'].append(prompts[i])
                        trial_data['domain'].append('IP-Feeling')
                        trial_data['type'].append(types[i])
                        trial_data['correct'].append(responses[i])
# %% Interpersonal 'doing' relations
# Premise: "I am doing A and you are doing B" -> Qs: "Am I/Are you doing A/B?", "What am I/are you doing?"?
            case 'interpersonal-doing':
                if reversal:
                    reversalPremise = 'If I were you and you were me;'  # always the same
                    revIyou = [] # need adapted pronouns for reversal doing prompts
                if irrelevant: # Specifcy some irrelevant premises
                    irrFeels = ['You feel cold', 'I feel cold',
                                'You feel sad', 'I feel sad',
                                'You feel happy', 'I feel happy',
                                'You feel warm', 'I feel warm',
                                'You feel hot', 'I feel hot',
                                'You feel dizzy', 'I feel dizzy',
                                'You feel scared', 'I feel scared',
                                'You feel good', 'I feel good',
                                'You feel stressed', 'I feel stressed',
                                'You feel bad', 'I feel bad',
                                'You feel great', 'I feel great'
                                ]
                action = relations[rel][0]
                doing = relations[rel][1]  # in case the lists are unnamed in input
                for d in range(action):  # loop specified actions (only 'doing' for loop purposes, not used here)
                    prompts = []
                    types = []
                    responses = []
                    for r in range(n_reps):
                        problem += 1
                        if len(action) == 1:
                            t_id = 2*r
                            if t_id >= len(doing):
                                loop = int(np.round(t_id/len(doing)))
                                t_id -= loop*len(doing) # cycle back through list
                        elif len(action) > 1:
                            t_id = 2*r + 2*(f+r)
                            if t_id >= len(doing):
                                loop = int(np.round(t_id/len(doing)))
                                t_id -= loop*len(doing) # cycle back through list
                        # Build problem premises, randomize I-You order
                        iyou = np.random.permutation(['I am', 'you are'])
                        iyou[0] = iyou[0][0].upper() + iyou[0][1:] # capitalize prompt
                        premise1 = '{} {}'.format(iyou[0],
                                                  doing[t_id])
                        premise2 = '{} {}.'.format(iyou[1],
                                                   doing[t_id+1])
                        
                        if 'You are' in iyou:  # adapt for queries
                            iyou[list.index(list(iyou), 'You are')] = 'Are you'
                        else:
                            iyou[list.index(list(iyou), 'you are')] = 'Are you'
                        iyou[list.index(list(iyou), 'I am')] = 'Am I'
                        if reversal:
                            for i in iyou:
                                if i == 'Am I':
                                    revIyou.append('Would I be')
                                else:
                                    revIyou.append('Would you be')                          
                        # Build queries depending on response format:
                        if forcedChoice:  # forced choice queries e.g. 'Do I think A?'
                            
                            if problem % 4 == 0:  # both correct
                                query1 = '{} {}?'.format(iyou[0], doing[t_id])
                                query2 = '{} {}?'.format(iyou[1], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2Correct'.format(problem+1))
                                responses.append(['yes', 'yes'])
                                # problem, id, premises, domain stored at end of loop
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                            elif problem % 4 == 1:  # First query incorrect
                                query1 = '{} {}?'.format(iyou[1], doing[t_id+1])
                                query2 = '{} {}?'.format(iyou[0], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 1stCorrect'.format(problem+1))
                                responses.append(['yes', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                            elif problem % 4 == 2:  # Second query incorrect
                                query1 = '{} {}?'.format(iyou[0], doing[t_id+1])
                                query2 = '{} {}?'.format(iyou[1], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2ndCorrect'.format(problem+1))
                                responses.append(['no', 'yes'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                            elif problem % 4 == 3:  # Both incorrect
                                query1 = '{} {}?'.format(iyou[1], doing[t_id])
                                query2 = '{} {}?'.format(iyou[0], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - NoCorrect'.format(problem+1))
                                responses.append(['no', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-NoCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                        else:  # open format questions
                            iyou[list.index(list(iyou), 'Are you')] = 'are you'
                            query1 = 'What {} doing?'.format(iyou[0])
                            query2 = 'What {} doing'.format(iyou[1])
                            prompt = '{} and {} {} {}'.format(
                                premise1, premise2, query1, query2)
                            prompts.append(prompt)
                            types.append('Problem {} - Open Format'.format(problem+1))
                            responses.append([doing[t_id], doing[t_id+1]])
                            if irrelevant:
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     irrPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Irrelevant-Open Format'.format(problem+1))
                                responses.append([doing[t_id], doing[t_id+1]])
                            if reversal and irrelevant:
                                query1 = 'What {} doing?'.format(revIyou[0])
                                query2 = 'What {} doing'.format(revIyou[1])
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                        irrPremise,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal+Irrelevant-Open Format'.format(problem+1))
                                responses.append([doing[t_id+1], doing[t_id]])
                            if reversal:
                                query1 = 'What {} doing?'.format(revIyou[0])
                                query2 = 'What {} doing'.format(revIyou[1])
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal - Open Format'.format(problem+1))
                                responses.append([doing[t_id+1], doing[t_id]])
                    for i in range(len(prompts)): # update trial data after iterations of problem
                        if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                            if i % 4 == 0:  # four versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            elif i %4 == 1:  # first both
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise, reversalPremise])
                            elif i %4 == 2:  # then reversal only
                                trial_data['premises'].append(
                                    [premise1, premise2, reversalPremise])
                            elif i %4 == 3:  # then irrelevant only
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise])
                        if irrelevant or reversal:
                            if i % 2 == 0:  # two versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            else:  # reversal trials
                                if irrelevant:
                                    trial_data['premises'].append(
                                        [premise1, premise2, irrPremise])
                                else:
                                    trial_data['premises'].append(
                                        [premise1, premise2, reversalPremise])
                        trial_data['prompt'].append(prompts[i])
                        trial_data['domain'].append('IP-Doing')
                        trial_data['type'].append(types[i])
                        trial_data['correct'].append(responses[i])
# %% Temporal relations 
# Premise: "A is now and B was then" -> Qs: "Is A/B now/then?", "What is now/then"?
            case 'temporal':
                times = relations[rel][0] # in case the lists are unnamed in input
                events = relations[rel][1]
                # to change verb tense in prompt
                past = ['yesterday', 'last week', 'last year']
                for t in range(len(times)):  # loop specified actions
                    if reversal:
                        reversalPremise = 'If {} were {} and {} were {};'.format(times[t][0],
                                                                                times[t][1],
                                                                                times[t][1],
                                                                                times[t][0],)
                    if irrelevant: # Specifcy some irrelevant premises
                        irrFeels = ['You feel cold', 'I feel cold',
                                    'You feel sad', 'I feel sad',
                                    'You feel happy', 'I feel happy',
                                    'You feel warm', 'I feel warm',
                                    'You feel hot', 'I feel hot',
                                    'You feel dizzy', 'I feel dizzy',
                                    'You feel scared', 'I feel scared',
                                    'You feel good', 'I feel good',
                                    'You feel stressed', 'I feel stressed',
                                    'You feel bad', 'I feel bad',
                                    'You feel great', 'I feel great'
                                    ]
                    prompts = []
                    types = []
                    responses = []
                    for r in range(n_reps):
                        problem += 1
                        if len(times) == 1:
                            t_id = 2*r
                            if t_id >= len(events):
                                loop = int(np.round(t_id/len(events)))
                                t_id -= loop*len(events) # cycle back through list
                        elif len(times) > 1:
                            t_id = 2*r + 2*(t+r)
                            if t_id >= len(events):
                                loop = int(np.round(t_id/len(events)))
                                t_id -= loop*len(events) # cycle back through list
                        # Build problem premises, randomize I-You order
                        nowthen = np.random.permutation(times[t])
                        nowthen[0] = nowthen[0][0].upper() + nowthen[0][1:]  # adapt caps
                        if nowthen[0].lower() in past:  # Fix capitalization for prompt
                            premise1 = '{} was {}'.format(nowthen[0],
                                                          events[t_id])
                            premise2 = '{} is {}.'.format(nowthen[1],
                                                          events[t_id+1])
                        else:
                            premise1 = '{} is {}'.format(nowthen[0],
                                                         events[t_id])
                            premise2 = '{} was {}.'.format(nowthen[1],
                                                           events[t_id+1])
                            # This will require an extra clause for when none in past
                            
                        nowthen[0] = nowthen[0].lower()
                        # Build queries depending on response format:
                        if forcedChoice:  # forced choice queries e.g. 'Do I think A?'
                            if problem % 4 == 0:  # Both correct
                                if nowthen[0] in past:
                                    query1 = 'Was {} {}?'.format(
                                        events[t_id], nowthen[0])
                                    query2 = 'Is {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                else:
                                    query1 = 'Is {} {}?'.format(
                                        events[t_id], nowthen[0])
                                    query2 = 'Was {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2Correct'.format(problem+1))
                                responses.append(['yes', 'yes'])
                                # problem, id, premises, domain stored at end of loop
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal and irrelevant:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id], nowthen[1])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[0])
                                    else:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id], nowthen[1])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[0])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id], nowthen[0])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                    else:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id], nowthen[0])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                            elif problem % 4 == 1:  # First query incorrect
                                if nowthen[0] in past:
                                    query1 = 'Is {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                    query2 = 'Was {} {}?'.format(
                                        events[t_id+1], nowthen[0])
                                else:
                                    query1 = 'Was {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                    query2 = 'Is {} {}?'.format(
                                        events[t_id+1], nowthen[0])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 1stCorrect'.format(problem+1))
                                responses.append(['yes', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[0])
                                    else:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[0])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[0])
                                    else:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[0])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                            elif problem % 4 == 2:  # Second query incorrect
                                if nowthen[0] in past:
                                    query1 = 'Was {} {}?'.format(
                                        events[t_id+1], nowthen[0])
                                    query2 = 'Is {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                else:
                                    query1 = 'Is {} {}?'.format(
                                        events[t_id+1], nowthen[0])
                                    query2 = 'Was {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2ndCorrect'.format(problem+1))
                                responses.append(['no', 'yes'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal and irrelevant:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[0])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                    else:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[0])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[0])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                    else:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[0])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                            elif problem % 4 == 3:  # Both incorrect
                                if nowthen[0] in past:
                                    query1 = 'Is {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                    query2 = 'Was {} {}?'.format(
                                        events[t_id], nowthen[0])
                                else:
                                    query1 = 'Was {} {}?'.format(
                                        events[t_id+1], nowthen[1])
                                    query2 = 'Is {} {}?'.format(
                                        events[t_id], nowthen[0])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - NoCorrect'.format(problem+1))
                                responses.append(['no', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-NoCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal and irrelevant:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id], nowthen[0])
                                    else:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id], nowthen[0])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal:
                                    if nowthen[0] in past:
                                        query1 = 'Would {} be {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} have been {}?'.format(
                                            events[t_id], nowthen[0])
                                    else:
                                        query1 = 'Would {} have been {}?'.format(
                                            events[t_id+1], nowthen[1])
                                        query2 = 'Would {} be {}?'.format(
                                            events[t_id], nowthen[0])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                        else:  # open format questions
                            if nowthen[0] in past:
                                query1 = 'What was {}?'.format(nowthen[0])
                                query2 = 'What is {}?'.format(nowthen[1])
                            else:
                                query1 = 'What is {}?'.format(nowthen[0])
                                query2 = 'What was {}?'.format(nowthen[1])
    
                            prompt = '{} and {} {} {}'.format(
                                premise1, premise2, query1, query2)
                            prompts.append(prompt)
                            types.append('Problem {} - Open Format'.format(problem+1))
                            responses.append([events[t_id], events[t_id+1]])
                            if irrelevant:
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     irrPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                responses.append([events[t_id], events[t_id+1]])
                            if reversal and irrelevant:
                                if nowthen[0] in past:
                                    query1 = 'What would have been {}?'.format(nowthen[0])
                                    query2 = 'What would be {}?'.format(nowthen[1])
                                else:
                                    query1 = 'What would be {}?'.format(nowthen[0])
                                    query2 = 'What would have been {}?'.format(nowthen[1])
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                        irrPremise,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal+Irrelevant-2ndCorrect'.format(problem+1))
                                responses.append([events[t_id+1], events[t_id]])
                            if reversal:
                                if nowthen[0] in past:
                                    query1 = 'What would have been {}?'.format(nowthen[0])
                                    query2 = 'What would be {}?'.format(nowthen[1])
                                else:
                                    query1 = 'What would be {}?'.format(nowthen[0])
                                    query2 = 'What would have been {}?'.format(nowthen[1])
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal - Open Format'.format(problem+1))
                                responses.append([events[t_id+1], events[t_id]])
                    for i in range(len(prompts)): # update trial data after iterations of problem
                        if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                            if i % 4 == 0:  # four versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            elif i %4 == 1:  # first both
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise, reversalPremise])
                            elif i %4 == 2:  # then reversal only
                                trial_data['premises'].append(
                                    [premise1, premise2, reversalPremise])
                            elif i %4 == 3:  # then irrelevant only
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise])
                        if irrelevant or reversal:
                            if i % 2 == 0:  # two versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            else:  # reversal trials
                                if irrelevant:
                                    trial_data['premises'].append(
                                        [premise1, premise2, irrPremise])
                                else:
                                    trial_data['premises'].append(
                                        [premise1, premise2, reversalPremise])
                        trial_data['prompt'].append(prompts[i])
                        trial_data['domain'].append('Temporal')
                        trial_data['type'].append(types[i])
                        trial_data['correct'].append(responses[i])
# %% Spatial relations
# Premise: 'A is here and B is there' -> Qq: Is A/B here/there?"/"Where is A/B?"
            case 'spatial':
                places = relations[rel][0] # in case the lists are unnamed in input
                things = relations[rel][1]
                # to change verb tense in prompt
                for p in range(len(places)):  # loop specified actions
                    if reversal:
                        reversalPremise = 'If {} were {} and {} were {};'.format(places[p][0],
                                                                                places[p][1],
                                                                                places[p][1],
                                                                                places[p][0],)
                    if irrelevant: # Specifcy some irrelevant premises
                        irrFeels = ['You feel cold', 'I feel cold',
                                    'You feel sad', 'I feel sad',
                                    'You feel happy', 'I feel happy',
                                    'You feel warm', 'I feel warm',
                                    'You feel hot', 'I feel hot',
                                    'You feel dizzy', 'I feel dizzy',
                                    'You feel scared', 'I feel scared',
                                    'You feel good', 'I feel good',
                                    'You feel stressed', 'I feel stressed',
                                    'You feel bad', 'I feel bad',
                                    'You feel great', 'I feel great'
                                    ]
                    prompts = []
                    types = []
                    responses = []
                    for r in range(n_reps):
                        problem += 1
                        if len(places) == 1:
                            t_id = 2*r
                            if t_id >= len(things):
                                loop = int(np.round(t_id/len(things)))
                                t_id -= loop*len(things) # cycle back through list
                        elif len(places) > 1:
                            t_id = 2*r + 2*(p+r)
                            if t_id >= len(things):
                                loop = int(np.round(t_id/len(things)))
                                t_id -= loop*len(things) # cycle back through list
                        # Build problem premises, randomize I-You order
                        herethere = np.random.permutation(places[p])
                        things[0] = things[0][0].upper() + things[0][1:]  # adapt caps
                        premise1 = '{} is {}'.format(things[t_id], herethere[0])
                        premise2 = '{} is {}.'.format(things[t_id+1], herethere[1])

                        herethere[0] = herethere[0].lower() # fix caps for queries
                        # Build queries depending on response format:
                        if forcedChoice:  # forced choice queries e.g. 'Do I think A?'
                            if problem % 4 == 0:  # Both correct
                                query1 = 'Is {} {}?'.format(
                                    things[t_id], herethere[0])
                                query2 = 'Is {} {}?'.format(
                                    things[t_id+1], herethere[1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2Correct'.format(problem+1))
                                responses.append(['yes', 'yes'])
                                # problem, id, premises, domain stored at end of loop
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes','yes'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id], herethere[0])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no','no'])
                                if reversal:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id], herethere[0])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                            elif problem % 4 == 1:  # First query incorrect
                                query1 = 'Is {} {}?'.format(
                                    things[t_id+1], herethere[1])
                                query2 = 'Is {} {}?'.format(
                                    things[t_id+1], herethere[0])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 1stCorrect'.format(problem+1))
                                responses.append(['yes', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes','no'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[0])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no','yes'])
                                if reversal:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[0])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                            elif problem % 4 == 2:  # Second query incorrect
                                query1 = 'Is {} {}?'.format(
                                    things[t_id+1], herethere[0])
                                query2 = 'Is {} {}?'.format(
                                    things[t_id+1], herethere[1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2ndCorrect'.format(problem+1))
                                responses.append(['no', 'yes'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no','yes'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[0])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes','no'])
                                if reversal:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[0])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                            elif problem % 4 == 3:  # Both incorrect
                                query1 = 'Is {} {}?'.format(
                                    things[t_id+1], herethere[1])
                                query2 = 'Is {} {}?'.format(
                                    things[t_id], herethere[0])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - NoCorrect'.format(problem+1))
                                responses.append(['no', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no','no'])
                                if reversal and irrelevant:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id], herethere[0])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes','yes'])
                                if reversal:
                                    query1 = 'Would {} be {}?'.format(
                                        things[t_id+1], herethere[1])
                                    query2 = 'Would {} be {}?'.format(
                                        things[t_id], herethere[0])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                        else:  # open format questions
                            query1 = 'Where is {}?'.format(things[t_id])
                            query2 = 'Where is {}?'.format(things[t_id+1])
                            prompt = '{} and {} {} {}'.format(
                                premise1, premise2, query1, query2)
                            prompts.append(prompt)
                            types.append('Problem {} - Open Format'.format(problem+1))
                            responses.append([herethere[0], herethere[1]])
                            if irrelevant:
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     irrPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Irrelevant-Open Format'.format(problem+1))
                            responses.append([herethere[0], herethere[1]])
                            if reversal and irrelevant:
                                query1 = 'Where would {} be?'.format(things[t_id])
                                query2 = 'Where would {} be?'.format(things[t_id+1])
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                        irrPremise,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal+Irrelevant-Open Format'.format(problem+1))
                            responses.append([herethere[1], herethere[0]])
                            if reversal:
                                query1 = 'Where would {} be?'.format(things[t_id])
                                query2 = 'Where would {} be?'.format(things[t_id+1])
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal - Open Format'.format(problem+1))
                            responses.append([herethere[1], herethere[0]])
                    for i in range(len(prompts)): # update trial data after iterations of problem
                        if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                            if i % 4 == 0:  # four versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            elif i %4 == 1:  # first both
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise, reversalPremise])
                            elif i %4 == 2:  # then reversal only
                                trial_data['premises'].append(
                                    [premise1, premise2, reversalPremise])
                            elif i %4 == 3:  # then irrelevant only
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise])
                        if irrelevant or reversal:
                            if i % 2 == 0:  # two versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            else:  # reversal trials
                                if irrelevant:
                                    trial_data['premises'].append(
                                        [premise1, premise2, irrPremise])
                                else:
                                    trial_data['premises'].append(
                                        [premise1, premise2, reversalPremise])
                        trial_data['prompt'].append(prompts[i])
                        trial_data['domain'].append('Spatial')
                        trial_data['type'].append(types[i])
                        trial_data['correct'].append(responses[i])

# %% Interpersonal 'doing' + spatial relations
# Premise: "I am doing A and you are doing B" -> Qs: "Am I/Are you doing A/B?", "What am I/are you doing?"?
            case 'IP-doing+spatial':
                places = relations[rel][2] # in case the lists are unnamed in input
                doing = relations[rel][1]  # in case the lists are unnamed in input
                action = relations[rel][0]
                for p in range(len(places)):
                    if reversal:
                        reversalPremise1 = 'If I were you and you were me;'  # manipulate which deictic rel is reversed
                        reversalPremise2 = 'If {} were {} and {} were {};'.format(places[p][0],
                                                                                  places[p][1],
                                                                                  places[p][1],
                                                                                  places[p][0],)# manipulate which deictic rel is reversed
    
                        revIyou = [] # need adapted pronouns for reversal doing prompts
                    if irrelevant: # Specifcy some irrelevant premises
                        irrFeels = ['You feel cold', 'I feel cold',
                                    'You feel sad', 'I feel sad',
                                    'You feel happy', 'I feel happy',
                                    'You feel warm', 'I feel warm',
                                    'You feel hot', 'I feel hot',
                                    'You feel dizzy', 'I feel dizzy',
                                    'You feel scared', 'I feel scared',
                                    'You feel good', 'I feel good',
                                    'You feel stressed', 'I feel stressed',
                                    'You feel bad', 'I feel bad',
                                    'You feel great', 'I feel great'
                                    ]
                
                for d in range(len(action)):  # loop specified actions
                    # correct for having only one list by halving iterations
                    prompts = []
                    types = []
                    responses = []
                    for r in range(n_reps):
                        problem += 1
                        if len(action) == 1:
                            t_id = 2*r
                            if t_id >= len(doing):
                                loop = int(np.round(t_id/len(doing)))
                                t_id -= loop*len(doing) # cycle back through list
                        elif len(action) > 1:
                            t_id = 2*r + 2*(f+r)
                            if t_id >= len(doing):
                                loop = int(np.round(t_id/len(doing)))
                                t_id -= loop*len(doing) # cycle back through list
                        # Build problem premises, randomize I-You order
                        iyou = np.random.permutation(['I am', 'you are'])
                        iyou = np.random.permutation(places[p])
                        iyou[0] = iyou[0][0].upper() + iyou[0][1:] # capitalize prompt
                        premise1 = '{} {} {}'.format(iyou[0],
                                                  doing[t_id], herethere[0])
                        premise2 = '{} {} {}.'.format(iyou[1],
                                                   doing[t_id+1], herethere[1])
                        
                        if 'You are' in iyou:  # adapt for queries
                            iyou[list.index(list(iyou), 'You are')] = 'Are you'
                        else:
                            iyou[list.index(list(iyou), 'you are')] = 'Are you'
                        iyou[list.index(list(iyou), 'I am')] = 'Am I'
                        if reversal:
                            for i in iyou:
                                if i == 'Am I':
                                    revIyou.append('Would I be')
                                else:
                                    revIyou.append('Would you be')                          
                        # Build queries depending on response format:
                        if forcedChoice:  # forced choice queries e.g. 'Do I think A?'
                            
                            if problem % 4 == 0:  # both correct
                                query1 = '{} {}?'.format(iyou[0], doing[t_id])
                                query2 = '{} {}?'.format(iyou[1], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2Correct'.format(problem+1))
                                responses.append(['yes', 'yes'])
                                # problem, id, premises, domain stored at end of loop
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-noCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                            elif problem % 4 == 1:  # First query incorrect
                                query1 = '{} {}?'.format(iyou[1], doing[t_id+1])
                                query2 = '{} {}?'.format(iyou[0], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 1stCorrect'.format(problem+1))
                                responses.append(['yes', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2ndCorrect'.format(problem+1))
                                    responses.append(['no', 'yes'])
                            elif problem % 4 == 2:  # Second query incorrect
                                query1 = '{} {}?'.format(iyou[0], doing[t_id+1])
                                query2 = '{} {}?'.format(iyou[1], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - 2ndCorrect'.format(problem+1))
                                responses.append(['no', 'yes'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-2ndCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-1stCorrect'.format(problem+1))
                                    responses.append(['yes', 'no'])
                            elif problem % 4 == 3:  # Both incorrect
                                query1 = '{} {}?'.format(iyou[1], doing[t_id])
                                query2 = '{} {}?'.format(iyou[0], doing[t_id+1])
                                prompt = '{} and {} {} {}'.format(
                                    premise1, premise2, query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} - NoCorrect'.format(problem+1))
                                responses.append(['no', 'no'])
                                if irrelevant:
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         irrPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Irrelevant-NoCorrect'.format(problem+1))
                                    responses.append(['no', 'no'])
                                if reversal and irrelevant:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id+1])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                    prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                            irrPremise,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal+Irrelevant-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                                if reversal:
                                    query1 = '{} {}?'.format(revIyou[1], doing[t_id])
                                    query2 = '{} {}?'.format(revIyou[0], doing[t_id+1])
                                    prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                         reversalPremise,
                                                                         query1, query2)
                                    prompts.append(prompt)
                                    types.append('Problem {} + Reversal-2Correct'.format(problem+1))
                                    responses.append(['yes', 'yes'])
                        else:  # open format questions
                            iyou[list.index(list(iyou), 'Are you')] = 'are you'
                            query1 = 'What {} doing?'.format(iyou[0])
                            query2 = 'What {} doing'.format(iyou[1])
                            prompt = '{} and {} {} {}'.format(
                                premise1, premise2, query1, query2)
                            prompts.append(prompt)
                            types.append('Problem {} - Open Format'.format(problem+1))
                            responses.append([doing[t_id], doing[t_id+1]])
                            if irrelevant:
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     irrPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Irrelevant-Open Format'.format(problem+1))
                                responses.append([doing[t_id], doing[t_id+1]])
                            if reversal and irrelevant:
                                query1 = 'What {} doing?'.format(revIyou[0])
                                query2 = 'What {} doing'.format(revIyou[1])
                                irrPremise = irrFeels[np.random.randint(0,len(irrFeels))]
                                prompt = '{} and {} {} {} {} {}'.format(premise1, premise2,
                                                                        irrPremise,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal+Irrelevant-Open Format'.format(problem+1))
                                responses.append([doing[t_id+1], doing[t_id]])
                            if reversal:
                                query1 = 'What {} doing?'.format(revIyou[0])
                                query2 = 'What {} doing'.format(revIyou[1])
                                prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                     reversalPremise,
                                                                     query1, query2)
                                prompts.append(prompt)
                                types.append('Problem {} + Reversal - Open Format'.format(problem+1))
                                responses.append([doing[t_id+1], doing[t_id]])
                    for i in range(len(prompts)): # update trial data after iterations of problem
                        if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                            if i % 4 == 0:  # four versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            elif i %4 == 1:  # first both
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise, reversalPremise])
                            elif i %4 == 2:  # then reversal only
                                trial_data['premises'].append(
                                    [premise1, premise2, reversalPremise])
                            elif i %4 == 3:  # then irrelevant only
                                trial_data['premises'].append(
                                    [premise1, premise2, irrPremise])
                        if irrelevant or reversal:
                            if i % 2 == 0:  # two versions of each problem
                                trial_data['premises'].append([premise1, premise2])
                            else:  # reversal trials
                                if irrelevant:
                                    trial_data['premises'].append(
                                        [premise1, premise2, irrPremise])
                                else:
                                    trial_data['premises'].append(
                                        [premise1, premise2, reversalPremise])
                        trial_data['prompt'].append(prompts[i])
                        trial_data['domain'].append('IP-Doing')
                        trial_data['type'].append(types[i])
                        trial_data['correct'].append(responses[i])
    # Add trial IDs
    for tr in range(len(trial_data['prompt'])):
        trial_data['id'].append(tr+1)
    
    if printTrials:
        for trial in range(len(trial_data['prompt'])):
            print('Trial {} ({}): {}. Answer: {}'.format(trial+1, trial_data['type'][trial],
                                                                 trial_data['prompt'][trial],
                                                                 trial_data['correct'][trial]))

    return trial_data
