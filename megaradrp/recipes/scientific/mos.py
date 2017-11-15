#
# Copyright 2011-2017 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

"""MOS Image Recipe for Megara"""

import numpy
from scipy.interpolate import interp1d
import astropy.wcs

from numina.core import Product

from megaradrp.processing.fluxcalib import FluxCalibration
from megaradrp.utils import add_collapsed_mos_extension
from megaradrp.types import ProcessedRSS, ProcessedFrame
from .base import ImageRecipe


class MOSImageRecipe(ImageRecipe):
    """Process MOS images.

    This recipe processes a set of images
    obtained in **MOS image** mode and returns
    the sky subtracted RSS.

    See Also
    --------
    megaradrp.recipes.scientific.lcb.LCBImageRecipe

    Notes
    -----
    Images provided by `obresult` are trimmed and corrected
    from overscan, bad pixel mask (if `master_bpm` is not None),
    bias, dark current (if `master_dark` is not None) and
    slit-flat (if `master_slitflat` is not None).

    Images thus corrected are the stacked using the median.
    The result of the combination is saved as an intermediate result, named
    'reduced_image.fits'. This combined image is also returned in the field
    `reduced_image` of the recipe result.

    The apertures in the 2D image are extracted, using the information in
    `master_traces` and resampled according to the wavelength calibration in
    `master_wlcalib`. Then is divided by the `master_fiberflat`.
    The resulting RSS is saved as an intermediate
    result named 'reduced_rss.fits'. This RSS is also returned in the field
    `reduced_rss` of the recipe result.

    The sky is subtracted by combining the the fibers marked as `SKY`
    in the fibers configuration. The RSS with sky subtracted is returned ini the
    field `final_rss` of the recipe result.

    """

    reduced_image = Product(ProcessedFrame)
    final_rss = Product(ProcessedRSS)
    reduced_rss = Product(ProcessedRSS)
    sky_rss = Product(ProcessedRSS)

    def run(self, rinput):
        self.logger.info('starting MOS reduction')

        reduced2d, rss_data = super(MOSImageRecipe, self).base_run(rinput)

        self.logger.info('start sky subtraction')
        final, origin, sky = self.run_sky_subtraction(rss_data)
        self.logger.info('end sky subtraction')
        # Flux calibration
        if rinput.master_sensitivity is not None:
            self.logger.info('start flux calibration')
            node = FluxCalibration(rinput.master_sensitivity.open(), self.datamodel)
            final = node(final)
            origin = node(origin)
            self.logger.info('end flux calibration')
        else:
            self.logger.info('no flux calibration')

        # Extinction calibration
        if rinput.reference_extinction is not None:
            self.logger.info('start extinction correction')
            extinc_interp = interp1d(rinput.reference_extinction[:, 0],
                                     rinput.reference_extinction[:, 1])

            wlcalib = astropy.wcs.WCS(final[0].header)
            pixrange = numpy.arange(final[0].data.shape[1])
            yrange = pixrange * 0
            calcwl = numpy.array([pixrange, yrange]).T
            wavelen = wlcalib.all_pix2world(calcwl, 0.0)[:, 0]
            airmass = final[0].header['AIRMASS']

            extinc_corr = numpy.power(10.0, 0.4 * extinc_interp(wavelen) * airmass)

            final[0].data *= extinc_corr
            origin[0].data *= extinc_corr
            self.logger.info('end extinction correction')
        else:
            self.logger.info('no extinction correction')

        self.logger.info('add collapsed extension')
        final = add_collapsed_mos_extension(final)
        origin = add_collapsed_mos_extension(origin)

        self.logger.info('end MOS reduction')
        return self.create_result(
            reduced_image=reduced2d,
            final_rss=final,
            reduced_rss=origin,
            sky_rss=sky
        )



