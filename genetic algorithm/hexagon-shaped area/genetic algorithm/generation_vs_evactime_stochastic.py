import numpy as np
import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')

n_generations= int(sys.argv[1])
population = int(sys.argv[2])
samples = int(sys.argv[3])

generations = np.arange(0,n_generations+1)
print(generations)

for i in range(0,n_generations+1):
    print(i)
    if i == 0:
        results = [float(line.rstrip('\n')) for line in open("{}{}{}".format('selected_sample_results_', i,'.txt'))]
        results = np.asarray(results)
    if i > 0:
        temp_array = [float(line.rstrip('\n')) for line in open("{}{}{}".format('selected_sample_results_', i, '.txt'))]
        temp_array = np.asarray(temp_array)
        results = np.concatenate((results, temp_array), axis=0)

#print(results)
#print(results.shape)
#print(n_generations)
#print(population)
results = np.reshape(results, (n_generations+1, population))

max_values = []
mean_values = []
min_values = []
std_values = []

for i in range(0,n_generations+1):
    max_values.append(np.max(results[i,:]))
    mean_values.append(np.mean(results[i,:]))
    min_values.append(np.min(results[i,:]))
    std_values.append(np.std(results[i,:]))

max_values = np.asarray(max_values)
mean_values = np.asarray(mean_values)
min_values = np.asarray(min_values)
std_values = np.asarray(std_values)

#print(max_values)
#print(max_values.shape)

#fig = plt.figure()
#ax = plt.subplot(111)
plt.plot(generations, max_values, linestyle='dashed', color='b')
plt.plot(generations, mean_values, color='k')
plt.plot(generations, min_values, linestyle='dashed', color='b')
plt.xlabel('Generation')
plt.ylabel('Total evacuation time (s)')
plt.title('Convergence')
plt.savefig("{}{}{}{}{}".format('generation_vs_mean_selected_', population, '_', samples, '.pdf'))
