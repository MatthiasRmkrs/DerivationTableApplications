This repository contains scripts to generate relational derivation tables and use them for various applications.
A paper describing the tables, tools and tutorials on how to use them is in production.

## Relational derivation tables 
The relational derivation tables we share are inspired by the work of Allen (1983) who constructed so-called transitivity tables of temporal relations to automate computer systems' reasoning about temporal relations.
These transitivty tables are essentially look-up tables for relational derivation: in Allen's example, the rows and colums of the transitivity table represent different temporal relations (i.e., rows represent relation between A-B, colums denote relations between B-C; e.g., A before B and B before C) , and the cells joining them represent the transitive relation that can be derived (i.e., A-C; e.g., A before C).

In this work, we expanded on Allen's tables by (1) including other relations beyond temporal relations that are typically studied in relational reasoning research; (2) included tables for both mutual entailment or bidirectionality of relations and the combinatorial entailment or transitivity of relations; and (3) included separate tables for the different ways in which two relations can be combined, leading to different derivations (e.g., A-B and B-C -> A-C vs. A-B and A-C -> B-C).
The tables in the illustration below feature a subset of supporteed relations. This subset was chosen because they can be considered as general versions of more specific relations. That is, the derivation patterns for these relations are the same as those for more specific instances of the general pattern (e.g., taller and shorter than are specific instances of more than and less than).
### Illustrations

*Derivation Table for Mutual Entailment*  
<img width="252" height="222" alt="MutualClean" src="https://github.com/user-attachments/assets/0c064ca3-2b06-4c1d-8aa4-c2bd3915eddb" />

*Derivation Table for Linear Combination of Relations*
<img width="817" height="450" alt="LinearDerivationTable_clean" src="https://github.com/user-attachments/assets/ac184414-3afa-48a8-9e9e-7d3c2e5fb38d" />

*Derivation Table for One-to-Many Combination of Relations*
<img width="816" height="340" alt="OTM_clean" src="https://github.com/user-attachments/assets/93fc1dab-841b-405a-96bd-aea1c914802a" />

## Tools Using Automated Relational Derivation
The derivation tables can be used to program an algorithm that automatically derives relations for a given set of input relations. This algorithm can then become the foundation for tools designed to facilitate relational reasoning research.
Specifically, we have created three tools: (1) Relational Network Visualizer; (2) Relational Syllogistic Reasoning Problem Generator and (3) Matching-to-Sample Procedure Generator. We briefly describe each tool below.

### Relational Network Visualizer

The first tool we share is intended to faciliate understanding of complex relational reasoning research. Due to the incredible generativity of human relational abilities, relational networks involved in experiments quickly become very large and intractable. To alleviate this, we have created a tool that illustrates relational networks as a graph network. Users can specify a set of input relations, for which the derivation algorithm will then derive all derived relations and illustrate the network given the plot settings provided by the user.
Users have control over which relations are plotted, over whether they are plotted all in one graph, or as separate graphs and over graph formatting (arrow styles, colors, etc.).

*Example Graph Illustration of the Relational Network Trained and Tested By Steele and Hayes (1991)* 
<img width="824" height="395" alt="image" src="https://github.com/user-attachments/assets/5b8c7d8d-555a-4129-82d4-07af4ae6fe69" />


Try the [Relational Network Plotter]()

### Relational Syllogistic Reasoning Task Generator

Try the [Relational Syllogistic Problem Generator](https://relationalsyllogismgenerator.streamlit.app/)
