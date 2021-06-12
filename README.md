# Vanishing size of critical mass for tipping points in social convention

This repository contains the code required to reproduce the results presented in the following paper:
- I. Iacopini, G. Petri, A. Baronchelli & A. Barrat (2021), *Vanishing size of critical mass for tipping points in social convention*, arXiv:2103.10411 [[link to preprint](https://arxiv.org/pdf/2103.10411.pdf)].

# Data
 
 This study relies on publicly available datasets that have been collected and released in previous publications:
 
- **Face-to-face interactions** by the [SocioPatterns collaboration](http://www.sociopatterns.org/) and downloaded from [here](http://www.sociopatterns.org/datasets/).
- **Email-EU** data set presented in [Paranjape et al. 2017](https://dl.acm.org/doi/10.1145/3018661.3018731) and downloaded from [here](https://github.com/arbenson/ScHoLP-Data).
- **Congress-bills** data set presented in [Fowler 2017](https://www.sciencedirect.com/science/article/pii/S0378873305000730) and downloaded from [here](https://github.com/arbenson/ScHoLP-Data).

Orinal and processed data are both stored in the `Data` folder.

# Code

Most of the scripts are Jupyter notebooks contained in the `Notebooks` folder:
- `0_Integrating MF equations for 2-words HONG.ipynb` defines mean field equations and integrates them numerically
- `1_Simulations - Homogeneous Mixing 2-HGs.ipynb` simulates the NG on homogeneous 2-hypergraphs for comparison with the analytics
- `2_ Comparing MF with stochastic simulations.ipynb` compares the esults from the previous two notebooks (MF vs analytical)
- `3_Preprocessing Email-EU and Congress-bills data sets.ipynb` processing the two biggest data sets on emails communication and US congress bills
- `4_Preprocessing Sociopatterns data sets.ipynb` processing the face-to-face interactions from the sociopatterns collaboration
- `5_Example of a simulation on a hypergraph.ipynb` simulates one game on a given higher-order structure
- `6_Aggregating simulations results (run externally) on empirical data sets.ipynb` performs an aggregation of the simulation results on empirical data sets (these are run separately through the authomatically created scripts contained in the `Scripts` folder)
- `7_Simulations - Homogeneous Mixing HGs with groups of different sizes.ipynb` simulates the NG on homogeneous k-hypergraphs of increasing size (these are run separately through the bash script contained in the notebook)
- `8_Figures.ipynb` plots most of the figures

Results are put in a `Results` folder.
