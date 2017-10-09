#
# Copyright 2016-2017 Universidad Complutense de Madrid
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

"""Data model for MEGARA"""

from __future__ import division

import re
import pkgutil
import enum

import astropy.io.fits as fits
from six import StringIO
from numina.datamodel import DataModel
from numina.core.products import convert_date, convert_qc


class MegaraDataModel(DataModel):
    """Data model of MEGARA images"""

    meta_info_headers = [
        'instrument',
        'object',
        'observation_date',
        'uuid',
        'type',
        'mode',
        'exptime',
        'darktime',
        'insconf',
        'blckuuid',
        'quality_control',
        'vph',
        'insmode'
    ]

    def __init__(self):
        self.all_values = {
            'instrument': 'INSTRUME',
            'object': 'OBJECT',
            'observation_date': ('DATE-OBS', 0, convert_date),
            'uuid': 'uuid',
            'type': 'numtype',
            'mode': 'obsmode',
            'exptime': 'exptime',
            'darktime': 'darktime',
            'insconf': 'insconf',
            'insconf_uuid': 'insconf',
            'blckuuid': 'blckuuid',
            'block_uuid': 'blckuuid',
            'quality_control': ('NUMRQC', 0, convert_qc),
            'vph': ('VPH', 'undefined'),
            'vphpos': ('VPHWHPOS', 'undefined'),
            'insmode': ('INSMODE', 'undefined'),
            'focus': ('FOCUS', 'undefined'),
            'osfilter': ('OSFILTER', 'undefined'),
            'temp': ('SENTEMP4', 0.0),
            'speclamp': ('SPECLMP', 'undefined')
        }

        super(MegaraDataModel, self).__init__('MEGARA', self.all_values)

        # Keys
        self._meta = [
            'exptime',
            'vph',
            'vphpos',
            'insmode',
            'focus',
            'osfilter',
            'uuid',
            'temp',
            'block_uuid',
            'insconf_uuid',
            'speclamp'
        ]

    def get_imgid(self, img):
        hdr = self.get_header(img)
        if 'UUID' in hdr:
            return 'uuid:{}'.format(hdr['UUID'])
        elif 'DATE-OBS' in hdr:
            return 'dateobs:{}'.format(hdr['DATE-OBS'])
        else:
            return super(MegaraDataModel, self).get_imgid(img)

    def get_fiberconf(self, img):
        """Obtain FIBER extension"""
        main_insmode = img[0].header.get('INSMODE', '')
        if 'FIBERS' in img:
            # We have a 'fibers' extension
            # Information os there
            hdr_fiber = img['FIBERS'].header
            return read_fibers_extension(hdr_fiber, insmode=main_insmode)
        else:
            insmode = img[0].header.get('INSMODE')
            if insmode == 'LCB':
                slit_file = 'lcb_default_header.txt'
            elif insmode == 'MOS':
                slit_file = 'mos_default_header.txt'
            else:
                # Read fiber info from headers
                raise ValueError('Invalid INSMODE {}'.format(insmode))

            data = pkgutil.get_data('megaradrp.instrument.configs', slit_file)
            default_hdr = StringIO(data.decode('utf8'))
            hdr_fiber = fits.header.Header.fromfile(default_hdr)
            return read_fibers_extension(hdr_fiber)

    def gather_info_oresult(self, val):
        return [self.gather_info_dframe(f) for f in val.images]

    def gather_info_dframe(self, img):
        with img.open() as hdulist:
            info = self.gather_info_hdu(hdulist)
        return info

    def gather_info_hdu(self, hdulist):
        values = {}
        values['n_ext'] = len(hdulist)
        extnames = [hdu.header.get('extname', '') for hdu in hdulist[1:]]
        values['name_ext'] = ['PRIMARY'] + extnames

        for key in self._meta:
            values[key] = self.extractor.extract(key, hdulist)

        values['imageid'] = self.get_imgid(hdulist)
        return values


class FibersConf(object):
    """Global configuration of the fibers"""
    def __init__(self):
        self.name = ""
        self.conf_id = 1
        self.nbundles = 0
        self.nfibers = 0
        self.bundles = {}
        self.fibers = {}

    def sky_fibers(self, valid_only=False):
        result = []
        for bundle in self.bundles.values():
            if bundle.target_type is TargetType.SKY:
                if valid_only:
                    for fib in bundle.fibers.values():
                        if fib.valid:
                            result.append(fib.fibid)
                else:
                    result.extend(bundle.fibers.keys())
        return result

    def conected_fibers(self, valid_only=False):

        if self.name == 'MOS':
            raise ValueError('not working for MOS')

        result = []
        for bundle in self.bundles.values():
            if bundle.target_type is not TargetType.SKY:
                if valid_only:
                    for fib in bundle.fibers.values():
                        if fib.valid:
                            result.append(fib)
                else:
                    result.extend(bundle.fibers.values())
        return result

    def inactive_fibers(self):
        result = []
        for fiber in self.fibers.values():
            if fiber.inactive:
                result.append(fiber.fibid)
        return result

    def active_fibers(self):
        result = []
        for fiber in self.fibers.values():
            if not fiber.inactive:
                result.append(fiber.fibid)
        return result

    def valid_fibers(self):
        result = []
        for fiber in self.fibers.values():
            if fiber.valid:
                result.append(fiber.fibid)
        return result

    def invalid_fibers(self):
        result = []
        for fiber in self.fibers.values():
            if not fiber.valid:
                result.append(fiber.fibid)
        return result

    def spectral_coverage(self):
        lowc = []
        upperc = []
        for fibid, r in self.fibers.items():
            if r.w1:
                lowc.append(r.w1)
            if r.w2:
                upperc.append(r.w2)

        mn = max(lowc)
        nn = min(lowc)

        mx = min(upperc)
        nx = max(upperc)
        return (mn, mx), (nn, nx)


class TargetType(enum.Enum):
    SOURCE = 1
    UNKNOWN = 2
    UNASSIGNED = 3
    SKY = 4
    REFERENCE = 5
    # aliases for the other fields
    STAR = 5
    BLANK = 4


class BundleConf(object):
    """Description of a bundle"""
    def __init__(self):
        self.id = 0
        self.target_type = TargetType.UNASSIGNED
        self.target_priority = 0
        self.target_name = 'unknown'
        self.x_fix = 0
        self.y_fix = 0
        self.pa_fix = 0
        self.x = 0
        self.y = 0
        self.pa = 0


class FiberConf(object):
    """Description of the fiber"""
    def __init__(self):
        self.fibid = 0
        self.inactive = False
        self.valid = True


def read_fibers_extension(hdr, insmode='LCB'):
    """Read the FIBERS extension

    Parameters
    ==========
    hdr:
       FITS header
    insmode: str
        default INSMODE

    Returns
    =======
    FibersConf


    """
    conf = FibersConf()
    defaults = {}
    defaults['LCB'] = (89, 623)
    defaults['MOS'] = (92, 644)

    if insmode not in ['LCB', 'MOS']:
        raise ValueError('insmode %s not in [LCB, MOS]' % insmode)

    conf.name = hdr.get('INSMODE', insmode)
    conf.conf_id = hdr.get('CONFID', 1)
    conf.nbundles = hdr.get('NBUNDLES', defaults[insmode][0])
    conf.nfibers = hdr.get('NFIBERS', defaults[insmode][1])
    # Read bundles

    bun_ids = []
    fib_ids = []
    bundles = conf.bundles
    fibers = conf.fibers

    # loop over everything, count BUN%03d_P and FIB%03d_B
    pattern1 = re.compile(r"BUN(\d+)_P")
    pattern2 = re.compile(r"FIB(\d+)_B")
    for key in hdr:
        bun_re = pattern1.match(key)
        fib_re = pattern2.match(key)
        if bun_re:
            bun_idx = int(bun_re.group(1))
            bun_ids.append(bun_idx)
        elif fib_re:
            fib_idx = int(fib_re.group(1))
            fib_ids.append(fib_idx)

    for i in bun_ids:
        bb = BundleConf()
        bb.id = i
        bb.target_priority = hdr["BUN%03d_P" % i]
        bb.target_name = hdr["BUN%03d_I" % i]
        bb.target_type = TargetType[hdr["BUN%03d_T" % i]]
        bb.fibers = {}
        bundles[i] = bb

    for fibid in fib_ids:
        ff = FiberConf()
        ff.fibid = fibid

        # Coordinates
        ff.d = hdr["FIB%03d_D" % fibid]
        ff.r = hdr["FIB%03d_R" % fibid]
        ff.o = 0 #hdr["FIB%03d_O" % fibid]
        # Active
        ff.inactive = not hdr["FIB%03d_A" % fibid]

        # Coordinates XY
        ff.x = hdr["FIB%03d_X" % fibid]
        ff.y = hdr["FIB%03d_Y" % fibid]

        ff.b = hdr["FIB%03d_B" % fibid]
        ff.name = hdr.get("FIB%03d_N" % fibid, 'unknown')

        ff.w1 = hdr.get("FIB%03dW1" % fibid, None)
        ff.w2 = hdr.get("FIB%03dW2" % fibid, None)

        # Validity
        if ff.inactive:
            ff.valid = False
        else:
            ff.valid = hdr.get("FIB%03d_V" % fibid, True)

        bundles[ff.b].fibers[ff.fibid] = ff
        fibers[ff.fibid] = ff

    return conf
