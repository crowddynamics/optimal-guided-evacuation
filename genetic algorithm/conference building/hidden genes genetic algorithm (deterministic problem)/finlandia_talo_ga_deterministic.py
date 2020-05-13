import numpy as np
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString, Point, LinearRing
from shapely.ops import polygonize, cascaded_union
from scipy.spatial.qhull import Delaunay
from crowddynamics.core.distance import distance_circle_line

from crowddynamics.core.sampling import triangle_area_cumsum, random_sample_triangle
from crowddynamics.core.vector2D import length

from crowddynamics.core.geometry import geom_to_linear_obstacles
from crowddynamics.simulation.agents import Circular, ThreeCircle, NO_TARGET, \
    Agents, AgentGroup
from crowddynamics.simulation.field import Field
from crowddynamics.simulation.logic import Reset, InsideDomain, Integrator, \
    Fluctuation, Adjusting, Navigation, ExitDetection, \
    Orientation, AgentAgentInteractions, AgentObstacleInteractions, \
    LeaderFollower, TargetReached
from crowddynamics.simulation.multiagent import MultiAgentSimulation
from shapely.geometry import Polygon
from shapely.geometry.linestring import LineString
from traitlets.traitlets import Enum, Int, default

class FinlandiaTalo2ndFloorField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def f(value, scale=10 / 1.5):
            if value:
                return tuple(map(lambda x: scale * x, value))
            else:
                return None

        A = list(map(f, [
            None,
            (19.226, 4.194),
            (19.444, 3.887),
            (21.368, 1.179),
            (1.567, 1.179),
            (1.574, 2.682),
            (1.565, 4.603),
            (4.012, 5.296),
            (2.736, 2.689),
        ]))
        B = list(map(f, [
            None,
            (4.421, 3.862),
            (3.881, 5.755),
            (4.998, 6.024),
            (5.209, 5.169),
            (4.677, 5.041),
            (4.787, 4.587),
            (5.394, 5.168),
            (4.858, 7.154),
            (6.048, 7.667),
            (5.993, 7.823),
            (6.71, 8.026),
        ]))
        C = list(map(f, [
            None,
            (6.916, 8.038),
            (7.043, 8.08),
            (7.291, 7.926),
            (7.411, 7.45),
            (7.669, 7.408),
            (7.709, 7.224),
            (8.026, 7.317),
            (8.257, 6.494),
            (8.141, 6.472),
            None,
            (8.387, 4.775),
            (6.416, 4.501),
            (6.372, 4.631),
            (6.047, 4.587),
            (6.336, 4.992),
            (5.889, 4.955),
            (5.549, 6.147),
        ]))
        D = list(map(f, [
            (),
            (8.198, 6.705),
            (10.513, 7.321),
            (10.598, 7.06),
            (10.705, 6.803),
            (10.441, 6.747),
            (10.806, 5.387),
            (12.112, 5.329),
            (8.915, 4.884),
            (8.518, 6.328),
            (9.929, 6.703),
            (10.304, 5.281),
            (11.936, 3.715),
            (12.488, 8.787),
            (15.002, 9.438),
            (18.288, 4.784),
            (18.634, 4.98),
            (18.906, 4.63),
            (19.6, 5.093),
            (21.673, 2.116),
        ]))
        E = list(map(f, [
            (),
            (17.693, 4.928),
            (18.233, 4.09),
            (16.799, 2.954),
            (16.457, 3.582),
            (15.73, 3.979),
            (15.998, 3.024),
            (14.23, 2.634),
            (14.142, 3.571),
            (13.579, 3.582),
            (13.568, 3.064),
            (12.311, 3.34),
            (12.311, 3.88),
            (8.859, 2.682),
            (8.435, 2.625),
            (8.266, 3.685),
            (8.718, 3.741),
            (8.333, 3.265),
            (8.208, 3.21),
            (8.267, 2.861),
            (7.978, 2.827),
            (7.816, 2.708),
            (5.787, 5.313),
            (6.217, 2.716),
            (5.732, 2.734),
            (4.432, 2.722),
            (4.332, 2.923),
            (4.24, 3.134),
            (4.07, 3.656),
            (2.375, 3.656),
            (2.375, 3.233),
            (3.675, 3.247),
            (16.487, 1.687),
            (18.101, 1.682),
            (18.107, 1.179),
            (18.734, 1.652),
            (19.087, 3.491),
            (6.295, 3.232),
            (4.571, 3.225),
            (4.444, 3.696),
        ]))
        G = list(map(f, [
            (),
            (12.327, 4.117),
            (12.356, 4.281),
            (12.374, 4.428),
            (12.4, 4.6),
            (12.428, 4.747),
            (12.456, 4.905),
            (12.484, 5.059),
            (12.509, 5.22),
            (12.537, 5.396),
            (12.558, 5.551),
            (12.588, 5.718),
            (12.616, 5.887),
            (12.644, 6.035),
            (12.66, 6.204),
            (12.702, 6.358),
            (12.715, 6.554),
            (12.748, 6.719),
        ]))
        H = list(map(f, [
            (),
            (12.996, 3.897),
            (13.024, 4.053),
            (13.044, 4.209),
            (13.069, 4.362),
            (13.06, 4.526),
            (13.113, 4.679),
            (13.119, 4.843),
            (13.137, 4.995),
            (13.177, 5.169),
            (13.214, 5.308),
            (13.239, 5.461),
            (13.253, 5.62),
            (13.297, 5.78),
            (13.313, 5.936),
            (13.364, 6.088),
            (13.385, 6.241),
            (13.4, 6.4),
        ]))
        I = list(map(f, [
            (),
            (13.572, 3.769),
            (13.595, 3.93),
            (13.608, 4.092),
            (13.613, 4.259),
            (13.631, 4.412),
            (13.626, 4.574),
            (13.64, 4.74),
            (13.649, 4.884),
            (13.671, 5.046),
            (13.676, 5.217),
            (13.689, 5.374),
            (13.703, 5.523),
            (13.698, 5.671),
            (13.716, 5.846),
            (13.73, 6.004),
            (13.743, 6.166),
            (13.748, 6.323),
        ]))
        J = list(map(f, [
            (),
            (16.789, 4.838),
            (16.713, 4.98),
            (16.666, 5.117),
            (16.6, 5.282),
            (16.506, 5.428),
            (16.465, 5.592),
            (16.36, 5.72),
            (16.301, 5.89),
            (16.205, 6.039),
            (16.083, 6.12),
            (16.044, 6.314),
            (15.987, 6.454),
            (15.895, 6.624),
            (15.796, 6.734),
            (15.692, 6.866),
            (15.6, 7),
            (15.516, 7.161),
        ]))
        K = list(map(f, [
            (),
            (17.339, 5.382),
            (17.263, 5.524),
            (17.16, 5.672),
            (17.067, 5.798),
            (16.99, 5.941),
            (16.888, 6.081),
            (16.8, 6.2),
            (16.703, 6.367),
            (16.59, 6.484),
            (16.495, 6.624),
            (16.396, 6.761),
            (16.31, 6.881),
            (16.217, 7.027),
            (16.113, 7.179),
            (16.005, 7.31),
            (15.898, 7.471),
            (15.793, 7.635),
        ]))
        O = list(map(f, [
            (),
            (5.152, 6.067),
            (6.837, 7.333),
            (7.07, 6.03),
            (8.192, 6.119),
            (12.288, 6.949),
            (8.895, 1.179),
            (12.027, 1.179),
            (16.478, 1.179),
            (3.672, 3.656),
            (4.249, 4.467),
            (17.815, 5.455),
            (11.97, 4.027),
            (14.846, 6.717),
            (14.097, 6.472),
            (12.699, 6.912),
            (15.987, 8.042),
        ]))
        U = list(map(f, [
            (),
            (14.169, 3.788),
            (14.153, 3.954),
            (14.159, 4.103),
            (14.167, 4.264),
            (14.162, 4.431),
            (14.176, 4.573),
            (14.177, 4.743),
            (14.179, 4.894),
            (14.176, 5.052),
            (14.187, 5.239),
            (14.2, 5.4),
            (14.19, 5.543),
            (14.192, 5.697),
            (14.195, 5.848),
            (14.195, 6.025),
            (14.2, 6.168),
            (14.2, 6.322),
        ]))
        V = list(map(f, [
            (),
            (14.908, 3.879),
            (14.855, 4.029),
            (14.897, 4.216),
            (14.83, 4.347),
            (14.847, 4.523),
            (14.763, 4.649),
            (14.735, 4.807),
            (14.745, 4.969),
            (14.739, 5.133),
            (14.737, 5.301),
            (14.702, 5.456),
            (14.656, 5.618),
            (14.634, 5.769),
            (14.594, 5.907),
            (14.613, 6.079),
            (14.599, 6.246),
            (14.564, 6.397),
        ]))
        W = list(map(f, [
            (),
            (15.676, 4.123),
            (15.644, 4.269),
            (15.588, 4.431),
            (15.549, 4.576),
            (15.496, 4.723),
            (15.449, 4.865),
            (15.399, 5.031),
            (15.359, 5.176),
            (15.297, 5.332),
            (15.259, 5.484),
            (15.203, 5.629),
            (15.151, 5.78),
            (15.119, 5.928),
            (15.063, 6.087),
            (15.009, 6.252),
            (14.963, 6.386),
            (14.914, 6.553),
        ]))
        X = list(map(f, [
            (),
            (6.007, 7.828),
            (5.869, 8.313),
            (12.146, 9.886),
            (12.447, 8.775),
            (12.41, 8.381),
            (12.308, 7.364),
            (10.598, 7.06),
            (10.552, 7.294),
            (9.632, 7.087),
            (9.575, 7.309),
            (8.878, 7.138),
            (8.926, 6.899),
            (8.205, 6.707),
            (8.028, 7.31),
            (7.76, 7.316),
            (7.462, 7.42),
            (7.291, 7.926),
            (7.046, 8.071),
            (6.71, 8.026),
        ]))
        Y = list(map(f, [
            (),
            (6.588, 8.493),
        ]))
        Z = list(map(f, [
            (),
            (16.176, 4.36),
            (16.099, 4.502),
            (16.053, 4.639),
            (15.986, 4.804),
            (15.947, 4.949),
            (15.876, 5.106),
            (15.84, 5.303),
            (15.758, 5.436),
            (15.704, 5.573),
            (15.662, 5.743),
            (15.6, 5.876),
            (15.559, 6.06),
            (15.495, 6.244),
            (15.421, 6.379),
            (15.374, 6.527),
            (15.316, 6.659),
            (15.239, 6.822),
        ]))

        A[3] = (21.368 * 10 / 1.5, 1.55 * 10 / 1.5)
        A[4] = (1.567 * 10 / 1.5, 1.55 * 10 / 1.5)
        # E[32] = ()
        # E[33] = ()
        E[34] = (18.107 * 10 / 1.5, 1.55 * 10 / 1.5)
        E[35] = (18.734 * 10 / 1.5, 2.3 * 10 / 1.5)
        O[6] = (8.895 * 10 / 1.5, 1.55 * 10 / 1.5)
        O[7] = (12.027 * 10 / 1.5, 1.55 * 10 / 1.5)
        O[8] = (16.478 * 10 / 1.5, 1.55 * 10 / 1.5)
        rest_midpoint = (6 * 10 / 1.5, 1.55 * 10 / 1.5)
        # New points for "Traffic Jam Puzzle"
        rest1 = (4*10/1.5, 1.55*10/1.5)
        rest2 = (8*10/1.5, 1.55*10/1.5)

        obstacles = Polygon()

        obstacles |= LineString(A[1:5 + 1] + [A[8]])
        obstacles |= LineString(A[5:7 + 1])

        obstacles |= LineString(B[1:6 + 1])
        obstacles |= LineString(B[7:11 + 1])

        # obstacles |= LineString(C[1:10] + C[11:14 + 1])
        obstacles |= LineString(C[1:6])  # INCLUDE
        obstacles |= LineString(C[7:10] + C[11:15])  # EXCLUDE?
        obstacles |= LineString(C[15:19])  # EXCLUDE?

        # obstacles |= LineString(D[1:7 + 1])
        obstacles |= LineString(D[2:7 + 1])  # INCLUDE
        obstacles |= LineString(D[8:11 + 1])  # INCLUDE
        # obstacles |= LineString(D[12:19 + 1])
        obstacles |= LineString([D[12]] + [X[5]])  # INCLUDE
        obstacles |= LineString(D[13:19 + 1])  # INCLUDE

        obstacles |= LineString(E[1:4 + 1])
        obstacles |= LineString(E[5:8 + 1])
        obstacles |= LineString(E[9:12 + 1])
        obstacles |= LineString(E[13:16 + 1])
        obstacles |= LineString(E[17:21 + 1] + [E[23]])
        obstacles |= LineString(E[24:26 + 1])
        obstacles |= LineString(E[27:31 + 1])
        # obstacles |= LineString(E[32:34 + 1])
        obstacles |= LineString(E[35:36 + 1])
        obstacles |= LineString(E[35:36 + 1])
        obstacles |= LineString(E[37:39 + 1])

        obstacles |= LineString(X[1:4] + [D[13]])  # INCLUDE
        # obstacles |= LineString(X[6:19]) # EXCLUDE?
        obstacles |= LineString(D[1:3] + [X[6]])  # INCLUDE
        obstacles |= LineString(X[9:12])  # INCLUDE

        # New obstacles for "Traffic Jam Puzzle"
        obstacles |= LineString([C[11]] + [E[16]])
        obstacles |= LineString([E[39]] + [B[1]])

        # These are the obstacles for the agents that start outside the Finlandia hall
        obstacles_finlandia = Polygon()

        # changes start
        # obstacles |= LineString(C[1:10] + C[11:14 + 1])
        obstacles_finlandia |= LineString(C[1:6])  # INCLUDE
        obstacles_finlandia |= LineString(C[7:10] + C[11:15])  # EXCLUDE?
        obstacles_finlandia |= LineString(C[15:19])  # EXCLUDE?

        # obstacles |= LineString(D[1:7 + 1])
        obstacles_finlandia |= LineString(D[2:7 + 1])  # INCLUDE
        obstacles_finlandia |= LineString(D[8:11 + 1])  # INCLUDE
        # obstacles_finlandia |= LineString(D[12:19 + 1])
        obstacles_finlandia |= LineString([D[12]] + [X[5]])  # INCLUDE
        obstacles_finlandia |= LineString(D[13:19 + 1])  # INCLUDE

        obstacles_finlandia |= LineString(X[1:4] + [D[13]])  # INCLUDE
        # obstacles |= LineString(X[6:19]) # EXCLUDE?
        obstacles_finlandia |= LineString(D[1:3] + [X[6]])  # INCLUDE
        obstacles_finlandia |= LineString(X[9:12])  # INCLUDE
        # changes end

        obstacles_finlandia |= LineString(A[1:5 + 1] + [A[8]])
        obstacles_finlandia |= LineString(A[5:7 + 1])

        obstacles_finlandia |= LineString(B[1:6 + 1])
        obstacles_finlandia |= LineString(B[7:11 + 1])

        # obstacles_finlandia |= LineString(D[1:7 + 1])
        # obstacles_finlandia |= LineString(D[8:11 + 1])
        # obstacles_finlandia |= LineString(D[12:19 + 1])

        obstacles_finlandia |= LineString(E[1:4 + 1])
        obstacles_finlandia |= LineString(E[5:8 + 1])
        obstacles_finlandia |= LineString(E[9:12 + 1])
        obstacles_finlandia |= LineString(E[13:16 + 1])
        obstacles_finlandia |= LineString(E[17:21 + 1] + [E[23]])
        obstacles_finlandia |= LineString(E[24:26 + 1])
        obstacles_finlandia |= LineString(E[27:31 + 1])
        obstacles_finlandia |= LineString(E[32:34 + 1])
        obstacles_finlandia |= LineString(E[35:36 + 1])
        obstacles_finlandia |= LineString(E[35:36 + 1])
        obstacles_finlandia |= LineString(E[37:39 + 1])
        obstacles_finlandia |= LineString([D[12]] + [E[11]] + [E[10]] + [E[7]] + [E[6]] + [E[3]] + [E[2]])

        # Benchrows
        # for i in range(1, 18):
        #     obstacles |= LineString([G[i], H[i], I[i]])
        #     obstacles |= LineString([U[i], V[i], W[i]])
        #     obstacles |= LineString([Z[i], J[i], K[i]])

        finlandiahall = Polygon(
            [O[12], E[12], E[9], E[8], E[5], E[1], O[11], O[16],
             O[13], O[14], O[15], O[5]])
        foyer = Polygon([B[6], C[12], E[15], E[21], E[23], E[38], E[39], B[1]])
        helsinkihall = Polygon([O[4], C[11], C[12], C[13], C[15], C[16], C[17],
                                O[1], B[8], B[9], C[3], C[4], O[2], O[3]])
        piazza_1 = Polygon(
            [C[11], E[16], E[13], O[6], O[7], (77.5, 24.767), (77.5, 26.847), (79, 35.527), D[6],
             D[11], D[8]])
        piazza_2 = Polygon(
            [O[7], O[8], E[32], E[3], E[6], E[7], E[10], E[11], D[12]])
        piazza_3 = Polygon(
            [O[8], A[3], A[2], A[1], D[17], E[2], E[3]])
        restaurant = Polygon(
            [A[4], A[5], A[8], E[25], E[24], rest_midpoint]
        )
        outer_bubblegum_finlandia = Polygon(
            [D[12], (75, 15), E[3], E[2], D[15], D[14], D[13]]
        )
        inner_bubblegum_finlandia = Polygon(
            [D[12], E[11], E[10], E[7], E[6], E[3], E[2], D[15], D[14], D[13]])
        orchestra_foyer = Polygon([X[1], X[2], X[3], D[13], X[5], X[6], D[2], X[13], X[14], C[5], C[4],
            C[3], C[2], C[1], X[19]])

        # New spawn areas for "Traffic jam puzzle"
        finlandia_spawn = Polygon([O[12], O[5], O[13], E[6], E[8], E[10], E[12]])
        piazza_3_spawn = Polygon([D[17], E[2], E[3], E[32], E[33], E[36]])
        piazza_1_spawn = Polygon([D[12], E[11], O[7], O[6], E[13]])
        restaurant_spawn = Polygon([rest1, rest2, E[21], E[25]])
        foyer_spawn = Polygon([E[15], C[11], C[12], B[1], E[38], E[37]])
        helsinki_spawn = Polygon([C[4], C[6], C[9], C[11], C[15], C[17], B[9]])
        orchestra_spawn = Polygon([X[3], X[4], X[5], X[6], X[8]])

        exit1 = LineString([D[17], A[1]])
        exit2 = LineString([D[8], D[11]])
        exit3 = LineString([E[31], O[9]])
        exit4 = LineString([O[10], B[6]])
        exit5 = LineString([Y[1], X[19]])
        exit6 = LineString([X[11], X[12]])

        fex = np.array([
            [11.936, 3.715],
            [12.311, 3.34],
            [13.568, 3.064],
            [14.23, 2.634],
            [15.998, 3.024],
            [16.799, 2.954],
            [18.288, 4.784],
            [18.233, 4.09]])
        fex = fex * 10 / 1.5

        slopes = np.array([
            (fex[1][1] - fex[0][1]) / (fex[1][0] - fex[0][0]),
            (fex[3][1] - fex[2][1]) / (fex[3][0] - fex[2][0]),
            (fex[5][1] - fex[4][1]) / (fex[5][0] - fex[4][0]),
            (fex[7][1] - fex[6][1]) / (fex[7][0] - fex[6][0])
        ])

        gradient_vectors = np.array([
            [-1, -slopes[0]],
            [-1, -slopes[1]],
            [-1, -slopes[2]],
            [-1, -slopes[3]]
        ])
        norms = np.hypot([gradient_vectors[0][0], gradient_vectors[1][0], gradient_vectors[2][0],
                          gradient_vectors[3][0]], [gradient_vectors[0][1], gradient_vectors[1][1],
                                                    gradient_vectors[2][1], gradient_vectors[3][1]])
        gradient_vectors = np.array([
            [slopes[0] / norms[0], -1 / norms[0]],
            [slopes[1] / norms[1], -1 / norms[1]],
            [slopes[2] / norms[2], -1 / norms[2]],
            [slopes[3] / norms[3], 1 / norms[3]]
        ])
        dx = 0.2

        fex = np.array([
            [11.936 + dx * gradient_vectors[0][0], 3.715 + dx * gradient_vectors[0][1]],
            [12.311 + dx * gradient_vectors[0][0], 3.34 + dx * gradient_vectors[0][1]],
            [13.568 + dx * gradient_vectors[1][0], 3.064 + dx * gradient_vectors[1][1]],
            [14.23 + dx * gradient_vectors[1][0], 2.634 + dx * gradient_vectors[1][1]],
            [15.998 + 0.3 * dx * gradient_vectors[2][0], 3.024 + 0.3 * dx * gradient_vectors[2][1]],
            [16.799 + 0.3 * dx * gradient_vectors[2][0], 2.954 + 0.3 * dx * gradient_vectors[2][1]],
            [18.288 + dx * gradient_vectors[3][0], 4.784 + dx * gradient_vectors[3][1]],
            [18.233 + dx * gradient_vectors[3][0], 4.09 + dx * gradient_vectors[3][1]]])
        fex = fex * 10 / 1.5

        fexit1 = LineString([fex[0], fex[1]])
        fexit2 = LineString([fex[2], fex[3]])
        fexit3 = LineString([fex[4], fex[5]])
        fexit4 = LineString([fex[6], fex[7]])
        # fexit1 = LineString([D[12], E[11]])
        # fexit2 = LineString([E[10], E[7]])
        # fexit3 = LineString([E[6], E[3]])
        # fexit4 = LineString([D[15], E[2]])

        # Spawns
        # Guides can be spawned anywhere (finlandiahall, foyer, helsinkihall, piazza_1, piazza_2, piazza_3, restaurant,
        # orchestra_foyer), and followers to the "spawn areas" (finlandia_spawn, piazza_3_spawn, piazza_1_spawn,
        # restaurant_spawn, foyer_spawn, helsinki_spawn, orchestra_spawn).
        spawns = [
            finlandiahall,
            foyer,
            helsinkihall,
            piazza_1,
            piazza_2,
            piazza_3,
            restaurant,
            orchestra_foyer,
            finlandia_spawn,
            piazza_3_spawn,
            piazza_1_spawn,
            restaurant_spawn,
            foyer_spawn,
            helsinki_spawn,
            orchestra_spawn
        ]

        # Targets (exits)
        targets = [exit1, exit3, exit4, exit5, exit6]
        #targets = [exit1, exit2, exit3, exit4, exit5, fexit1, fexit2, fexit3, fexit4]
        #targets = [exit1, exit2, exit3, exit4, exit5, exit6, fexit1, fexit2, fexit3, fexit4]
        #targets = [exit1, exit2, exit3, exit4, exit5, exit6]


        self.obstacles = obstacles # obstacles
        self.obstacles_finlandia = obstacles_finlandia # obstacles_finlandia
        self.targets = targets
        self.spawns = spawns
        #self.domain_f = self.convex_hull()
        #self.domain = self.domain_f.difference(finlandiahall)
        self.domain = self.convex_hull()
        self.finlandiahall_extended = outer_bubblegum_finlandia # this should be made as small as possible
        self.finlandiahall = inner_bubblegum_finlandia
        self.helsinkihall = helsinkihall
        self.orchestra_foyer = orchestra_foyer
        self.piazza_2 = piazza_2
        self.piazza_3 = piazza_3


class FinlandiaTalo2ndFloor(MultiAgentSimulation):

    agent_type = Enum(
        default_value=Circular,
        values=(Circular, ThreeCircle))
    body_type = Enum(
        default_value='adult',
        values=('adult',))

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

    @default('logic')
    def _default_logic(self):
        return Reset(self) << \
               TargetReached(self) << (
                   Integrator(self) << (
                       #Fluctuation(self),
                       Adjusting(self) << (
                           Navigation(self) << ExitDetection(
                               self) << LeaderFollower(self),
                           Orientation(self)),
                       AgentAgentInteractions(self),
                       AgentObstacleInteractions(self)))

    @default('field')
    def _default_field(self):
        return FinlandiaTalo2ndFloorField()

    @default('agents')
    def _default_agents(self):
        agents = Agents(agent_type=self.agent_type)
        return agents
