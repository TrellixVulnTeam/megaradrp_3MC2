#
# Copyright 2011-2015 Universidad Complutense de Madrid
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

"""Calibrate the non linearity correciont of MEGARA Detector"""

import logging

from numina.core import RecipeError

from megaradrp.core.recipe import MegaraBaseRecipe


_logger = logging.getLogger('numina.recipes.megara')

class LinearityTestRecipe(MegaraBaseRecipe):

    """Process LINTEST images and create LINEARITY_CORRECTON."""


    def __init__(self):
        super(LinearityTestRecipe, self).__init__(
            version="0.1.0"
        )

    def run(self, rinput):
        raise RecipeError("Recipe not inplemented")
