# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 17:31:25 2024

NEW, MORE EFFICIENT VERSION OF DEICTIC SYLLOGISM GENERATOR FUNCTION

Provided minimal task characteristics, generates a set of syllogistic reasoning problems,
inspired by McHugh protocol (McHugh et al., 2004) and the deictic framing
subset of the RAI, typically two premises are presented along with a number of questions.
As in the above, problems involve interpersonal 'I-You', temporal 'now-then' and
spatial 'here-there' relations and all possible combinations therof (at some point).

Further have the options to include a reversal of the premises 
(e.g., 'if now was then & then was now'), an irrelevant premise, vary query format 
(open format versus forced choice) the number of queries provided and the task 
(simple Y/N responding versus select all T/F, in case of forced-choice, of course).

Function input:
    - relations: a dict containing the different deictic relations to test
        - keys: labes for different relations
        - values: list including two lists with verbs, deictis or objects, depending on relation
            * 'interpersonal-thinking': [thinking, thoughts], 
            * 'interpersonal-feeling': [feeling, feelings],
            * 'interpersonal-doing': [doing, actions],
            * 'temporal': [times, events],
            * 'spatial': [places, things],
            * 'temporalIPthinking': [thinking, thoughts, times],
            * 'temporalIPfeeling': [feeling, feelings, times],
            * 'temporalIPdoing': [doing, actions, times],
            * 'IPthinking+spatial': [thinking, thoughts, places], # Maybe a little weird?
            * 'IP-feeling+spatial': [feeling, feelings, places], # Maybe a little weird?
            * 'IP-doing+spatial': [doing, actions, places],
            * 'spatTempIPthinking': [thinking, thoughts, times, places],
            * 'spatTempIPfeeling': [feelng, feelings, times, places],
            * 'spatTempIPdoing': [doing, actions, times, places]
    - n_reps: number of repetitions (with unique stimuli) of each problem
    - reversal: whether to include a reversal variant of the problem
        'if I were you and you were me', 'if here were there and there were here', ...
    - irrelevant: True/False whether to include an irrelevant premise in the problem statement?
    - forcedChoice: whether questions should be Yes/bno (True) or open format
    - n_opt: number of response options/questions presented
    - printTrials: print a list of all trials after creating?
    - selectTF: if True, prompt is added that 'task is to select all queries that are true/false'
    
TODO:
    - Add combined relations
    - Add Dutch translation

@author: mraemaek
"""

# %%  Define function
def generateDeicticSyllogisms2(relations, n_reps, reversal, irrelevant, 
                               forcedChoice, n_opt, printTrials, selectTF=None):
    #dependencies
    import numpy as np
    import pdb
    
    # Initialise dict and counters
    trial_data = dict({'id': [], 'premises': [], 'domain': [], 'prompt': [],
                       'correct': [], 'type': [], 'problem': []})
    t = -1
    problem = -1
# %%
    for rel in list(relations.keys()): # Lopp deictic relations specified in input
    
        # Workflow:
            # 1- Get verbs/objects and Determine irrelevant and reversal prompt
                # -> Stored in general containers, same for all relations
            # 2 - Randomize I-You
            # 3: Create premises
            # 4: Create queries
                
        # Get relevant pronouns, verbs and objects for prompts
        if rel in ['interpersonal-thinking', 
                   'interpersonal-feeling', 
                   'interpersonal-doing']:
            deictics = relations[rel][0]
            objects = relations[rel][1]
        if rel in ['temporal', 'spatial']:
            deictics = relations[rel][0]
            objects = relations[rel][1]


        for d in range(len(deictics)):
            prompts = []
            types = []
            responses = []
            
            #specify  reversal premise and irrelevant premises, depends on deictic relations
            if reversal:
                if rel in  ['interpersonal-thinking', 'interpersonal-feeling', 'interpersonal-doing']:
                    reversalPremise = 'If I were you and you were me;'  # always the same
                elif rel in ['spatial', 'temporal']:
                    reversalPremise = 'If {} were {} and {} were {};'.format(deictics[d][0],
                                                                             deictics[d][1],
                                                                            deictics[d][1],
                                                                            deictics[d][0])
            if irrelevant:  # Specifcy some irrelevant premises
                if rel in  ['interpersonal-thinking', 'interpersonal-feeling']:
                    irrPrems = ['You are wearing a red shirt.', 'I am wearing a red shirt.',
                                  'You are playing chess.', 'I am playing chess.',
                                  'You are playing outside.', 'I am playing outside.',
                                  'You are drinking a coke.', 'I am drinking a coke.',
                                  'You are feeding the cat.', 'I am feeding the cat.',
                                  'You are playing videogames.', 'I am playing videogames.', 
                                  'You are reading a book.', 'I am reading a book.',
                                  'You are cleaning.','I am cleaning.', 
                                  'You are cooking.', 'I am cooking.',
                                  'You are playing football. ', 'I am playing football', 
                                  'You are watching television.', 'I am watching television.', 
                                  'You are reading a magazine.', 'I am reading a magazine.',
                                  'You are sitting on a red chair.', 'I am sitting on a red chair.', 
                                  'You are sitting on a blue chair.', 'I am sitting on a blue chair.', 
                                  'You are sitting on a black chair.', 'I am sitting on a black chair.'
                                  ]
                elif rel in ['interpersonal-doing', 'spatial', 'temporal']:
                    irrPrems = ['You feel cold.', 'I feel cold.',
                                'You feel sad.', 'I feel sad.',
                                'You feel happy.', 'I feel happy.',
                                'You feel warm.', 'I feel warm.',
                                'You feel hot.', 'I feel hot.',
                                'You feel dizzy.', 'I feel dizzy.',
                                'You feel scared.', 'I feel scared.',
                                'You feel good.', 'I feel good.',
                                'You feel stressed.', 'I feel stressed.',
                                'You feel bad.', 'I feel bad.',
                                'You feel great.', 'I feel great.'
                                ]
                     
            for r in range(n_reps): # Loop repetitions of each trial type
                problem += 1 # Update problem ID - unique premises
                if len(deictics) == 1: # determine id for verbs/objects in loop
                    t_id = 2*r
                    if t_id +1 >= len(objects):
                        loop = int(np.round(t_id/len(objects)))
                        t_id -= loop*len(objects) # cycle back through list
                    elif len(deictics) > 1:
                        t_id = 2*r + 2*(d+r)
                        if t_id +1 >= len(objects):
                            loop = int(np.round(t_id/len(objects)))
                            t_id -= loop*len(objects) # cycle back through list
                            
                # find random irrelevant object to insert in 'irrelevant(false)' questions
                half = len(objects)/2
                if t_id < half:
                    irr_id = np.random.randint(half+1, len(objects))
                else:
                    irr_id = np.random.randint(0,half-1)
                   
#%%              # (2) Build problem premises
                 
                #randomize I-You/here-there/now-then order
                if rel == 'interpersonal-doing':
                    iyou = np.random.permutation(['I am', 'you are'])
                else:
                    iyou = np.random.permutation(['I', 'you'])
                
                if rel in ['temporal']: # for temproal relations, first list is [now, then] variants
                    nowthen = np.random.permutation(deictics[d])
                    nowthen[0] = nowthen[0][0].upper() + nowthen[0][1:]  # adapt caps
                if rel in ['spatial']: # For spatial, first list is [here, there]
                    herethere = np.random.permutation(deictics[d])
                    objects[t_id] = objects[t_id][0].upper() + objects[0][1:]  # adapt caps
                # Premises have different format for different relations
                if rel in ['interpersonal-thinking', 'interpersonal-feeling']:
                    # 'thinking' and 'feeling' have same premise structure
                    iyou[0] = iyou[0][0].upper() + iyou[0][1:] # capitalize prompt
                    premise1 = '{} {} {}'.format(iyou[0],
                                                 deictics[d],
                                                 objects[t_id])
                    premise2 = '{} {} {}.'.format(iyou[1],
                                             deictics[d],
                                             objects[t_id+1])
                elif rel == 'interpersonal-doing':
                    premise1 = '{} {}'.format(iyou[0],
                                              objects[t_id])
                    premise2 = '{} {}.'.format(iyou[1],
                                               objects[t_id+1])
                elif rel == 'temporal':
                    # Past tense 'then' relations require slightly different premise
                    past = ['yesterday', 'last week', 'last year']
                    if nowthen[0].lower() in past:  # Fix capitalization for prompt
                        premise1 = '{} was {}'.format(nowthen[0],
                                                      objects[t_id])
                        premise2 = '{} is {}.'.format(nowthen[1],
                                                      objects[t_id+1])
                    elif nowthen[1].lower() in past:
                        premise1 = '{} is {}'.format(nowthen[0],
                                                     objects[t_id])
                        premise2 = '{} was {}.'.format(nowthen[1],
                                                       objects[t_id+1])
                    else: # No past tense
                        premise1 = '{} is {}'.format(nowthen[0],
                                                     objects[t_id])
                        premise2 = '{} is {}.'.format(nowthen[1],
                                                       objects[t_id+1])
                elif rel == 'spatial':
                     premise1 = '{} is {}'.format(objects[t_id], herethere[0])
                     premise2 = '{} is {}.'.format(objects[t_id+1], herethere[1])
                # elif rel == 'IPdoing+spatial':
                # elif rel == 'IPthinking+spatial':    
                # elif rel == 'IPfeeling+spatial':    
                # elif rel == 'IPthinking+temporal':
                # elif rel == 'IPfeeling+temporal':
                # elif rel == 'IPdoing+temporal':
                # elif rel == 'IPthinking+temporal+spatial':
                # elif rel == 'IPfeeling+temporal+spatial':
                 # elif rel == 'IPdoing+temporal+spatial':
                   
# %%             # (3) Build queries depending on response format:
                # adapt caps for queries
                
                if 'You' in iyou: # Account for caps in queries
                    iyou[list.index(list(iyou), 'You')] = 'you'
                if rel in ['temporal']:
                    nowthen[0] = nowthen[0].lower()
                if rel in ['spatial']: 
                    herethere[0] = herethere[0].lower()
                    objects[t_id] = objects[t_id].lower() 
                if rel == 'interpersonal-doing': # requires adapted 'i-you' given tat verb sentences are provided
                    revIyou = []
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

                
                if forcedChoice:  # Y/N queries e.g. 'Do I think A?'
                # Specify the number of premises and the number that are correct
                    # Say max four premises: Many T/F configurations
                    # Maybe better to just generate a number of T/F premises and randomly select
                    # Benefit is no need to repeat 4x
                    
                    # Generate a set of queries to select from
                    if rel in ['interpersonal-thinking', 'interpersonal-feeling']:
                        # 'TRUE' statements
                        true1 = 'Do {} {} {}?'.format(iyou[0], deictics[d],
                                                       objects[t_id])
                        true2 = 'Do {} {} {}?'.format(iyou[1], deictics[d],
                                                       objects[t_id+1])
                        false1 = 'Do {} {} {}?'.format(iyou[0], deictics[d],
                                                       objects[t_id+1])
                        false2 = 'Do {} {} {}?'.format(iyou[1], deictics[d],
                                                       objects[t_id])
                        # Can't really add more using only those four pieces of info
                        # could add irrelevant statements, but easy/always false?
                        irr1 = 'Do {} {} {}?'.format(iyou[0], deictics[d],
                                                       objects[irr_id]) # object not in premise
                        irr2 = 'Do {} {} {}?'.format(iyou[1], deictics[d],
                                                       objects[irr_id])
                        if reversal:
                            r_true1 = 'Would {} {} {}?'.format(iyou[0], deictics[d],
                                                           objects[t_id+1])
                            r_true2 = 'Would {} {} {}?'.format(iyou[1], deictics[d],
                                                           objects[t_id])
                            r_false1 = 'Would {} {} {}?'.format(iyou[0], deictics[d],
                                                           objects[t_id])
                            r_false2 = 'Would {} {} {}?'.format(iyou[1], deictics[d],
                                                           objects[t_id+1])
                            r_irr1 = 'Would {} {} {}?'.format(iyou[0], deictics[d],
                                                           objects[irr_id])
                            r_irr2 = 'Would {} {} {}?'.format(iyou[1], deictics[d],
                                                           objects[irr_id])
                    elif rel == 'interpersonal-doing':
                        true1 = '{} {}?'.format(iyou[0], objects[t_id])
                        true2 = '{} {}?'.format(iyou[1], objects[t_id+1])
                        false1 = '{} {}?'.format(iyou[0], objects[t_id+1])
                        false2 = '{} {}?'.format(iyou[1], objects[t_id])
                        irr1= '{} {}?'.format(iyou[0], objects[irr_id])
                        irr2 = '{} {}?'.format(iyou[1], objects[irr_id])
                        if reversal:
                            r_true1 = '{} {}?'.format(revIyou[0], objects[t_id+1])
                            r_true2 = '{} {}?'.format(revIyou[1], objects[t_id])
                            r_false1 = '{} {}?'.format(revIyou[0], objects[t_id])
                            r_false2 = '{} {}?'.format(revIyou[1], objects[t_id+1])
                            r_irr1 = '{} {}?'.format(revIyou[0], objects[irr_id])
                            r_irr2 = '{} {}?'.format(revIyou[1], objects[irr_id])
                    elif rel == 'temporal':
                        if nowthen[0] in past:
                            true1 = 'Was {} {}?'.format(
                                objects[t_id], nowthen[0])
                            true2 = 'Is {} {}?'.format(
                                objects[t_id+1], nowthen[1])
                            false1 = 'Was {} {}?'.format(
                                objects[t_id+1], nowthen[0])
                            false2 = 'Is {} {}?'.format(
                                objects[t_id], nowthen[1])
                            irr1 = 'Was {} {}?'.format(
                                objects[irr_id], nowthen[0])
                            irr2 = 'Is {} {}?'.format(
                                objects[irr_id], nowthen[1])
                            if reversal:
                                r_true1 = 'Would {} be {}?'.format(
                                    objects[t_id+1], nowthen[1])
                                r_true2 = 'Would {} have been {}?'.format(
                                    objects[t_id], nowthen[0])
                                r_false1 = 'Would {} be {}?'.format(
                                    objects[t_id], nowthen[1])
                                r_false2 = 'Would {} have been {}?'.format(
                                    objects[t_id+1], nowthen[0])
                                r_irr1 = 'Would {} be {}?'.format(
                                    objects[irr_id], nowthen[1])
                                r_irr2 = 'Would {} have been {}?'.format(
                                    objects[irr_id], nowthen[0])
                        elif nowthen[1] in past:
                            true1 = 'Is {} {}?'.format(
                                objects[t_id], nowthen[0])
                            true2 = 'Was {} {}?'.format(
                                objects[t_id+1], nowthen[1])
                            false1 = 'Is {} {}?'.format(
                                objects[t_id+1], nowthen[0])
                            false2 = 'Was {} {}?'.format(
                                objects[t_id], nowthen[1])
                            irr1 = 'Is {} {}?'.format(
                                objects[irr_id], nowthen[0])
                            irr2 = 'Was {} {}?'.format(
                                objects[irr_id], nowthen[1])
                            if reversal:
                                r_true1 = 'Would {} have been {}?'.format(
                                    objects[t_id+1], nowthen[1])
                                r_true2 = 'Would {} be {}?'.format(
                                    objects[t_id], nowthen[0])
                                r_false1 = 'Would {} have been {}?'.format(
                                    objects[t_id], nowthen[1])
                                r_false2 = 'Would {} be {}?'.format(
                                    objects[t_id+1], nowthen[0])
                                r_irr1 = 'Would {} have been {}?'.format(
                                    objects[irr_id], nowthen[1])
                                r_irr2 = 'Would {} be {}?'.format(
                                    objects[irr_id], nowthen[0])
                        else:
                            true1 = 'Is {} {}?'.format(
                                objects[t_id], nowthen[0])
                            true2 = 'Is {} {}?'.format(
                                objects[t_id+1], nowthen[1])
                            false1 = 'Is {} {}?'.format(
                                objects[t_id+1], nowthen[0])
                            false2 = 'Is {} {}?'.format(
                                objects[t_id], nowthen[1])
                            irr1 = 'Is {} {}?'.format(
                                objects[irr_id], nowthen[0])
                            irr2 = 'Is {} {}?'.format(
                                objects[irr_id], nowthen[1])
                            if reversal:
                                r_true1 = 'Would {} be {}?'.format(
                                    objects[t_id+1], nowthen[1])
                                r_true2 = 'Would {} be {}?'.format(
                                    objects[t_id], nowthen[0])
                                r_false1 = 'Would {} be {}?'.format(
                                    objects[t_id], nowthen[1])
                                r_false2 = 'Would {} be {}?'.format(
                                    objects[t_id+1], nowthen[0])
                                r_irr1 = 'Would {} be {}?'.format(
                                    objects[irr_id], nowthen[1])
                                r_irr2 = 'Would {} be {}?'.format(
                                    objects[irr_id], nowthen[0])
                    elif rel == 'spatial':
                       true1 = 'Is {} {}?'.format(
                           objects[t_id], herethere[0])
                       true2 = 'Is {} {}?'.format(
                           objects[t_id+1], herethere[1])
                       false1 = 'Is {} {}?'.format(
                           objects[t_id+1], herethere[0])
                       false2 = 'Is {} {}?'.format(
                           objects[t_id], herethere[1])
                       irr1 = 'Is {} {}?'.format(
                           objects[irr_id], herethere[0])
                       irr2 = 'Is {} {}?'.format(
                           objects[irr_id], herethere[1])
                       if reversal:
                           r_true1 = 'Would {} be {}?'.format(
                               objects[t_id+1], herethere[0])
                           r_true2 = 'Would {} be {}?'.format(
                               objects[t_id], herethere[1])
                           r_false1 = 'Would {} be {}?'.format(
                               objects[t_id], herethere[0])
                           r_false2 = 'Would {} be {}?'.format(
                               objects[t_id+1], herethere[1])
                           r_irr1 = 'Would {} be {}?'.format(
                               objects[irr_id], herethere[0])
                           r_irr2 = 'Would {} be {}?'.format(
                               objects[irr_id], herethere[1])
                   # # Can add other relations later
                   # elif rel == 'IPdoing+spatial':
                   # elif rel == 'IPthinking+spatial':    
                   # elif rel == 'IPfeeling+spatial':    
                   # elif rel == 'IPthinking+temporal':
                   # elif rel == 'IPfeeling+temporal':
                   # elif rel == 'IPdoing+temporal':
                   # elif rel == 'IPthinking+temporal+spatial':
                   # elif rel == 'IPfeeling+temporal+spatial':
                   # elif rel == 'IPdoing+temporal+spatial':
                        
                    options = [true1, true2, false1, false2,
                               # irr1, irr2,
                               ]
                    correct = ['yes', 'yes','no', 'no', 
                               # 'no', 'no'
                               ]
                    revOptions = [r_true1, r_true2, r_false1, r_false2,
                                  # r_irr1, r_irr2,
                                  ]
                else:  # open format questions
                    if rel in ['interpersonal-thinking', 'interpersonal-feeling']:
                        if 'You' in iyou: # Account for caps in queries
                            iyou[list.index(list(iyou), 'You')] == 'you'
                        open1 = 'What do {} {}?'.format(iyou[0], deictics[d])
                        open2 = 'What do {} {}?'.format(iyou[1], deictics[d])
                        open3 = 'Who {}s {}?'.format(deictics[d], objects[t_id])
                        open4 = 'Who {}s {}?'.format(deictics[d], objects[t_id+1])
                        correct = [objects[t_id], objects[t_id+1], iyou[1], iyou[0]] # I-you reverses in open format
                        if reversal:
                            r_open1 = 'What would {} {}?'.format(iyou[0], deictics[d])
                            r_open2 = 'What would {} {}?'.format(iyou[1], deictics[d])
                            r_open3 = 'Who would {} {}?'.format(deictics[d], objects[t_id])
                            r_open4 = 'Who would {} {}?'.format(deictics[d], objects[t_id+1])
                            r_correct = [objects[t_id+1], objects[t_id], iyou[0], iyou[1]] # I-you reverses in open format
                    elif rel == 'interpersonal-doing':
                        iyou[list.index(list(iyou), 'Am I')] = 'am I' # adapt caps
                        iyou[list.index(list(iyou), 'Are you')] = 'are you' # adapt caps
                        open1 = 'What {} doing?'.format(iyou[0])
                        open2 = 'What {} doing?'.format(iyou[1])
                        open3 = 'Who is {}?'.format(objects[t_id])
                        open4 = 'Who is {}?'.format(objects[t_id+1])
                        iyou[list.index(list(iyou), 'am I')] = 'I' # adapt caps
                        iyou[list.index(list(iyou), 'are you')] = 'you' # adapt caps
                        correct = [objects[t_id], objects[t_id+1], iyou[1], iyou[0]] # I-you reverses in open format
                        if reversal:
                            revIyou[list.index(revIyou, 'Would I be')] = 'What would I be' # adapt caps
                            revIyou[list.index(revIyou, 'Would you be')] = 'What would you be' # adapt caps
                            r_open1 = '{} doing?'.format(revIyou[0])
                            r_open2 = '{} doing'.format(revIyou[1])
                            r_open3 = 'Who would be {}?'.format(objects[t_id])
                            r_open4 = 'What would be {}?'.format(objects[t_id+1])
                            revIyou[list.index(list(revIyou), 'What would I be')] = 'I' # adapt caps
                            revIyou[list.index(list(revIyou), 'What would you be')] = 'you' # adapt caps
                            r_correct = [objects[t_id+1], objects[t_id], iyou[0], iyou[1]] # I-you reverses in open format
                    elif rel == 'temporal':
                        if nowthen[0] in past:
                            open1 = 'What was {}?'.format(nowthen[0])
                            open2 = 'What is {}?'.format(nowthen[1])
                            open3 = 'When is {}?'.format(objects[t_id])
                            open4 = 'When is {}?'.format(objects[t_id+1])
                        elif nowthen[1] in past:
                            open1 = 'What is {}?'.format(nowthen[0])
                            open2 = 'What was {}?'.format(nowthen[1])
                            open3 = 'When is {}?'.format(objects[t_id])
                            open4 = 'When is {}?'.format(objects[t_id+1])
                        else: # no past tense
                            open1 = 'What is {}?'.format(nowthen[0])
                            open2 = 'What is {}?'.format(nowthen[1])
                            open3 = 'When is {}?'.format(objects[t_id])
                            open4 = 'When is {}?'.format(objects[t_id+1])
                        correct = [objects[t_id], objects[t_id+1], nowthen[0], nowthen[1]]
                        if reversal:
                            if nowthen[0] in past:
                                r_open1 = 'What would have been {}?'.format(nowthen[0])
                                r_open2 = 'What would be {}?'.format(nowthen[1])
                                r_open3 = 'When would {} be?'.format(objects[t_id])
                                r_open4 = 'When would {} be ?'.format(objects[t_id+1])
                            elif nowthen[1] in past:
                                r_open1 = 'What would be {}?'.format(nowthen[0])
                                r_open2 = 'What would have been {}?'.format(nowthen[1])
                                r_open3 = 'When would {} be?'.format(objects[t_id])
                                r_open4 = 'When would {} be ?'.format(objects[t_id+1])
                            else:
                                r_open1 = 'What would be {}?'.format(nowthen[0])
                                r_open2 = 'What would be {}?'.format(nowthen[1])
                                r_open3 = 'When would {} be?'.format(objects[t_id])
                                r_open4 = 'When would {} be ?'.format(objects[t_id+1])
                            r_correct = [objects[t_id+1], objects[t_id], nowthen[1], nowthen[0]]
                    elif rel == 'spatial':
                        open1 = 'Where is {}?'.format(objects[t_id])
                        open2 = 'Where is {}?'.format(objects[t_id+1])
                        open3 = 'What is {}?'.format(herethere[0])
                        open4 = 'What is {}?'.format(herethere[1])
                        correct = [herethere[0], herethere[1], objects[t_id], objects[t_id+1]]
                        if reversal:
                            r_open1 = 'Where would {} be?'.format(objects[t_id])
                            r_open2 = 'Where would {} be?'.format(objects[t_id+1])
                            r_open3 = 'What would {} be?'.format(herethere[t_id])
                            r_open4 = 'What would {} be?'.format(herethere[t_id+1])
                            r_correct = [herethere[1], herethere[0], objects[t_id+1], objects[t_id]]
                    options = [open1, open2, open3, open4]
                    
                    revOptions = [r_open1, r_open2, r_open3, r_open4]  
                    

# %%            # Build prompt by combining premises, task and queries


                # Manipulate wheter task is to select TRUE or FALSE statements
                if selectTF:
                    taskPremise = np.random.choice(['Select all statements that are correct.',
                                                    'Select all statements that are false.'])
                prompt = '{} and {}'.format(premise1, premise2)
                rPrems = ''
                
                # Randomly select input-specified number of questions/queries
                picks = np.random.choice(options, n_opt, replace = False)
                rpicks = np.random.choice(revOptions, n_opt, replace = False)
                corr = []
                rcorr = []
                for o in range(n_opt):
                    prompt = prompt + '\n{}: {}'.format(o+1, picks[o])
                    corr.append(correct[list.index(options, picks[o])])
                if reversal:
                    for o in range(n_opt):
                        rPrems = rPrems + '\n{}: {}'.format(o+1, rpicks[o])
                        if forcedChoice: rcorr.append(correct[list.index(revOptions, rpicks[o])])
                        else: rcorr.append(r_correct[list.index(revOptions, rpicks[o])])
                if selectTF and forcedChoice:
                    prompt = prompt + '\n{}'.format(taskPremise)
                # temp store data for regular prompt here
                prompts.append(prompt)
                types.append('Problem {} - Regular'.format(problem+1))
                responses.append(corr)
                
                if irrelevant:
                    irrPremise = irrPrems[np.random.randint(0,len(irrPrems))]
                    prompt = '{} and {} {}'.format(premise1, premise2,
                                                             irrPremise)
                    # recycle the same queries
                    for i in range(len(picks)):
                        prompt = prompt + '\n{}: {}'.format(i+1,picks[i])
                    if selectTF:
                        prompt = prompt + '\n{}'.format(taskPremise)
                    prompts.append(prompt)
                    types.append('Problem {} + Irrelevant'.format(problem+1))
                    responses.append(corr)
                if reversal:
                    if selectTF and forcedChoice:
                        prompt = '{} and {} {} {} \n{}'.format(premise1, premise2,
                                                          reversalPremise, rPrems, taskPremise)
                    else:
                        prompt = '{} and {} {} {}'.format(premise1, premise2,
                                                              reversalPremise, rPrems)
                    prompts.append(prompt)
                    types.append('Problem {} Reversal'.format(problem+1))
                    responses.append(rcorr)
                if reversal and irrelevant:
                    irrPremise = irrPrems[np.random.randint(0,len(irrPrems))]
                    if selectTF and forcedChoice: # Only makes sense for forced-choice problems.
                        prompt = '{} and {} {} {} {} \n{}'.format(premise1, premise2,
                                                                irrPremise,
                                                                reversalPremise, rPrems,
                                                                taskPremise)
                    else:
                        prompt = '{} and {} {} {} {}'.format(premise1, premise2,
                                                                irrPremise,
                                                                reversalPremise, rPrems)
                    
                    # temp store reversal + irrelevant prompt data here
                    prompts.append(prompt)
                    types.append('Problem {} Reversal + Irrelevant'.format(problem+1))
                    responses.append(rcorr)
            
            for i in range(len(prompts)): # update trial data after iterations of problem
               if reversal and irrelevant:  # Creates reversed for each type, so can loop uneven
                   if i % 4 == 0:  # four versions of each problem
                       trial_data['premises'].append([premise1, premise2])
                   elif i %4 == 1:  # first both
                       trial_data['premises'].append(
                           [premise1, premise2, irrPremise, rPrems])
                   elif i %4 == 2:  # then reversal only
                       trial_data['premises'].append(
                           [premise1, premise2, rPrems])
                   elif i %4 == 3:  # then irrelevant only
                       trial_data['premises'].append(
                           [premise1, premise2, irrPremise])
               elif irrelevant or reversal:
                   if i % 2 == 0:  # two versions of each problem
                       trial_data['premises'].append([premise1, premise2])
                   else:  # reversal trials
                       if irrelevant:
                           trial_data['premises'].append(
                               [premise1, premise2, irrPremise])
                       else:
                           trial_data['premises'].append(
                               [premise1, premise2, rPrems])
               trial_data['prompt'].append(prompts[i])
               # trial_data['domain'].append('IP-')
               trial_data['type'].append(types[i])
               trial_data['correct'].append(responses[i])
# %% Add trial id's and print list of trials if required
    # Add trial IDs
    for tr in range(len(trial_data['prompt'])):
        trial_data['id'].append(tr+1)
    
    if printTrials:
        for trial in range(len(trial_data['prompt'])):
            answers = ''
            for a in range(len(trial_data['correct'][trial])):
                answers = answers + '{} - {}; '.format(a, trial_data['correct'][trial][a])
            print('Trial {} ({}): {} \nAnswers: {}; \n'.format(trial+1, trial_data['type'][trial],
                                                                 trial_data['prompt'][trial],
                                                                 answers))            
    return trial_data