import numpy as np

def onepointcrossover(exits1, cells1, exits2, cells2):

    """Apply a one point crossover on parents.
    """
    n_guides = len(exits1)
    crossover_point = np.round(n_guides/2)

    newexits1 = []
    newcells1 = []
    newexits2 = []
    newcells2 = []
    for i in range(n_guides):
        if i < crossover_point:
            newexits1.append(exits1[i])
            newcells1.append(cells1[i])
            newexits2.append(exits2[i])
            newcells2.append(cells2[i])
        else:
            newexits1.append(exits2[i])
            newcells1.append(cells2[i])
            newexits2.append(exits1[i])
            newcells2.append(cells1[i])

    return newexits1, newcells1, newexits2, newcells2

