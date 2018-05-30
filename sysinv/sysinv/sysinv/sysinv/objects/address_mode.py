#
# Copyright (c) 2015 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

# vim: tabstop=4 shiftwidth=4 softtabstop=4
# coding=utf-8
#

from sysinv.db import api as db_api
from sysinv.objects import base
from sysinv.objects import utils


class AddressMode(base.SysinvObject):
    # VERSION 1.0: Initial version
    VERSION = '1.0'

    dbapi = db_api.get_instance()

    fields = {'id': int,
              'uuid': utils.uuid_or_none,
              'forihostid': utils.int_or_none,
              'interface_uuid': utils.uuid_or_none,
              'ifname': utils.str_or_none,
              'family': utils.int_or_none,
              'mode': utils.str_or_none,
              'pool_uuid': utils.uuid_or_none,
              }

    _foreign_fields = {'interface_uuid': 'interface:uuid',
                       'ifname': 'interface:ifname',
                       'forihostid': 'interface:forihostid',
                       'pool_uuid': 'address_pool:uuid'}

    @base.remotable_classmethod
    def get_by_uuid(cls, context, uuid):
        return cls.dbapi.address_mode_get(uuid)

    def save_changes(self, context, updates):
        self.dbapi.address_mode_update(self.uuid, updates)
