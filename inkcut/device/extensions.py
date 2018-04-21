# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jan 16, 2015

@author: jrm
"""
import enaml
from atom.api import Unicode, List, Callable, Dict
from inkcut.core.declarative import Declarative, d_

DEVICE_DRIVER_POINT = 'inkcut.device.driver'
DEVICE_PROTOCOL_POINT = 'inkcut.device.protocols'
DEVICE_TRANSPORT_POINT = 'inkcut.device.transport'


def default_device_factory(driver, transports, protocols):
    """ Generates a device if none is given by the driver.
    Parameters
    ----------
    driver: DeviceDriver
        The declaration of the device driver that was selected by the user
    transports: List[DeviceTransport]
        A list of DeviceTransport declarations that this device driver supports 
    protocols: List[DeviceProtocol]
        A list of DeviceProtocol declarations that this device driver supports 

    Returns
    -------
    result: Device
        A configured Device that the application can use.
    """
    from .plugin import Device, DeviceConfig
    return Device(declaration=driver,
                  transports=transports,
                  protocols=protocols,
                  config=DeviceConfig(**driver.get_device_config()))


def default_device_config_view_factory():
    with enaml.imports():
        from .view import DeviceConfigView
    return DeviceConfigView


def default_config_view_factory():
    with enaml.imports():
        from .view import ConfigView
    return ConfigView


class DeviceDriver(Declarative):
    """ Provide meta info about this device """
    #: ID of the device. If none exits one is created from manufacturer.model
    id = d_(Unicode())

    #: Name of the device (optional)
    name = d_(Unicode())

    #: Model of the device (optional)
    model = d_(Unicode())

    #: Manufacturer of the device (optional)
    manufacturer = d_(Unicode())

    #: Width of the device (required)
    width = d_(Unicode())

    #: Length of the device, if it uses a roll, leave blank
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
    config_view = d_(Callable(default=default_device_config_view_factory))

    #: Default settings to contribute to the config when selected
    default_config = d_(Dict())

    def get_device_config(self):
        """ Pull the default device config params from the default_config 
        """
        cfg = self.default_config.copy()
        for k in ('connection', 'protocol', 'job'):
            cfg.pop(k, None)
        return cfg

    def get_job_config(self):
        """ Pull the default device config params from the default_config 
        """
        return self.default_config.get('job', {}).copy()

    def get_connection_config(self, id):
        """ Pull the connection config params from the default_config 
        for the given transport id.
        """
        cfg = self.default_config.get('connection', {}).copy()
        return cfg.get(id, {})

    def get_protocol_config(self, id):
        """ Pull the protocol config from the default_config """
        cfg = self.default_config.get('protocol', {}).copy()
        return cfg.get(id, {})


class DeviceProtocol(Declarative):
    #: Id of the protocol
    id = d_(Unicode())

    #: Name of the protocol (optional)
    name = d_(Unicode())

    #: Factory to construct the protocol. It receives the DeviceDriver
    #: as the first argument and the DeviceProtocol declaration as the second
    factory = d_(Callable())

    #: Config view for editing the config of this device
    config_view = d_(Callable(default=default_config_view_factory))


class DeviceTransport(Declarative):
    #: Id of the transport
    id = d_(Unicode())

    #: Name of the transport (optional)
    name = d_(Unicode())

    #: Factory to construct the transport. It receives the DeviceDriver
    #: as the first argument and the DeviceProtocol declaration as the second
    factory = d_(Callable())

    #: Config view for editing the config of this device
    config_view = d_(Callable(default=default_config_view_factory))
