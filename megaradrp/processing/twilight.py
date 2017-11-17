#
# Copyright 2011-2017 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import logging
import datetime

from astropy.io import fits
import numpy

from numina.flow.processing import Corrector


_logger = logging.getLogger('numina.processing')


class TwilightCorrector(Corrector):

    """A Node that corrects from twilight flat."""

    def __init__(self, twilight, datamodel=None, calibid='calibid-unknown', dtype='float32'):

        super(TwilightCorrector, self).__init__(datamodel=datamodel,
                                                calibid=calibid,
                                                dtype=dtype)

        if isinstance(twilight, fits.HDUList):
            self.corr = twilight[0].data
        elif isinstance(twilight, fits.ImageHDU):
            self.corr = twilight.data
        else:
            self.corr = numpy.asarray(twilight)

        self.corrmean = self.corr.mean()
        self.flattag = 'twilight'

    def run(self, img):
        imgid = self.get_imgid(img)
        cap = self.flattag.capitalize()
        _logger.debug('correct from %s in image %s', cap, imgid)

        # Avoid nan values when divide
        my_mask = self.corr == 0.0
        self.corr[my_mask] = 1.0

        img[0].data /= self.corr
        hdr = img['primary'].header

        self.header_update(hdr, imgid)

        return img

    def header_update(self, hdr, imgid):
        hdr['NUM-TWIF'] = self.calibid
        cap = self.flattag.capitalize()
        now = datetime.datetime.utcnow().isoformat()
        hdr['history'] = '{} flat correction {}'.format(cap, imgid)
        hdr['history'] = '{} flat correction time {}'.format(cap, now)
