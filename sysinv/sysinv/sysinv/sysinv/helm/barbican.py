#
# Copyright (c) 2018 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import constants
from sysinv.common import exception
from sysinv.helm import common
from sysinv.helm import openstack


class BarbicanHelm(openstack.OpenstackBaseHelm):
    """Class to encapsulate helm operations for the barbican chart"""

    CHART = constants.HELM_CHART_BARBICAN

    SERVICE_NAME = constants.HELM_CHART_BARBICAN

    def get_overrides(self, namespace=None):
        overrides = {
            common.HELM_NS_OPENSTACK: {
                'images': self._get_images_overrides(),
                'pod': {
                    'replicas': {
                        'api': self._num_controllers()
                    }
                }
            }
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides

    def _get_images_overrides(self):
        heat_image = self._operator.chart_operators[
            constants.HELM_CHART_HEAT].docker_image
        return {
            'tags': {
                'barbican_api': self.docker_image,
                'barbican_db_sync': self.docker_image,
                'bootstrap': heat_image,
                'db_drop': heat_image,
                'db_init': heat_image,
                'ks_endpoints': heat_image,
                'ks_service': heat_image,
                'ks_user': heat_image,
                'scripted_test': heat_image,
            }
        }
