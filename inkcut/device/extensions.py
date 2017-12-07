# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jan 16, 2015

@author: jrm
"""
import enaml
from atom.api import (
    Atom, Float, Instance, Unicode, Bool, ForwardInstance,
    List, Int, Callable, Coerced, observe
)
from enaml.core.declarative import Declarative, d_
from enaml.widgets.api import Container

DEVICE_DRIVER_POINT = 'inkcut.device.driver'
DEVICE_PROTOCOL_POINT = 'inkcut.device.protocols'
DEVICE_TRANSPORT_POINT = 'inkcut.device.transport'


def default_device_factory():
    """ Generates a device if none is given by the driver.
    
    Returns
    -------
        result: Device
            A configured Device that the application can use.
    """
    from .plugin import Device
    return Device()


def default_config_view_factory():
    with enaml.imports():
        from .view import ConfigView
    return ConfigView


class DeviceDriver(Declarative):
    """ Provide meta info about this device """
    # ID of the device
    # If none exits one i created from manufacturer.model
    id = d_(Unicode())

    # Name of the device (optional)
    name = d_(Unicode())

    # Model of the device (optional)
    model = d_(Unicode())

    # Manufacturer of the device (optional)
    manufacturer = d_(Unicode())

    # Width of the device (required)
    width = d_(Unicode())

    # Length of the device, if it uses a roll, leave blank
    length = d_(Unicode())

    # Factory to construct the inkcut.device.plugin.Device or subclass.
    # If none is given it will be generated by the DevicePlugin
    #: for an example, see the DeviceDriver in the inkcut.device.pi.manifest
    factory = d_(Callable(default=default_device_factory))

    # List of protocol IDs supported by this device
    protocols = d_(List(Unicode()))

    # List of transport IDs supported by this device
    connections = d_(List(Unicode()))

    #: Config view for editing the config of this device
    config_view = d_(Callable(default=default_config_view_factory))


class DeviceProtocol(Declarative):
    # Id of the protocol
    id = d_(Unicode())

    # Name of the protocol (optional)
    name = d_(Unicode())

    # Factory to construct the protocol,
    # takes a single argument for the transport
    factory = d_(Callable())

    #: Config view for editing the config of this device
    config_view = d_(Callable(default=default_config_view_factory))


class DeviceTransport(Declarative):
    # Id of the protocol
    id = d_(Unicode())

    # Name of the protocol (optional)
    name = d_(Unicode())

    # Factory to construct the protocol,
    # takes a single argument for the transport
    factory = d_(Callable())

    #: Config view for editing the config of this device
    config_view = d_(Callable(default=default_config_view_factory))
