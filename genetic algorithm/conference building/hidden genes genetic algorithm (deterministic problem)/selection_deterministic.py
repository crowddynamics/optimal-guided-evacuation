import sys
import os
import numpy as np

from onepointcrossover import onepointcrossover
from onepointcrossover_tags import onepointcrossover_tags
from mutation import mutation
from mutation_tags import mutation_tags 

# Slurm JOBID for the simulations of current generation
jobid = str(sys.argv[1])

# Generation number
generation = int(sys.argv[2])

# Number of individuals in a population
population = int(sys.argv[3])

# Total number of simulations
n_simulations = population

# Probability for crossover
CXPB = 0.85
CXPB_tags = 0.85

# Probability for mutation
MUTPB = 0.1
MUTPB_tags = 0.1
#MUTPB = 0.4
#MUTPB_tags = 0.4

# Elitism fractions for different generations (starting from generation number 1)
# If generation number is over length of the elitism_pr list (>20) use just all parents for selection
elitism_pr = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

# Write simulation results to a single file
positions = []
all_output = []

# Due to user quotas, we have to run one generation in three parts
for i in range(0,int(population)):
    fname = "{}{}{}{}{}".format('slurm-', jobid, '_', i, '.out')
    with open(fname) as infile:
        lines1 = [line.rstrip('\n') for line in infile]
        if len(lines1) == 2:
            positions.append(lines1[0])
            all_output.append(lines1[1])
        elif len(lines1) == 1:
            positions.append([])
            all_output.append(lines1[0])
        else:
            positions.append([])
            all_output.append(0.0)

# There might be a few invalid runs (because of faults in the spawning).
# Replace the results of invalid runs with 0.0
evactimes = []
for i in range(0, population):
    try:
        evactimes.append(float(all_output[i]))
    except ValueError:
        evactimes.append(0.0)

# If there are invalid samples, replace them with a random valid sample
waste = np.argwhere(np.asarray(evactimes)==0.0)
nonwaste = np.argwhere(np.asarray(evactimes)!=0.0)
n_waste = len(waste)
n_nonwaste = len(nonwaste)

if n_waste > 0:
    indxs_replacement = []
    for i in range(0, n_waste):
        rand_indx = np.random.randint(0, population-n_waste, 1)[0]
        indxs_replacement.append(nonwaste[rand_indx][0])
        evactimes[waste[i][0]] = evactimes[indxs_replacement[i]]
        positions[waste[i][0]] = positions[indxs_replacement[i]]

# Use eliticism.
# Take the n_simulations best individuals from the parents and the offspring
# The population of the first generation will always be random.
# Already the second generation will consist of the n_simulations best individuals from the first generation
# and the crossovered and mutated offspring.
  
# Save the sample means (here the invalid samples have been replaced, and only valid values exist)
np.savetxt("{}{}{}".format('results_', generation, '.txt'), np.asarray(evactimes), fmt='%.14f')
   
# Save the sample positions (here the invalid samples have been replaced, and only valid values exist)
f = open("{}{}{}".format('positions_', generation, '.txt'), "w")
for i in range(population):
    f.write("{}{}".format(positions[i], '\n'))
f.close()
    
if generation > 0:
    
    # Open the results of the previous generation and extend them to the results of current generation

    # Sample means
    parents_results = np.loadtxt("{}{}{}".format('selected_results_', generation-1, '.txt'))
    parents_results = parents_results.tolist()
    evactimes.extend(parents_results)

    # Sample positions
    with open("{}{}{}".format('selected_positions_', generation-1, '.txt')) as infile:
        lines3 = [line.rstrip('\n') for line in infile]
    positions.extend(lines3)

# If generation number greater or equal to 1 use elitism.
# NOTE DOESN'T WORK FOR SMALLER POPULATIONS THAN 20, OR POPULATIONS NOT DIVISIBLE BY 20
if generation >= 1:
    parents_evactimes = evactimes[population:]
    sorted_indices_parents = sorted(range(population), key=lambda k : parents_evactimes[k])
    sorted_indices_parents = sorted_indices_parents[0:population*int(elitism_pr[generation]*population)]
    sorted_indices_parents = [sorted_indices_parents[i] + population for i in range(len(sorted_indices_parents))]

help_indices = [i for i in range(population)]
scores = evactimes[0:population]

if generation >= 1:
    for i in range(len(sorted_indices_parents)):
        help_indices.append(sorted_indices_parents[i])
        scores.append(evactimes[sorted_indices_parents[i]])

sorted_indices = sorted(range(len(scores)), key=lambda k : scores[k])

selected_ordered = np.empty(population, dtype=int)
for i in range(population):
    selected_ordered[i] = help_indices[sorted_indices[i]]

# Scramble the selected individuals
permuted_order = np.random.permutation(population)
selected = np.empty(population, dtype=int)
for i in range(population):
    selected[i] = selected_ordered[permuted_order[i]]

# Check if some of the chosen individuals where of "invalid" type. Replace their
# indices with their replacement. => This way we won't breed any of the invalid
# types.
# THIS IS DONE SO THAT WE USE THE CORRECT EXIT AND CELL DATA WHEN BREEDING!
if n_waste > 0:
    for i in range(0, n_waste):
        wrongly_chosen = np.argwhere(selected==waste[i])
        if len(wrongly_chosen) > 0:
            for j in range(0, len(wrongly_chosen)):
                selected[wrongly_chosen[j]] = indxs_replacement[i]

# Load data of individuals and create lists where to store data of new generation.
exits1 = np.loadtxt("{}{}{}".format('exits1_', generation, '.txt'), dtype=int)
cells1 = np.loadtxt("{}{}{}".format('cells1_', generation, '.txt'), dtype=int)
tags1 = np.loadtxt("{}{}{}".format('tags1_', generation, '.txt'), dtype=int)
if generation > 0:
    exits1_prev = np.loadtxt("{}{}{}".format('selected_exits1_', generation-1, '.txt'), dtype=int)
    cells1_prev = np.loadtxt("{}{}{}".format('selected_cells1_', generation-1, '.txt'), dtype=int)
    tags1_prev = np.loadtxt("{}{}{}".format('selected_tags1_', generation-1, '.txt'), dtype=int)
    tags1 = np.concatenate((tags1, tags1_prev), axis=None)
    exits1 = np.concatenate((exits1, exits1_prev), axis=None)
    cells1 = np.concatenate((cells1, cells1_prev), axis=None)

exits1.tolist()
cells1.tolist()
selected_exits1 = []
selected_cells1 = []
new_exits1 = []
new_cells1 = []
tags1.tolist()
selected_tags1 = []
new_tags1 = []

exits2 = np.loadtxt("{}{}{}".format('exits2_', generation, '.txt'), dtype=int)
cells2 = np.loadtxt("{}{}{}".format('cells2_', generation, '.txt'), dtype=int)
tags2 = np.loadtxt("{}{}{}".format('tags2_', generation, '.txt'), dtype=int)
if generation > 0:
    exits2_prev = np.loadtxt("{}{}{}".format('selected_exits2_', generation-1, '.txt'), dtype=int)
    cells2_prev = np.loadtxt("{}{}{}".format('selected_cells2_', generation-1, '.txt'), dtype=int)
    tags2_prev = np.loadtxt("{}{}{}".format('selected_tags2_', generation-1, '.txt'), dtype=int)
    tags2 = np.concatenate((tags2, tags2_prev), axis=None)
    exits2 = np.concatenate((exits2, exits2_prev), axis=None)
    cells2 = np.concatenate((cells2, cells2_prev), axis=None)

exits2.tolist()
cells2.tolist()
selected_exits2 = []
selected_cells2 = []
new_exits2 = []
new_cells2 = []
tags2.tolist()
selected_tags2 = []
new_tags2 = []

exits3 = np.loadtxt("{}{}{}".format('exits3_', generation, '.txt'), dtype=int)
cells3 = np.loadtxt("{}{}{}".format('cells3_', generation, '.txt'), dtype=int)
tags3 = np.loadtxt("{}{}{}".format('tags3_', generation, '.txt'), dtype=int)
if generation > 0:
    exits3_prev = np.loadtxt("{}{}{}".format('selected_exits3_', generation-1, '.txt'), dtype=int)
    cells3_prev = np.loadtxt("{}{}{}".format('selected_cells3_', generation-1, '.txt'), dtype=int)
    tags3_prev = np.loadtxt("{}{}{}".format('selected_tags3_', generation-1, '.txt'), dtype=int)
    tags3 = np.concatenate((tags3, tags3_prev), axis=None)
    exits3 = np.concatenate((exits3, exits3_prev), axis=None)
    cells3 = np.concatenate((cells3, cells3_prev), axis=None)

exits3.tolist()
cells3.tolist()
selected_exits3 = []
selected_cells3 = []
new_exits3 = []
new_cells3 = []
tags3.tolist()
selected_tags3 = []
new_tags3 = []

exits4 = np.loadtxt("{}{}{}".format('exits4_', generation, '.txt'), dtype=int)
cells4 = np.loadtxt("{}{}{}".format('cells4_', generation, '.txt'), dtype=int)
tags4 = np.loadtxt("{}{}{}".format('tags4_', generation, '.txt'), dtype=int)
if generation > 0:
    exits4_prev = np.loadtxt("{}{}{}".format('selected_exits4_', generation-1, '.txt'), dtype=int)
    cells4_prev = np.loadtxt("{}{}{}".format('selected_cells4_', generation-1, '.txt'), dtype=int)
    tags4_prev = np.loadtxt("{}{}{}".format('selected_tags4_', generation-1, '.txt'), dtype=int)
    tags4 = np.concatenate((tags4, tags4_prev), axis=None)
    exits4 = np.concatenate((exits4, exits4_prev), axis=None)
    cells4 = np.concatenate((cells4, cells4_prev), axis=None)

exits4.tolist()
cells4.tolist()
selected_exits4 = []
selected_cells4 = []
new_exits4 = []
new_cells4 = []
tags4.tolist()
selected_tags4 = []
new_tags4 = []

exits5 = np.loadtxt("{}{}{}".format('exits5_', generation, '.txt'), dtype=int)
cells5 = np.loadtxt("{}{}{}".format('cells5_', generation, '.txt'), dtype=int)
tags5 = np.loadtxt("{}{}{}".format('tags5_', generation, '.txt'), dtype=int)
if generation > 0:
    exits5_prev = np.loadtxt("{}{}{}".format('selected_exits5_', generation-1, '.txt'), dtype=int)
    cells5_prev = np.loadtxt("{}{}{}".format('selected_cells5_', generation-1, '.txt'), dtype=int)
    tags5_prev = np.loadtxt("{}{}{}".format('selected_tags5_', generation-1, '.txt'), dtype=int)
    tags5 = np.concatenate((tags5, tags5_prev), axis=None)
    exits5 = np.concatenate((exits5, exits5_prev), axis=None)
    cells5 = np.concatenate((cells5, cells5_prev), axis=None)

exits5.tolist()
cells5.tolist()
selected_exits5 = []
selected_cells5 = []
new_exits5 = []
new_cells5 = []
tags5.tolist()
selected_tags5 = []
new_tags5 = []

exits6 = np.loadtxt("{}{}{}".format('exits6_', generation, '.txt'), dtype=int)
cells6 = np.loadtxt("{}{}{}".format('cells6_', generation, '.txt'), dtype=int)
tags6 = np.loadtxt("{}{}{}".format('tags6_', generation, '.txt'), dtype=int)
if generation > 0:
    exits6_prev = np.loadtxt("{}{}{}".format('selected_exits6_', generation-1, '.txt'), dtype=int)
    cells6_prev = np.loadtxt("{}{}{}".format('selected_cells6_', generation-1, '.txt'), dtype=int)
    tags6_prev = np.loadtxt("{}{}{}".format('selected_tags6_', generation-1, '.txt'), dtype=int)
    tags6 = np.concatenate((tags6, tags6_prev), axis=None)
    exits6 = np.concatenate((exits6, exits6_prev), axis=None)
    cells6 = np.concatenate((cells6, cells6_prev), axis=None)

exits6.tolist()
cells6.tolist()
selected_exits6 = []
selected_cells6 = []
new_exits6 = []
new_cells6 = []
tags6.tolist()
selected_tags6 = []
new_tags6 = []

exits7 = np.loadtxt("{}{}{}".format('exits7_', generation, '.txt'), dtype=int)
cells7 = np.loadtxt("{}{}{}".format('cells7_', generation, '.txt'), dtype=int)
tags7 = np.loadtxt("{}{}{}".format('tags7_', generation, '.txt'), dtype=int)
if generation > 0:
    exits7_prev = np.loadtxt("{}{}{}".format('selected_exits7_', generation-1, '.txt'), dtype=int)
    cells7_prev = np.loadtxt("{}{}{}".format('selected_cells7_', generation-1, '.txt'), dtype=int)
    tags7_prev = np.loadtxt("{}{}{}".format('selected_tags7_', generation-1, '.txt'), dtype=int)
    tags7 = np.concatenate((tags7, tags7_prev), axis=None)
    exits7 = np.concatenate((exits7, exits7_prev), axis=None)
    cells7 = np.concatenate((cells7, cells7_prev), axis=None)

exits7.tolist()
cells7.tolist()
selected_exits7 = []
selected_cells7 = []
new_exits7 = []
new_cells7 = []
tags7.tolist()
selected_tags7 = []
new_tags7 = []

exits8 = np.loadtxt("{}{}{}".format('exits8_', generation, '.txt'), dtype=int)
cells8 = np.loadtxt("{}{}{}".format('cells8_', generation, '.txt'), dtype=int)
tags8 = np.loadtxt("{}{}{}".format('tags8_', generation, '.txt'), dtype=int)
if generation > 0:
    exits8_prev = np.loadtxt("{}{}{}".format('selected_exits8_', generation-1, '.txt'), dtype=int)
    cells8_prev = np.loadtxt("{}{}{}".format('selected_cells8_', generation-1, '.txt'), dtype=int)
    tags8_prev = np.loadtxt("{}{}{}".format('selected_tags8_', generation-1, '.txt'), dtype=int)
    tags8 = np.concatenate((tags8, tags8_prev), axis=None)
    exits8 = np.concatenate((exits8, exits8_prev), axis=None)
    cells8 = np.concatenate((cells8, cells8_prev), axis=None)

exits8.tolist()
cells8.tolist()
selected_exits8 = []
selected_cells8 = []
new_exits8 = []
new_cells8 = []
tags8.tolist()
selected_tags8 = []
new_tags8 = []

exits9 = np.loadtxt("{}{}{}".format('exits9_', generation, '.txt'), dtype=int)
cells9 = np.loadtxt("{}{}{}".format('cells9_', generation, '.txt'), dtype=int)
tags9 = np.loadtxt("{}{}{}".format('tags9_', generation, '.txt'), dtype=int)
if generation > 0:
    exits9_prev = np.loadtxt("{}{}{}".format('selected_exits9_', generation-1, '.txt'), dtype=int)
    cells9_prev = np.loadtxt("{}{}{}".format('selected_cells9_', generation-1, '.txt'), dtype=int)
    tags9_prev = np.loadtxt("{}{}{}".format('selected_tags9_', generation-1, '.txt'), dtype=int)
    tags9 = np.concatenate((tags9, tags9_prev), axis=None)
    exits9 = np.concatenate((exits9, exits9_prev), axis=None)
    cells9 = np.concatenate((cells9, cells9_prev), axis=None)

exits9.tolist()
cells9.tolist()
selected_exits9 = []
selected_cells9 = []
new_exits9 = []
new_cells9 = []
tags9.tolist()
selected_tags9 = []
new_tags9 = []

exits10 = np.loadtxt("{}{}{}".format('exits10_', generation, '.txt'), dtype=int)
cells10 = np.loadtxt("{}{}{}".format('cells10_', generation, '.txt'), dtype=int)
tags10 = np.loadtxt("{}{}{}".format('tags10_', generation, '.txt'), dtype=int)
if generation > 0:
    exits10_prev = np.loadtxt("{}{}{}".format('selected_exits10_', generation-1, '.txt'), dtype=int)
    cells10_prev = np.loadtxt("{}{}{}".format('selected_cells10_', generation-1, '.txt'), dtype=int)
    tags10_prev = np.loadtxt("{}{}{}".format('selected_tags10_', generation-1, '.txt'), dtype=int)
    tags10 = np.concatenate((tags10, tags10_prev), axis=None)
    exits10 = np.concatenate((exits10, exits10_prev), axis=None)
    cells10 = np.concatenate((cells10, cells10_prev), axis=None)

exits10.tolist()
cells10.tolist()
selected_exits10 = []
selected_cells10 = []
new_exits10 = []
new_cells10 = []
tags10.tolist()
selected_tags10 = []
new_tags10 = []

# Store the data of the individuals selected for breeding
selected_evactimes = []
selected_positions = []
for i in range(population):
    selected_evactimes.append(evactimes[selected[i]])
    selected_positions.append(positions[selected[i]])
    # Remember that the cells and exits contain each values several times (the amount is equal to samples)
    selected_exits1.append(exits1[selected[i]])
    selected_cells1.append(cells1[selected[i]])
    selected_tags1.append(tags1[selected[i]])

    selected_exits2.append(exits2[selected[i]])
    selected_cells2.append(cells2[selected[i]])
    selected_tags2.append(tags2[selected[i]])

    selected_exits3.append(exits3[selected[i]])
    selected_cells3.append(cells3[selected[i]])
    selected_tags3.append(tags3[selected[i]])

    selected_exits4.append(exits4[selected[i]])
    selected_cells4.append(cells4[selected[i]])
    selected_tags4.append(tags4[selected[i]])

    selected_exits5.append(exits5[selected[i]])
    selected_cells5.append(cells5[selected[i]])
    selected_tags5.append(tags5[selected[i]])

    selected_exits6.append(exits6[selected[i]])
    selected_cells6.append(cells6[selected[i]])
    selected_tags6.append(tags6[selected[i]])

    selected_exits7.append(exits7[selected[i]])
    selected_cells7.append(cells7[selected[i]])
    selected_tags7.append(tags7[selected[i]])

    selected_exits8.append(exits8[selected[i]])
    selected_cells8.append(cells8[selected[i]])
    selected_tags8.append(tags8[selected[i]])

    selected_exits9.append(exits9[selected[i]])
    selected_cells9.append(cells9[selected[i]])
    selected_tags9.append(tags9[selected[i]])

    selected_exits10.append(exits10[selected[i]])
    selected_cells10.append(cells10[selected[i]])
    selected_tags10.append(tags10[selected[i]])
    
# Eliticism
# Save results of all the runs (whole invalid samples have been replaced, but single invalid values, disguised as 0.0 can occur)
np.savetxt("{}{}{}".format('selected_results_', generation, '.txt'), np.asarray(selected_evactimes), fmt='%.14f')

# Save the positions of all the runs (whole invalid samples have been replaced, but single invalid values, which are error messages can occur)
f = open("{}{}{}".format('selected_positions_', generation, '.txt'), "w")
for i in range(n_simulations):
    f.write("{}{}".format(selected_positions[i], '\n'))
f.close()

# Save the exits and cells of the selected individuals
f = open("{}{}{}".format('selected_', generation, '.txt'), "w")
for i in range(population):
    f.write("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(selected_tags1[i], ' ', selected_exits1[i], ' ', selected_cells1[i], ' ', selected_tags2[i], ' ', selected_exits2[i], ' ', selected_cells2[i], ' ', selected_tags3[i], ' ', selected_exits3[i], ' ', selected_cells3[i], ' ', selected_tags4[i], ' ', selected_exits4[i], ' ', selected_cells4[i], ' ', selected_tags5[i], ' ', selected_exits5[i], ' ', selected_cells5[i], ' ', selected_tags6[i], ' ', selected_exits6[i], ' ', selected_cells6[i], ' ', selected_tags7[i], ' ', selected_exits7[i], ' ', selected_cells7[i], ' ', selected_tags8[i], ' ', selected_exits8[i], ' ', selected_cells8[i], ' ', selected_tags9[i], ' ', selected_exits9[i], ' ', selected_cells9[i], ' ', selected_tags10[i], ' ', selected_exits10[i], ' ', selected_cells10[i],'\n'))

f.close()

inds1 = np.arange(0,population,2)
inds2 = np.arange(1,population,2)
# Start breeding
for ind1, ind2 in zip(inds1, inds2):
    
    ind1_exits = []
    ind1_cells = []
    ind1_tags = []
    ind2_exits = []
    ind2_cells = []
    ind2_tags = []    

    # Store the data of the individuals in lists
    ind1_exits.append(selected_exits1[ind1])
    ind1_cells.append(selected_cells1[ind1])
    ind1_tags.append(selected_tags1[ind1])
    ind2_exits.append(selected_exits1[ind2])
    ind2_cells.append(selected_cells1[ind2])
    ind2_tags.append(selected_tags1[ind2])

    ind1_exits.append(selected_exits2[ind1])
    ind1_cells.append(selected_cells2[ind1])
    ind1_tags.append(selected_tags2[ind1])
    ind2_exits.append(selected_exits2[ind2])
    ind2_cells.append(selected_cells2[ind2])
    ind2_tags.append(selected_tags2[ind2])

    ind1_exits.append(selected_exits3[ind1])
    ind1_cells.append(selected_cells3[ind1])
    ind1_tags.append(selected_tags3[ind1])
    ind2_exits.append(selected_exits3[ind2])
    ind2_cells.append(selected_cells3[ind2])
    ind2_tags.append(selected_tags3[ind2])

    ind1_exits.append(selected_exits4[ind1])
    ind1_cells.append(selected_cells4[ind1])
    ind1_tags.append(selected_tags4[ind1])
    ind2_exits.append(selected_exits4[ind2])
    ind2_cells.append(selected_cells4[ind2])
    ind2_tags.append(selected_tags4[ind2])

    ind1_exits.append(selected_exits5[ind1])
    ind1_cells.append(selected_cells5[ind1])
    ind1_tags.append(selected_tags5[ind1])
    ind2_exits.append(selected_exits5[ind2])
    ind2_cells.append(selected_cells5[ind2])
    ind2_tags.append(selected_tags5[ind2])

    ind1_exits.append(selected_exits6[ind1])
    ind1_cells.append(selected_cells6[ind1])
    ind1_tags.append(selected_tags6[ind1])
    ind2_exits.append(selected_exits6[ind2])
    ind2_cells.append(selected_cells6[ind2])
    ind2_tags.append(selected_tags6[ind2])

    ind1_exits.append(selected_exits7[ind1])
    ind1_cells.append(selected_cells7[ind1])
    ind1_tags.append(selected_tags7[ind1])
    ind2_exits.append(selected_exits7[ind2])
    ind2_cells.append(selected_cells7[ind2])
    ind2_tags.append(selected_tags7[ind2])

    ind1_exits.append(selected_exits8[ind1])
    ind1_cells.append(selected_cells8[ind1])
    ind1_tags.append(selected_tags8[ind1])
    ind2_exits.append(selected_exits8[ind2])
    ind2_cells.append(selected_cells8[ind2])
    ind2_tags.append(selected_tags8[ind2])

    ind1_exits.append(selected_exits9[ind1])
    ind1_cells.append(selected_cells9[ind1])
    ind1_tags.append(selected_tags9[ind1])
    ind2_exits.append(selected_exits9[ind2])
    ind2_cells.append(selected_cells9[ind2])
    ind2_tags.append(selected_tags9[ind2])

    ind1_exits.append(selected_exits10[ind1])
    ind1_cells.append(selected_cells10[ind1])
    ind1_tags.append(selected_tags10[ind1])
    ind2_exits.append(selected_exits10[ind2])
    ind2_cells.append(selected_cells10[ind2])
    ind2_tags.append(selected_tags10[ind2])

    # Crossover with probability CXPB
    if np.random.uniform(0,1,1) <= CXPB:
        ind1_newexits, ind1_newcells, ind2_newexits, ind2_newcells = onepointcrossover(ind1_exits, ind1_cells, ind2_exits, ind2_cells)

        # Mutate genes of chromosomes
        ind1_newexits, ind1_newcells = mutation(ind1_newexits, ind1_newcells, MUTPB)
        ind2_newexits, ind2_newcells = mutation(ind2_newexits, ind2_newcells, MUTPB)

    else:
        # Mutate genes of chromosomes
        ind1_newexits, ind1_newcells = mutation(ind1_exits, ind1_cells, MUTPB)
        ind2_newexits, ind2_newcells = mutation(ind2_exits, ind2_cells, MUTPB)

    # Crossover tags with probability CXPB_tag
    if np.random.uniform(0,1,1) <= CXPB_tags:
        ind1_newtags, ind2_newtags = onepointcrossover_tags(ind1_tags, ind2_tags)

        # Mutate tags of chromosomes
        ind1_newtags = mutation_tags(ind1_newtags, MUTPB_tags)
        ind2_newtags = mutation_tags(ind2_newtags, MUTPB_tags)

    else:
        # Mutate tags of chromosomes
        ind1_newtags = mutation_tags(ind1_tags, MUTPB_tags)
        ind2_newtags = mutation_tags(ind2_tags, MUTPB_tags)

    # Append data of offspring to lists
    new_exits1.append(ind1_newexits[0])
    new_exits1.append(ind2_newexits[0])
    new_cells1.append(ind1_newcells[0])
    new_cells1.append(ind2_newcells[0])
    new_tags1.append(ind1_newtags[0])
    new_tags1.append(ind2_newtags[0])

    new_exits2.append(ind1_newexits[1])
    new_exits2.append(ind2_newexits[1])
    new_cells2.append(ind1_newcells[1])
    new_cells2.append(ind2_newcells[1])
    new_tags2.append(ind1_newtags[1])
    new_tags2.append(ind2_newtags[1])

    new_exits3.append(ind1_newexits[2])
    new_exits3.append(ind2_newexits[2])
    new_cells3.append(ind1_newcells[2])
    new_cells3.append(ind2_newcells[2])
    new_tags3.append(ind1_newtags[2])
    new_tags3.append(ind2_newtags[2])

    new_exits4.append(ind1_newexits[3])
    new_exits4.append(ind2_newexits[3])
    new_cells4.append(ind1_newcells[3])
    new_cells4.append(ind2_newcells[3])
    new_tags4.append(ind1_newtags[3])
    new_tags4.append(ind2_newtags[3])

    new_exits5.append(ind1_newexits[4])
    new_exits5.append(ind2_newexits[4])
    new_cells5.append(ind1_newcells[4])
    new_cells5.append(ind2_newcells[4])
    new_tags5.append(ind1_newtags[4])
    new_tags5.append(ind2_newtags[4])

    new_exits6.append(ind1_newexits[5])
    new_exits6.append(ind2_newexits[5])
    new_cells6.append(ind1_newcells[5])
    new_cells6.append(ind2_newcells[5])
    new_tags6.append(ind1_newtags[5])
    new_tags6.append(ind2_newtags[5])

    new_exits7.append(ind1_newexits[6])
    new_exits7.append(ind2_newexits[6])
    new_cells7.append(ind1_newcells[6])
    new_cells7.append(ind2_newcells[6])
    new_tags7.append(ind1_newtags[6])
    new_tags7.append(ind2_newtags[6])

    new_exits8.append(ind1_newexits[7])
    new_exits8.append(ind2_newexits[7])
    new_cells8.append(ind1_newcells[7])
    new_cells8.append(ind2_newcells[7])
    new_tags8.append(ind1_newtags[7])
    new_tags8.append(ind2_newtags[7])

    new_exits9.append(ind1_newexits[8])
    new_exits9.append(ind2_newexits[8])
    new_cells9.append(ind1_newcells[8])
    new_cells9.append(ind2_newcells[8])
    new_tags9.append(ind1_newtags[8])
    new_tags9.append(ind2_newtags[8])

    new_exits10.append(ind1_newexits[9])
    new_exits10.append(ind2_newexits[9])
    new_cells10.append(ind1_newcells[9])
    new_cells10.append(ind2_newcells[9])
    new_tags10.append(ind1_newtags[9])
    new_tags10.append(ind2_newtags[9])

# Make copies of exits and cells for all next generation simulations
all_new_exits1 = []
all_new_cells1 = []
all_new_tags1 = []

all_new_exits2 = []
all_new_cells2 = []
all_new_tags2 = []

all_new_exits3 = []
all_new_cells3 = []
all_new_tags3 = []

all_new_exits4 = []
all_new_cells4 = []
all_new_tags4 = []

all_new_exits5 = []
all_new_cells5 = []
all_new_tags5 = []

all_new_exits6 = []
all_new_cells6 = []
all_new_tags6 = []

all_new_exits7 = []
all_new_cells7 = []
all_new_tags7 = []

all_new_exits8 = []
all_new_cells8 = []
all_new_tags8 = []

all_new_exits9 = []
all_new_cells9 = []
all_new_tags9 = []

all_new_exits10 = []
all_new_cells10 = []
all_new_tags10 = []

for i in range(population):
    all_new_exits1.append(new_exits1[i])
    all_new_cells1.append(new_cells1[i])
    all_new_tags1.append(new_tags1[i])

    all_new_exits2.append(new_exits2[i])
    all_new_cells2.append(new_cells2[i])
    all_new_tags2.append(new_tags2[i])

    all_new_exits3.append(new_exits3[i])
    all_new_cells3.append(new_cells3[i])
    all_new_tags3.append(new_tags3[i])

    all_new_exits4.append(new_exits4[i])
    all_new_cells4.append(new_cells4[i])
    all_new_tags4.append(new_tags4[i])

    all_new_exits5.append(new_exits5[i])
    all_new_cells5.append(new_cells5[i])
    all_new_tags5.append(new_tags5[i])

    all_new_exits6.append(new_exits6[i])
    all_new_cells6.append(new_cells6[i])
    all_new_tags6.append(new_tags6[i])

    all_new_exits7.append(new_exits7[i])
    all_new_cells7.append(new_cells7[i])
    all_new_tags7.append(new_tags7[i])

    all_new_exits8.append(new_exits8[i])
    all_new_cells8.append(new_cells8[i])
    all_new_tags8.append(new_tags8[i])

    all_new_exits9.append(new_exits9[i])
    all_new_cells9.append(new_cells9[i])
    all_new_tags9.append(new_tags9[i])

    all_new_exits10.append(new_exits10[i])
    all_new_cells10.append(new_cells10[i])
    all_new_tags10.append(new_tags10[i])

# Remove previous generation data and store new data
np.savetxt("{}{}{}".format('exits1_', generation+1, '.txt'), np.asarray(all_new_exits1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells1_', generation+1, '.txt'), np.asarray(all_new_cells1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags1_', generation+1, '.txt'), np.asarray(all_new_tags1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits1_', generation, '.txt'), np.asarray(selected_exits1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells1_', generation, '.txt'), np.asarray(selected_cells1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags1_', generation, '.txt'), np.asarray(selected_tags1, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits2_', generation+1, '.txt'), np.asarray(all_new_exits2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells2_', generation+1, '.txt'), np.asarray(all_new_cells2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags2_', generation+1, '.txt'), np.asarray(all_new_tags2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits2_', generation, '.txt'), np.asarray(selected_exits2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells2_', generation, '.txt'), np.asarray(selected_cells2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags2_', generation, '.txt'), np.asarray(selected_tags2, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits3_', generation+1, '.txt'), np.asarray(all_new_exits3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells3_', generation+1, '.txt'), np.asarray(all_new_cells3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags3_', generation+1, '.txt'), np.asarray(all_new_tags3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits3_', generation, '.txt'), np.asarray(selected_exits3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells3_', generation, '.txt'), np.asarray(selected_cells3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags3_', generation, '.txt'), np.asarray(selected_tags3, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits4_', generation+1, '.txt'), np.asarray(all_new_exits4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells4_', generation+1, '.txt'), np.asarray(all_new_cells4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags4_', generation+1, '.txt'), np.asarray(all_new_tags4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits4_', generation, '.txt'), np.asarray(selected_exits4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells4_', generation, '.txt'), np.asarray(selected_cells4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags4_', generation, '.txt'), np.asarray(selected_tags4, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits5_', generation+1, '.txt'), np.asarray(all_new_exits5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells5_', generation+1, '.txt'), np.asarray(all_new_cells5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags5_', generation+1, '.txt'), np.asarray(all_new_tags5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits5_', generation, '.txt'), np.asarray(selected_exits5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells5_', generation, '.txt'), np.asarray(selected_cells5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags5_', generation, '.txt'), np.asarray(selected_tags5, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits6_', generation+1, '.txt'), np.asarray(all_new_exits6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells6_', generation+1, '.txt'), np.asarray(all_new_cells6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags6_', generation+1, '.txt'), np.asarray(all_new_tags6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits6_', generation, '.txt'), np.asarray(selected_exits6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells6_', generation, '.txt'), np.asarray(selected_cells6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags6_', generation, '.txt'), np.asarray(selected_tags6, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits7_', generation+1, '.txt'), np.asarray(all_new_exits7, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells7_', generation+1, '.txt'), np.asarray(all_new_cells7, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags7_', generation+1, '.txt'), np.asarray(all_new_tags7, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits7_', generation, '.txt'), np.asarray(selected_exits7, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells7_', generation, '.txt'), np.asarray(selected_cells7, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags7_', generation, '.txt'), np.asarray(selected_tags7, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits8_', generation+1, '.txt'), np.asarray(all_new_exits8, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells8_', generation+1, '.txt'), np.asarray(all_new_cells8, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags8_', generation+1, '.txt'), np.asarray(all_new_tags8, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits8_', generation, '.txt'), np.asarray(selected_exits8, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells8_', generation, '.txt'), np.asarray(selected_cells8, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags8_', generation, '.txt'), np.asarray(selected_tags8, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits9_', generation+1, '.txt'), np.asarray(all_new_exits9, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells9_', generation+1, '.txt'), np.asarray(all_new_cells9, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags9_', generation+1, '.txt'), np.asarray(all_new_tags9, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits9_', generation, '.txt'), np.asarray(selected_exits9, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells9_', generation, '.txt'), np.asarray(selected_cells9, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags9_', generation, '.txt'), np.asarray(selected_tags9, dtype=int), fmt='%i', delimiter=' ', newline=' ')

np.savetxt("{}{}{}".format('exits10_', generation+1, '.txt'), np.asarray(all_new_exits10, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells10_', generation+1, '.txt'), np.asarray(all_new_cells10, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('tags10_', generation+1, '.txt'), np.asarray(all_new_tags10, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits10_', generation, '.txt'), np.asarray(selected_exits10, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells10_', generation, '.txt'), np.asarray(selected_cells10, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_tags10_', generation, '.txt'), np.asarray(selected_tags10, dtype=int), fmt='%i', delimiter=' ', newline=' ')
