#
# Copyright 2015 Universidad Complutense de Madrid
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

"""Tests for the bpm mode recipe module."""

from numina.core import DataFrame, ObservationResult
import astropy.io.fits as fits
from numina.core.requirements import ObservationResultRequirement


from megaradrp.core.recipe import MegaraBaseRecipe
from megaradrp.requirements import MasterBiasRequirement, MasterBPMRequirement

from numina.array import combine

from megaradrp.processing.combine import basic_processing_with_combination

from megaradrp.recipes.calibration.tests.test_bpm_common import crear_archivos
from megaradrp.instrument.loader import build_instrument_config, Loader


class TestRecipe(MegaraBaseRecipe):
    obresult = ObservationResultRequirement()
    master_bias = MasterBiasRequirement()
    master_bpm = MasterBPMRequirement()

    def __init__(self, directorio):
        self.directorio = directorio
        super(TestRecipe, self).__init__()

    def run(self, rinput):
        import copy

        N = len(rinput.obresult.frames)
        obresult1 = copy.copy(rinput.obresult)
        obresult1.frames = rinput.obresult.frames[:N]

        flow1 = self.init_filters(rinput, rinput.obresult.configuration)
        img = basic_processing_with_combination(rinput, flow1, method=combine.median)
        hdr = img[0].header
        self.set_base_headers(hdr)

        reduced1 = img

        fits.writeto(self.directorio + '/reduced_flat.fits', reduced1[0].data,
                     clobber=True)

        fits.writeto(self.directorio + '/reduced_flat_bpm.fits',
                     reduced1[0].data, clobber=True)

        return True


def test_bpm_corrector():
    import shutil
    from tempfile import mkdtemp

    directorio = mkdtemp()
    names = crear_archivos(directorio, number=4)

    ob = ObservationResult()
    ob.instrument = 'MEGARA'
    ob.mode = 'bias_image'
    ob.configuration = build_instrument_config('4fd05b24-2ed9-457b-b563-a3c618bb1d4c', loader=Loader())
    ob.frames = [DataFrame(filename=open(nombre).name) for nombre in names]

    recipe = TestRecipe(directorio)
    ri = recipe.create_input(obresult=ob, master_bias=DataFrame(
        filename=open(directorio + '/master_bias_data0.fits').name),
                             master_bpm=DataFrame(filename=open(
                                 directorio + '/master_bpm.fits').name))

    recipe.run(ri)
    shutil.rmtree(directorio)

if __name__ == "__main__":
    test_bpm_corrector()
