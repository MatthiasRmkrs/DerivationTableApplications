# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:49:00 2026

Create task set for Morgane's deictic RR studywith human participants.
Create deictic relational responding task battery with different 'subscales':
    - Interpersonal (thinking, feeling, doing)
    - Temporal
    - Spatial
    - Temporal + Spatial
    - Temporal + IP
    - Spatial + IP
    - Temporal + Spatial + IP
    

@author: mraemaek
"""
import numpy as np
import pdb
import pandas as pd
from derTables.utils_deictics import * 
from derTables.generateDeicticSyllogisms import generateDeicticSyllogisms2

# define items to use for different subscales

thinking = ['think']
past_think = ['thought'] 
feeling = ['feel'] # Interpersonal feeling: 
past_feelings = ['felt']
doing = ['doing'] # Interpersonal 'doing' relations
times = [['today', 'yesterday']] # for temporal relations
places = [['here', 'there']] # for spatial relations

relations_1d_ip = {
    "interpersonal-thinking": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": None
        },
        "temporal": None,
        "spatial": None,
        "objects": ['cats are fun', 'cats are annoying and dirty', 
                    'ducks are funny and cute', 'ducks are boring',
                    'politics is boring', 'politics is important', 
                    'the beach is nice', 'mountains are cool',
                    'ice cream is better than cookies', 'cookies are better than ice cream',
                    'MacDonalds is disgusting', 'MacDonalds is amazing', 
                    'MacDonalds is good', "Wendy's is better",
                    'AI is cool', 'AI is scary',
                    'football is fun', 'football is stupid',
                    'Die Hard is a good movie', 'Die Hard is a terrible movie']
    },
    "interpersonal-feeling": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": None
        },
        "temporal": None,
        "spatial": None,
        "objects": ['happy', 'sad',
                    'angry', 'confused', 
                    'scared', 'safe',
                    'rather cold', 'nice and warm',
                    'hot', 'cold',
                    'nauseous', 'perfectly fine',
                    'happy', 'angry', 
                    'nauseous', 'fine',
                    'great', 'sad', 
                    'dissapointed', 'sad']
    },
    "interpersonal-doing": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": None,
        "spatial": None,
        "objects": ['sitting on a red chair', 'sitting on a blue chair',
                    'playing chess', 'reading a book',
                    'drinking a coke', 'drinking a glass of water',
                    'playing videogames', 'reading a book',
                    'cleaning', 'cooking',
                    'playing football', 'playing tennis',
                    'watching television', 'reading a magazine'
                    'playing videogames', 'cooking',
                    'feeding the cat', 'cleaning the kitchen' 
                    'sitting on a red chair', 'sitting on a black chair']
    }}
relations_1d = {
    "temporal": {
        "ip": None,
        "temporal": times,
        "spatial": None,
        "objects": ['the opening of the new shop', 'the start of the academic year',
                  'my birthday', 'your birthday', 'the first day of school', 
                  'my birthday', "John's birthday", 
                  'the festival', 'the closing of the old shop',
                   'the opening of the new shop', 'the closing of the old shop',
                   'Christmas', 'my birthday', 
                   'Easter', 'the final of the Voice', 
                   'the opening of the new supermarket', 'your birthday',
                   "mom's birthday", "dad's birthday",
                   "the first day of the year", 'game night']
    },
    "spatial": {
        "ip": None,
        "temporal": None,
        "spatial": places,
        "objects": ['the red chair', 'the blue chair', 
                  'the pharmacy', 'the grocery store',
                  'the school', 'my home',
                  'the bank', 'the supermarket',
                  'my wallet', 'my phone',
                  'the bus stop', 'the post office',
                  'the chair', 'the table',
                  'the green chair', 'the red chair',
                  'my book', 'my bag', 
                  'my cup', 'your cup']  
    }}

relations_2d= {
    "temporal+spatial": {
        "ip": None,
        "temporal": times,
        "spatial": places,
        "objects": ['the newspaper', 'my phone',
                  'your phone', 'your wallet',
                  'my key', 'your phone',
                  'the bleu chair', 'the green table',          
                  'the fridge', 'the sink',
                  'the car', 'your bicycle',
                  'the post office', 'the store',
                  'the bank', 'the supermarket',
                  'the remote', 'the book you are reading',
                  'the salt', 'the pepper']  
    }}
relations_ip_temp = {
    "IPthinking+temporal": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": past_think
        },
        "temporal": times,
        "spatial": None,
        "objects": ['football is the best sport', 'football is a nuisance',
                    'tennis is boring to watch', 'tennis is very entertaining',
                    'reading is fun', 'reading is boring',
                    'cats are better than dogs', 'dogs are better than cats',
                    'breakfast is the most important meal of the day', 'skipping breakafast is okay',
                    'cilantro tastes amazing', 'cilantro tastes like soap',
                    'AI will only bring enormous benefits', 'AI will destroy humanity',
                    'history is interesting', 'history is boring',
                    'newspapers are important', 'newspapers are obsolete',
                    'TikTok is a fun pass-time', 'TikTok makes you stupid']
    },

    "IPfeeling+temporal": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": past_feelings
        },
        "temporal": times,
        "spatial": None,
        "objects": ['awfull', 'guilty',
                    'a little sick', 'fine',
                    'agitated', 'relaxed',
                    'stressed out', 'totally zen',
                    'warm', 'freezing cold',
                    'hungry', 'satiated',
                    'bored', 'like doing nothing',
                    'a little sad', 'happy',
                    'calm', 'nervous',
                    'angry', 'happy']
    },

    "IPdoing+temporal": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": times,
        "spatial": None,
        "objects": ['sitting on a blue chair', 'sitting on a black chair',
                    'reading a magazine', 'watching TikToks',
                    'reading a newspaper', 'scrolling Instagram',
                    'reading a poem', 'solving a sudoku',
                    'cleaning the living room', 'watching tv',
                    'sitting on the couch', 'sitting at the table',
                    "solving a Rubik's cube", 'reading a book',
                    'playing a game of chess', 'making homework',
                    'taking a nap', 'making a cup of coffee',            
                    'shopping', 'cleaning the house']
    }}
relations_ip_spat = {
    "IPthinking+spatial": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": None
        },
        "temporal": None,
        "spatial": places,
        "objects": ['football is the best sport', 'football is a nuisance',
                    'tennis is boring to watch', 'tennis is very entertaining',
                    'reading is fun', 'reading is boring',
                    'cats are better than dogs', 'dogs are better than cats',
                    'breakfast is the most important meal of the day', 'skipping breakafast is okay',
                    'cilantro tastes amazing', 'cilantro tastes like soap',
                    'AI will only bring enormous benefits', 'AI will destroy humanity',
                    'history is interesting', 'history is boring',
                    'newspapers are important', 'newspapers are obsolete',
                    'TikTok is a fun pass-time', 'TikTok makes you stupid']
    },
    "IPfeeling+spatial": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": None
        },
        "temporal": None,
        "spatial": places,
        "objects": ['awfull', 'guilty',
                    'a little sick', 'fine',
                    'agitated', 'relaxed',
                    'stressed out', 'totally zen',
                    'warm', 'freezing cold',
                    'hungry', 'satiated',
                    'bored', 'like doing nothing',
                    'a little sad', 'happy',
                    'calm', 'nervous',
                    'angry', 'happy']
    },
    "IPdoing+spatial": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": None,
        "spatial": places,
        "objects": ['sitting on a blue chair', 'sitting on a black chair',
                    'reading a magazine', 'watching TikToks',
                    'reading a newspaper', 'scrolling Instagram',
                    'reading a poem', 'solving a sudoku',
                    'cleaning the living room', 'watching tv',
                    'sitting on the couch', 'sitting at the table',
                    "solving a Rubik's cube", 'reading a book',
                    'playing a game of chess', 'making homework',
                    'taking a nap', 'making a cup of coffee',            
                    'shopping', 'cleaning the house']
    }}

relations_3d = {
    "IPthinking+temporal+spatial": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": past_think
        },
        "temporal": times,
        "spatial": places,
        "objects": ['it is okay to cry sometimes', 'crying is for children',
                    'psychology is a science', 'psychology is pseudoscience',
                    'Titanic is a great movie', 'Titanic is a boring movie',
                    'Brussels sprouts are tasty', 'Brussels sprouts are disgusting',
                    'Pizza is the best food', 'Pasta is the best food',
                    'you should drink milk cold', 'you should drink milk at room temperature',
                    'holidays in nature are better than citytrips', 'city trips are better than holidays in nature',
                    'Inception is the best movie ever', 'Pulp Fiction is the best movie ever',
                    'apples are tastier than bananas', 'bananas are tastier than apples'
                    'think pigeons are basically rats', 'pigeons are okay']
    },
    "IPfeeling+temporal+spatial": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": past_feelings
        },
        "temporal": times,
        "spatial": places,
        "objects": ['a little hot', 'a little cold',
                    'a little sick', 'completely healthy',
                    'scared at night', 'comfortable',
                    'hopeful', 'hopeless',            
                    'anxious', 'relaxed',
                    'scared', 'calm',
                    'unprepared', 'prepared',
                    'energetic', 'tired',
                    'too warm', 'too cold'
                    'restless', 'relaxed']
    },

    "IPdoing+temporal+spatial": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": times,
        "spatial": places,
        "objects": ['working in the garden', 'doing the dishes',
                    'taking a bath', 'taking a shower',
                    'doing laundry', 'hanging out with friends',
                    'reading a news article', 'reading a cartoon',
                    'doing the dishes', 'doing laundry',
                    'out with friends', 'walking the dog in the park',
                    'visiting the zoo', 'watching TV all day',            
                    'shopping online', 'drawing',
                    'listening to music', 'cooking',
                    'fixing the lamp', 'sitting on the couch']
    },
}

reversal = True
allReversals = False
irrelevant = False
forcedChoice = True
n_opt = 3
printTrials = True
output = 'labjs'
csv_file = "MorganeTestTrials.csv"

# combine trials
blocks = {
    '1dim': relations_1d,
          '1dim_ip': relations_1d_ip,
          '2dim': relations_2d,
          '2dim_ip_temp': relations_ip_temp,
          '2dim_ip_spat': relations_ip_spat,
          '3dim': relations_3d
          }
reps = {'1dim': 9,
        '1dim_ip': 3,
          '2dim': 9,
          '2dim_ip_temp': 3,
          '2dim_ip_spat': 3,
          '3dim': 3
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
            
trial_data_df = pd.DataFrame.from_dict(trial_data_combined) # create pandas dataframe
trial_data_df.to_csv(csv_file) # store in csv for later use