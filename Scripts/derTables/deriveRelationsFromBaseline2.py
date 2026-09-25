# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 23:49:42 2026

@author: mraemaek
"""
# Dependencies
import numpy as np
import matplotlib.pyplot as plt
import pdb
from derTables.createDerivationTables import createDerivationTables # to create derivation tables for input relations
from derTables.utils_tables import (cleanRelationLabels, # helper functions
                   findCommon,
                   deriveCombi,
                   determineProtocol,
                   createRelationTable
                   )
from derTables.plot_utils import (plotNetworkHeatmap, plotRelNetworkGraph) # plot functions

from collections import deque

def deriveRelationsFromBaseline(
    baseline,
    sLabs=None,
    illustrate=None,
    max_depth=None
):
    
    if sLabs is None or len(sLabs) == 0:
        sLabs = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

    # -----------------------------------------------------
    # Relation lookup tables
    # -----------------------------------------------------

    mutual, combi, relations = createDerivationTables(
        list(baseline.keys())
    )

    relation_list = list(relations.keys())

    # -----------------------------------------------------
    # Convert baseline into a set of relational facts
    # -----------------------------------------------------

    baseline_facts = set()

    for rel_label, instances in baseline.items():
        for source, target in instances:
            baseline_facts.add(
                (rel_label, source, target)
            )

    # All currently known relations
    known = set(baseline_facts)

    # Worklist of relations that still need to be processed
    queue = deque()

    # depth of each derivation
    depth = {}

    # optional record of how relation was derived
    provenance = {}

    for fact in baseline_facts:
        queue.append(fact)
        depth[fact] = 0
        provenance[fact] = {
            "type": "baseline"
        }

    # -----------------------------------------------------
    # Helper for adding a new fact
    # -----------------------------------------------------

    def add_fact(
        rel_label,
        source,
        target,
        new_depth,
        derivation_type,
        parents
    ):

        # Ignore reflexive relations
        if source == target:
            return False

        fact = (
            rel_label,
            source,
            target
        )

        # Already known
        if fact in known:
            return False

        # Optional depth restriction
        if (
            max_depth is not None
            and new_depth > max_depth
        ):
            return False

        known.add(fact)
        queue.append(fact)

        depth[fact] = new_depth

        provenance[fact] = {
            "type": derivation_type,
            "parents": parents
        }

        return True

    # -----------------------------------------------------
    # Iteratively derive until closure
    # -----------------------------------------------------

    while queue:

        rel1Lab, s1a, s1b = queue.popleft()

        rel1 = relations[rel1Lab]
        source1 = (s1a, s1b)

        current_depth = depth[
            (rel1Lab, s1a, s1b)
        ]

        # =================================================
        # 1. MUTUAL ENTAILMENT
        # =================================================

        mrel = mutual[rel1]
        mrelLab = relation_list[mrel]

        add_fact(
            rel_label=mrelLab,
            source=s1b,
            target=s1a,
            new_depth=current_depth + 1,
            derivation_type="mutual",
            parents=[
                (rel1Lab, s1a, s1b)
            ]
        )

        # =================================================
        # 2. COMBINATORIAL ENTAILMENT
        # =================================================

        # snapshot because known can grow while processing
        known_snapshot = list(known)

        for rel2Lab, s2a, s2b in known_snapshot:

            fact2 = (
                rel2Lab,
                s2a,
                s2b
            )

            fact1 = (
                rel1Lab,
                s1a,
                s1b
            )

            # Don't combine a fact with itself
            if fact1 == fact2:
                continue

            rel2 = relations[rel2Lab]
            source2 = (s2a, s2b)

            common = findCommon(
                source1,
                source2
            )

            if common < 0:
                continue

            crel, source12 = deriveCombi(
                source1,
                source2,
                common,
                rel1,
                rel2,
                combi
            )

            # Ill-defined combination
            if crel < 0:
                continue

            crelLab = relation_list[crel]

            # source12 should represent the newly derived pair
            new_source, new_target = source12

            new_depth = max(
                depth[fact1],
                depth[fact2]
            ) + 1

            add_fact(
                rel_label=crelLab,
                source=new_source,
                target=new_target,
                new_depth=new_depth,
                derivation_type="combinatorial",
                parents=[
                    fact1,
                    fact2
                ]
            )

    # -----------------------------------------------------
    # Convert back to your existing dictionary format
    # -----------------------------------------------------

    derived = {
        rel: []
        for rel in relation_list
    }

    for rel_label, source, target in known:

        fact = (
            rel_label,
            source,
            target
        )

        # Don't return baseline relations as derived
        if fact in baseline_facts:
            continue

        derived[rel_label].append(
            (source, target)
        )

    # deterministic ordering
    for rel in derived:
        derived[rel] = sorted(
            derived[rel]
        )

    relTab = createRelationTable(
        baseline,
        derived
    )

    if illustrate == "heatmap":
        plotNetworkHeatmap(
            baseline,
            derived,
            sLabs
        )

    if illustrate == "graph":
        plotRelNetworkGraph(
            baseline,
            derived,
            sLabs,
            ['baseline', 'mutual', 'combi']
        )

    return relTab, derived