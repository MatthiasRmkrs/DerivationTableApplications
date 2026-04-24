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
    
TO DO:
    - Comments, description, cleanup, transfer to OG script
    - ADD open Qs for combined relations and wrap in function
    - Add Dutch translation
    -...
@author: mraemaek
"""

# Dependencies
import numpy as np
import pandas as pd
import pdb
from derTables.utils_deictics import ( # helpers for formatting deictic relational responding problems
    resolve_relations,
    normalize_pair,
    build_premises,
    build_deictic_option_sets,
    build_irrelevant_context,
    _append_labjs_options,
    _convert_selecttf,
    append_row,
    append_rows,
    emit_mc_trial,
    emit_single_option_trials,
    _correct_subset_for_picks,
    _pick_task_premise,
    _options_to_prems_block
)
# note that default labels to use in problems are now defined in resolve_relations()
# function in utils!


#   Define function
def generateDeicticSyllogisms2(relations, n_rep, reversal, allReversals,
                               irrelevant, forcedChoice, n_opt, printTrials, output = None):
    rng = np.random.default_rng() 
    
    # Initialise dict and counters
    trial_data = {'id': [], 
                  'Premises': [], 
                  'Relations': [], 
                  'Prompt': [],
                  'Correct': [], 
                  'Type': [], 
                  'n_p': [], 
                  'Derivation': [],
                  'pPrems': [], 
                  'pCorrect': []
                  }
    output = output or "default" # default output format if not specified
    if output == "labjs": # some additional columns for running/presenting task in labjs
        trial_data["taskPremise"] = []
        trial_data["Premise1"] = []
        trial_data["Premise2"] = []
        trial_data["extraPremises"] = []
        for i in range(n_opt):
            trial_data[f"option{i+1}"] = []
    if output in ("csv", "default"):
        trial_data["t_options"] = []
        

    t = -1 # init trial index
    problem = -1 # init counter for unique problems (premises)
    
    # get default pronouns and objects for problelms if not provided by user
    specs = resolve_relations(relations)
    # Past tense markers (used in a few prompt variants)
    past = ['yesterday', 'last week', 'last year']
    for rel, spec in specs.items(): # Lopp deictic relations specified in input
        # get relevant specs for current relation
        ip = spec["ip"] # e.g., I/You
        temporal = spec["temporal"] # e.g., now/then
        spatial = spec["spatial"] # e.g., here/there
        objects = spec["objects"] # objects
        if ip:
            deictics = ip["present"]
            pastdeictics = ip["past"]

        # Normalize temporal/spatial pairs so downstream code can treat them as simple 2-item lists
        nowthen = normalize_pair(temporal) if temporal is not None else None
        herethere = normalize_pair(spatial) if spatial is not None else None

        # don't need the below?
        if output == 'labjs':
            option_cols = [[] for _ in range(n_opt)] 



        for r in range(n_rep): # Loop repetitions of each trial type
            problem += 1 # Update problem ID - unique premises
            # determine id for verbs/objects in loop
            t_id = 2*r
            if t_id +1 >= len(objects): # account for overindexing
                loop = int(np.round(t_id/len(objects)))
                t_id -= loop*len(objects) # cycle back through list
            
                        
            # create irrelevant problem context: irrelevant premise and stimulus/id
            irr_ctx = build_irrelevant_context(
                irrelevant=irrelevant,
                objects=objects,
                t_id=t_id,
                rng=rng,
            )
            irrPrems = irr_ctx["irrPrems"]
            irr_id = irr_ctx["irr_id"]
                           
            # (2) Build problem premises
            premise1, premise2, ctx = build_premises(
                rel=rel,
                spec=spec,
                t_id=t_id,
                r=r,
                rng=rng,
            )
            d = ctx["d"]
            # if later code still expects these names
            # can be removed???
            iyou = ctx["iyou"]
            nowthen = ctx["nowthen"]
            herethere = ctx["herethere"]
            
            # Base prompt stem
            prompt_stem = f"{premise1}. {premise2}"

            # (3) Build queries depending on response format:
            
            if forcedChoice:  # Y/N queries (options are generated programmatically now)
                deictic_verb = None
                if ip and ip.get('type') in ('thinking', 'feeling'):
                    deictic_verb = deictics[d]

                optset = build_deictic_option_sets(
                    rel=rel,
                    ip=ip,
                    temporal=nowthen,
                    spatial=herethere,
                    objects=objects,
                    iyou=list(iyou),
                    deictic_verb=deictic_verb,
                    t_id=t_id,
                    irr_id=irr_id,
                    reversal=reversal,
                    allReversals=allReversals,
                    past_words=past,
                )
                
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
                        r_open3 = 'What would be {}?'.format(herethere[t_id])
                        r_open4 = 'What would be {}?'.format(herethere[t_id+1])
                        r_correct = [herethere[1], herethere[0], objects[t_id+1], objects[t_id]]
                
                ### CAN DO OTHER COMBINATIONS LATER, want to test forced/multiple choice primarily
                
                options = [open1, open2, open3, open4]
                
                revOptions = [r_open1, r_open2, r_open3, r_open4]  
                

            # (4) Build prompt by combining premises, task and queries

            
            # Manipulate wheter task is to select TRUE or FALSE statements
                
            base_options = optset["options"]
            base_correct = optset["correct"]

            # Reversal structures created inside build_deictic_option_sets
            rev_dict = optset.get("reversals", {})          # key -> {"premise":..., "type":...}
            key_orders = optset.get("reversal_key_orders", {})  # level -> [keys...]
            taskPremise = '' # stable
            # ---------------- Base (Regular) ----------------
            if n_opt == 1:
                rows = emit_single_option_trials(
                    premise1 = premise1,
                    premise2 = premise2,
                    trial_type_yes="Regular",
                    trial_type_no="Incorrect",
                    options_pool = base_options,
                    correct_pool = base_correct,
                    extra_premises = None,
                    output = output
                )
                for row in rows:
                    row["Relations"] = [rel]
                append_rows(trial_data, rows, output=output, n_opt=n_opt)
            else:
                if forcedChoice: taskPremise = _pick_task_premise(rng=rng)
                rows = emit_mc_trial(
                    premise1 = premise1,
                    premise2 = premise2,
                    trial_type="Regular",
                    options_pool = base_options,
                    correct_pool = base_correct,
                    extra_premises = None,
                    n_opt = n_opt,
                    output = output,
                    taskPremise = taskPremise,
                    forcedChoice = forcedChoice,
                    rng = rng
                )
                rows["Relations"] = [rel]
                append_row(trial_data, rows, output=output, n_opt=n_opt)
            # ---------------- Irrelevant (base) ----------------
            if irrelevant:
                irrPremise = rng.choice(irrPrems) if irrPrems else ""
                irr_stem = f"{premise1}. {premise2} {irrPremise}".strip()

                if n_opt == 1:
                    rows = emit_single_option_trials(
                        premise1 = premise1,
                        premise2 = premise2,
                        trial_type_yes="Irrelevant",
                        trial_type_no="Irrelevant Incorrect",
                        options_pool=base_options,
                        correct_pool=base_correct,
                        extra_premises=[irrPremise] if irrPremise else None,
                        output = output,
                    )
                    for row in rows:
                        row["Relations"] = [rel]
                    append_rows(trial_data, rows, output=output, n_opt=n_opt)
                else:
                    if forcedChoice: taskPremise = _pick_task_premise(rng=rng)
                    rows = emit_mc_trial(
                        premise1 = premise1,
                        premise2 = premise2,
                        trial_type="Irrelevant",
                        options_pool = base_options,
                        correct_pool = base_correct,
                        extra_premises=[irrPremise] if irrPremise else None,
                        n_opt = n_opt,
                        output = output,
                        taskPremise = taskPremise,
                        forcedChoice = forcedChoice,
                        rng = rng
                    )
                    rows["Relations"] = [rel]
                    append_row(trial_data, rows, output=output, n_opt=n_opt)
            # ---------------- Reversals ----------------
            if reversal:
                for level in (1, 2, 3):
                    for key in key_orders.get(level, []):
                        if key not in rev_dict:
                            raise KeyError(f"{rel}: key_orders requested '{key}', but rev_dict only has {list(rev_dict.keys())}")
                        info = rev_dict[key]
                        reversalPremise = info["premise"]
                        revType = info["type"]

                        # Option pools live in legacy fields as concatenated 4-item blocks.
                        # build_deictic_option_sets already concatenated them per key order.
                        # We re-derive the appropriate pool slice by using the helper inside that function,
                        # but since we don't have direct access here, we rely on optset's legacy fields:
                        if level == 1:
                            options_pool = optset.get("revOptions") or []
                            correct_pool = optset.get("r_correct") or []
                            block_index = list(key_orders.get(1, [])).index(key)
                        elif level == 2:
                            options_pool = optset.get("rev2Options") or []
                            correct_pool = optset.get("rr_correct") or []
                            block_index = list(key_orders.get(2, [])).index(key)
                        elif level == 3:
                            options_pool = optset.get("rev3Options") or []
                            correct_pool = optset.get("rrr_correct") or []
                            block_index = list(key_orders.get(3, [])).index(key)
                        else:
                            continue

                        # Slice out the 4-option block for this key
                        start = 4 * block_index
                        end = start + 4
                        block_opts = options_pool[start:end]
                        block_corr = correct_pool[start:end]

                        rev_stem = f"{premise1}. {premise2} {reversalPremise}".strip()

                        if n_opt == 1:
                            rows = emit_single_option_trials(
                                premise1 = premise1,
                                premise2 = premise2,
                                trial_type_yes=revType,
                                trial_type_no=f"{revType} Incorrect",
                                options_pool=block_opts,
                                correct_pool=block_corr,
                                extra_premises=[reversalPremise] if reversalPremise else None,
                                output = output
                            )
                            for row in rows:
                                row["Relations"] = [rel]
                            append_rows(trial_data, rows, output=output, n_opt=n_opt)
                        else:
                            if forcedChoice: taskPremise = _pick_task_premise(rng=rng)
                            rows = emit_mc_trial(
                                premise1 = premise1,
                                premise2 = premise2,
                                trial_type = revType,
                                options_pool = block_opts,
                                correct_pool = block_corr,
                                extra_premises=[reversalPremise] if reversalPremise else None,
                                n_opt = n_opt,
                                output = output,
                                taskPremise = taskPremise,
                                forcedChoice = forcedChoice,
                                rng = rng
                            )
                            rows["Relations"] = [rel]
                            append_row(trial_data, rows, output=output, n_opt=n_opt)

                        # Reversal + irrelevant
                        if irrelevant:
                            irrPremise = rng.choice(irrPrems) if irrPrems else ""
                            stem2 = f"{premise1}. {premise2} {irrPremise} {reversalPremise}".strip()
                            type2 = f"{revType} + Irrelevant"

                            if n_opt == 1:
                                rows = emit_single_option_trials(
                                    premise1 = premise1,
                                    premise2 = premise2,
                                    trial_type_yes=type2,
                                    trial_type_no=f"{type2} Incorrect",
                                    options_pool=block_opts,
                                    correct_pool=block_corr,
                                    extra_premises=[irrPremise, reversalPremise] if irrPremise else [reversalPremise],
                                    output = output
                                )
                                for row in rows:
                                    row["Relations"] = [rel]
                                append_rows(trial_data, rows, output=output, n_opt=n_opt)
                            else:
                                if forcedChoice: taskPremise = _pick_task_premise(rng=rng)
                                rows = emit_mc_trial(
                                    premise1 = premise1,
                                    premise2 = premise2,
                                    trial_type = type2,
                                    options_pool = block_opts,
                                    correct_pool = block_corr,
                                    extra_premises=[irrPremise, reversalPremise] if irrPremise else [reversalPremise],
                                    n_opt = n_opt,
                                    output = output,
                                    taskPremise = taskPremise,
                                    forcedChoice = forcedChoice,
                                    rng = rng
                                )
                                rows["Relations"] = [rel]
                                append_row(trial_data, rows, output=output, n_opt=n_opt)
            
    # %% Add trial id's and print list of trials if required
    # Add trial IDs
    for tr in range(len(trial_data['Prompt'])):
        trial_data['id'].append(tr+1)
    
    trial_data = pd.DataFrame.from_dict(trial_data)
    
    if printTrials:
        for trial in range(len(trial_data['Prompt'])):
            if n_opt == 1:
                answers = trial_data['pCorrect'][trial]
                print('Trial {} ({}): {} \nAnswer: {} \n'.format(trial+1, trial_data['Type'][trial],
                                                                     trial_data['Prompt'][trial],
                                                                     answers))          
            else:
                answers = ''
                for a in range(len(trial_data['pCorrect'][trial])):
                    answers += '{} - {}; '.format(a, trial_data['pCorrect'][trial][a])
                print('Trial {} ({}): {} {} \nAnswers: {}; \n'.format(trial+1, trial_data['Type'][trial],
                                                                     trial_data['Prompt'][trial], trial_data['pPrems'][trial],
                                                                     answers))            
    return trial_data