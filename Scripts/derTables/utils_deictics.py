# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:50:01 2026

Utils and helpers for deictic relational syllogism generator function.


@author: mraemaek
"""


# %% dependencies

import numpy as np
from itertools import product
import pdb
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple



# %% resolveRelations - interpret input for deictic syllogism function

# Specify default exemplars for different deictic relations
thinking = ['think', 
            # 'believe'
            ]
past_think = ['thought'] 
thoughts = ['cats are fun', 'cats are annoying and dirty', 
            'ducks are funny and cute', 'ducks are boring',
            'politics is boring', 'politics is important', 
            'the beach is nice', 'mountains are cool',
            'ice cream is better than cookies', 'cookies are better than ice cream',
            'MacDonalds is disgusting', 'MacDonalds is amazing', 
            'MacDonalds is good', "Wendy's is better",
            'AI is cool', 'AI is scary',
            'football is fun', 'football is stupid',
            'Die Hard is a good movie', 'Die Hard is a terrible movie', #10
            'football is the best sport', 'football is a nuisance',
            'tennis is boring to watch', 'tennis is very entertaining',
            'reading is fun', 'reading is boring',
            'cats are better than dogs', 'dogs are better than cats',
            'breakfast is the most important meal of the day', 'skipping breakafast is okay',
            'cilantro tastes amazing', 'cilantro tastes like soap',
            'AI will only bring enormous benefits', 'AI will destroy humanity',
            'history is interesting', 'history is boring',
            'newspapers are important', 'newspapers are obsolete',
            'TikTok is a fun pass-time', 'TikTok makes you stupid', # 20
            'it is okay to cry sometimes', 'crying is for children',
            'psychology is a science', 'psychology is pseudoscience',
            'Titanic is a great movie', 'Titanic is a boring movie',
            'Brussels sprouts are tasty', 'Brussels sprouts are disgusting',
            'Pizza is the best food', 'Pasta is the best food',
            'you should drink milk cold', 'you should drink milk at room temperature',
            'prefer holidays in nature', 'prefer city trips',
            'Inception is the best movie ever', 'Pulp Fiction is the best movie ever',
            'prefer apples over bananas', 'prefer bananas over apples',
            'think pigeons are basically rats', 'pigeons are okay', # 30
            ]

feeling = ['feel'] # Interpersonal feeling: 
past_feelings = ['felt']
feelings = ['happy', 'sad',
            'angry', 'confused', 
            'scared', 'safe',
            'rather cold', 'nice and warm',
            'hot', 'cold',
            'nauseous', 'perfectly fine',
            'happy', 'angry', 
            'nauseous', 'fine',
            'great', 'sad', 
            'dissapointed', 'sad', # 10
            'awfull', 'guilty',
            'a little sick', 'fine',
            'agitated', 'relaxed',
            'stressed out', 'totally zen',
            'warm', 'freezing cold',
            'hungry', 'satiated',
            'bored', 'like doing nothing',
            'a little sad', 'happy',
            'calm', 'nervous',
            'angry', 'happy', # 20
            'a little hot', 'a little cold',
            'a little sick', 'completely healthy',
            'scared at night', 'comfortable',
            'hopeful', 'hopeless',            
            'anxious', 'relaxed',
            'scared', 'calm',
            'unprepared', 'prepared',
            'energetic', 'tired',
            'too warm', 'too cold'
            'restless', 'relaxed', # 30
            ]

doing = ['doing'] # Interpersonal 'doing' relations
actions = ['sitting on a red chair', 'sitting on a blue chair',
            'playing chess', 'reading a book',
            'drinking a coke', 'drinking a glass of water',
            'playing videogames', 'reading a book',
            'cleaning', 'cooking',
            'playing football', 'playing tennis',
            'watching television', 'reading a magazine',
            'playing videogames', 'cooking',
            'feeding the cat', 'cleaning the kitchen' 
            'sitting on a red chair', 'sitting on a black chair', # 10
            'sitting on a blue chair', 'sitting on a black chair',
            'reading a magazine', 'watching TikToks',
            'reading a newspaper', 'scrolling Instagram',
            'reading a poem', 'solving a sudoku',
            'cleaning the living room', 'watching tv',
            'sitting on the couch', 'sitting at the table',
            "solving a Rubik's cube", 'reading a book',
            'playing a game of chess', 'making homework',
            'taking a nap', 'making a cup of coffee',            
            'shopping', 'cleaning the house', # 20
            'working in the garden', 'doing the dishes',
            'taking a bath', 'taking a shower',
            'doing laundry', 'hanging out with friends',
            'reading a news article', 'reading a cartoon',
            'doing the dishes', 'doing laundry',
            'out with friends', 'walking the dog in the park',
            'visiting the zoo', 'watching TV all day',            
            'shopping online', 'drawing',
            'listening to music', 'cooking',
            'fixing the lamp', 'sitting on the couch', # 30
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
           "the first day of the year", 'game night', # 10
           "New Year's Eve", 'your birthday',
           'my birthday','Easter', 
           "my mom's birthday", "my dad's birthday",
           "the opening ceremony of the Olympics", 'my birthday',
           'Easter', 'the opening of the mall',
           'the start of spring', 'your twentieth birthday',
           'the first day of school', 'my birthday',
           'card game night', 'movie night',
           'Thanksgiving', "your mom's birthday",                     
           'my birthday', 'the first day of the month', # 20
           'the last day of school', 'the start of our holiday',
           'the start of the weekend', 'the last day of school',
           'my graduation', 'our dinner',
           'the deadline to submit your taxes', 'the start of shopping season',           
           'my first day at work', 'your last day at work',
           'your first day at school', 'your birthday',
           'a holiday', 'a workday',
           'my last day in Belgium', 'the start of my holiday',
           'the first day of winter', 'the last exam',
           'the last day of summer', 'the start of the school year', # 30
          ]
# Spatial relations (here-there)
# Premise: 'A is here and B is there' -> Qq: Is A/B here/there?"/"Where is A/B?"
places = [['here', 'there'],
           # ['in the store', 'at home'], ['at the pool', 'in the gym']
          ] # others? 

things = ['the red chair', 'the blue chair', 
          'the pharmacy', 'the grocery store',
          'the school', 'my home',
          'the bank', 'the supermarket',
          'my wallet', 'my phone',
          'the bus stop', 'the post office',
          'the chair', 'the table',
          'the green chair', 'the red chair',
          'my book', 'my bag', 
          'my cup', 'your cup', # 10
          'the newspaper', 'my phone',
          'your phone', 'your wallet',
          'my key', 'your phone',
          'the bleu chair', 'the green table',          
          'the fridge', 'the sink',
          'the car', 'your bicycle',
          'the post office', 'the store',
          'the bank', 'the supermarket',
          'the remote', 'the book you are reading',
          'the salt', 'the pepper', # 20
          'your book', 'my phone',
          'the water bottle', 'the glass',
          'the door', 'the bed',
          'the computer', 'the printer',
          'the magazine', 'the newpaper',
          'the living room', 'the kitchen',
          'the bedroom', 'the bathroom',
          'your bike', 'my car',
          'the mail box', 'the bus stop',
          'the bank', 'the good cheese shop' # 30
          ]
DEFAULT_RELATIONS = {
    "interpersonal-thinking": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": None
        },
        "temporal": None,
        "spatial": None,
        "objects": thoughts
    },
    "interpersonal-feeling": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": None
        },
        "temporal": None,
        "spatial": None,
        "objects": feelings
    },
    "interpersonal-doing": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": None,
        "spatial": None,
        "objects": actions
    },
    "temporal": {
        "ip": None,
        "temporal": times,
        "spatial": None,
        "objects": events
    },
    "spatial": {
        "ip": None,
        "temporal": None,
        "spatial": places,
        "objects": things  
    },
    "temporal+spatial": {
        "ip": None,
        "temporal": times,
        "spatial": places,
        "objects": things  
    },
    "IPthinking+temporal": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": past_think
        },
        "temporal": times,
        "spatial": None,
        "objects": thoughts
    },

    "IPfeeling+temporal": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": past_feelings
        },
        "temporal": times,
        "spatial": None,
        "objects": feelings
    },

    "IPdoing+temporal": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": times,
        "spatial": None,
        "objects": actions
    },
    "IPthinking+spatial": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": None
        },
        "temporal": None,
        "spatial": places,
        "objects": thoughts
    },
    "IPfeeling+spatial": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": None
        },
        "temporal": None,
        "spatial": places,
        "objects": feelings
    },
    "IPdoing+spatial": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": None,
        "spatial": places,
        "objects": actions
    },
    "IPthinking+temporal+spatial": {
        "ip": {
            "type": "thinking",
            "present": thinking,
            "past": past_think
        },
        "temporal": times,
        "spatial": places,
        "objects": thoughts
    },
    "IPfeeling+temporal+spatial": {
        "ip": {
            "type": "feeling",
            "present": feeling,
            "past": past_feelings
        },
        "temporal": times,
        "spatial": places,
        "objects": feelings
    },

    "IPdoing+temporal+spatial": {
        "ip": {
            "type": "doing",
            "present": doing,
            "past": None
        },
        "temporal": times,
        "spatial": places,
        "objects": actions
    },
}

from copy import deepcopy
def resolve_relations(relations_input):

    resolved = {}

    # Case 1: list of relation names
    if isinstance(relations_input, list):
        for rel in relations_input:
            resolved[rel] = deepcopy(DEFAULT_RELATIONS[rel])

    # Case 2: dict (possibly partial override)
    elif isinstance(relations_input, dict):
        for rel, spec in relations_input.items():
            base = deepcopy(DEFAULT_RELATIONS.get(rel, {}))
            base.update(spec)   # user overrides defaults
            resolved[rel] = base

    # Case 2: dict (possibly partial override)
    elif isinstance(relations_input, dict):
        for rel, spec in relations_input.items():
            base = deepcopy(DEFAULT_RELATIONS.get(rel, {}))
            base.update(spec)   # user overrides defaults
            resolved[rel] = base

    return resolved

# %% normalize_pair - fix input list dimensions to avoid indexing issues

def normalize_pair(x):
    return x[0] if isinstance(x, list) and len(x) == 1 else x

# %% irrelevant premises - find id and randomly select premise


IRR_PREMS_DEFAULT = [
    "You are wearing a red shirt.", "I am wearing a red shirt.",
    "You are playing chess.", "I am playing chess.",
    "You are playing outside.", "I am playing outside.",
    "You are drinking a coke.", "I am drinking a coke.",
    "You are feeding the cat.", "I am feeding the cat.",
    "You are playing videogames.", "I am playing videogames.",
    "You are reading a book.", "I am reading a book.",
    "You are cleaning.", "I am cleaning.",
    "You are cooking.", "I am cooking.",
    "You are playing football.", "I am playing football.",
    "You are watching television.", "I am watching television.",
    "You are reading a magazine.", "I am reading a magazine.",
    "You are sitting on a red chair.", "I am sitting on a red chair.",
    "You are sitting on a blue chair.", "I am sitting on a blue chair.",
    "You are sitting on a black chair.", "I am sitting on a black chair.",
    "You feel cold.", "I feel cold.",
    "You feel sad.", "I feel sad.",
    "You feel happy.", "I feel happy.",
    "You feel warm.", "I feel warm.",
    "You feel hot.", "I feel hot.",
    "You feel dizzy.", "I feel dizzy.",
    "You feel scared.", "I feel scared.",
    "You feel good.", "I feel good.",
    "You feel stressed.", "I feel stressed.",
    "You feel bad.", "I feel bad.",
    "You feel great.", "I feel great.",
]


def choose_irr_id(objects, t_id: int, rng=None) -> int:
    """
    Picks an 'irrelevant' object index from the opposite half of the objects list,
    relative to t_id, to avoid overlap with the current trial's objects.
    """
    if rng is None:
        rng = np.random.default_rng()

    n = len(objects)
    if n < 4:
        raise ValueError("Need at least 4 objects to choose an irr_id robustly.")

    half = n // 2  # integer
    if t_id < half:
        # choose from [half, n-1]
        return int(rng.integers(half, n))
    else:
        # choose from [0, half-1]
        return int(rng.integers(0, half))


def build_irrelevant_context(
    *,
    irrelevant: bool,
    objects,
    t_id: int,
    rng=None,
    irr_prems=None,
) -> dict:
    """
    Returns:
      {"irrPrems": list[str] or None, "irr_id": int or None}
    """
    if rng is None:
        rng = np.random.default_rng()

    if not irrelevant:
        return {"irrPrems": None, "irr_id": None}

    if irr_prems is None:
        irr_prems = IRR_PREMS_DEFAULT

    irr_id = choose_irr_id(objects, t_id, rng=rng)
    return {"irrPrems": irr_prems, "irr_id": irr_id}


# %% build_premises - take relevant formatting for relation and create two premises
PAST_WORDS_DEFAULT = {"yesterday", "last week", "last year"}


def _cap_first(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def _is_past_time_word(x: str, past_words=PAST_WORDS_DEFAULT) -> bool:
    return (x or "").strip().lower() in past_words


def _shuffle_pair_or_list(rng, x):
    """
    Shuffles a 2-item pair or a list-of-pairs. Returns same type as input.
    """
    if x is None:
        return None
    x = list(x)
    rng.shuffle(x)
    return x


def _choose_subject_tokens(rel: str, rng) -> np.ndarray:
    """
    'doing' uses "I am/you are", everything else uses "I/you"
    """
    if "doing" in rel:
        base = ["I am", "you are"]
    else:
        base = ["I", "you"]
    return rng.permutation(base)


def _adjust_doing_subject_for_past(subj: str) -> str:
    # subj is "I am" or "you are"
    if subj == "I am":
        return "I was"
    if subj == "you are":
        return "you were"
    return subj


def build_premises(
    *,
    rel: str,
    spec: dict,
    t_id: int,
    irrelevant: bool=False,
    r: int,
    rng=None,
    past_words=PAST_WORDS_DEFAULT,
) -> tuple[str, str, dict]:
    """
    Returns (premise1, premise2, ctx) where ctx contains the randomized
    tokens used to later build options consistently:
      ctx["iyou"], ctx["nowthen"], ctx["herethere"]
    """
    if rng is None:
        rng = np.random.default_rng()

    ip = spec.get("ip")
    objects = spec["objects"]

    # These may be None depending on relation
    nowthen = spec.get("temporal")
    herethere = spec.get("spatial")

    # IP verb lists (may be None)
    deictics = ip["present"] if ip else None
    pastdeictics = ip.get("past") if ip else None

    if deictics:    
        d = r # index for deictic relations (n_rep instead of loop)
        if d >= len(deictics): 
            loop = int(np.round(d/len(deictics)))
            d -= loop*len(deictics) # cycle back through list
        if rel in ['IPthinking+temporal', 'IPfeeling+temporal',
                   'IPthinking+temporal+spatial', 'IPfeeling+temporal+spatial']:
            if d >= len(pastdeictics): 
                loop = int(np.round(d/len(pastdeictics)))
                d -= loop*len(pastdeictics) # cycle back through list

    # Randomize I/you order, and the temporal/spatial pairs if present
    iyou = _choose_subject_tokens(rel, rng)

    if nowthen is not None:
        nowthen = _shuffle_pair_or_list(rng, nowthen)
        # normalize if someone passes list-of-one-pair
        if isinstance(nowthen, list) and len(nowthen) == 1:
            nowthen = nowthen[0]

    if herethere is not None:
        herethere = _shuffle_pair_or_list(rng, herethere)
        if isinstance(herethere, list) and len(herethere) == 1:
            herethere = herethere[0]

    # Convenience flags
    has_ip = ip is not None
    has_temp = nowthen is not None
    has_spat = herethere is not None

    # Premise builders
    def p_ip_thinkfeel(i: int, verb_list, obj_idx: int, add_spat: bool, add_temp: bool, past_tense_override: bool):
        subj = iyou[i]
        # if i == 0:
        subj = _cap_first(subj)

        verb = verb_list[d]
        obj = objects[obj_idx]

        parts = [subj, verb, obj]
        if add_spat:
            parts.append(herethere[i])
        if add_temp:
            parts.append(nowthen[i])

        # End punctuation
        s = " ".join(parts)
        return s if i == 0 else s + "."

    def p_ip_doing(i: int, obj_idx: int, add_spat: bool, add_temp: bool):
        subj = iyou[i]
        # Adjust tense for temporal relations with past time words
        if add_temp and _is_past_time_word(nowthen[i], past_words):
            subj = _adjust_doing_subject_for_past(subj)

        # if i == 0:
        subj = _cap_first(subj)

        parts = [subj, objects[obj_idx]]
        if add_spat:
            parts.append(herethere[i])
        if add_temp:
            parts.append(nowthen[i])

        s = " ".join(parts)
        return s if i == 0 else s + "."

    def p_temporal_only(i: int, obj_idx: int):
        # Capitalize first token for premise1 / premise2 starts
        time_word = _cap_first(nowthen[i])
        cop = "was" if _is_past_time_word(nowthen[i], past_words) else "is"
        s = f"{time_word} {cop} {objects[obj_idx]}"
        return s if i == 0 else s + "."
    
    def p_spatial_only(i: int, obj_idx: int):
        # Capitalize object at sentence start
        obj = _cap_first(objects[obj_idx])
        s = f"{obj} is {herethere[i]}"
        return s if i == 0 else s + "."
    
    def p_temp_spat(i: int, obj_idx: int):
        obj = _cap_first(objects[obj_idx])
        time_word = nowthen[i]   # no capitalization
        cop = "was" if _is_past_time_word(nowthen[i], past_words) else "is"
        s = f"{obj} {cop} {herethere[i]} {time_word}"
        return s if i == 0 else s + "."

    # --- Dispatch by relation family ---
    if rel in ("interpersonal-thinking", "interpersonal-feeling"):
        premise1 = p_ip_thinkfeel(0, deictics, t_id, add_spat=False, add_temp=False, past_tense_override=False)
        premise2 = p_ip_thinkfeel(1, deictics, t_id + 1, add_spat=False, add_temp=False, past_tense_override=False)

    elif rel == "interpersonal-doing":
        premise1 = p_ip_doing(0, t_id, add_spat=False, add_temp=False)
        premise2 = p_ip_doing(1, t_id + 1, add_spat=False, add_temp=False)

    elif rel == "temporal":
        premise1 = p_temporal_only(0, t_id)
        premise2 = p_temporal_only(1, t_id + 1)

    elif rel == "spatial":
        premise1 = p_spatial_only(0, t_id)
        premise2 = p_spatial_only(1, t_id + 1)

    elif rel == "temporal+spatial":
        premise1 = p_temp_spat(0, t_id)
        premise2 = p_temp_spat(1, t_id + 1)

    elif rel == "IPdoing+spatial":
        premise1 = p_ip_doing(0, t_id, add_spat=True, add_temp=False)
        premise2 = p_ip_doing(1, t_id + 1, add_spat=True, add_temp=False)

    elif rel in ("IPthinking+spatial", "IPfeeling+spatial"):
        premise1 = p_ip_thinkfeel(0, deictics, t_id, add_spat=True, add_temp=False, past_tense_override=False)
        premise2 = p_ip_thinkfeel(1, deictics, t_id + 1, add_spat=True, add_temp=False, past_tense_override=False)

    elif rel == "IPdoing+temporal":
        premise1 = p_ip_doing(0, t_id, add_spat=False, add_temp=True)
        premise2 = p_ip_doing(1, t_id + 1, add_spat=False, add_temp=True)

    elif rel in ("IPthinking+temporal", "IPfeeling+temporal"):
        # Use past verb list on the side whose time word is past (matches your original logic)
        verb0 = pastdeictics if (pastdeictics is not None and _is_past_time_word(nowthen[0], past_words)) else deictics
        verb1 = pastdeictics if (pastdeictics is not None and _is_past_time_word(nowthen[1], past_words)) else deictics
        premise1 = p_ip_thinkfeel(0, verb0, t_id, add_spat=False, add_temp=True, past_tense_override=False)
        premise2 = p_ip_thinkfeel(1, verb1, t_id + 1, add_spat=False, add_temp=True, past_tense_override=False)

    elif rel in ("IPthinking+temporal+spatial", "IPfeeling+temporal+spatial"):
        verb0 = pastdeictics if (pastdeictics is not None and _is_past_time_word(nowthen[0], past_words)) else deictics
        verb1 = pastdeictics if (pastdeictics is not None and _is_past_time_word(nowthen[1], past_words)) else deictics
        premise1 = p_ip_thinkfeel(0, verb0, t_id, add_spat=True, add_temp=True, past_tense_override=False)
        premise2 = p_ip_thinkfeel(1, verb1, t_id + 1, add_spat=True, add_temp=True, past_tense_override=False)

    elif rel == "IPdoing+temporal+spatial":
        premise1 = p_ip_doing(0, t_id, add_spat=True, add_temp=True)
        premise2 = p_ip_doing(1, t_id + 1, add_spat=True, add_temp=True)

    else:
        raise ValueError(f"Unhandled relation: {rel}")

    ctx = {"iyou": iyou, "nowthen": nowthen, "herethere": herethere, "d": d if deictics else None}
    return premise1, premise2, ctx

# %% helpers

def _append_labjs_options(option_cols, t_options_local, n_opt):
    for i in range(n_opt):
        option_cols[i].append(str(t_options_local[i]))

def _convert_selecttf(corr_list, output, taskPremise):
    
    """ 
    Convert 'correct' list for labjs output data and printing
    """
    
    if output == 'csv':
        out = [1 if x == "yes" else 0 for x in corr_list] # default select TRUE
        if taskPremise != "Select all questions to which the answer is 'yes'.":
            out = [1 - x for x in out] # convert if task is to select false
        out = ['select' if x == 1 else 'no select' for x in out] # convert
        printOut = out
    elif output == 'labjs':
        out = [1 if x == "yes" else 0 for x in corr_list] # default select TRUE
        if taskPremise != "Select all questions to which the answer is 'yes'.":
            out = [1 - x for x in out] # convert if task is to select false
        printOut = ['select' if x == 1 else 'no select' for x in out] # convert
    return out, printOut

# %% build_reversal_dict - creates reversal premises for current deictic relation(s)

def build_reversal_dict(*, rel, ip, nowthen, herethere, reversal):
    rev = {}

    if not reversal:
        return rev

    has_ip = ip is not None
    has_temp = nowthen is not None
    has_spat = herethere is not None

    if has_ip and has_temp and has_spat:
        rev["ip+spatial+temporal"] = {
            "premise": f"If I were you and you were me, \
                if {nowthen[0]} were {nowthen[1]} and {nowthen[1]} were {nowthen[0]}, \
                    and if {herethere[0]} were {herethere[1]} and {herethere[1]} were {herethere[0]};",
            "type": "IP+Temporal+Spatial Reversal",
            "level": 3,
        }
    elif has_ip and has_temp:
        rev["ip+temporal"] = {
            "premise": f"If I were you and you were me and if {nowthen[0]} were {nowthen[1]} and {nowthen[1]} were {nowthen[0]};",
            "type": "IP+Temporal Reversal",
            "level": 2,
        }
    elif has_ip and has_spat:
        rev["ip+spatial"] = {
            "premise": f"If I were you and you were me and if {herethere[0]} were {herethere[1]} and {herethere[1]} were {herethere[0]};",
            "type": "IP+Spatial Reversal",
            "level": 2,
        }
    elif has_spat and has_temp:
        rev["spatial+temporal"] = {
            "premise": f"If {herethere[0]} were {herethere[1]} and {herethere[1]} were {herethere[0]} and if {nowthen[0]} were {nowthen[1]} and {nowthen[1]} were {nowthen[0]};",
            "type": "Spatial+Temporal Reversal",
            "level": 2,
        }
    elif has_ip:
        rev["ip"] = {
            "premise": "If I were you and you were me;",
            "type": "Interpersonal Reversal",
            "level": 1,
        }

    elif has_temp:
        rev["temporal"] = {
            "premise": f"If {nowthen[0]} were {nowthen[1]} and {nowthen[1]} were {nowthen[0]};",
            "type": "Temporal Reversal",
            "level": 1,
        }

    elif has_spat:
        rev["spatial"] = {
            "premise": f"If {herethere[0]} were {herethere[1]} and {herethere[1]} were {herethere[0]};",
            "type": "Spatial Reversal",
            "level": 1,
        }

    return rev

# %% get_reversal_key_orders

def get_reversal_key_orders(*, rel, reversal, allReversals):
    """
    Return only level-1 reversal keys, consistent with build_reversal_dict().
    """
    if not reversal:
        return {1: [], 2: [], 3: []}

    has_ip = ("IP" in rel) or ("interpersonal" in rel)
    has_temp = "temporal" in rel
    has_spat = "spatial" in rel

    level1 = []

    # single-dimension relations
    if has_ip and not has_temp and not has_spat:
        level1 = ["ip"]
    elif has_temp and not has_ip and not has_spat:
        level1 = ["temporal"]
    elif has_spat and not has_ip and not has_temp:
        level1 = ["spatial"]

    # two-dimension relations
    elif has_ip and has_temp and not has_spat:
        level1 = ["ip", "temporal"] if allReversals else ["ip+temporal"]
    elif has_ip and has_spat and not has_temp:
        level1 = ["ip", "spatial"] if allReversals else ["ip+spatial"]
    elif has_temp and has_spat and not has_ip:
        level1 = ["temporal", "spatial"] if allReversals else ["spatial+temporal"]

    # three-dimension relations
    elif has_ip and has_temp and has_spat:
        level1 = ["ip", "temporal", "spatial"] if allReversals else ["ip+spatial+temporal"]

    return {1: level1, 2: [], 3: []}

# %% build_deictic_option_sets - programmatic replacement for the huge if/elif forest in generateDeicticSyllogisms

def build_deictic_option_sets(
    *,
    rel: str,
    ip: dict | None,
    temporal,
    spatial,
    objects: list,
    iyou: list,
    deictic_verb: str | None,
    t_id: int,
    irr_id: int,
    reversal: bool,
    allReversals: bool,
    past_words: list | None = None,
):
    """Create base and reversal option banks for a single deictic problem.

    Returns a dict with legacy fields expected by the main generator:
        options, correct,
        revOptions, r_correct,
        rev2Options, rr_correct,
        rev3Options, rrr_correct,
    plus:
        reversals (premise text + type), reversal_key_orders

    
    """

    past_words = past_words or ['yesterday', 'last week', 'last year']
    past_set = {w.lower() for w in past_words}

    # --- helpers -------------------------------------------------------------

    def is_past_time(word: str | None) -> bool:
        if word is None:
            return False
        return str(word).lower() in past_set

    def past_aux_for_do(lead: str, *, past: bool) -> str:
        # thinking/feeling questions: Do -> Did when time is past
        if not past:
            return lead
        return "Did" if lead == "Do" else lead  # only flip Do->Did
    
    def pastify_doing_question_subj(s: str) -> str:
        # doing questions: Am/Are -> Was/Were when time is past
        # keep it conservative and only replace known patterns
        s_stripped = s.strip()
        if s_stripped == "Am I":
            return "Was I"
        if s_stripped == "Are you":
            return "Were you"
        # if you ever pass statement-like subjects by accident:
        if s_stripped == "I am":
            return "I was"
        if s_stripped == "you are":
            return "you were"
        return s
    
    def base_subject(j: int) -> str:
        return iyou[j]

    def swapped_subject(j: int) -> str:
        return iyou[1 - j]

    def pick_obj(kind: str, j: int):
        if kind == "t":
            return objects[t_id + j]
        if kind == "swap_t":
            return objects[t_id + (1 - j)]
        if kind == "irr":
            return objects[irr_id]
        raise ValueError(kind)

    def pick_time(kind: str, j: int):
        if temporal is None:
            return None
        pair = normalize_pair(temporal)
        if isinstance(pair[0], (list, tuple)):
            pair = pair[0]
        if kind == "t":
            return pair[j]
        if kind == "swap_t":
            return pair[1 - j]
        raise ValueError(kind)

    def pick_place(kind: str, j: int):
        if spatial is None:
            return None
        pair = normalize_pair(spatial)
        if isinstance(pair[0], (list, tuple)):
            pair = pair[0]
        if kind == "t":
            return pair[j]
        if kind == "swap_t":
            return pair[1 - j]
        raise ValueError(kind)
        
    def doing_statement_to_question_subj(s: str) -> str:
        s = (s or "").strip()
        if s.lower() == "i am":
            return "Am I"
        if s.lower() == "you are":
            return "Are you"
        # already in question form?
        if s.lower() == "am i":
            return "Am I"
        if s.lower() == "are you":
            return "Are you"
        return s
    def past_deictic_verb_for_current(current: str) -> str:
        """
        Map present deictic verb to the corresponding past participle-ish form
        used in counterfactual past questions.
        """
        if not ip or not ip.get("past"):
            return current
    
        present_list = ip.get("present", [])
        past_list = ip.get("past", [])
    
        if current in present_list:
            idx = present_list.index(current)
            if idx < len(past_list):
                return past_list[idx]
    
        return current
    def fmt_query(*, subj: str | None, obj: str, place: str | None, time: str | None, 
                  ip_would: bool = False,
                  cf_would: bool = False) -> str:
        has_ip = subj is not None
        has_place = place is not None
        has_time = time is not None

        if has_ip:
            if ip and ip.get("type") in ("thinking", "feeling"):
                if ip_would:
                    if has_time and is_past_time(time):
                        past_verb = past_deictic_verb_for_current(deictic_verb)
                        bits = [f"Would {subj} have {past_verb} {obj}"]
                    else:
                        bits = [f"Would {subj} {deictic_verb} {obj}"]
                else:
                    lead = "Do"
                    if has_time and is_past_time(time):
                        lead = past_aux_for_do(lead, past=True)  # Do -> Did
                    bits = [f"{lead} {subj} {deictic_verb} {obj}"]
        
                if has_place:
                    bits.append(place)
                if has_time:
                    bits.append(time)
                return " ".join(bits) + "?"

            # doing (or unspecified)
            if ip_would:
                s = str(subj)
                if "I" in s:
                    pron = "I"
                elif "you" in s.lower():
                    pron = "you"
                else:
                    pron = s
                aux = "have been" if (has_time and is_past_time(time)) else "be"
                bits = [f"Would {pron} {aux} {obj}"]
            else:
                # doing (factual question): Am I/Are you -> Was I/Were you when time is past
                subj_out = doing_statement_to_question_subj(str(subj))

                # if temporal and past: Am/Are -> Was/Were
                if has_time and is_past_time(time):
                    subj_out = pastify_doing_question_subj(subj_out)
                
                bits = [f"{subj_out} {obj}"]

            if has_place:
                bits.append(place)
            if has_time:
                bits.append(time)
            return " ".join(bits) + "?"

        # non-interpersonal
        if cf_would:
            # Counterfactual copula for temporal/spatial reversals
            aux = "have been" if (has_time and is_past_time(time)) else "be"
            bits = [f"Would {obj} {aux}"]
            if has_place:
                bits.append(place)
            if has_time:
                bits.append(time)
            return " ".join(bits) + "?"
    
        # factual non-IP
        aux = "Was" if (has_time and is_past_time(time)) else "Is"
        bits = [f"{aux} {obj}"]
        if has_place:
            bits.append(place)
        if has_time:
            bits.append(time)
        return " ".join(bits) + "?"

    def block(kind_subj: str, kind_time: str, kind_place: str, *, ip_would: bool = False, cf_would: bool = False):
        """Return a 4-option block + its correct labels."""

        opts = []
        for j in (0, 1):
            subj = base_subject(j) if kind_subj == "base" else swapped_subject(j)
            # Keep underlying facts aligned to side j; swapping subject changes *labels*, not facts.
            obj = pick_obj("t", j)
            time = pick_time(kind_time, j)
            place = pick_place(kind_place, j)
            opts.append(fmt_query(subj=subj if ip else None, obj=obj, place=place, time=time, ip_would=ip_would, cf_would=cf_would,))

        subj0 = base_subject(0) if kind_subj == "base" else swapped_subject(0)
        subj1 = base_subject(1) if kind_subj == "base" else swapped_subject(1)
        time0 = pick_time(kind_time, 0)
        time1 = pick_time(kind_time, 1)
        place0 = pick_place(kind_place, 0)
        place1 = pick_place(kind_place, 1)

        if ip:
            false1 = fmt_query(subj=subj0, obj=pick_obj("swap_t", 0), place=place0, time=time0, ip_would=ip_would, cf_would=cf_would,)
            false2 = fmt_query(subj=subj1, obj=pick_obj("swap_t", 1), place=place1, time=time1, ip_would=ip_would, cf_would=cf_would,)
        else:
            false1 = fmt_query(subj=None, obj=pick_obj("swap_t", 0), place=place0, time=time0, cf_would=cf_would,)
            false2 = fmt_query(subj=None, obj=pick_obj("swap_t", 1), place=place1, time=time1, cf_would=cf_would,)

        return [opts[0], opts[1], false1, false2], ["yes", "yes", "no", "no"]

    # --- base block ----------------------------------------------------------

    base_opts, base_correct = block("base", "t", "t", ip_would=False)
    legacy = {
        "options": base_opts,
        "correct": base_correct,
        "revOptions": None,
        "r_correct": None,
        "rev2Options": None,
        "rr_correct": None,
        "rev3Options": None,
        "rrr_correct": None,
    }

    # --- reversal blocks -----------------------------------------------------

    rev_dict = build_reversal_dict(
        rel=rel,
        ip=ip,
        nowthen=normalize_pair(temporal) if temporal is not None else None,
        herethere=normalize_pair(spatial) if spatial is not None else None,
        reversal=reversal,
    )
    key_orders = get_reversal_key_orders(
        rel=rel,
        reversal=reversal,
        allReversals=allReversals,
    )

    def block_for_key(key: str):
        if key == "ip":
            return block("swap", "t", "t", ip_would=True)
        if key == "temporal":
            return block("base", "swap_t", "t", ip_would=False, cf_would=True)
        if key == "spatial":
            return block("base", "t", "swap_t", ip_would=False, cf_would=True)
        if key == "ip+temporal":
            return block("swap", "swap_t", "t", ip_would=True)
        if key == "ip+spatial":
            return block("swap", "t", "swap_t", ip_would=True)
        if key == "spatial+temporal":
            return block("base", "swap_t", "swap_t", ip_would=False, cf_would=True)
        if key == "ip+spatial+temporal":
            return block("swap", "swap_t", "swap_t", ip_would=True)
        raise ValueError(f"Unknown reversal key: {key}")

    if key_orders.get(1):
        ropts, rcorr = [], []
        for k in key_orders[1]:
            o, c = block_for_key(k)
            ropts.extend(o) 
            rcorr.extend(c)
        legacy["revOptions"] = ropts
        legacy["r_correct"] = rcorr

    if key_orders.get(2):
        ropts, rcorr = [], []
        for k in key_orders[2]:
            o, c = block_for_key(k)
            ropts.extend(o)
            rcorr.extend(c)
        legacy["rev2Options"] = ropts
        legacy["rr_correct"] = rcorr

    if key_orders.get(3):
        ropts, rcorr = [], []
        for k in key_orders[3]:
            o, c = block_for_key(k)
            ropts.extend(o)
            rcorr.extend(c)
        legacy["rev3Options"] = ropts
        legacy["rrr_correct"] = rcorr

    legacy["reversals"] = rev_dict
    legacy["reversal_key_orders"] = key_orders

    return legacy

# %% pick_task_premise - for MC problems, randomize whether to select TRUE/FALSE statements
def _pick_task_premise(*, rng: np.random.Generator) -> str:
    """Task premise only matters for forced-choice multiple-choice."""
    TASK_PREMISE_YES = "Select all questions to which the answer is 'yes'."
    TASK_PREMISE_NO = "Select all questions to which the answer is 'no'."
    return rng.choice([TASK_PREMISE_YES, TASK_PREMISE_NO])

# %% options-to-prems - MC response options into numbered list

def _options_to_prems_block(options: Sequence[str]) -> str:
    """Pretty-print the selected options as numbered lines for debugging/printing."""
    return "".join([f"\n{i+1}: {opt}" for i, opt in enumerate(options)])

# %% correct_subset_for_picks - get correct responses to randomly selected prompts

def _correct_subset_for_picks(options_pool: Sequence[str], correct_pool: Sequence[str], picks: Sequence[str]) -> List[str]:
    """Map picked options back to their corresponding 'yes'/'no' correct labels."""
    # Keep legacy behavior: index by exact string match.
    out = []
    for pick in picks:
        idx = list.index(list(options_pool), pick)
        out.append(correct_pool[idx])
    return out

# %% append_row - append all relevant data for one trial to dataframe
def append_row(trial_data, row, *, output, n_opt):
    trial_data["Premises"].append(row["Premises"])
    trial_data["Prompt"].append(row["Prompt"])
    trial_data["Type"].append(row["Type"])
    trial_data["Correct"].append(row["Correct"])
    trial_data["pCorrect"].append(row.get("pCorrect"))
    trial_data["pPrems"].append(row.get("pPrems"))
    trial_data["Relations"].append(row["Relations"])
    trial_data["Derivation"].append(row["Derivation"])
    trial_data["n_p"].append(row["n_p"])

    if output == "labjs":
        trial_data["taskPremise"].append(str(row.get("taskPremise", "")))
        trial_data["Premise1"].append(str(row.get("Premise1", "")))
        trial_data["Premise2"].append(str(row.get("Premise2", "")))
        trial_data["extraPremises"].append(str(row.get("extraPremises", "")))

        opts = row.get("t_options", [])
        for i in range(n_opt):
            val = str(opts[i]) if i < len(opts) else ""
            trial_data[f"option{i+1}"].append(val)
    else:
        trial_data["t_options"].append(row.get("t_options", []))
        
# %% append_rows - append multiple rows outputted for single-option problems

def append_rows(trial_data, rows, *, output, n_opt):
    for row in rows:
        append_row(trial_data, row, output=output, n_opt=n_opt)

# %% emit_mc_trial - # Helper to emit a single multiple-choice trial row
def emit_mc_trial(
    *,
    premise1: str,
    premise2: str,
    trial_type: str,
    options_pool: Sequence[str],
    correct_pool: Sequence[str],
    extra_premises: Optional[List[str]] = None,
    n_opt: int,
    output: str,
    taskPremise: str,
    forcedChoice: bool,
    rng: np.random.Generator
):
    picks = [str(p) for p in np.random.choice(options_pool, n_opt, replace=False)]
    q_block = _options_to_prems_block(picks)
    corr_yn = _correct_subset_for_picks(options_pool, correct_pool, picks)
    # Convert correctness for storage + printing
    corr_for_data, corr_for_print = _convert_selecttf(corr_yn, output, taskPremise)

    stem = f"{premise1}. {premise2}".strip()

    if extra_premises:
        # extra_premises can be ["If I were you ...;"] or ["<irrPrem>", "<revPrem>"]
        extra = " ".join([p.strip() for p in extra_premises if p and str(p).strip()])
        if extra:
            stem = f"{stem} {extra}".strip()
            
    full_prompt = stem
    if n_opt > 1 and forcedChoice:
        full_prompt = f"{taskPremise}\n{full_prompt}"
    return {
        "Premises": [premise1, premise2],
        "Premise1": premise1,
        "Premise2": premise2,
        "extraPremises": extra if extra_premises else '',
        "taskPremise": taskPremise,
        "Prompt": full_prompt,
        "Type": trial_type,
        "Correct": corr_for_data,
        "pCorrect": corr_for_print,
        "pPrems": q_block,
        "Derivation": "Mutual",
        "n_p": 2,
        "t_options": picks,   
    }

# %% emit_single_option_trial - format deictic problem with one response prompted
from typing import Sequence, Optional, List

def emit_single_option_trials(
    *,
    premise1: str,
    premise2: str,
    trial_type_yes: str,
    trial_type_no: str,
    options_pool: Sequence[str],
    correct_pool: Sequence[str],
    extra_premises: Optional[List[str]] = None,
    output: str,
):
    stem = f"{premise1}. {premise2}".strip()

    extra = ""
    if extra_premises:
        extra = " ".join([p.strip() for p in extra_premises if p and str(p).strip()])
        if extra:
            stem = f"{stem} {extra}".strip()

    rows = []

    for opt, corr in zip(options_pool, correct_pool):
        full_prompt = f"{stem}\n{opt}"
        trial_type = trial_type_yes if corr == "yes" else trial_type_no

        row = {
            "Premises": [premise1, premise2],
            "Premise1": premise1,
            "Premise2": premise2,
            "extraPremises": extra,
            "Prompt": full_prompt,
            "Type": trial_type,
            "Correct": corr,
            "pCorrect": corr,
            "pPrems": opt,          # useful for printing
            "t_options": [opt],     # single option
            "taskPremise": "",
            "Derivation": "Mutual",
            "n_p": 2,
        }
        rows.append(row)

    return rows