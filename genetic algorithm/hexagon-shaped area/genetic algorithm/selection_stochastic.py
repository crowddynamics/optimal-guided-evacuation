import sys
import os
import numpy as np

from onepointcrossover import onepointcrossover
from mutation import mutation

# Slurm JOBID for the simulations of current generation
jobida = str(sys.argv[1])
jobidb = str(sys.argv[2])
jobidc = str(sys.argv[3])
jobidd = str(sys.argv[4])

# Generation number
generation = int(sys.argv[5])

# Number of individuals in a population
population = int(sys.argv[6])

# Number of samples of same individuals
samples = int(sys.argv[7])

# Number of guides
n_guides = int(sys.argv[8])

# Total number of simulations
n_simulations = population*samples

# Probability for crossover
CXPB = 0.85

# Probability for mutation
if generation < 30:
    MUTPB = 0.4
else:
    MUTPB = 0.05

# Elitism fractions for different generations (starting from generation number 1)
# If generation number is over length of the elitism_pr list (>20) use just all parents for selection.
elitism_pr = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

# Write simulation results to a single file
all_positions = []
all_output = []

# Due to user quotas, we have to run one generation in three parts
for i in range(0,int(n_simulations/4)):
    fname = "{}{}{}{}{}".format('slurm-', jobida, '_', i, '.out')
    #print(fname)
    with open(fname) as infile:
        lines1 = [line.rstrip('\n') for line in infile]
        #print(lines1)
        all_positions.append(lines1[0])
        if len(lines1) > 1:
            all_output.append(lines1[1])
        else:
            all_output.append(0.0)

for i in range(0,int(n_simulations/4)):
    fname = "{}{}{}{}{}".format('slurm-', jobidb, '_', i, '.out')
    with open(fname) as infile:
        lines1 = [line.rstrip('\n') for line in infile]
        all_positions.append(lines1[0])
        if len(lines1) > 1:
            all_output.append(lines1[1])
        else:
            all_output.append(0.0)

for i in range(0,int(n_simulations/4)):
    fname = "{}{}{}{}{}".format('slurm-', jobidc, '_', i, '.out')
    with open(fname) as infile:
        lines1 = [line.rstrip('\n') for line in infile]
        all_positions.append(lines1[0])
        if len(lines1) > 1:
            all_output.append(lines1[1])
        else:
            all_output.append(0.0)

for i in range(0,int(n_simulations/4)):
    fname = "{}{}{}{}{}".format('slurm-', jobidd, '_', i, '.out')
    with open(fname) as infile:
        lines1 = [line.rstrip('\n') for line in infile]
        all_positions.append(lines1[0])
        if len(lines1) > 1:
            all_output.append(lines1[1])
        else:
            all_output.append(0.0)  

# There might be a few invalid runs (because of faults in the spawning).
# Replace the results of invalid runs with 0.0
all_evactimes = []
for i in range(0, n_simulations):
    try:
        all_evactimes.append(float(all_output[i]))
    except ValueError:
        all_evactimes.append(0.0)

# Store the sample mean results and the sample positions
sample_evactimes = []
sample_positions = []
counter = 0
for i in range(0, population):
    sample_mean = 0
    valid_runs = 0
    first_valid_run = -1
    for j in range(0, samples):
        counter = i*samples + j
        if first_valid_run == -1:
            first_valid_run = counter
            sample_positions.append(all_positions[counter])
        if all_evactimes[counter] != 0.0:
            sample_mean += all_evactimes[counter]
            valid_runs += 1
    if sample_mean == 0:
        sample_evactimes.append(0.0)
    else:
        sample_evactimes.append(sample_mean/valid_runs)

# Store the sample max results
sample_maxs = []
for i in range(0, population):
    sample_maxs.append(np.max(all_evactimes[i*samples:(i+1)*samples]))

# If there are invalid samples, replace them with a random valid sample
waste = np.argwhere(np.asarray(sample_evactimes)==0.0)
nonwaste = np.argwhere(np.asarray(sample_evactimes)!=0.0)
n_waste = len(waste)
n_nonwaste = len(nonwaste)

if n_waste > 0:
    indxs_replacement = []
    for i in range(0, n_waste):
        rand_indx = np.random.randint(0, population-n_waste, 1)[0]
        indxs_replacement.append(nonwaste[rand_indx][0])
        sample_evactimes[waste[i][0]] = sample_evactimes[indxs_replacement[i]]
        sample_positions[waste[i][0]] = sample_positions[indxs_replacement[i]]
        sample_maxs[waste[i][0]] = sample_maxs[indxs_replacement[i]]

# In the lists all_evactimes and all_positions, replace the invalid runs with the valid run (these might include invalid values)
if n_waste > 0:
    for i in range(0, n_waste):
        all_positions[waste[i][0]*samples:(waste[i][0]+1)*samples] = all_positions[indxs_replacement[i]*samples:(indxs_replacement[i]+1)*samples]
        all_evactimes[waste[i][0]*samples:(waste[i][0]+1)*samples] = all_evactimes[indxs_replacement[i]*samples:(indxs_replacement[i]+1)*samples]

# Use eliticism.
# Take the n_simulations best individuals from the parents and the offspring
# The population of the first generation will always be random.
# Already the second generation will consist of the n_simulations best individuals from the first generation
# and the crossovered and mutated offspring.
  
# Save results of all the runs (whole invalid samples have been replaced, but single invalid values, disguised as 0.0 can occur)
np.savetxt("{}{}{}".format('results_', generation, '.txt'), np.asarray(all_evactimes), fmt='%.14f')

# Save the sample means (here the invalid samples have been replaced, and only valid values exist)
np.savetxt("{}{}{}".format('sample_results_', generation, '.txt'), np.asarray(sample_evactimes), fmt='%.14f')
   
# Save the sample maximums (here the invalid samples have been replaced, and only valid values exist)
np.savetxt("{}{}{}".format('sample_maxs_',  generation, '.txt'), np.asarray(sample_maxs), fmt='%.14f')  

# Save the positions of all the runs (whole invalid samples have been replaced, but single invalid values, which are error messages can occur)
f = open("{}{}{}".format('positions_', generation, '.txt'), "w")
for i in range(n_simulations):
    f.write("{}{}".format(all_positions[i], '\n'))
f.close()
   
# Save the sample positions (here the invalid samples have been replaced, and only valid values exist)
f = open("{}{}{}".format('sample_positions_', generation, '.txt'), "w")
for i in range(population):
    f.write("{}{}".format(sample_positions[i], '\n'))
f.close()
    
if generation > 0:
    
    # Open the results of the previous generation and extend them to the results of current generation
    
    # Results of all the runs
    parents_results = np.loadtxt("{}{}{}".format('selected_results_', generation-1, '.txt'))
    parents_results = parents_results.tolist()
    all_evactimes.extend(parents_results)

    # Sample means
    parents_sample_results = np.loadtxt("{}{}{}".format('selected_sample_results_', generation-1, '.txt'))
    parents_sample_results = parents_sample_results.tolist()
    sample_evactimes.extend(parents_sample_results)

    # Sample maximums
    parents_sample_maximums = np.loadtxt("{}{}{}".format('selected_sample_maxs_', generation-1, '.txt'))
    parents_sample_maximums = parents_sample_maximums.tolist()
    sample_maxs.extend(parents_sample_maximums)

    # Positions of all the runs
    with open("{}{}{}".format('selected_positions_', generation-1, '.txt')) as infile:
        lines2 = [line.rstrip('\n') for line in infile]
    all_positions.extend(lines2)

    # Sample positions
    with open("{}{}{}".format('selected_sample_positions_', generation-1, '.txt')) as infile:
        lines3 = [line.rstrip('\n') for line in infile]
    sample_positions.extend(lines3)

# If generation number greater or equal to 1 use elitism.
# NOTE DOESN'T WORK FOR SMALLER POPULATIONS THAN 20, OR POPULATIONS NOT DIVISIBLE BY 20
if generation >= 1:
    parents_sample_evactimes = sample_evactimes[population:]
    sorted_indices_parents = sorted(range(population), key=lambda k : parents_sample_evactimes[k])
    sorted_indices_parents = sorted_indices_parents[0:population*int(elitism_pr[generation]*population)]
    sorted_indices_parents = [sorted_indices_parents[i] + population for i in range(len(sorted_indices_parents))]

help_indices = [i for i in range(population)]
scores = sample_evactimes[0:population]

if generation >= 1:
    for i in range(len(sorted_indices_parents)):
        help_indices.append(sorted_indices_parents[i])
        scores.append(sample_evactimes[sorted_indices_parents[i]])

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
exits1 = exits1[0::samples]
cells1 = np.loadtxt("{}{}{}".format('cells1_', generation, '.txt'), dtype=int)
cells1 = cells1[0::samples]
if generation > 0:
    exits1_prev = np.loadtxt("{}{}{}".format('selected_exits1_', generation-1, '.txt'), dtype=int)
    cells1_prev = np.loadtxt("{}{}{}".format('selected_cells1_', generation-1, '.txt'), dtype=int)
    exits1 = np.concatenate((exits1, exits1_prev), axis=None)
    cells1 = np.concatenate((cells1, cells1_prev), axis=None)

exits1.tolist()
cells1.tolist()
selected_exits1 = []
selected_cells1 = []
new_exits1 = []
new_cells1 = []

if n_guides >= 2:

    exits2 = np.loadtxt("{}{}{}".format('exits2_', generation, '.txt'), dtype=int)
    cells2 = np.loadtxt("{}{}{}".format('cells2_', generation, '.txt'), dtype=int)
    exits2 = exits2[0::samples]
    cells2 = cells2[0::samples]
    if generation > 0:
        exits2_prev = np.loadtxt("{}{}{}".format('selected_exits2_', generation-1, '.txt'), dtype=int)
        cells2_prev = np.loadtxt("{}{}{}".format('selected_cells2_', generation-1, '.txt'), dtype=int)
        exits2 = np.concatenate((exits2, exits2_prev), axis=None)
        cells2 = np.concatenate((cells2, cells2_prev), axis=None)

    exits2.tolist()
    cells2.tolist()
    selected_exits2 = []
    selected_cells2 = []
    new_exits2 = []
    new_cells2 = []

    if n_guides >= 3:

        exits3 = np.loadtxt("{}{}{}".format('exits3_', generation, '.txt'), dtype=int)
        cells3 = np.loadtxt("{}{}{}".format('cells3_', generation, '.txt'), dtype=int)
        exits3 = exits3[0::samples]
        cells3 = cells3[0::samples]
        if generation > 0:
            exits3_prev = np.loadtxt("{}{}{}".format('selected_exits3_', generation-1, '.txt'), dtype=int)
            cells3_prev = np.loadtxt("{}{}{}".format('selected_cells3_', generation-1, '.txt'), dtype=int)
            exits3 = np.concatenate((exits3, exits3_prev), axis=None)
            cells3 = np.concatenate((cells3, cells3_prev), axis=None)

        exits3.tolist()
        cells3.tolist()
        selected_exits3 = []
        selected_cells3 = []
        new_exits3 = []
        new_cells3 = []

        if n_guides >= 4:

            exits4 = np.loadtxt("{}{}{}".format('exits4_', generation, '.txt'), dtype=int)
            cells4 = np.loadtxt("{}{}{}".format('cells4_', generation, '.txt'), dtype=int)
            exits4 = exits4[0::samples]
            cells4 = cells4[0::samples]
            if generation > 0:
                exits4_prev = np.loadtxt("{}{}{}".format('selected_exits4_', generation-1, '.txt'), dtype=int)
                cells4_prev = np.loadtxt("{}{}{}".format('selected_cells4_', generation-1, '.txt'), dtype=int)
                exits4 = np.concatenate((exits4, exits4_prev), axis=None)
                cells4 = np.concatenate((cells4, cells4_prev), axis=None)

            exits4.tolist()
            cells4.tolist()
            selected_exits4 = []
            selected_cells4 = []
            new_exits4 = []
            new_cells4 = []

            if n_guides >= 5:

                exits5 = np.loadtxt("{}{}{}".format('exits5_', generation, '.txt'), dtype=int)
                cells5 = np.loadtxt("{}{}{}".format('cells5_', generation, '.txt'), dtype=int)
                exits5 = exits5[0::samples]
                cells5 = cells5[0::samples]
                if generation > 0:
                    exits5_prev = np.loadtxt("{}{}{}".format('selected_exits5_', generation-1, '.txt'), dtype=int)
                    cells5_prev = np.loadtxt("{}{}{}".format('selected_cells5_', generation-1, '.txt'), dtype=int)
                    exits5 = np.concatenate((exits5, exits5_prev), axis=None)
                    cells5 = np.concatenate((cells5, cells5_prev), axis=None)

                exits5.tolist()
                cells5.tolist()
                selected_exits5 = []
                selected_cells5 = []
                new_exits5 = []
                new_cells5 = []

                if n_guides >= 6:

                    exits6 = np.loadtxt("{}{}{}".format('exits6_', generation, '.txt'), dtype=int)
                    cells6 = np.loadtxt("{}{}{}".format('cells6_', generation, '.txt'), dtype=int)
                    exits6 = exits6[0::samples]
                    cells6 = cells6[0::samples]
                    if generation > 0:
                        exits6_prev = np.loadtxt("{}{}{}".format('selected_exits6_', generation-1, '.txt'), dtype=int)
                        cells6_prev = np.loadtxt("{}{}{}".format('selected_cells6_', generation-1, '.txt'), dtype=int)
                        exits6 = np.concatenate((exits6, exits6_prev), axis=None)
                        cells6 = np.concatenate((cells6, cells6_prev), axis=None)

                    exits6.tolist()
                    cells6.tolist()
                    selected_exits6 = []
                    selected_cells6 = []
                    new_exits6 = []
                    new_cells6 = []
# Store the data of the individuals selected for breeding
selected_evactimes = []
selected_sample_evactimes = []
selected_sample_maxs = []
selected_positions = []
selected_sample_positions = []
for i in range(population):
    selected_sample_evactimes.append(sample_evactimes[selected[i]])
    selected_sample_maxs.append(sample_maxs[selected[i]])
    selected_sample_positions.append(sample_positions[selected[i]])
    # Remember that the cells and exits contain each values several times (the amount is equal to samples)
    selected_exits1.append(exits1[selected[i]])
    selected_cells1.append(cells1[selected[i]])

    if n_guides >= 2:
        selected_exits2.append(exits2[selected[i]])
        selected_cells2.append(cells2[selected[i]])

        if n_guides >= 3:
            selected_exits3.append(exits3[selected[i]])
            selected_cells3.append(cells3[selected[i]])

            if n_guides >= 4:
                selected_exits4.append(exits4[selected[i]])
                selected_cells4.append(cells4[selected[i]])

                if n_guides >= 5:
                    selected_exits5.append(exits5[selected[i]])
                    selected_cells5.append(cells5[selected[i]])

                    if n_guides >= 6:
                        selected_exits6.append(exits6[selected[i]])
                        selected_cells6.append(cells6[selected[i]])
    for j in range(samples):
        selected_evactimes.append(all_evactimes[selected[i]*samples+j])
        selected_positions.append(all_positions[selected[i]*samples+j])
    
# Eliticism
# Save results of all the runs (whole invalid samples have been replaced, but single invalid values, disguised as 0.0 can occur)
np.savetxt("{}{}{}".format('selected_results_', generation, '.txt'), np.asarray(selected_evactimes), fmt='%.14f')

# Save the sample means (here the invalid samples have been replaced, and only valid values exist)
np.savetxt("{}{}{}".format('selected_sample_results_', generation, '.txt'), np.asarray(selected_sample_evactimes), fmt='%.14f')

# Save the sample maximums (here the invalid samples have been replaced, and only valid values exist)
np.savetxt("{}{}{}".format('selected_sample_maxs_', generation, '.txt'), np.asarray(selected_sample_maxs), fmt='%.14f')

# Save the positions of all the runs (whole invalid samples have been replaced, but single invalid values, which are error messages can occur)
f = open("{}{}{}".format('selected_positions_', generation, '.txt'), "w")
for i in range(n_simulations):
    f.write("{}{}".format(selected_positions[i], '\n'))
f.close()

# Save the sample positions (here the invalid samples have been replaced, and only valid values exist)
f = open("{}{}{}".format('selected_sample_positions_', generation, '.txt'), "w")
for i in range(population):
    f.write("{}{}".format(selected_sample_positions[i], '\n'))
f.close()

# Save the exits and cells of the selected individuals
f = open("{}{}{}".format('selected_', generation, '.txt'), "w")

if n_guides == 1:
    for i in range(population):
        f.write("{}{}{}{}".format(selected_exits1[i], ' ', selected_cells1[i], '\n'))

if n_guides == 2:
    for i in range(population):
        f.write("{}{}{}{}{}{}{}{}".format(selected_exits1[i], ' ', selected_cells1[i],  ' ', selected_exits2[i], ' ', selected_cells2[i], '\n'))

if n_guides == 3:
    for i in range(population):
        f.write("{}{}{}{}{}{}{}{}{}{}{}{}".format(selected_exits1[i], ' ', selected_cells1[i],  ' ', selected_exits2[i], ' ', selected_cells2[i], ' ', selected_exits3[i], ' ', selected_cells3[i], '\n'))

if n_guides == 4:
    for i in range(population):
        f.write("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(selected_exits1[i], ' ', selected_cells1[i],  ' ', selected_exits2[i], ' ', selected_cells2[i], ' ', selected_exits3[i], ' ', selected_cells3[i], ' ', selected_exits4[i], ' ', selected_cells4[i], '\n'))

if n_guides == 5:
    for i in range(population):
        f.write("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(selected_exits1[i], ' ', selected_cells1[i],  ' ', selected_exits2[i], ' ', selected_cells2[i], ' ', selected_exits3[i], ' ', selected_cells3[i], ' ', selected_exits4[i], ' ', selected_cells4[i], ' ', selected_exits5[i], ' ', selected_cells5[i], '\n'))

if n_guides == 6:
    for i in range(population):
        f.write("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(selected_exits1[i], ' ', selected_cells1[i],  ' ', selected_exits2[i], ' ', selected_cells2[i], ' ', selected_exits3[i], ' ', selected_cells3[i], ' ', selected_exits4[i], ' ', selected_cells4[i], ' ', selected_exits5[i], ' ', selected_cells5[i], ' ', selected_exits6[i], ' ', selected_cells6[i], '\n'))

f.close()

inds1 = np.arange(0,population,2)
inds2 = np.arange(1,population,2)
# Start breeding
for ind1, ind2 in zip(inds1, inds2):
    
    ind1_exits = []
    ind1_cells = []
    ind2_exits = []
    ind2_cells = []    

    # Store the data of the individuals in lists
    ind1_exits.append(selected_exits1[ind1])
    ind1_cells.append(selected_cells1[ind1])
    ind2_exits.append(selected_exits1[ind2])
    ind2_cells.append(selected_cells1[ind2])

    if n_guides >= 2:
        ind1_exits.append(selected_exits2[ind1])
        ind1_cells.append(selected_cells2[ind1])
        ind2_exits.append(selected_exits2[ind2])
        ind2_cells.append(selected_cells2[ind2])

        if n_guides >= 3:
            ind1_exits.append(selected_exits3[ind1])
            ind1_cells.append(selected_cells3[ind1])
            ind2_exits.append(selected_exits3[ind2])
            ind2_cells.append(selected_cells3[ind2])

            if n_guides >= 4:
                ind1_exits.append(selected_exits4[ind1])
                ind1_cells.append(selected_cells4[ind1])
                ind2_exits.append(selected_exits4[ind2])
                ind2_cells.append(selected_cells4[ind2])

                if n_guides >= 5:
                    ind1_exits.append(selected_exits5[ind1])
                    ind1_cells.append(selected_cells5[ind1])
                    ind2_exits.append(selected_exits5[ind2])
                    ind2_cells.append(selected_cells5[ind2])

                    if n_guides >= 6:
                        ind1_exits.append(selected_exits6[ind1])
                        ind1_cells.append(selected_cells6[ind1])
                        ind2_exits.append(selected_exits6[ind2])
                        ind2_cells.append(selected_cells6[ind2])

    # Crossover with probability CXPB
    if ((np.random.uniform(0,1,1) <= CXPB) and (n_guides >= 2)):
        ind1_newexits, ind1_newcells, ind2_newexits, ind2_newcells = onepointcrossover(ind1_exits, ind1_cells, ind2_exits, ind2_cells)

        # Mutate genes of chromosomes
        ind1_newexits, ind1_newcells = mutation(ind1_newexits, ind1_newcells, MUTPB)
        ind2_newexits, ind2_newcells = mutation(ind2_newexits, ind2_newcells, MUTPB)

    else:
        # Mutate genes of chromosomes
        ind1_newexits, ind1_newcells = mutation(ind1_exits, ind1_cells, MUTPB)
        ind2_newexits, ind2_newcells = mutation(ind2_exits, ind2_cells, MUTPB)    

    # Append data of offspring to lists
    new_exits1.append(ind1_newexits[0])
    new_exits1.append(ind2_newexits[0])
    new_cells1.append(ind1_newcells[0])
    new_cells1.append(ind2_newcells[0])

    if n_guides >= 2:
        new_exits2.append(ind1_newexits[1])
        new_exits2.append(ind2_newexits[1])
        new_cells2.append(ind1_newcells[1])
        new_cells2.append(ind2_newcells[1])

        if n_guides >= 3:
            new_exits3.append(ind1_newexits[2])
            new_exits3.append(ind2_newexits[2])
            new_cells3.append(ind1_newcells[2])
            new_cells3.append(ind2_newcells[2])

            if n_guides >= 4:
                new_exits4.append(ind1_newexits[3])
                new_exits4.append(ind2_newexits[3])
                new_cells4.append(ind1_newcells[3])
                new_cells4.append(ind2_newcells[3])

                if n_guides >= 5:
                    new_exits5.append(ind1_newexits[4])
                    new_exits5.append(ind2_newexits[4])
                    new_cells5.append(ind1_newcells[4])
                    new_cells5.append(ind2_newcells[4])

                    if n_guides >= 6:
                        new_exits6.append(ind1_newexits[5])
                        new_exits6.append(ind2_newexits[5])
                        new_cells6.append(ind1_newcells[5])
                        new_cells6.append(ind2_newcells[5])

# Make copies of exits and cells for all next generation simulations
all_new_exits1 = []
all_new_cells1 = []

if n_guides >= 2:
    all_new_exits2 = []
    all_new_cells2 = []

    if n_guides >= 3:
        all_new_exits3 = []
        all_new_cells3 = []

        if n_guides >= 4:
            all_new_exits4 = []
            all_new_cells4 = []

            if n_guides >= 5:
                all_new_exits5 = []
                all_new_cells5 = []

                if n_guides >= 6:
                    all_new_exits6 = []
                    all_new_cells6 = []

for i in range(population):
    for j in range(samples):
        all_new_exits1.append(new_exits1[i])
        all_new_cells1.append(new_cells1[i])

        if n_guides >= 2:
            all_new_exits2.append(new_exits2[i])
            all_new_cells2.append(new_cells2[i])

            if n_guides >= 3:
                all_new_exits3.append(new_exits3[i])
                all_new_cells3.append(new_cells3[i])

                if n_guides >= 4:
                    all_new_exits4.append(new_exits4[i])
                    all_new_cells4.append(new_cells4[i])

                    if n_guides >= 5:
                        all_new_exits5.append(new_exits5[i])
                        all_new_cells5.append(new_cells5[i])

                        if n_guides >= 6:
                            all_new_exits6.append(new_exits6[i])
                            all_new_cells6.append(new_cells6[i])

# Remove previous generation data and store new data
np.savetxt("{}{}{}".format('exits1_', generation+1, '.txt'), np.asarray(all_new_exits1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('cells1_', generation+1, '.txt'), np.asarray(all_new_cells1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_exits1_', generation, '.txt'), np.asarray(selected_exits1, dtype=int), fmt='%i', delimiter=' ', newline=' ')
np.savetxt("{}{}{}".format('selected_cells1_', generation, '.txt'), np.asarray(selected_cells1, dtype=int), fmt='%i', delimiter=' ', newline=' ')

if n_guides >= 2:
    np.savetxt("{}{}{}".format('exits2_', generation+1, '.txt'), np.asarray(all_new_exits2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
    np.savetxt("{}{}{}".format('cells2_', generation+1, '.txt'), np.asarray(all_new_cells2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
    np.savetxt("{}{}{}".format('selected_exits2_', generation, '.txt'), np.asarray(selected_exits2, dtype=int), fmt='%i', delimiter=' ', newline=' ')
    np.savetxt("{}{}{}".format('selected_cells2_', generation, '.txt'), np.asarray(selected_cells2, dtype=int), fmt='%i', delimiter=' ', newline=' ')

    if n_guides >= 3:
        np.savetxt("{}{}{}".format('exits3_', generation+1, '.txt'), np.asarray(all_new_exits3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
        np.savetxt("{}{}{}".format('cells3_', generation+1, '.txt'), np.asarray(all_new_cells3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
        np.savetxt("{}{}{}".format('selected_exits3_', generation, '.txt'), np.asarray(selected_exits3, dtype=int), fmt='%i', delimiter=' ', newline=' ')
        np.savetxt("{}{}{}".format('selected_cells3_', generation, '.txt'), np.asarray(selected_cells3, dtype=int), fmt='%i', delimiter=' ', newline=' ')

        if n_guides >= 4:
            np.savetxt("{}{}{}".format('exits4_', generation+1, '.txt'), np.asarray(all_new_exits4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
            np.savetxt("{}{}{}".format('cells4_', generation+1, '.txt'), np.asarray(all_new_cells4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
            np.savetxt("{}{}{}".format('selected_exits4_', generation, '.txt'), np.asarray(selected_exits4, dtype=int), fmt='%i', delimiter=' ', newline=' ')
            np.savetxt("{}{}{}".format('selected_cells4_', generation, '.txt'), np.asarray(selected_cells4, dtype=int), fmt='%i', delimiter=' ', newline=' ')

            if n_guides >= 5:
                np.savetxt("{}{}{}".format('exits5_', generation+1, '.txt'), np.asarray(all_new_exits5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
                np.savetxt("{}{}{}".format('cells5_', generation+1, '.txt'), np.asarray(all_new_cells5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
                np.savetxt("{}{}{}".format('selected_exits5_', generation, '.txt'), np.asarray(selected_exits5, dtype=int), fmt='%i', delimiter=' ', newline=' ')
                np.savetxt("{}{}{}".format('selected_cells5_', generation, '.txt'), np.asarray(selected_cells5, dtype=int), fmt='%i', delimiter=' ', newline=' ')

                if n_guides >= 6:
                    np.savetxt("{}{}{}".format('exits6_', generation+1, '.txt'), np.asarray(all_new_exits6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
                    np.savetxt("{}{}{}".format('cells6_', generation+1, '.txt'), np.asarray(all_new_cells6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
                    np.savetxt("{}{}{}".format('selected_exits6_', generation, '.txt'), np.asarray(selected_exits6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
                    np.savetxt("{}{}{}".format('selected_cells6_', generation, '.txt'), np.asarray(selected_cells6, dtype=int), fmt='%i', delimiter=' ', newline=' ')
