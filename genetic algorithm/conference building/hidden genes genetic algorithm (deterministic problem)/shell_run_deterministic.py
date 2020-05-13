import sys
import os
import random
import numpy as np

from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString, Point, LinearRing
from shapely.ops import polygonize, cascaded_union

from scipy.spatial.qhull import Delaunay

from crowddynamics.simulation.agents import Agents, AgentGroup, Circular
from crowddynamics.core.geometry import geom_to_linear_obstacles
from crowddynamics.core.sampling import triangle_area_cumsum, random_sample_triangle
from crowddynamics.core.vector2D import length
from crowddynamics.core.distance import distance_circle_line, distance_circles

# Use the finlandia_talo_ga file, which contains the class for FinlandiaTalo2ndFloor, used with the genetic algorithm
from finlandia_talo_ga_deterministic import FinlandiaTalo2ndFloor

from solutionbank_deterministic import solutionbank

# A helper function to create spawn points for leaders out of their cell coordinates.
# The input is the array of leader spawn cells and the number of leaders in the simulation.
#def generate_leader_pos(cell, n_lead, seed_number):
def generate_leader_pos(self, cell, n_lead):
    # Load data of followers
    followers = np.load('agents_initialization_conference.npy')
    follower_positions = followers['position']
    follower_radii = followers['radius']

    # Minimal radius of a guide (the same value given in agents.py to the guides).
    max_r = 0.27

    # Number of times spawned leaders are allowed to overlap each other before the program is
    # terminated.
    overlaps = 10000

    # Import Finlandia Hall floor field
    field = FinlandiaTalo2ndFloor().field

    # Bound box representing the room. Used later in making Voronoi tessalation.
    width = 150
    height = 70

    # Create a grid structure over the room geometry.
    # Cell size in the grid, determines the resolution of the micro-macro converted data
    cell_size = 10
    m = np.round(width / cell_size)
    n = np.round(height / cell_size)
    m = m.astype(int)
    n = n.astype(int)
    X = np.linspace(0, width, m + 1)
    Y = np.linspace(0, height, n + 1)
    hlines = [((x1, yi), (x2, yi)) for x1, x2 in zip(X[:-1], X[1:]) for yi in Y]
    vlines = [((xi, y1), (xi, y2)) for y1, y2 in zip(Y[:-1], Y[1:]) for xi in X]
    grids = list(polygonize(MultiLineString(hlines + vlines)))

    # Leaders' spawn areas
    leader_spawns = []

    # Leader's spawn points
    spawn_points = []

    # Truth values or whether the leader is inside Finlandia Hall
    inside_finlandia = []

    # Loop through the cells and calculate intersections with spawn areas.
    for i in range(n_lead):

        polygons = []

        # Loop through the seven possible spawn areas in FinlandiaTalo class,
        # and check which of these areas the spawn cell of the leader intersects.
        # Append this intersecting area to the "polygons" list.
        # NB! The cell can intersect with multiple spawn areas of the FinlandiaTalo class.
        # A cascaded union is created of all these intersecting areas and saved in the "spawn_poly"
        # variable.
        # "spawn_poly" is appended to the "leader_spawns" list.
        for j in range(8):
            poly = field.spawns[j].intersection(grids[cell[i]])
            if not poly.is_empty:
                polygons.append(poly)
        spawn_poly = cascaded_union(polygons)
        if not spawn_poly.is_empty:
            leader_spawns.append(spawn_poly)

    # Import obstacles
    obstacles = field.obstacles

    # Spawn a random position from the starting area.
    # Loop through all the leaders.
    # (1) Take into account that there might be obstacles in the spawn areas, and take also
    # into account that agents have a buffer radius.
    # (2) If the spawn area is a MultiPolygon, loop through the polygons in a MultiPolygon. Create a
    # mesh grid of the spawn area with Delaunay triangulation.
    # (2.1) Spawn a random point from the mesh grid.
    # (2.2) Check that the position doesn't interfere with other agents' positions
    # (2.3) Set the Boolean value for if the leader is initially inside the Finlandiahall
    # (this is needed for the movement simulation).
    # (3) If the spawn area is not a MultiPolygon, just directly create a mesh grid of the spawn area
    # with Delaunay triangulation.
    # (3.1) Spawn a random point from the mesh grid.
    # (3.2) Check that the position doesn't interfere with other agents' positions
    # (3.3) Set the Boolean value for if the leader is initially inside the Finlandiahall (this is
    # is needed for the movement simulation).
    for i in range(n_lead):
        seed = 0
        # (1)
        n_spawnpoints = len(spawn_points)
        geom = leader_spawns[i] - obstacles.buffer(max_r)
        j = 0  # set overlaps counter to zero
        # (2)
        if isinstance(geom, MultiPolygon):
            n_polygons = len(geom)
            for j in range(n_polygons):
                vertices = np.asarray(geom[j].convex_hull.exterior)
                delaunay = Delaunay(vertices)
                mesh = vertices[delaunay.simplices]
                if j == 0:
                    meshes = mesh
                else:
                    meshes = np.concatenate((mesh, meshes), axis=0)
            # Computes cumulative sum of the areas of the triangle mesh.
            weights = triangle_area_cumsum(meshes)
            weights /= weights[-1]

            while j < overlaps:
                seed += 1
                distances = []  # temporarily store distances from the spawned point to the previously spawned
                n_overlaps = 0  # for each attempt to position the guide, set number of overlaps to zero
                # (2.1) Spawn a random point for the guide.
                np.random.seed(seed)
                x = np.random.random()
                k = np.searchsorted(weights, x)
                a, b, c = meshes[k]
                spawn_point = random_sample_triangle(a, b, c)
                # (2.2)
                if n_spawnpoints != 0:  # if there are no other spawned guides skip this step
                    for k in range(0, n_spawnpoints):
                        d = length(spawn_point - spawn_points[k])
                        h = d - 2 * max_r
                        distances.append(h)
                    distances_array = distances
                    distances_array = np.asarray(distances_array)
                    n_overlaps += len(np.where(distances_array < 0)[0])
                for obstacle in obstacles:
                    obstacle = list(obstacle.coords)
                    n_obstacle_points = len(obstacle)
                    for k in range(0, n_obstacle_points):
                        if k == n_obstacle_points - 1:
                            h, _ = distance_circle_line(spawn_point, max_r, np.asarray(obstacle[k]),
                                                        np.asarray(obstacle[0]))
                        else:
                            h, _ = distance_circle_line(spawn_point, max_r, np.asarray(obstacle[k]),
                                                        np.asarray(obstacle[k + 1]))
                        if h < 0.0:
                            n_overlaps += 1
                for agent in range(len(follower_radii)):
                    h, _ = distance_circles(follower_positions[agent], follower_radii[agent], spawn_point, max_r)
                    if h < 0.0:
                        n_overlaps += 1

                if n_overlaps == 0:
                    # (2.3)
                    if field.finlandiahall_extended.contains(Point([spawn_point[0], spawn_point[1]])):
                        inside_finlandia.append(True)
                    else:
                        inside_finlandia.append(False)
                    # Append the point to spawn points
                    spawn_points.append([spawn_point[0], spawn_point[1]])
                    #print("Guide spawned")
                    #sys.stdout.flush()
                    break
                j += 1
                if j == overlaps:
                    raise Exception('Leaders do not fit in the cell')
                    # (3)
        else:
            vertices = np.asarray(geom.convex_hull.exterior)
            delaunay = Delaunay(vertices)
            mesh = vertices[delaunay.simplices]
            weights = triangle_area_cumsum(mesh)
            weights /= weights[-1]

            while j < overlaps:
                seed += 1
                distances = []  # temporarily store distances from the spawned point to the previously spawned
                n_overlaps = 0  # for each attempt to position the guide, set number of overlaps to zero
                # (3.1) Spawn a random point for the guide
                np.random.seed(seed)
                x = np.random.random()
                k = np.searchsorted(weights, x)
                a, b, c = mesh[k]
                spawn_point = random_sample_triangle(a, b, c)
                if n_spawnpoints != 0:
                    for k in range(0, n_spawnpoints):
                        d = length(spawn_point - spawn_points[k])
                        h = d - 2 * max_r
                        distances.append(h)
                    distances_array = distances
                    distances_array = np.asarray(distances_array)
                    n_overlaps += len(np.where(distances_array < 0)[0])
                for obstacle in obstacles:
                    obstacle = list(obstacle.coords)
                    n_obstacle_points = len(obstacle)
                    for k in range(0, n_obstacle_points):
                        if k == n_obstacle_points - 1:
                            h, _ = distance_circle_line(spawn_point, max_r, np.asarray(obstacle[k]),
                                                        np.asarray(obstacle[0]))
                        else:
                            h, _ = distance_circle_line(spawn_point, max_r, np.asarray(obstacle[k]),
                                                        np.asarray(obstacle[k + 1]))
                        if h < 0.0:
                            n_overlaps += 1
                for agent in range(len(follower_radii)):
                    h, _ = distance_circles(follower_positions[agent], follower_radii[agent], spawn_point, max_r)
                    if h < 0.0:
                        n_overlaps += 1

                if n_overlaps == 0:
                    # (3.3)
                    if field.finlandiahall_extended.contains(Point([spawn_point[0], spawn_point[1]])):
                        inside_finlandia.append(True)
                    else:
                        inside_finlandia.append(False)
                    # Append the point to spawn points
                    spawn_points.append([spawn_point[0], spawn_point[1]])
                    #print("Guide spawned")
                    #sys.stdout.flush()
                    break
                j += 1
                if j == overlaps:
                    raise Exception('Leaders do not fit in the cell')
    return spawn_points, inside_finlandia


def attributes(self, familiar, in_finlandia: bool = False, in_finlandia_extended: bool = False,
               has_target: bool = True, is_follower: bool = True):
    def wrapper():
        target = familiar if has_target else NO_TARGET
        orientation = np.random.uniform(-np.pi, np.pi)
        d = dict(
            target=target,
            is_leader=not is_follower,
            is_follower=is_follower,
            body_type=self.body_type,
            orientation=orientation,
            velocity=np.zeros(2),
            angular_velocity=0.0,
            target_direction=np.zeros(2),
            target_orientation=orientation,
            familiar_exit=familiar,
            in_finlandia_extended=in_finlandia_extended,
            in_finlandia=in_finlandia,
            in_orchestra = False,
            in_helsinki = False,
            in_piazza_2 = False,
            in_piazza_3 = False
            )
        return d
    return wrapper

def attributes_leader(self, fin_ext_iter, fin_iter, target_iter, has_target: bool = True,
                      is_follower: bool = False):
    def wrapper():
        target = next(target_iter)
        in_finlandia_extended = next(fin_ext_iter)
        in_finlandia = next(fin_iter)
        orientation = np.random.uniform(-np.pi, np.pi)
        d = dict(
            target=target,
            is_leader=not is_follower,
            is_follower=is_follower,
            body_type=self.body_type,
            orientation=orientation,
            velocity=np.zeros(2),
            angular_velocity=0.0,
            target_direction=np.zeros(2),
            target_orientation=orientation,
            familiar_exit=4,
            in_finlandia_extended=in_finlandia_extended,
            in_finlandia=in_finlandia,
            in_orchestra = False,
            in_helsinki = False,
            in_piazza_2 = False,
            in_piazza_3 = False)
        return d
    return wrapper


# The "objective function", i.e., the evacuation simulator, which returns the total evacuation time.
def run(individual, n_leaders):

    # Import simulation
    simulation = FinlandiaTalo2ndFloor()

    # Import Finlandia Building floor field
    field = simulation.field

    # Generate iterators for group of leaders.
    target_exits = [] # Target exit for the leader
    cells = []

    if n_leaders > 0:
        for i in range(n_leaders):
            target_exits.append(individual[i][0])
            cells.append(individual[i][1])

    # Save the target exits, in another list for later use
    exits = target_exits

    # Number of followers
    # NB! By changing these numbers and the settings below, the scenario under study can be altered. If one wants to
    # change the geometry of the scenario go to 'finlandia_talo_ga.py' and alter the FinlandiTalo2ndFloorField() class.
    # TODO Change these
    size_finlandiahall = 300
    #size_finlandiahall = 0
    size_foyer = 100
    size_helsinkihall = 200
    #size_helsinkihall = 0
    size_piazza_1 = 200
    #size_piazza_1 = 0
    size_piazza_2 = 0
    size_piazza_3 = 100
    #size_piazza_3 = 0
    size_restaurant = 100
    #size_restaurant = 0
    size_orchestra = 100
    #size_orchestra = 0

    # Add followers. There is some randomness in how the followers are placed in each simulation, but the distribution
    # is the same. This could be changes, so that the positions of the followers are fixed.
    # Followers in Finlandia hall
    group_follower_finlandiahall = AgentGroup(
        agent_type=Circular,
        size=size_finlandiahall,
        attributes=attributes(simulation, familiar=1, in_finlandia=True, in_finlandia_extended=True, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_finlandiahall",
        group_follower_finlandiahall,
        position_gen=False,
        position_iter=iter([]),
        spawn=8,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    # Followers in Piazza 3
    group_follower_piazza_3 = AgentGroup(
        agent_type=Circular,
        size=size_piazza_3,
        attributes=attributes(simulation, familiar=0, in_finlandia=False, in_finlandia_extended=False, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_piazza_3",
        group_follower_piazza_3,
        position_gen=False,
        position_iter=iter([]),
        spawn=9,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    # Followers in Piazza 1
    group_follower_piazza_1 = AgentGroup(
        agent_type=Circular,
        size=size_piazza_1,
        attributes=attributes(simulation, familiar=4, in_finlandia=False, in_finlandia_extended=False, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_piazza_1",
        group_follower_piazza_1,
        position_gen=False,
        position_iter=iter([]),
        spawn=10,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    # Followers in Restaurant
    group_follower_restaurant = AgentGroup(
        agent_type=Circular,
        size=size_restaurant,
        attributes=attributes(simulation, familiar=1, in_finlandia=False, in_finlandia_extended=False, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_restaurant",
        group_follower_restaurant,
        position_gen=False,
        position_iter=iter([]),
        spawn=11,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    # Followers in foyer
    group_follower_foyer = AgentGroup(
        agent_type=Circular,
        size=size_foyer,
        attributes=attributes(simulation, familiar=2, in_finlandia=True, in_finlandia_extended=True, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_foyer",
        group_follower_foyer,
        position_gen=False,
        position_iter=iter([]),
        spawn=12,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    # Followers in Helsinki hall
    group_follower_helsinkihall = AgentGroup(
        agent_type=Circular,
        size=size_helsinkihall,
        attributes=attributes(simulation, familiar=3, in_finlandia=False, in_finlandia_extended=False, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_helsinkihall",
        group_follower_helsinkihall,
        position_gen=False,
        position_iter=iter([]),
        spawn=13,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    # Followers in Orchestra
    group_follower_orchestra = AgentGroup(
        agent_type=Circular,
        size=size_orchestra,
        attributes=attributes(simulation, familiar=0, in_finlandia=False, in_finlandia_extended=False, has_target=True, is_follower=True))

    simulation.agents.add_non_overlapping_group(
        "group_follower_orchestra",
        group_follower_orchestra,
        position_gen=False,
        position_iter=iter([]),
        spawn=14,
        obstacles=geom_to_linear_obstacles(field.obstacles))

    if n_leaders == 0:
        # Check if the solution has already been evaluated, if it has printed the total evacuation time and return
        bank_evactime = solutionbank(cells, target_exits, n_leaders)
        if bank_evactime != 0:
            print(bank_evactime)
            return

    if n_leaders > 0:
        # generate_leader_pos() should check that guides are not spawned in unfeasible positions
        init_pos, inside_ext = generate_leader_pos(simulation, cells, n_leaders)
        inside = inside_ext
        print(init_pos)
        target_exits = iter(target_exits)
        init_pos = iter(init_pos)
        inside_ext = iter(inside_ext)
        inside = iter(inside)

        # Check if the solution has already been evaluated, if it has printed the total evacuation time and return
        bank_evactime = solutionbank(cells, target_exits, n_leaders)
        if bank_evactime != 0:
            print(bank_evactime)
            return


        # Add leaders.
        # NB! If there are multiple leaders, the function that is set to create the leaders should check that the leaders do
        # not overlap each other.
        group_leader = AgentGroup(
            agent_type=Circular,
            size=n_leaders,
            attributes=attributes_leader(simulation, fin_iter=inside, fin_ext_iter=inside_ext,
                                         target_iter=target_exits, has_target=True, is_follower=False))

        # If it is not taken care before hand that leaders can't overlap, the function will terminate here.
        simulation.agents.add_non_overlapping_group(
            "group_leader",
            group_leader,
            position_gen=True,
            position_iter=init_pos,
            spawn=0,
            obstacles=geom_to_linear_obstacles(field.obstacles))

    # We do not need to set the seed number, since we use the deterministic social force model
    #np.random.seed(seed)
    simulation.update()
    simulation.run()

    print(simulation.data['time_tot'])

    # Write the solution to the solution bank
    if n_leaders == 0:
        banksolution = "{}{}".format(simulation.data['time_tot'], '\n')
    if n_leaders == 1:
        banksolution = "{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], '\n')
    if n_leaders == 2:
        banksolution = "{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], '\n')
    if n_leaders == 3:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], '\n')
    if n_leaders == 4:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], '\n')
    if n_leaders == 5:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], ' ', cells[4], ' ', exits[4], '\n')
    if n_leaders == 6:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], ' ', cells[4], ' ', exits[4], ' ', cells[5], ' ', exits[5], '\n')
    if n_leaders == 7:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], ' ', cells[4], ' ', exits[4], ' ', cells[5], ' ', exits[5], ' ', cells[6], ' ', exits[6], '\n')
    if n_leaders == 8:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], ' ', cells[4], ' ', exits[4], ' ', cells[5], ' ', exits[5], ' ', cells[6], ' ', exits[6], ' ', cells[7], ' ', exits[7], '\n')
    if n_leaders == 9:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], ' ', cells[4], ' ', exits[4], ' ', cells[5], ' ', exits[5], ' ', cells[6], ' ', exits[6], ' ', cells[7], ' ', exits[7], ' ', cells[8], ' ', exits[8], '\n')
    if n_leaders == 10:
        banksolution = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(simulation.data['time_tot'], ' ', cells[0], ' ', exits[0], ' ', cells[1], ' ', exits[1], ' ', cells[2], ' ', exits[2], ' ', cells[3], ' ', exits[3], ' ', cells[4], ' ', exits[4], ' ', cells[5], ' ', exits[5], ' ', cells[6], ' ', exits[6], ' ', cells[7], ' ', exits[7], ' ', cells[8], ' ', exits[8], ' ', cells[9], ' ', exits[9], '\n')

    if os.path.isfile("deterministic/bank_deterministic.out"):
        bankfile = open("deterministic/bank_deterministic.out", "a")
        bankfile.write(banksolution)
        bankfile.close()
    else:
        bankfile = open("deterministic/bank_deterministic.out", "w")
        bankfile.write(banksolution)
        bankfile.close()

    return



if __name__ == '__main__':
    arguments = sys.argv
    gene_data = arguments[1:]

    # Cells of guides
    cells_data = gene_data[0::3]
    cells_data = [int(cells_data[i]) for i in range(len(cells_data))]

    # Exits of guides
    exits_data = gene_data[1::3]
    exits_data = [int(exits_data[i]) for i in range(len(exits_data))]

    # Tags to determine which genes are active (0) or inactive (1)
    tags = gene_data[2::3]
    tags = [int(tags[i]) for i in range(len(tags))]

    cells=[]
    exits=[]
    for i in range(len(tags)):
        if tags[i] == 0:
            cells.append(cells_data[i])
            exits.append(exits_data[i])

    # Number of guides
    n_guides = len(cells)

    # Run the evacuation simulation
    if n_guides == 0:
        run([[],[]], 0)
    if n_guides == 1:
        run([[exits[0], cells[0]]], 1)
    elif n_guides == 2:
        run([[exits[0], cells[0]], [exits[1], cells[1]]], 2)
    elif n_guides == 3:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]]], 3)
    elif n_guides == 4:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]]], 4)
    elif n_guides == 5:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]], [exits[4], cells[4]]], 5)
    elif n_guides == 6:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]], [exits[4], cells[4]], [exits[5], cells[5]]], 6)
    elif n_guides == 7:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]], [exits[4], cells[4]], [exits[5], cells[5]], [exits[6], cells[6]]], 7)
    elif n_guides == 8:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]], [exits[4], cells[4]], [exits[5], cells[5]], [exits[6], cells[6]], [exits[7], cells[7]]], 8)
    elif n_guides == 9:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]], [exits[4], cells[4]], [exits[5], cells[5]], [exits[6], cells[6]], [exits[7], cells[7]], [exits[8], cells[8]]], 9)
    elif n_guides == 10:
        run([[exits[0], cells[0]], [exits[1], cells[1]], [exits[2], cells[2]], [exits[3], cells[3]], [exits[4], cells[4]], [exits[5], cells[5]], [exits[6], cells[6]], [exits[7], cells[7]], [exits[8], cells[8]], [exits[9], cells[9]]], 10)

