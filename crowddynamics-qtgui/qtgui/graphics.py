from copy import deepcopy

from PyQt4 import QtGui
import logging
import os
from collections import Iterable

import numba
import numpy as np
import pyqtgraph as pg
from crowddynamics.core.vector2D import normalize, unit_vector, length
from crowddynamics.simulation.agents import is_model
from loggingtools import log_with
from numba import f8
from shapely.geometry import Point, LineString, Polygon

from qtgui.exceptions import CrowdDynamicsGUIException, FeatureNotImplemented

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'conf')
GRAPHICS_CFG = os.path.join(CONFIG_DIR, 'graphics.cfg')
GRAPHICS_CFG_SPEC = os.path.join(CONFIG_DIR, 'graphics_spec.cfg')


def color(name, alpha=255):
    return {
        'blue': QtGui.QColor(0, 0, 255, alpha),
        'green': QtGui.QColor(0, 255, 0, alpha),
        'red': QtGui.QColor(255, 0, 0, alpha),
        'cyan': QtGui.QColor(0, 255, 255, alpha),
        'magenta': QtGui.QColor(255, 0, 255, alpha),
        'yellow': QtGui.QColor(255, 255, 0, alpha),
        'black': QtGui.QColor(0, 0, 0, alpha),
        'white': QtGui.QColor(255, 255, 255, alpha),
        'd': QtGui.QColor(150, 150, 150, alpha),
        'l': QtGui.QColor(200, 200, 200, alpha),
        's': QtGui.QColor(100, 100, 150, alpha),
    }[name]


def gray_scale(arg, alpha=255):
    r = g = b = int(arg * 255)
    return QtGui.QColor(r, g, b, alpha)


def color_cycle(size):
    if size == 1:
        return [color('red')]
    elif size == 2:
        return [color('red'), color('green')]
    elif size == 3:
        return [color('red'), color('green'), color('blue')]
    elif size == 4:
        return [color('red'), color('green'), color('blue'), color('yellow')]
    else:
        return [gray_scale(value) for value in np.linspace(0.2, 0.8, size)]


def frames_per_second():
    """Timer for computing frames per second"""
    from timeit import default_timer as timer

    last_time = timer()
    fps_prev = 0.0
    while True:
        now = timer()
        dt = now - last_time
        last_time = now
        fps = 1.0 / dt
        s = np.clip(3 * dt, 0, 1)
        fps_prev = fps_prev * (1 - s) + fps * s
        yield fps_prev


def circles(radius):
    """Defaults opts for circular plot items

    Args:
        radius (numpy.ndarray):

    Returns:
        dict:
    """
    return {
        'pxMode': False,
        'pen': None,
        'symbol': 'o',
        'symbolSize': 2 * radius,
    }


def mk_opts(size=1, **kwargs):
    opts = dict()

    if 'pen' in kwargs:
        pen = kwargs['pen']
        opts['pen'] = pen if size == 1 else np.full(size, pen)

    if 'symbolPen' in kwargs:
        brush = kwargs['symbolPen']
        opts['symbolPen'] = brush if size == 1 else np.full(size, brush)

    if 'symbolBrush' in kwargs:
        brush = kwargs['symbolBrush']
        opts['symbolBrush'] = brush if size == 1 else np.full(size, brush)

    return opts


@numba.jit([(f8[:, :], f8[:, :], f8[:])],
           nopython=True, nogil=True, cache=True)
def lines(origin, direction, lengths):
    """Lines

    Args:
        origin (numpy.ndarray):
        direction (numpy.ndarray):
        lengths (numpy.ndarray):
    """
    n, m = origin.shape
    values = np.empty(shape=(2 * n, m))
    for i in range(n):
        l = lengths[i]
        v_d = direction[i]

        if length(v_d) < 0.05:
            # Handle direction vector that is zero vector
            l = 0.05
            v_d = np.array((1.0, 0.0))

        values[2 * i, :] = origin[i, :]
        values[2 * i + 1, :] = origin[i, :] + normalize(v_d) * l
    return values


def lines_connect(n):
    connect = np.ones(shape=2 * n, dtype=np.uint8)
    connect[1::2] = 0
    return connect


class AgentsBase(object):
    __slots__ = ('center', 'left', 'right', 'orientation', 'direction',
                 'target_direction')

    def __init__(self):
        # Torso
        self.center = pg.PlotDataItem()
        self.left = pg.PlotDataItem()
        self.right = pg.PlotDataItem()

        # Direction indicators
        self.orientation = pg.PlotDataItem()
        self.direction = pg.PlotDataItem()
        self.target_direction = pg.PlotDataItem()

    def addItem(self, widget: pg.PlotItem):
        raise NotImplementedError

    def setData(self, agents: np.ndarray):
        raise NotImplementedError


class CircularAgents(AgentsBase):
    def __init__(self, agents):
        super().__init__()
        assert is_model(agents, 'circular'), 'Agent should be circular model'

    @log_with(qualname=True, ignore=('self',))
    def addItem(self, widget: pg.PlotItem):
        widget.addItem(self.center)
        widget.addItem(self.direction)
        widget.addItem(self.target_direction)

    def setData(self, agents):
        connect = lines_connect(agents.size)
        self.center.opts.update(**circles(agents['radius']))

        brushes = np.full(shape=agents.size, fill_value=color('white'))

        is_leader = agents['is_leader']
        #print(agents['is_leader'])
        #brushes[is_leader] = color_cycle(size=int(np.sum(is_leader)))
        brushes[is_leader] = color('black')
#
#        for i, j in enumerate(agents['index_leader']):
#            if j == -1:
#                continue
#            r, g, b, a = brushes[j].getRgb()
#            brushes[i] = QtGui.QColor(r, g, b, int(0.30 * 255))

        # For inactive agents set lower alpha for current color
        for i, b in enumerate(~agents['active']):
            if b:
                r, g, b, a = brushes[i].getRgb()
                brushes[i] = QtGui.QColor(r, g, b, int(0.15 * a))

        self.center.opts.update(symbolBrush=brushes,
                                symbolPen=pg.mkPen(color=0.0))

        self.direction.opts.update(
            connect=connect,
            pen=pg.mkPen('l', width=0.03, cosmetic=False))
        self.target_direction.opts.update(
            connect=connect,
            pen=pg.mkPen('g', width=0.03, cosmetic=False))

        self.center.setData(agents['position'])

        self.direction.setData(
            lines(agents['position'], agents['velocity'],
                  2 * agents['radius']))
        self.target_direction.setData(
            lines(agents['position'], agents['target_direction'],
                  2 * agents['radius']))


class ThreeCircleAgents(AgentsBase):
    def __init__(self, agents):
        super().__init__()
        assert is_model(agents, 'three_circle'), \
            'Agent should the three_circle model'

    @log_with(qualname=True, ignore=('self',))
    def addItem(self, widget: pg.PlotItem):
        widget.addItem(self.left)
        widget.addItem(self.right)
        widget.addItem(self.center)
        widget.addItem(self.orientation)
        widget.addItem(self.direction)
        widget.addItem(self.target_direction)

    def setData(self, agents):
        self.center.opts.update(**circles(agents['r_t']))
        self.left.opts.update(**circles(agents['r_s']))
        self.right.opts.update(**circles(agents['r_s']))

        connect = lines_connect(agents.size)
        self.orientation.opts.update(
            connect=connect,
            pen=pg.mkPen('m', width=0.03, cosmetic=False))
        self.direction.opts.update(
            connect=connect,
            pen=pg.mkPen('l', width=0.03, cosmetic=False))
        self.target_direction.opts.update(
            connect=connect,
            pen=pg.mkPen('g', width=0.03, cosmetic=False))

        self.left.setData(agents['position_ls'])
        self.right.setData(agents['position_rs'])
        self.center.setData(agents['position'])

        self.orientation.setData(
            lines(agents['position'], unit_vector(agents['orientation']),
                  1.1 * agents['radius']))
        self.direction.setData(
            lines(agents['position'], agents['velocity'],
                  2 * agents['radius']))
        self.target_direction.setData(
            lines(agents['position'], agents['target_direction'],
                  2 * agents['radius']))


@log_with()
def linestring(geom, **kargs):
    """Make plotitem from LineString

    Args:
        geom (LineString|LinearRing):

    Returns:
        PlotDataItem:
    """
    # TODO: MultiLineString
    return pg.PlotDataItem(*geom.xy, **kargs)


@log_with()
def polygon(geom, **kargs):
    """Make plotitem from Polygon

    Args:
        geom (Polygon):

    Returns:
        PlotDataItem:
    """
    return pg.PlotDataItem(*geom.exterior.xy, **kargs)


@log_with()
def shapes(geom, **kargs):
    """Shape

    Args:
        geom:
        **kargs:

    Returns:
        list:
    """
    if isinstance(geom, Point):
        return []  # NotImplemented
    if isinstance(geom, LineString):
        return [linestring(geom, **kargs)]
    elif isinstance(geom, Polygon):
        return [polygon(geom, **kargs)]
    elif isinstance(geom, Iterable):
        return sum((shapes(geo, **kargs) for geo in geom), [])
    else:
        raise CrowdDynamicsGUIException


class DataPlot(pg.PlotItem):
    def __init__(self, parent=None):
        super(DataPlot, self).__init__(parent)
        self.time_tot = []
        self.goal_reached = []
        self.plot = pg.PlotDataItem()
        self.addItem(self.plot)
        self.setAspectLocked(lock=True, ratio=4)
        self.showGrid(x=True, y=True, alpha=0.25)
        # TODO: clear

    def update_data(self, message):
        self.time_tot.append(message.data['time_tot'])
        self.goal_reached.append(message.data['goal_reached'])
        self.plot.setData(self.time_tot, self.goal_reached)


class MultiAgentPlot(pg.PlotItem):
    r"""MultiAgentPlot

    GraphicsItem for displaying individual graphics of individual simulation.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, parent=None):
        super(MultiAgentPlot, self).__init__(parent)

        self.frames_per_second = frames_per_second()

        # Plot settings
        self.setAspectLocked(lock=True, ratio=1)
        self.showGrid(x=True, y=True, alpha=0.25)
        self.disableAutoRange()

        self.obstacles_kw = dict(
            pen=pg.mkPen(color=0.0, width=1))

        self.targets_kw = dict(
            pen=pg.mkPen(color=0.5, width=1))

        # Geometry
        self.__domain = None
        self.__obstacles = None
        self.__targets = None
        self.__agents = None

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, geom):
        """Set domain

        Args:
            geom (Polygon):
        """
        if geom is None:
            self.__domain = None
        else:
            x, y = geom.exterior.xy
            x, y = np.asarray(x), np.asarray(y)
            self.setRange(xRange=(x.min(), x.max()), yRange=(y.min(), y.max()))
            item = polygon(geom)
            self.addItem(item)
            self.__domain = item

    @property
    def obstacles(self):
        return self.__obstacles

    @obstacles.setter
    def obstacles(self, geom):
        """Set obstacles

        Args:
            geom (LineString|MultiLineString):
        """
        if geom is None:
            self.__obstacles = None
        else:
            items = shapes(geom, **self.obstacles_kw)
            for item in items:
                self.addItem(item)
            self.__obstacles = items

    @property
    def targets(self):
        return self.__targets

    @targets.setter
    def targets(self, geom):
        """Targets

        Args:
            geom (Polygon|MultiPolygon):
        """
        if geom is None:
            self.__targets = None
        else:
            items = shapes(geom)
            for item in items:
                self.addItem(item)
            self.__targets = items

    @property
    def agents(self):
        return self.__agents

    @agents.setter
    def agents(self, agents):
        if is_model(agents, 'circular'):
            self.__agents = CircularAgents(agents)
            self.agents.addItem(self)
            self.agents.setData(agents)
        elif is_model(agents, 'three_circle'):
            self.__agents = ThreeCircleAgents(agents)
            self.agents.addItem(self)
            self.agents.setData(agents)
        else:
            raise FeatureNotImplemented('Wrong agents type: "{}"'.format(
                agents))

    @log_with(qualname=True, timed=True, ignore=('self',))
    def configure(self, domain, obstacles, targets, agents):
        """Configure plot items"""
        # Clear previous plots and items
        self.clearPlots()
        self.clear()
        self.domain = domain
        self.obstacles = obstacles
        self.targets = targets
        self.agents = agents

    def update_data(self, message):
        """Update plot data"""
        agents = message.agents
        data = message.data
        self.agents.setData(agents)
        title = 'Fps: {:.2f} | Iterations: {} | Time: {:.2f} '.format(
            next(self.frames_per_second), data['iterations'], data['time_tot'])
        self.setTitle(title)
