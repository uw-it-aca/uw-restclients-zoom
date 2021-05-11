# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from commonconf import override_settings


fdao_zoom_override = override_settings(RESTCLIENTS_ZOOM_DAO_CLASS='Mock')
