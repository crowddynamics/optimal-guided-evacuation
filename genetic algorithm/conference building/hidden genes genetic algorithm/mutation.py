import numpy as np


def mutation(exits, locations, mutpb):
    """Mutation that alters the routes of the guides of a single chromosome."""

    # Feasible starting cells
    # The space the agents are evacuating from has been divided into 10m x 10m cells, and we have checked which of these are feasible.
    cells = np.array(
        [8, 15, 22, 23, 24, 25, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 43, 44, 45, 46, 47, 48, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 64, 65, 66, 67, 71, 72, 73, 74, 75, 78, 79, 80, 81, 85, 86, 92, 93, 99])

    # Feasible exits
    feasible_exits = np.array([0, 1, 2, 3, 4])

    # Number of guides
    n_guides = len(locations)
    # Number of exits
    n_exits = len(feasible_exits)

    # Loop through genes of the chromosome and mutate each with probability mutpb.
    for i in range(n_guides):

        if np.random.rand(1)[0] <= mutpb:

            # Move the guide's location randomly
            switch = 0 # gets value 0 if we don't generate the same location as before
            random_cell = cells[np.random.randint(len(cells))]
            if random_cell == locations[i]:
                switch = 1
            else:
                locations[i] = random_cell

            # Move the guide's exit randomly
            # If the location is the same as before, the exit cant be
            if switch == 1:
                delete_element = np.where(feasible_exits == exits[i])
                available_exits = np.delete(feasible_exits, delete_element, None)
                random_exit = available_exits[np.random.randint(len(available_exits))]

            else:
                random_exit = feasible_exits[np.random.randint(len(feasible_exits))]


            # Generate a random exit from the available exits
            exits[i] = random_exit

    return exits, locations
