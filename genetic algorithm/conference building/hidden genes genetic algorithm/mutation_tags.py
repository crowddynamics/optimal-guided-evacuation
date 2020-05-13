import numpy as np


def mutation_tags(tags, mutpb):
    """Mutation that alters each tag with 0.1 probability."""

    # Number of guides
    n_guides = len(tags)

    new_tags = []
    for i in range(n_guides):

        rnd = np.random.rand(1)[0]

        if rnd <= mutpb:

            new_tags.append(1-tags[i])
        else:
            new_tags.append(tags[i])

    return new_tags
