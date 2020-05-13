import logging

from PyQt4 import QtGui
from crowddynamics.exceptions import InvalidValue, InvalidType
from loggingtools import log_with
from traitlets.traitlets import TraitType, Int, Float, Complex, \
    Bool, Unicode, Enum, is_trait, Tuple, UseEnum

from qtgui.exceptions import CrowdDynamicsGUIException


def to_string(value):
    if isinstance(value, str):
        return value
    elif hasattr(value, '__name__'):
        return value.__name__
    elif value is None:
        return ''
    else:
        return str(value)


@log_with()
def mkQComboBox(default, callback, values):
    """Create QComboBOx

    Args:
        callback:
        default:
        values:

    Returns:
        QtGui.QComboBox:

    """
    # Because Combobox can only handle string convert values to strings
    d = {to_string(v): v for v in values}

    new_values = tuple(d.keys())
    new_default = to_string(default)

    def new_callback(value): callback(d[value])

    widget = QtGui.QComboBox()
    widget.addItems(new_values if new_values else [new_default])
    index = widget.findText(new_default)
    widget.setCurrentIndex(index)
    widget.currentIndexChanged[str].connect(new_callback)
    return widget


def mkQRadioButton(default, callback):
    """Create QRadioButton

    Args:
        callback:
        default:

    Returns:
        QtGui.QRadioButton:

    """
    widget = QtGui.QRadioButton()
    widget.setChecked(default)
    widget.toggled.connect(callback)
    return widget


def mkQDoubleSpinBox(default, callback, values):
    """Create QDoubleSpinBox

    Args:
        callback:
        default:
        values:

    Returns:
        QtGui.QDoubleSpinBox:

    """
    widget = QtGui.QDoubleSpinBox()
    inf = float("inf")
    minimum, maximum = values if values else (None, None)
    widget.setMinimum(minimum if minimum else -inf)
    widget.setMaximum(maximum if maximum else inf)
    widget.setValue(default)
    widget.valueChanged.connect(callback)
    return widget


def mkQSpinBox(default, callback, values):
    """Create QSpinBox

    Args:
        callback:
        default:
        values:

    Returns:
        QtGui.QSpinBox:

    """
    widget = QtGui.QSpinBox()
    minimum, maximum = values if values else (None, None)
    widget.setMinimum(minimum if minimum else -int(10e7))
    widget.setMaximum(maximum if maximum else int(10e7))
    widget.setValue(default)
    widget.valueChanged.connect(callback)
    return widget


def create_data_widget(name, default, values, callback):
    """Create QWidget for setting data

    .. list-table::
       :header-rows: 1

       * - Type
         - Validation
         - Qt widget
       * - int
         - Tuple[int, int]
         - QSpinBox
       * - float
         - Tuple[float, float]
         - QDoubleSpinBox
       * - bool
         - bool
         - QRadioButton
       * - str
         - Sequence[str]
         - QComboBox

    Args:
        name (str):
            Name for the label of the widget
        default (int|float|bool|str):
            Default value for the widget
        values (typing.Sequence):
            Values that are valid input for the widget
        callback (typing.Callable):
            Callback function that is called when the value of widget changes.

    Returns:
        typing.Tuple[QtGui.QLabel, QtGui.QWidget]:
    """
    label = QtGui.QLabel(name)

    if isinstance(default, int):
        return label, mkQSpinBox(default, callback, values)
    elif isinstance(default, float):
        return label, mkQDoubleSpinBox(default, callback, values)
    elif isinstance(default, bool):
        return label, mkQRadioButton(default, callback)
    elif isinstance(default, str):
        return label, mkQComboBox(default, callback, values)
    else:
        logger = logging.getLogger(__name__)
        error = CrowdDynamicsGUIException(
            'Invalid default type: {type}'.format(type=type(default)))
        logger.error(error)
        raise error


def trait_to_QWidget(name, trait, callback=lambda _: None):
    if is_trait(trait):
        label = QtGui.QLabel(name)

        if isinstance(trait, Int):
            return label, mkQSpinBox(trait.default_value, callback,
                                     (trait.min, trait.max))
        elif isinstance(trait, Float):
            return label, mkQDoubleSpinBox(trait.default_value, callback,
                                           (trait.min, trait.max))
        elif isinstance(trait, Complex):
            raise NotImplementedError
        elif isinstance(trait, Bool):
            return label, mkQRadioButton(trait.default_value, callback)
        elif isinstance(trait, Unicode):
            raise NotImplementedError
        elif isinstance(trait, Enum):
            return label, mkQComboBox(trait.default_value, callback,
                                      trait.values)
        # elif isinstance(trait, UseEnum):
        #     # TODO
        #     return label, mkQComboBox(trait.default_value, callback,
        #                               trait.enum_class)
        elif isinstance(trait, Tuple):
            raise NotImplementedError
        else:
            raise InvalidValue('Trait conversion is not supported for: '
                               '{}'.format(trait))
    else:
        raise InvalidType('Trait should be instance of {}'.format(TraitType))
