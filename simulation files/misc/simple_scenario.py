import numpy as np
from crowddynamics.core.geometry import geom_to_linear_obstacles
from crowddynamics.simulation.agents import Circular, ThreeCircle, NO_TARGET, \
    Agents, AgentGroup
from crowddynamics.simulation.field import Field
from crowddynamics.simulation.logic import Reset, InsideDomain, Integrator, \
    Fluctuation, Adjusting, Navigation, ExitDetection, \
    Orientation, AgentAgentInteractions, AgentObstacleInteractions, \
    LeaderFollower, TargetReached
from crowddynamics.simulation.multiagent import MultiAgentSimulation
from shapely.geometry import Polygon, Point, LineString, MultiPolygon, MultiLineString, LinearRing
from traitlets.traitlets import Enum, Int, default

from shapely.ops import polygonize
from scipy.spatial.qhull import Delaunay
from crowddynamics.core.sampling import triangle_area_cumsum, random_sample_triangle
from crowddynamics.core.vector2D import length
from crowddynamics.core.distance import distance_circle_line, distance_circles
from crowddynamics.simulation.agents import Agents, AgentGroup, Circular



class SimpleScenarioFloorField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        r = 15
        exitwidth = 1.2
        exit1_x = (r/2-exitwidth/2)*np.sin(np.deg2rad(60))
        exit1_y = (r/2-exitwidth/2)*np.cos(np.deg2rad(60))
        exit2_x = (r/2+exitwidth/2)*np.sin(np.deg2rad(60))
        exit2_y = (r/2+exitwidth/2)*np.cos(np.deg2rad(60))
        # Maximum bufferradius is r*tan30
        bufferradius = 0.25*r*np.tan(np.deg2rad(30))
        #print(bufferradius)

        def f(value, scale=1):
            if value:
                return tuple(map(lambda x: scale * x, value))
            else:
                return None

        # Corner points from the top point counterclockwards
        hexagon = list(map(f, [
            None,
            (r, 2 * r),
            (r * (1 - np.cos(np.deg2rad(30))), r * (1 + np.sin(np.deg2rad(30)))),
            (r * (1 - np.cos(np.deg2rad(30))), r * (1 - np.sin(np.deg2rad(30)))),
            (r, 0),
            (r*(1+np.cos(np.deg2rad(30))), r*(1-np.sin(np.deg2rad(30)))),
            (r*(1+np.cos(np.deg2rad(30))), r*(1+np.sin(np.deg2rad(30)))),
        ]))

        # Midpoints from the top left piece counterclockwards
        midpoints = list(map(f, [
            None,
            (r * (1 - 0.5*np.cos(np.deg2rad(60)) / np.cos(np.deg2rad(30))), r*(1 + 0.5*np.sin(np.deg2rad(60))/np.cos(np.deg2rad(30)))),
            (r * (1 - 0.5 / np.cos(np.deg2rad(30))), r),
            (r * (1 - 0.5*np.cos(np.deg2rad(60)) / np.cos(np.deg2rad(30))), r * (1 -0.5*np.sin(np.deg2rad(60))/np.cos(np.deg2rad(30)))),
            (r * (1 + 0.5*np.cos(np.deg2rad(60)) / np.cos(np.deg2rad(30))), r * (1 -0.5*np.sin(np.deg2rad(60))/np.cos(np.deg2rad(30)))),
            (r * (1 + 0.5 / np.cos(np.deg2rad(30))), r),
            (r*(1+0.5*np.cos(np.deg2rad(60))/np.cos(np.deg2rad(30))), r*(1+0.5*np.sin(np.deg2rad(60))/np.cos(np.deg2rad(30)))),
        ]))
        #print(midpoints)

        # Exitpoints from the top left piece counterclockwards
        exitpoints = list(map(f, [
            None,
            (r - exit1_x, 2 * r - exit1_y),
            (r - exit2_x, 2 * r - exit2_y),
            (r * (1 - np.cos(np.deg2rad(30))), r + exitwidth / 2),
            (r * (1 - np.cos(np.deg2rad(30))), r - exitwidth / 2),
            (r - exit2_x, exit2_y),
            (r - exit1_x, exit1_y),
            (r + exit1_x, exit1_y),
            (r + exit2_x, exit2_y),
            (r * (1 + np.cos(np.deg2rad(30))), r - exitwidth / 2),
            (r * (1 + np.cos(np.deg2rad(30))), r + exitwidth / 2),
            (r + exit2_x, 2 * r - exit2_y),
            (r+exit1_x, 2*r-exit1_y),


        ]))
        obstacles = Polygon()

        # Obstacles from the top of the hexagon counterclockwards
        obstacles |= LineString([exitpoints[12]] + [hexagon[1]] + [exitpoints[1]])
        obstacles |= LineString([exitpoints[2]] + [hexagon[2]] + [exitpoints[3]])
        obstacles |= LineString([exitpoints[4]] + [hexagon[3]] + [exitpoints[5]])
        obstacles |= LineString([exitpoints[6]] + [hexagon[4]] + [exitpoints[7]])
        obstacles |= LineString([exitpoints[8]] + [hexagon[5]] + [exitpoints[9]])
        obstacles |= LineString([exitpoints[10]] + [hexagon[6]] + [exitpoints[11]])

        floorplan = Polygon([
            hexagon[1], hexagon[2], hexagon[3], hexagon[4], hexagon[5], hexagon[6]]
        )

        # Exits from the upper left piece counterclockwards
        exit1 = LineString([exitpoints[1], exitpoints[2]])
        exit2 = LineString([exitpoints[3], exitpoints[4]])
        exit3 = LineString([exitpoints[5], exitpoints[6]])
        exit4 = LineString([exitpoints[7], exitpoints[8]])
        exit5 = LineString([exitpoints[9], exitpoints[10]])
        exit6 = LineString([exitpoints[11], exitpoints[12]])

        # Spawn areas from the upper left piece counterclockwards
        spawn1 = Point(midpoints[1]).buffer(bufferradius)
        spawn2 = Point(midpoints[2]).buffer(bufferradius)
        spawn3 = Point(midpoints[3]).buffer(bufferradius)
        spawn4 = Point(midpoints[4]).buffer(bufferradius)
        spawn5 = Point(midpoints[5]).buffer(bufferradius)
        spawn6 = Point(midpoints[6]).buffer(bufferradius)

        # Spawns
        spawns = [
            spawn1,
            spawn2,
            spawn3,
            spawn4,
            spawn5,
            spawn6
        ]

        targets = [exit1, exit2, exit3, exit4, exit5, exit6]

        self.obstacles = obstacles  # obstacles
        self.targets = targets
        self.spawns = spawns
        self.domain = floorplan



class SimpleScenarioFloor(MultiAgentSimulation):
    #def __init__(self, kokeilu):
    #    self.kokeilu = kokeilu

    size_spawn1 = Int(
        default_value=25, min=0, max=30, help='')
    size_spawn2 = Int(
        default_value=25, min=0, max=30, help='')
    size_spawn3 = Int(
        default_value=25, min=0, max=30, help='')
    size_spawn4 = Int(
        default_value=25, min=0, max=30, help='')
    size_spawn5 = Int(
        default_value=25, min=0, max=30, help='')
    size_spawn6 = Int(
        default_value=25, min=0, max=30, help='')
    size_leader = Int(
        default_value=1, min=0, max=6, help='')

    agent_type = Enum(
        default_value=Circular,
        values=(Circular, ThreeCircle))
    body_type = Enum(
        default_value='adult',
        values=('adult',))

    # A helper function to create spawn points for leaders out of their cell coordinates.
    # The input is the array of leader spawn cells and the number of leaders in the simulation.
    # def generate_leader_pos(cell, n_lead, seed_number):
    def generate_leader_pos(self, cell, n_lead):

        # Load data of followers
        followers = np.load('agents_initialization_simple.npy')
        follower_positions = followers['position']
        follower_radii = followers['radius']

        # Minimal radius of a guide (the same value given in agents.py to the guides).
        max_r = 0.27

        # Number of times spawned leaders are allowed to overlap each other before the program is
        # terminated.
        overlaps = 10000

        # Import Finlandia Hall floor field
        field = SimpleScenarioFloor().field

        # Bound box representing the room. Used later in making Voronoi tessalation.
        width = 30
        height = 30

        # Create a grid structure over the room geometry.
        # Cell size in the grid, determines the resolution of the micro-macro converted data
        cell_size = 3
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

        # Loop through the cells and calculate intersections with spawn areas.
        for i in range(n_lead):

            poly = field.domain.intersection(grids[cell[i]])
            if not poly.is_empty:
                leader_spawns.append(poly)

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
                    #spawn_point = random_sample_triangle(a, b, c, seed)
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
                        # Append the point to spawn points
                        spawn_points.append([spawn_point[0], spawn_point[1]])
                        # print("Guide spawned")
                        # sys.stdout.flush()
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
                    #spawn_point = random_sample_triangle(a, b, c, seed)
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
                        # Append the point to spawn points
                        spawn_points.append([spawn_point[0], spawn_point[1]])
                        # print("Guide spawned")
                        # sys.stdout.flush()
                        break
                    j += 1
                    if j == overlaps:
                        raise Exception('Leaders do not fit in the cell')
        return spawn_points

    def attributes(self, familiar, has_target: bool = True, is_follower: bool = True):
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
            )
            return d

        return wrapper

    def attributes_leader(self, target_iter, has_target: bool = True, is_follower: bool = False):
        def wrapper():
            target = next(target_iter)
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
            )
            return d

        return wrapper

    @default('logic')
    def _default_logic(self):
        return Reset(self) << \
               TargetReached(self) << (
                   Integrator(self) << (
                       Fluctuation(self),
                       Adjusting(self) << (
                           Navigation(self) << LeaderFollower(self),
                           Orientation(self)),
                       AgentAgentInteractions(self),
                       AgentObstacleInteractions(self)))

    @default('field')
    def _default_field(self):
        return SimpleScenarioFloorField()

    @default('agents')
    def _default_agents(self):
        agents = Agents(agent_type=self.agent_type)

        # Generate iterators for group of leaders.
        target_exits = []
        cells = []
        # Hidden gene
        #target_exits = [3,2,5,4,1]
        #cells = [54,21,49,95,6]
        # 1 guide
        #target_exits = [3]
        #cells = [56]
        # 2 guides
        #target_exits = [3,5]
        #cells = [65,48]
        # 3 guides
        #target_exits = [2,4,3]
        #cells = [33,66,55]
        # 4 guides
        #target_exits = [4,2,2,5]
        #cells = [55,24,33,48]
        # 5 guides
        #target_exits = [5,2,1,3,4]
        #cells = [58,24,24,63,94]
        # 6 guides
        #target_exits = [4,0,2,1,5,3]
        #cells = [76,47,33,25,57,61]
        n_guides = len(target_exits)

        # Followers in Spawn 1
        group_follower_spawn1 = AgentGroup(
            agent_type=self.agent_type,
            size=getattr(self, 'size_spawn1'),
            attributes=self.attributes(familiar=0, has_target=True, is_follower=True))

        agents.add_non_overlapping_group(
            "group_follower_spawn1",
            group_follower_spawn1,
            position_gen=False,
            position_iter=iter([]),
            spawn=0,
            obstacles=geom_to_linear_obstacles(self.field.obstacles))

        # Followers in Spawn 2
        group_follower_spawn2 = AgentGroup(
            agent_type=self.agent_type,
            size=getattr(self, 'size_spawn2'),
            attributes=self.attributes(familiar=0, has_target=True, is_follower=True))

        agents.add_non_overlapping_group(
            "group_follower_spawn2",
            group_follower_spawn2,
            position_gen=False,
            position_iter=iter([]),
            spawn=1,
            obstacles=geom_to_linear_obstacles(self.field.obstacles))

        # Followers in Spawn 3
        group_follower_spawn3 = AgentGroup(
            agent_type=self.agent_type,
            size=getattr(self, 'size_spawn3'),
            attributes=self.attributes(familiar=0, has_target=True, is_follower=True))

        agents.add_non_overlapping_group(
            "group_follower_spawn3",
            group_follower_spawn3,
            position_gen=False,
            position_iter=iter([]),
            spawn=2,
            obstacles=geom_to_linear_obstacles(self.field.obstacles))

        # Followers in Spawn 4
        group_follower_spawn4 = AgentGroup(
            agent_type=self.agent_type,
            size=getattr(self, 'size_spawn4'),
            attributes=self.attributes(familiar=0, has_target=True, is_follower=True))

        agents.add_non_overlapping_group(
            "group_follower_spawn4",
            group_follower_spawn4,
            position_gen=False,
            position_iter=iter([]),
            spawn=3,
            obstacles=geom_to_linear_obstacles(self.field.obstacles))

        # Followers in Spawn 5
        group_follower_spawn5 = AgentGroup(
            agent_type=self.agent_type,
            size=getattr(self, 'size_spawn5'),
            attributes=self.attributes(familiar=0, has_target=True, is_follower=True))

        agents.add_non_overlapping_group(
            "group_follower_spawn5",
            group_follower_spawn5,
            position_gen=False,
            position_iter=iter([]),
            spawn=4,
            obstacles=geom_to_linear_obstacles(self.field.obstacles))

        # Followers in Spawn 6
        group_follower_spawn6 = AgentGroup(
            agent_type=self.agent_type,
            size=getattr(self, 'size_spawn6'),
            attributes=self.attributes(familiar=0, has_target=True, is_follower=True))

        agents.add_non_overlapping_group(
            "group_follower_spawn6",
            group_follower_spawn6,
            position_gen=False,
            position_iter=iter([]),
            spawn=5,
            obstacles=geom_to_linear_obstacles(self.field.obstacles))

        if n_guides != 0:

            init_pos = self.generate_leader_pos(cells, n_guides)
            print(init_pos)
            #init_pos = [[8, 6]]
            target_exits = iter(target_exits)
            init_pos = iter(init_pos)

            # Leaders in second floor
            group_leader = AgentGroup(
                agent_type=self.agent_type,
                size=n_guides,
                attributes=self.attributes_leader(target_iter=target_exits, has_target=True, is_follower=False))

            #print(group_leader)

            agents.add_non_overlapping_group(
                "group_leader",
                group_leader,
                position_gen=True,
                position_iter=init_pos,
                spawn=0,
                obstacles=geom_to_linear_obstacles(self.field.obstacles))


        return agents
