# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 08:23:48 2024

Test LLMs on deictic reasoning syllogisms

1) Specify the task to create with custom function: 
    - which deictic relations to test (interpersonal, temporal, spatial, combinations thereof)
        -> Specify lists of verbs, objects to include in different relations
    - what types of trials to include (reversal, irrelevant premises, ...)
    - Query/response format (forced choice Y/N or open format)
--> Then create a set of trials to loop models on.

2) Select models to test, set up csv writer and/or storage array
    
3) Loop different models through task and store
@author: mraemaek

"""

#%% Import dependencies and set API
import numpy as np
import os
import csv 
from together import Together
from datetime import datetime
import pdb
import pandas as pd
from derTables.generateDeicticSyllogisms import generateDeicticSyllogisms2
import matplotlib.pyplot as plt


client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

#for deictic relations
thinking = ['think', 'believe']# Interpersonal feeling: 
past_think = ['thought'] 
thoughts = ['cats are fun', 'dogs are fun', 'ducks are superior', 'mosquitos suck',
            'psychology is fun', 'homework is lame', 'Trump is stupid', 'Harris is smart',
            'the beach is nice', 'mountains are cool', 'ice cream is better than cookies', 'cookies are better than ice cream',
            'MacDonalds is disgusting', 'MacDonalds is amazing', 'MacDonalds is good', "Wendy's is better",
            'AI is cool', 'AI is scary', 'football is fun', 'football is stupid'
            ]

feeling = ['feel'] # Interpersonal feeling: 
past_feelings = ['felt']
feelings = ['happy', 'sad', 'angry', 'confused', 
            'scared', 'safe', 'cold', 'warm', 'hot', 'cold',
            'sick', 'dizzy', 'happy', 'angry', 'nauseous', 'fine',
            'great', 'sad', 'dissapointed', 'sad', 'awfull', 'guilty'
            ]

doing = ['doing'] # Interpersonal 'doing' relations
actions = ['sitting on a red chair', 'sitting on a blue chair',
            'playing chess', 'playing outside',
            'drinking a coke', 'feeding the cat',
            'playing videogames', 'reading a book',
            'cleaning', 'cooking',
            'playing football', 'playing tennis', 'watching television', 'reading a magazine'
            'playing videogames', 'cooking', 'feeding the cat', 'cleaning the kitchen' 
            'sitting on a red chair', 'sitting on a black chair', 'sitting on a blue chair', 'sitting on a black chair',
           ]

# Temporal relations (now-then)
times = [['today', 'yesterday'], 
          # ['today', 'tomorrow'], ['yesterday', 'tomorrow'], ['last week', 'this week'], 
          # ['last week', 'next week'], ['this week', 'next week'], ['tomorrow', 'next week'],
          # ['last week', 'tomorrow'], ['yesterday', 'last week'], ['last week', 'today'], 
          # ['yesterday', 'next week'], ['this week', 'yesterday'], ['yesterday', 'this week']
         ]
events = ['the opening of the new shop', 'the start of the academic year',
          'my birthday', 'your birthday', 'the first day of school', 
          'my birthday', "John's birthday", 
            'the festival', 'the closing of the old shop',
           'the opening of the new shop', 'the closing of the old shop',
           'Christmas', 'my birthday', 
           'Easter', 'the final of the Voice', 
           'the opening of the new supermarket', 'your birthday',
           "mom's birthday", "dad's birthday",
           "the first day of the year", 'game night'
          ]
# Spatial relations (here-there)
# Premise: 'A is here and B is there' -> Qq: Is A/B here/there?"/"Where is A/B?"
places = [['here', 'there'],
           # ['in the store', 'at home'], ['at the pool', 'in the gym']
          ] # others? 

things = ['the red chair', 'the blue chair', 'the pharmacy', 'the grocery store',
          'the school', 'my home', 'the bank', 'the supermarket',
          'my wallet', 'my keys', 'the bus stop', 'the post office',
          ' the chair', 'the table', 'the green chair', 'the red chair',
          'my book', 'my bag', 'my cup', 'your cup']

# %%

# Specify relations to test
relations = dict({
                'interpersonal-thinking': [thinking, thoughts], 
                'interpersonal-feeling': [feeling, feelings],
                'interpersonal-doing': [doing, actions],
                'temporal': [times, events],
                'spatial': [places, things],
                # 'temporal+spatial': [things, times, places],
                # 'IPthinking+temporal': [thinking, past_think, thoughts, times],
                # 'IPfeeling+temporal': [feeling, past_feelings, feelings, times],
                # 'IPdoing+temporal': [doing, actions, times],
                # 'IPthinking+spatial': [thinking, thoughts, places], # Maybe a little weird?7
                # 'IPfeeling+spatial': [feeling, feelings, places], # Maybe a little weird?
                # 'IPdoing+spatial': [doing, actions, places],
                # 'IPthinking+temporal+spatial': [thinking, past_think, thoughts, times, places],
                # 'IPfeeling+temporal+spatial': [feeling, past_feelings, feelings, times, places],
                # 'IPdoing+temporal+spatial': [doing, actions, times, places]
})
# Specify task characteristics
n_reps = 15  # Repetitions of relations
reversal = True
allReversals = True
irrelevant = True
printTrials = True
forcedChoice = True  # Open (False) or forced choice (True)
n_opt = 3
selectTF = True
csv_file = 'LlamaModels_FullDeictic.csv'
output = 'labjs' 
# trial_data = generateDeicticSyllogisms(relations, n_reps, reversal, irrelevant, forcedChoice, printTrials)
trial_data_1dim = generateDeicticSyllogisms2(relations, n_reps, reversal, allReversals,
                                        irrelevant, forcedChoice, n_opt, printTrials, selectTF, output)
# %% Create trial set

# general settnigs
reversal = True
reversal2 = True
reversal3 = True
allReversals = True
irrelevant = False
printTrials = True
forcedChoice = True  # Open (False) or forced choice (True)
n_opt = 3
selectTF = True
csv_file = 'LlamaModels_FullDeictic.csv'
output = 'labjs' 

# Specify relations to test
relations_1dim_ip = dict({
                'interpersonal-thinking': [thinking, thoughts], 
                'interpersonal-feeling': [feeling, feelings],
                'interpersonal-doing': [doing, actions]})
relations_1dim = dict({
                'temporal': [times, events],
                'spatial': [places, things]
})
relations_2dim = dict({
                # 'temporal+spatial': [things, times, places],
                'IPthinking+temporal': [thinking, past_think, thoughts, times],
                'IPfeeling+temporal': [feeling, past_feelings, feelings, times],
                'IPdoing+temporal': [doing, actions, times],
                'IPthinking+spatial': [thinking, thoughts, places], # Maybe a little weird?7
                'IPfeeling+spatial': [feeling, feelings, places], # Maybe a little weird?
                'IPdoing+spatial': [doing, actions, places]
})
relations_3dim = dict({
                'IPthinking+temporal+spatial': [thinking, past_think, thoughts, times, places],
                'IPfeeling+temporal+spatial': [feeling, past_feelings, feelings, times, places],
                'IPdoing+temporal+spatial': [doing, actions, times, places]
})

# combine trials
blocks = {'1dim': relations_1dim,
          '1dim_ip': relations_1dim_ip,
          '2dim': relations_2dim,
          '3dim': relations_3dim
          }
reps = {'1dim': 1,
        '1dim_ip': 1,
          '2dim': 1,
          '3dim': 1
          }
trial_data_combined = dict()
t =-1
for block, rels in blocks.items():
    t+=1
    relations = rels
    n_reps = reps[block]
    trial_data = generateDeicticSyllogisms2(relations, n_reps, reversal, allReversals,
                                            irrelevant, forcedChoice, n_opt, printTrials, output)
    
    # combine all block data
    if not trial_data_combined:
        trial_data_combined = {k: list(v) for k, v in trial_data.items()}
    else:
        prev_len = len(next(iter(trial_data_combined.values()))) # align
        for k in trial_data.keys(): # check for new keys
            if k not in trial_data_combined:
                trial_data_combined[k] = [None] * prev_len
        for k in trial_data_combined.keys(): # check for missing keys
            if k not in trial_data:
                trial_data[k] = [None] * len(trial_data.get('id', next(iter(trial_data.values()))))
   
        for k, v in trial_data.items(): # extend dict
            trial_data_combined[k].extend(v)
            
# %% for testing new updated generator function
import numpy as np
import pdb
import pandas as pd
from derTables.utils_deictics import * 
from derTables.generateDeicticSyllogisms import generateDeicticSyllogisms2

relations = [
    'interpersonal-doing',
    'interpersonal-thinking', 
    'interpersonal-feeling',
    'temporal',
    'spatial',
    'temporal+spatial',
    'IPthinking+temporal',
    'IPfeeling+temporal',
    'IPdoing+temporal',
    'IPthinking+spatial', # Maybe a little weird?7
    'IPfeeling+spatial', # Maybe a little weird?
    'IPdoing+spatial',
    'IPthinking+temporal+spatial', 
    'IPfeeling+temporal+spatial',
    'IPdoing+temporal+spatial'
]
n_reps = 5
reversal = True
allReversals = False
irrelevant = False
forcedChoice = True
n_opt = 3
printTrials = True
output = 'labjs'
csv_file = "MorganeTestTrials.csv"
trial_data = generateDeicticSyllogisms2(relations, n_reps, reversal, allReversals,
                                        irrelevant, forcedChoice, n_opt, printTrials, output)

trial_data_df = pd.DataFrame.from_dict(trial_data) # create pandas dataframe
trial_data_df.to_csv(csv_file) # store in csv for later use
  # %% Select models & set filename to store data

filename = 'Meta8Bvs405B_DeicticRelations.csv'

# Can select form all models available on Together, listed below
models = [
          # "zero-one-ai/Yi-34B-Chat",
          # "Austism/chronos-hermes-13b",
          # "cognitivecomputations/dolphin-2.5-mixtral-8x7b",
          # "databricks/dbrx-instruct",
          # "deepseek-ai/deepseek-coder-33b-instruct",
          # "deepseek-ai/deepseek-llm-67b-chat",
          # "garage-bAInd/Platypus2-70B-instruct	"
          # "google/gemma-2b-it",
          # #"google/gemma-7b-it",
          # "Gryphe/MythoMax-L2-13b",
          # "lmsys/vicuna-13b-v1.5",
          # "lmsys/vicuna-7b-v1.5",
          # "codellama/CodeLlama-13b-Instruct-hf",
          # "codellama/CodeLlama-7b-Instruct-hf",
          # "codellama/CodeLlama-34b-Instruct-hf",
          # "codellama/CodeLlama-70b-Instruct-hf",
          # "meta-llama/Llama-2-7b-chat-hf",
          # "meta-llama/Llama-2-13b-chat-hf",
          # "meta-llama/Llama-2-70b-chat-hf",
          # "meta-llama/Llama-3-8b-chat-hf",
          # "meta-llama/Llama-3-70b-chat-hf",
           # "meta-llama/Meta-Llama-3-8B-Instruct-Turbo", # Often produces strange responses...
           # "meta-llama/Meta-Llama-3-70B-Instruct-Turbo", 
           "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
           # "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", 
           "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
          # "mistralai/Mistral-7B-Instruct-v0.1",
          # "mistralai/Mistral-7B-Instruct-v0.2",
          # "mistralai/Mistral-7B-Instruct-v0.3",
          # "mistralai/Mixtral-8x7B-Instruct-v0.1",
          # "mistralai/Mixtral-8x22B-Instruct-v0.1",
          # "NousResearch/Nous-Capybara-7B-V1p9"
          # "NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
          # "NousResearch/Nous-Hermes-2-Mistral-8x7B-DPO",
          # "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT",
          # "NousResearch/Nous-Hermes-llama-2-7b",
          # "NousResearch/Nous-Hermes-Llama-2-13b",
          # "NousResearch/Nous-Hermes-2-Yi-34B",
          # "openchat/openchat-3.5-1210",
          # "Open-Orca/Mistral-7B-OpenOrca",
          # "Qwen/Qwen1.5-0.5B-Chat",
          # "Qwen/Qwen1.5-1.8B-Chat",
          # "Qwen/Qwen1.5-4B-Chat",
          # "Qwen/Qwen1.5-7B-Chat",
          # "Qwen/Qwen1.5-14B-Chat",
          # "Qwen/Qwen1.5-32B-Chat",
          # "Qwen/Qwen1.5-72B-Chat",
          # "Qwen/Qwen1.5-110B-Chat",
          # "Qwen/Qwen2-72B-Instruct",
          # "snorkelai/Snorkel-Mistral-PairRM-DPO",
          # "Snowflake/snowflake-arctic-instruct",
          # "togethercomputer/alpaca-7b",
          # "teknium/OpenHermes-2-Mistral-7B",
          # "teknium/OpenHermes-2p5-Mistral-7B",
          # "togethercomputer/Llama-2-7B-32K-Instruct",
          # "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
          # "togethercomputer/RedPajama-INCITE-7B-Chat",
          # "togethercomputer/StripedHyena-Nous-7B",
          # "teknium/OpenHermes-2p5-Mistral-7B",
          # "Undi95/ReMM-SLERP-L2-13B",
          # "Undi95/Toppy-M-7B",
          # "WizardLM/WizardLM-13B-V1.2",
          # "upstage/SOLAR-10.7B-Instruct-v1.0"
          ]

# %% Loop models through task and store data

# Will need to adapt somewhat to trial_data structure, write to csv only after loop?

# # # open csv file to write data to
# csv_file = 'MetaLlaMaModelComparison-Comparative3premises.csv' 
# f = open(csv_file, 'w')
# # create csv writer
# writer = csv.writer(f)
# # write header to csv file
# header = ['rowid', 'model_id', 'model', 'Timestamp', 'choiceSeed', 'Temperature', 
#                'Prompt', 'promptType', 'n_prem', 'relations', 
#                'correctResponse', 'modelResponse', 'accuracy']
# writer.writerow(header)

# backup dict to avoid issues with csv missing rows?
data_runs = dict({'rowid': [],'prompt':[], 'correctResponse':[], 'modelResponse': [],
                  'model_id':[], 'model':[], 'promptType':[],'domain':[],
                  # 'accuracy':[], # temporary untill robust way to compute
                  'choiceSeed':[]})

# Loop model through task
rowid =  0
for m in range(len(models)):
    for p in range(len(trial_data['id'])):
        temp = 0
        stream = client.chat.completions.create(
          model=models[m],
          messages=[{"role": "system", 
                     "content": "You will be given some information and asked two questions. \
                         Answer with yes or no only, in the order of the questions \
                             and with a space in between your responses, no punctuation is needed."},
                     {"role": "user", "content": trial_data['prompt'][p]}],
          stream=False, temperature= temp,
          )
        
        # for chunk in stream:
        #     print(chunk.choices[0].delta.content or "", end="", flush=True)
        
        rowid = rowid + 1
        prompt = trial_data['prompt'][p]
        correctResponse = trial_data['correct'][p]
        modelResponse = stream.choices[0].message.content
        if modelResponse[-1] == '.': # Account for punctuation (even w system prompt?)
            modelResponse = modelResponse[:-1]
        elif modelResponse[0] == ' ': # Mixtral answers after a space...
            modelResponse = modelResponse[1:]
        choiceSeed = stream.choices[0].seed
        # accuracy = modelResponse.lower() == trial_data['correct'][p].lower()
            # Need to see how to do this best with the multiple queries and all
        model_id = stream.id
        model = stream.model
        promptType = trial_data['type'][p]
        domain = trial_data["domain"][p]
        row = [rowid, model_id, model, datetime.now(), choiceSeed, temp, 
               prompt, promptType, domain, correctResponse, modelResponse, 
               # accuracy
               ]
        print(row)
        # writer.writerow(row)
        # Store in backup dict also
        data_runs['rowid'].append(rowid)
        data_runs['prompt'].append(prompt)
        data_runs['correctResponse'].append(correctResponse)
        data_runs['modelResponse'].append(modelResponse)
        data_runs['model_id'].append(model_id)
        data_runs['model'].append(model)
        data_runs['promptType'].append(promptType)
        data_runs['domain'].append(domain)
        # data_runs['accuracy'].append(accuracy)
        data_runs['choiceSeed'].append(choiceSeed)
        

data_runs = pd.DataFrame(data_runs)
data_runs.to_csv(filename)
  
# %% Some basic performance assessment

# Load data and select relevant variables, group and compute mean acc
# data = pd.read_csv() 
data = pd.DataFrame.from_dict(data_runs)

data_accXdomain = data[["model", "domain", "modelResponse", 'correctResponse']]
# temporary calculation of accuracy

#### NOT WORKING rn
accuracy = []
tr = -1
for t in data["modelResponse"]:
    tr +=1
    mid = int(len(t)/2)
    acc = 0
    if data["correctResponse"][tr][0] in t[0:mid].lower(): acc +=1 
    if data["correctResponse"][tr][1] in t[mid:].lower(): acc +=1 
    accuracy.append(acc/2) # transform to 0-1 scale
    
data_accXdomain.insert(4,"accuracy", accuracy) # add column

grouped = data_accXdomain.groupby(['model', 'domain']).agg(
    mean_acc=('accuracy', 'mean'),
    se_acc=('accuracy', lambda x: np.std(x, ddof=1) / np.sqrt(len(x)))
).reset_index()

# Bar plot
# Clean up model labels for plot
models = grouped['model'].unique()
domains = grouped['domain'].unique()
modelLabs = []
for m in range(len(models)):
    # Extract model name from path string
    model = models[m][str.index(models[m], '/')+1:]

    if 'Instruct-Turbo'.lower() in models[m].lower():
            modelLabs.append(model.replace('Instruct-Turbo'.lower(), 'IT'))
    elif 'Instruct-v0.1'.lower() in models[m].lower():
            modelLabs.append(model.replace('Instruct'.lower(), 'I'))

fig, ax = plt.subplots(figsize=(8, 6))

# Creating separate bars for each 
index = np.arange(len(domains))
width = 0.1 # bars
multiplier = 0

for i, m in enumerate(models):
    model_data = grouped[grouped['model'] == m]
    ax.bar(
        index + i * width,
        model_data['mean_acc'],
        width,
        label=modelLabs[i],
        # Also plot error bars
        yerr=model_data['se_acc'],  # Add error bars (SEM)
        capsize=5  # Error bar caps
    )

# Step 3: Customize the plot
ax.set_xlabel('Deictic Responding Domain') 
ax.set_ylabel('Mean Accuracy (%)')
ax.set_title('Deictic Syllogism Performance by Model and Type of Deictic Relation')
ax.set_xticks(index + (len(models)*width)/2.5) # WHY 2.5?? Feel like it should be 2 to be halfway?
ax.set_xticklabels(domains)
ax.legend(title = "Model", loc='upper left', ncols=2, labels = modelLabs)
ax.set_ylim(0, 1.2)
plt.tight_layout()

# Show plot
plt.show()

#%% Plot accuracy by model and problem type 
# Performance on trials with incorrect response prompt, irrelevant premises, .. vs. normal

data_accXtypes = data[["model", "promptType", "domain"]] 
data_accXtypes.insert(len(data_accXtypes.keys()),"accuracy", accuracy)


# (temp?) NEED TO EDIT TYPES FIRST TO REMOVE 'PROBLEM x' (and 'correct'?)
ttypes = []
for t in data_accXtypes["promptType"]:
    if 'Reversal' in t and 'Irrelevant' in t:
        ttypes.append('Reversal + Irrelevant')
    elif 'Reversal'in t and 'Irrelevant' not in t:
        ttypes.append('Reversal')
    elif 'Irrelevant'in t and 'Reversal' not in t:
        ttypes.append('Irrelevant')
    else:
        ttypes.append('Regular')

data_accXtypes.insert(len(data_accXtypes.keys()),"type", ttypes)

grouped = data_accXtypes.groupby(['model', 'type', 'domain']).agg(
    mean_acc=('accuracy', 'mean'),
    se_acc=('accuracy', lambda x: np.std(x, ddof=1) / np.sqrt(len(x)))
).reset_index()

# Bar plot
# Clean up model labels for plot
models = grouped['model'].unique()
types = grouped['type'].unique()
modelLabs = []
for m in range(len(models)):
    # Extract model name from path string
    model = models[m][str.index(models[m], '/')+1:]

    if 'Instruct-Turbo'.lower() in models[m].lower():
            modelLabs.append(model.replace('Instruct-Turbo'.lower(), 'IT'))
    elif 'Instruct-v0.1'.lower() in models[m].lower():
            modelLabs.append(model.replace('Instruct'.lower(), 'I'))


# Creating separate bars for each 
index = np.arange(len(types))
width = 0.1  # bars
multiplier = 0

for d in range(len(domains)):
    fig, ax = plt.subplots(figsize=(8, 6))
    for i, m in enumerate(models):
        model_data = grouped[grouped['model'] == m]
        dmodel_data = model_data[model_data['domain'] == domains[d]]
        ax.bar(
            index + i * width,
            dmodel_data['mean_acc'],
            width,
            label=modelLabs[i],
            # Also plot error bars
            yerr=dmodel_data['se_acc'],  # Add error bars (SEM)
            capsize=5  # Error bar caps
        )
    
    # Step 3: Customize the plot
    ax.set_xlabel('Trial Type') 
    ax.set_ylabel('Mean Accuracy (%)')
    ax.set_title('Deictic {} Syllogism Performance by Trial Type'.format(domains[d]))
    ax.set_xticks(index + (len(models)*width)/ 2.5)
    ax.set_xticklabels(types)
    ax.set_ylim(0, 1.2)
    plt.tight_layout()

    ax.legend(title = "Model", loc='upper left', ncols=2, labels = modelLabs)
    
    # Show plot
    plt.show()

#%% Plot correlation matrix for performance in different domains in each model

### Work in progress
# Might want to do this for n_premises separately?
data_corr = pd.DataFrame()
for d in range(len(domains)):
    data_corr[domains[d]] = data_accXdomain["accuracy"][data_accXdomain["domain"]==domains[d]]
    
data_corr.corr()