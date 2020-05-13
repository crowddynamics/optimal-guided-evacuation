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

    agent_type = Enum(
        default_value=Circular,
        values=(Circular, ThreeCircle))
    body_type = Enum(
        default_value='adult',
        values=('adult',))

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
        return agents
