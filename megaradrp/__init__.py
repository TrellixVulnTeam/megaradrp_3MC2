#
# Copyright 2011-2017 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

"""The MEGARA Data Reduction Pipeline."""

import logging


__version__ = '0.6.dev4'


# Top level NullHandler
logging.getLogger("megaradrp").addHandler(logging.NullHandler())
