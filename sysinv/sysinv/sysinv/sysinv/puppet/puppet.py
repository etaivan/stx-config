#
# Copyright (c) 2017-2018 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

""" System Inventory Puppet Configuration Operator."""

from __future__ import absolute_import

import eventlet
import os
import tempfile
import yaml

from sysinv.common import constants
from sysinv.common import exception
from sysinv.openstack.common import log as logging
from sysinv.openstack.common.gettextutils import _

from . import aodh
from . import ceilometer
from . import ceph
from . import cinder
from . import common
from . import dcmanager
from . import dcorch
from . import glance
from . import heat
from . import horizon
from . import interface
from . import inventory
from . import ironic
from . import keystone
from . import ldap
from . import magnum
from . import mtce
from . import murano
from . import networking
from . import neutron
from . import nfv
from . import nova
from . import panko
from . import patching
from . import platform
from . import storage
from . import device
from . import service_parameter


LOG = logging.getLogger(__name__)


def puppet_context(func):
    """Decorate to initialize the local threading context"""
    def _wrapper(self, *args, **kwargs):
        thread_context = eventlet.greenthread.getcurrent()
        setattr(thread_context, '_puppet_context', dict())
        func(self, *args, **kwargs)
    return _wrapper


class PuppetOperator(object):
    """Class to encapsulate puppet operations for System Inventory"""

    def __init__(self, dbapi=None, path=None):
        if path is None:
            path = common.PUPPET_HIERADATA_PATH

        self.dbapi = dbapi
        self.path = path

        self.aodh = aodh.AodhPuppet(self)
        self.ceilometer = ceilometer.CeilometerPuppet(self)
        self.ceph = ceph.CephPuppet(self)
        self.cinder = cinder.CinderPuppet(self)
        self.dcmanager = dcmanager.DCManagerPuppet(self)
        self.dcorch = dcorch.DCOrchPuppet(self)
        self.glance = glance.GlancePuppet(self)
        self.heat = heat.HeatPuppet(self)
        self.horizon = horizon.HorizonPuppet(self)
        self.interface = interface.InterfacePuppet(self)
        self.keystone = keystone.KeystonePuppet(self)
        self.ldap = ldap.LdapPuppet(self)
        self.magnum = magnum.MagnumPuppet(self)
        self.mtce = mtce.MtcePuppet(self)
        self.murano = murano.MuranoPuppet(self)
        self.networking = networking.NetworkingPuppet(self)
        self.neutron = neutron.NeutronPuppet(self)
        self.nfv = nfv.NfvPuppet(self)
        self.nova = nova.NovaPuppet(self)
        self.panko = panko.PankoPuppet(self)
        self.patching = patching.PatchingPuppet(self)
        self.platform = platform.PlatformPuppet(self)
        self.storage = storage.StoragePuppet(self)
        self.sysinv = inventory.SystemInventoryPuppet(self)
        self.device = device.DevicePuppet(self)
        self.ironic = ironic.IronicPuppet(self)
        self.service_parameter = service_parameter.ServiceParamPuppet(self)

    @property
    def context(self):
        thread_context = eventlet.greenthread.getcurrent()
        return getattr(thread_context, '_puppet_context')

    @puppet_context
    def create_static_config(self):
        """
        Create the initial static configuration that sets up one-time
        configuration items that are not generated by standard system
        configuration. This is invoked once during initial bootstrap to
        create the required parameters.
        """

        # use the temporary keyring storage during bootstrap phase
        os.environ["XDG_DATA_HOME"] = "/tmp"

        try:
            config = {}
            config.update(self.platform.get_static_config())
            config.update(self.patching.get_static_config())
            config.update(self.mtce.get_static_config())
            config.update(self.keystone.get_static_config())
            config.update(self.sysinv.get_static_config())
            config.update(self.ceph.get_static_config())
            config.update(self.nova.get_static_config())
            config.update(self.neutron.get_static_config())
            config.update(self.glance.get_static_config())
            config.update(self.cinder.get_static_config())
            config.update(self.ceilometer.get_static_config())
            config.update(self.aodh.get_static_config())
            config.update(self.heat.get_static_config())
            config.update(self.magnum.get_static_config())
            config.update(self.murano.get_static_config())
            config.update(self.ironic.get_static_config())
            config.update(self.panko.get_static_config())
            config.update(self.ldap.get_static_config())
            config.update(self.dcmanager.get_static_config())
            config.update(self.dcorch.get_static_config())

            filename = 'static.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create static config")
            raise

    @puppet_context
    def create_secure_config(self):
        """
        Create the secure config, for storing passwords.
        This is invoked once during initial bootstrap to
        create the required parameters.
        """

        # use the temporary keyring storage during bootstrap phase
        os.environ["XDG_DATA_HOME"] = "/tmp"

        try:
            config = {}
            config.update(self.platform.get_secure_static_config())
            config.update(self.ldap.get_secure_static_config())
            config.update(self.patching.get_secure_static_config())
            config.update(self.mtce.get_secure_static_config())
            config.update(self.keystone.get_secure_static_config())
            config.update(self.sysinv.get_secure_static_config())
            config.update(self.nfv.get_secure_static_config())
            config.update(self.ceph.get_secure_static_config())
            config.update(self.nova.get_secure_static_config())
            config.update(self.neutron.get_secure_static_config())
            config.update(self.horizon.get_secure_static_config())
            config.update(self.glance.get_secure_static_config())
            config.update(self.cinder.get_secure_static_config())
            config.update(self.ceilometer.get_secure_static_config())
            config.update(self.aodh.get_secure_static_config())
            config.update(self.heat.get_secure_static_config())
            config.update(self.magnum.get_secure_static_config())
            config.update(self.murano.get_secure_static_config())
            config.update(self.ironic.get_secure_static_config())
            config.update(self.panko.get_secure_static_config())
            config.update(self.dcmanager.get_secure_static_config())
            config.update(self.dcorch.get_secure_static_config())

            filename = 'secure_static.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create secure config")
            raise

    @puppet_context
    def update_system_config(self):
        """Update the configuration for the system"""
        try:
            # NOTE: order is important due to cached context data
            config = {}
            config.update(self.platform.get_system_config())
            config.update(self.networking.get_system_config())
            config.update(self.patching.get_system_config())
            config.update(self.mtce.get_system_config())
            config.update(self.keystone.get_system_config())
            config.update(self.sysinv.get_system_config())
            config.update(self.nfv.get_system_config())
            config.update(self.ceph.get_system_config())
            config.update(self.nova.get_system_config())
            config.update(self.neutron.get_system_config())
            config.update(self.horizon.get_system_config())
            config.update(self.glance.get_system_config())
            config.update(self.cinder.get_system_config())
            config.update(self.ceilometer.get_system_config())
            config.update(self.aodh.get_system_config())
            config.update(self.heat.get_system_config())
            config.update(self.magnum.get_system_config())
            config.update(self.murano.get_system_config())
            config.update(self.storage.get_system_config())
            config.update(self.ironic.get_system_config())
            config.update(self.panko.get_system_config())
            config.update(self.dcmanager.get_system_config())
            config.update(self.dcorch.get_system_config())
            config.update(self.service_parameter.get_system_config())

            filename = 'system.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create system config")
            raise

    @puppet_context
    def update_secure_system_config(self):
        """Update the secure configuration for the system"""
        try:
            # NOTE: order is important due to cached context data
            config = {}
            config.update(self.platform.get_secure_system_config())
            config.update(self.keystone.get_secure_system_config())
            config.update(self.sysinv.get_secure_system_config())
            config.update(self.nova.get_secure_system_config())
            config.update(self.neutron.get_secure_system_config())
            config.update(self.glance.get_secure_system_config())
            config.update(self.cinder.get_secure_system_config())
            config.update(self.ceilometer.get_secure_system_config())
            config.update(self.aodh.get_secure_system_config())
            config.update(self.heat.get_secure_system_config())
            config.update(self.magnum.get_secure_system_config())
            config.update(self.murano.get_secure_system_config())
            config.update(self.ironic.get_secure_system_config())
            config.update(self.panko.get_secure_system_config())
            config.update(self.dcmanager.get_secure_system_config())
            config.update(self.dcorch.get_secure_system_config())

            filename = 'secure_system.yaml'
            self._write_config(filename, config)
        except Exception:
            LOG.exception("failed to create secure_system config")
            raise

    def update_host_config(self, host, config_uuid=None):
        """Update the host hiera configuration files for the supplied host"""

        if host.personality == constants.CONTROLLER:
            self.update_controller_config(host, config_uuid)
        elif host.personality == constants.COMPUTE:
            self.update_compute_config(host, config_uuid)
        elif host.personality == constants.STORAGE:
            self.update_storage_config(host, config_uuid)
        else:
            raise exception.SysinvException(_(
                "Invalid method call: unsupported personality: %s") %
                    host.personality)

    @puppet_context
    def update_controller_config(self, host, config_uuid=None):
        """Update the configuration for a specific controller host"""
        try:
            # NOTE: order is important due to cached context data
            config = {}
            config.update(self.platform.get_host_config(host, config_uuid))
            config.update(self.interface.get_host_config(host))
            config.update(self.networking.get_host_config(host))
            config.update(self.storage.get_host_config(host))
            config.update(self.ldap.get_host_config(host))
            config.update(self.nfv.get_host_config(host))
            config.update(self.ceph.get_host_config(host))
            config.update(self.cinder.get_host_config(host))
            config.update(self.device.get_host_config(host))
            config.update(self.nova.get_host_config(host))
            config.update(self.neutron.get_host_config(host))
            config.update(self.service_parameter.get_host_config(host))

            self._write_host_config(host, config)
        except Exception:
            LOG.exception("failed to create host config: %s" % host.uuid)
            raise

    @puppet_context
    def update_compute_config(self, host, config_uuid=None):
        """Update the configuration for a specific compute host"""
        try:
            # NOTE: order is important due to cached context data
            config = {}
            config.update(self.platform.get_host_config(host, config_uuid))
            config.update(self.interface.get_host_config(host))
            config.update(self.networking.get_host_config(host))
            config.update(self.storage.get_host_config(host))
            config.update(self.ceph.get_host_config(host))
            config.update(self.device.get_host_config(host))
            config.update(self.nova.get_host_config(host))
            config.update(self.neutron.get_host_config(host))
            config.update(self.service_parameter.get_host_config(host))
            config.update(self.ldap.get_host_config(host))

            self._write_host_config(host, config)
        except Exception:
            LOG.exception("failed to create host config: %s" % host.uuid)
            raise

    @puppet_context
    def update_storage_config(self, host, config_uuid=None):
        """Update the configuration for a specific storage host"""
        try:
            # NOTE: order is important due to cached context data
            config = {}
            config.update(self.platform.get_host_config(host, config_uuid))
            config.update(self.interface.get_host_config(host))
            config.update(self.networking.get_host_config(host))
            config.update(self.storage.get_host_config(host))
            config.update(self.ceph.get_host_config(host))
            config.update(self.service_parameter.get_host_config(host))
            config.update(self.ldap.get_host_config(host))

            self._write_host_config(host, config)
        except Exception:
            LOG.exception("failed to create host config: %s" % host.uuid)
            raise

    def remove_host_config(self, host):
        """Remove the configuration for the supplied host"""
        try:
            filename = "%s.yaml" % host.mgmt_ip
            self._remove_config(filename)
        except Exception:
            LOG.exception("failed to remove host config: %s" % host.uuid)

    def _write_host_config(self, host, config):
        """Update the configuration for a specific host"""
        filename = "%s.yaml" % host.mgmt_ip
        self._write_config(filename, config)

    def _write_config(self, filename, config):
        filepath = os.path.join(self.path, filename)
        try:
            fd, tmppath = tempfile.mkstemp(dir=self.path, prefix=filename,
                                           text=True)
            with open(tmppath, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            os.close(fd)
            os.rename(tmppath, filepath)
        except Exception:
            LOG.exception("failed to write config file: %s" % filepath)
            raise

    def _remove_config(self, filename):
        filepath = os.path.join(self.path, filename)
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
        except Exception:
            LOG.exception("failed to delete config file: %s" % filepath)
            raise
