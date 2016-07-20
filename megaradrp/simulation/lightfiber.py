#
# Copyright 2016 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# Megara DRP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Megara DRP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Megara DRP.  If not, see <http://www.gnu.org/licenses/>.
#

import math

from astropy import units as u

from .efficiency import Efficiency


class LightFiber(object):
    def __init__(self, name, fibid, transmission=None, inactive=False):
        self.name = name
        self.fibid = fibid
        # Geometry of the fibers
        self.size = 0.31 * u.arcsec
        self.area = math.sqrt(3) * self.size ** 2 / 2.0
        self.fwhm = 3.6
        self.sigma = self.fwhm / 2.3548
        self.inactive = inactive

        if transmission is None:
            self._transmission = Efficiency()
        else:
            self._transmission = transmission

    def transmission(self, wl):
        return self._transmission.response(wl)

    def config_info(self):
        return {'name': self.name,
                'fibid': self.fibid,
                'inactive': self.inactive
                }
