from crowddynamics.exceptions import CrowdDynamicsException


class CrowdDynamicsGUIException(CrowdDynamicsException):
    """CrowdDynamics GUI exception base class"""
    pass


class FeatureNotImplemented(CrowdDynamicsGUIException, NotImplementedError):
    """Feature not implemented"""
