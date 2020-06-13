Here are instructions for using the genetic algorithm codes in the subfolders. "conference building" contains genetic algorithm codes for the evacuation of a conference building, while "hexagon-shaped area" contains genetic algorithm codes for the evacuation of a hexagon-shaped area. For the conference building, there is the hidden gene genetic algorithm for both the stochastic and deterministic equivalent problems. For the hexagon-shaped are, there is both the genetic algorithm (fixed number of genes/guides) and hidden gene genetic algorithm codes.
NOTE! The specifications for the bash script files have to probably be changed depending on the computational cluster being used.

grand_scheme_stochastic.sh / grand_scheme_deterministic.sh
The main script, that calls other scripts to execute the genetic algorithm. Here you can specify the number of generations, population size, sample size, and, if you are running the regular genetic algorithm, you can specify the number of guides. The simulation of one generation is partitioned to four parts (for all other than the deterministic conference case) due to user quotas on the computational cluster, and the algorithm is run using a dependency chain, so the algorithm can be stopped and continued.

generate_seeds.sh
The script that creates seed numbers for the different samples of the crowd simulation.

initialize.sh
Creates randomly the values for the optimization variables (=the guides' starting positions and target exits) for the 0th generation.

genetic_algorithm_stochastic.sh / genetic_algorithm_deterministic.sh
Sends the seed number and values for the optimization variables to the crowd simulation model (shell_run_stochastic.py, shell_run_deterministic.py, shell_run_simple_stochastic.py, or shell_run_simple_nonhidden_stochastic.py depending on which case is simulated).

shell_run_stochastic.py / shell_run_deterministic.py / shell_run_simple_stochastic.py / shell_run_simple_nonhidden_stochastic.py
Python script for simulating the crowd evacuation.

finlandia_talo_ga_stochastic.py / finlandia_talo_ga_deterministic.py / simple_scenario_ga_stochastic.py
Contains the floor of the building and some other model specifications.

agents_initialization_conference.npy / agents_initialization_simple.npy
Data file that includes the initial positions of the exiting agents. We need this so that the guides are not positioned so that they overlap with the exiting agents.

gather_results_stochastic.sh / gather_results_deterministic.sh
Sends the current generation number, population size, sample size, number of guides and the names for the associated output files to "selection_stochastic.py" or "selection_deterministic.py.

selection_stochastic.py / selection_deterministic.py
Gathers the data from the solutions of one generation, and performs selection, crossover and mutation to create the next the population for the next generation.

onepointcrossover.py
The onepointcrossover operation for the genes.

onepointcrossover_tags.py
The onepointcrossover operation for the tags.

mutation.py
The mutation operation for the genes.

mutation_tags.py
The mutation operation for the tags.

plot_stochastic.sh / plot_deterministic.sh
A script that calls the file "generation_vs_evactime_stochastic.py" or "generation_vs_evactime_deterministic.py".

generation_vs_evactime_stochastic.py / generation_vs_evactime_deterministic.py
A file to inspect the convergence of the genetic algorithm. Plots the mean total evacuation time for the solutions in one generation.

solutionbank_deterministic.py
This was implemented in the first revision round of the article von Schantz & Ehtamo "Minimizing the evacuation time of a crowd from a complex building using rescue guides", that is why we only have it for the deterministic problem simulations. It is a python function for storing the genes and their associated fitnesses, so that they only have to be simulated once.

