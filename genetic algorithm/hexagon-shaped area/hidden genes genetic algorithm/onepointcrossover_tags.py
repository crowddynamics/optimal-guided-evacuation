import numpy as np

def onepointcrossover_tags(tags1, tags2):

    """Apply a one point crossover on parents.
    """
    n_guides = len(tags1)
    crossover_point = np.round(n_guides/2)

    newtags1 = []
    newtags2 = []
    for i in range(n_guides):
        if i < crossover_point:
            newtags1.append(tags1[i])
            newtags2.append(tags2[i])
        else:
            newtags1.append(tags2[i])
            newtags2.append(tags1[i])

    return newtags1, newtags2

