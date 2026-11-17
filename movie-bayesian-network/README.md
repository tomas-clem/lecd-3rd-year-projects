# Movie Bayesian Network

A Bayesian network learned from a dataset of IMDB movies, used to reason about how budget, revenue, score, status, country and genre relate to each other. For example, it estimates the probability that a film falls in a given budget or revenue range, or in the Action/Science Fiction/Adventure genre cluster, given what is known about it.

*Developed with Afonso Cordeiro. Course: APRP, University of Coimbra, 2023/24 (final project).*

## Approach

The notebook [movie_bayesian_network.ipynb](movie_bayesian_network.ipynb) keeps its outputs. The report is in [report-pt.pdf](report-pt.pdf) (Portuguese).

1. **Exploration and cleaning:**
   - checks for duplicates and missing values;
   - drops the 141 movies without genre or crew;
   - notes that budget and revenue are partly artificially imputed in the source data.
2. **Pre-processing:**
   - ordinal encoding of status and country;
   - one column per genre, with genres then grouped into clusters;
   - date split into month and year;
   - budget, revenue and score discretised into ranges chosen from their histograms.
3. **Structure learning:** hill climbing scored with BDeu, K2 and BIC. Knowledge engineering then removes nodes and edges that make no sense, such as the release year, and adds the expected relations between country and genre clusters.
4. **Parameters and inference:** maximum-likelihood CPDs and queries with variable elimination.

## Dataset

The IMDB movies dataset provided with the assignment (derived from the Kaggle "IMDB Movies Dataset"). It is not included. The notebook was run with the file in `Dataset_1/imdb_movies.csv`.

## Changes from the submitted version

- One cell's output was removed: 25 MB of repeated pandas `SettingWithCopyWarning` messages, which stopped GitHub from rendering the notebook. Code and all other outputs are unchanged.

## Known limitations

- Part 2 of the assignment (a variational autoencoder on movie posters) was not completed: its cells were never executed in this notebook, and a later conditional VAE attempt did not work.
- The notebook uses pgmpy's `BayesianModel`, which newer pgmpy versions have renamed to `BayesianNetwork`.
