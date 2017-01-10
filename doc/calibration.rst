Calibration Modes
=================

The calibration modes are those operating modes that are intended (1) to either
analyze the state of the instrument or (2) to be used for processing scientific
observations from raw to science-grade data.

With respect to the determination of the status of the instrument the following
calibration images should be acquired:

* Bias

* Dark

* Fiber-flat

* Arc

Regarding the processing of scientific data this basically implies obtaining
calibration images in number and quality required to remove the instrumental
signatures so to obtain a science-grade image. These images, which are taken as
part of routine scientific operations, include:

* Bias

* Dark

* Slit-flat

* Fiber-flat

* Twilight fiber-flat

* Arc

* Standard star

Except for the slit-flat, that might be taken only occasionally, the rest of
this latter set of observing modes will be taken routinely as part of either
daytime or nighttime operations. We will refer to these as
"Daily CalibrationModes". Besides these modes we have identified a series of
calibration modes (named "System Calibration Modes") that are also necessary
for processing MEGARA observations but that are only produced occasionally as
part of long-term calibrations of the instrument to be carried out by the
observatory staff.

Thus, the "System Calibration Modes" will be:

* Bad-pixels mask

* Linearity Test

* Slit-flat. Whether the slit-flat should be considered as a "Daily Calibration" or "System Calibration" mode is TBD and will depend on the stability of the pixel-to-pixel efficiency of the MEGARA CCD.

In this latter case, the difference between a "System Calibration Mode" and the
corresponding "Auxiliary Mode" described in Section 3 depends on the frequency
the observing mode has to be executed. Auxiliary modes are typically run once
every observing run (e.g. the fine-acquisition ones) or, in the best case,
after a long period of inactivity. System Calibration modes, on the other hand,
are expected to be run only after major changes in the telescope or the
instrument or if a degradation of any of the subsystems of the instrument is
suspected.

The need for obtaining all these sets of images drives the requirements and
characteristics of the Calibration modes described below as defined by the
MEGARA team.


Arc
---

:Mode: Arc
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.arc.ArcCalibrationRecipe`

This mode sequence includes the required actions to translate the geometrical
position of each point in the detector into physical units of wavelength. The
calibration is performed by means of using reference calibration lamps
(arc lamps) that should be part of the Instrument Calibration Module (ICM) at
F-C. Note that the optical distortions in the spectrograph will lead to
different wavelength calibrations from each individual fiber, therefore the
entire focal plane should be illuminated by the corresponding arc lamp of
choice. Given the relatively high spectral resolution and broad wavelength
coverage of MEGARA we anticipate that more than one arc lamp will be needed at
the ICM. The lamps at ICM have to deliver enough bright spectral lines for
calibrating the whole range of MEGARA spectral resolutions and wavelength
ranges (for HR modes only two VPHs shall be provided by MEGARA but more
gratings could come funded by GTC users). MEGARA has provided a whole review of
the possible illumination systems in the document TEC/MEG/151, but the
responsibility of the development of the ICM module is on the GTC side.

Requirements
++++++++++++
The entire focal plane should be illuminated with light from the ICM arc lamp
with the required  input focal ratio. This mode requires having the ICM turned
on, one of the arc lamps at the ICM also turned on, the focal-plane cover
configured (at least one of the sides should be open), the instrument shutter
open, to move the pseudo-slit to that of the instrument mode of choice, to
configure the VPH wheel mechanism in order to select the grating to be used, to
move the focusing mechanism to the position pre-defined for the specific VPH of
choice and to expose a certain time and to readout the detector a series of
exposures, being this series the arc image set.

+--------------------------+---------------+------------+-------------------------------+
| Name                     | Type          | Default    | Meaning                       |
+==========================+===============+============+===============================+
| ``'obresult'``           | ObservationResult |        |      Observation Result       |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_dark'``        | MasterDark    | NA         |      Master Dark frame        |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_bias'``        | MasterBias    | NA         |      Master Bias frame        |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_bpm'``         | masterBPM     | NA         |      Master BPM frame         |
+--------------------------+---------------+------------+-------------------------------+
| ``'tracemap'``           | TraceMap      | NA         |      TraceMap                 |
+--------------------------+---------------+------------+-------------------------------+
| ``'lines_catalog'``      | LinesCatalog  | NA         |      Lines Catalog            |
+--------------------------+---------------+------------+-------------------------------+
| ``'polynomial_degree'``  | integer       | 3          |      Polynomial Degree        |
+--------------------------+---------------+------------+-------------------------------+

Procedure
+++++++++
The "User" processes an observing block obtained in the observing mode Arc.
This mode includes the required actions to translate the geometrical position
of each point in the detector into physical units of wavelength. The wavelength
calibration generated is used in other stages of the data processing.

Products
++++++++

Arc image sets are to be obtained both as part of the activities related to the
verification of the instrument status and for processing data for scientific
exploitation and are part of the "Daily Calibration Modes".

=====================    ===================================================================
 Name                     Type
=====================    ===================================================================
``'arc_image'``          :class:`~numina.core.DataFrameType`
``'arc_rss'``            :class:`~numina.core.DataFrameType`
``'master_wlcalib'``     :class:`~megaradrp.products.wavecalibration.WavelengthCalibration`
``'fwhm_image'``         :class:`~numina.core.DataFrameType`
=====================    ===================================================================

A data structure containing information about wavelength calibrations
(the format is TBD), a QA flag, a text log file of the processing and a
structured text file containing information about the processing.


Bad-pixels mask
---------------

:Mode: Bad-pixels mask
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.bpm.BadPixelsMaskRecipe`

Although science-grade CCD detectors show very few bad pixels / bad columns
there will be a number of pixels (among the ~17 Million pixels in the MEGARA
CCD) whose response could not be corrected by means of using calibration images
such as dark frames or flat-field images. These pixels, commonly called either
dead or hot pixels, should be identified and masked so their expected signal
could be derived using dithered images or, alternatively, locally interpolated.
While a bad-pixels mask will be generated as part of the AIV activities, an
increase in the number of such bad pixels with time is expected. Therefore, we
here define an observing mode that the observatory staff could use to generate
an updated version of the bad-pixels masks should the number of bad pixels
increase significantly.

In the case of fiber-fed spectrographs the fiber flats (either lamp or twilight
flats) are not optimal for generating bad-pixels masks as these leave many
regions in the CCD not exposed to light. The whole CCD should be illuminated at
different intensity levels in order to clearly identify both dead and hot
pixels.

Requirements
++++++++++++

In the case of MEGARA we will offset the pseudo-slit from its optical focus
position to ensure that the gaps between fibers are also illuminated when a
continuum (halogen) lamp at the ICM is used. The NSC zemax model of the
spectrograph indicates that by offsetting 3mm the pseudo-slit we would already
obtain a homogenous illumination of the CCD. A series of images with different
count levels would be obtained.

This mode requires having the ICM halogen lamp on, the instrument shutter open,
to move the pseudo-slit to the open position, to configure the VPH wheel
mechanism in order to select the grating to be used, to move the focusing
mechanism to the position pre-defined for the specific VPH of choice but offset
by 3mm and to expose a certain time and to readout the detector a series of
exposures, being this series the slit-flat image set. Note that only one
Bad-pixels mask will be used for all spectral setups. The specific choice for
the VPH will depend on the actual color of the ICM halogen lamp and on the
actual response of the VPHs. In principle, we should choose the VPH at the peak
of the lamp spectral energy distribution but we should also consider the fact
that the VPH should have the flattest spectral response possible. We call this
specific VPH the "BPM VPH". LR-R and LR-I are currently the best candidates for
finally being the BPM VPH.

Procedure
+++++++++

The "User" processes an observing block obtained in the observing mode
Bad-pixels mask. This mode includes the required actions to obtain a bad-pixel
mask. The master bad pixel mask generated is used in other stages of the data
processing.

Products
++++++++
This Bad-pixels mask observing mode will be used only sporadically as it is
considered part of the "System Calibration Modes".

+-------------------+---------------------------------------------------------+
| Name              | Type                                                    |
+===================+=========================================================+
| ``'master_bpm'``  | :class:`~megaradrp.types.MasterBPM`                     |
+-------------------+---------------------------------------------------------+

A bidimensional mask of bad pixels, a QA flag, a text log file of the
processing and a structured text file with information about the processing.


Bias
----

:Mode: Bias
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.bias.BiasRecipe`

Before the Analog-to-Digital conversion is performed a pedestal (electronic)
level is added to all images obtained with the MEGARA CCD. This is a standard
procedure in CCD imaging and spectroscopy applications for Astronomy and is
intended to minimize the ADC errors produced when very low analog values are
converted to DUs.

Requirements
++++++++++++
The sequence for this observing mode should include the actions to calibrate
the pedestal level of the detectors and associated control electronics by
taking images with null integration time. This mode requires having the shutter
closed and to readout the detector in a series of exposures with null
integration time, being this series the bias image set.


========================== ==================================== ============ ===============================
 Name                       Type                                 Default      Meaning
========================== ==================================== ============ ===============================
  ``'master_bpm'``         :class:`~megaradrp.types.MasterBPM`   NA            Master BPM frame
========================== ==================================== ============ ===============================


Procedure
+++++++++
The frames in the observed block are stacked together using the median of them
as the final result. The variance of the result frame is computed using two
different methods. The first method computes the variance across the pixels in
the different frames stacked. The second method computes the variance in each
channel in the result frame.

Products
++++++++

Bias image sets are to be obtained both as part of the activities related to
the verification of the instrument status and for processing data for
scientific exploitation.

+-------------------+---------------------------------------------------------+
| Name              | Type                                                    |
+===================+=========================================================+
| ``'master_bias'`` | :class:`~megaradrp.types.MasterBias`                    |
+-------------------+---------------------------------------------------------+


A bidimensional bias image, QA flag, a text log file of the processing and a
structured text file containing information about the processing.

Dark
----

:Mode: Dark
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.dark.DarkRecipe`

The potential wells in CCD detectors spontaneously generate electron-ion pairs
at a rate that is a function of temperature. For very long exposures this
translates into a current that is associated with no light source and that is
commonly referred to as dark current.

Requirements
++++++++++++
While in imaging or low-resolution spectroscopy this is nowadays a negligible
effect thanks to the extremely low dark current levels of state-of-the-art CCDs
(typically < 1 e-/hour) when working at intermediate-to-high spectral
resolutions where the emission per pixel coming from the sky background and the
astronomical source can be very low this is worth considering.


The sequence for this observing mode should include the actions to measure the
variation of the intrinsic signal of the system by taking images under zero
illumination condition and long integration time. This mode requires that the
focal-plane cover is configured (it should be fully closed), the shutter is
closed and to expose a certain time and readout the detector a series of
exposures, being this series the dark image set.

+--------------------------+---------------+------------+-------------------------------+
| Name                     | Type          | Default    | Meaning                       |
+==========================+===============+============+===============================+
| ``'master_bias'``        | Product       | NA         |      Master Bias frame        |
+--------------------------+---------------+------------+-------------------------------+

Procedure
+++++++++
The "User" processes an observing block obtained in the observing mode Dark.
This mode includes the required actions to obtain a master dark frame. The
master dark generated is used in other stages of the data processing.

Products
++++++++
Dark image sets are to be obtained both as part of the activities related to
the verification of the instrument status and for processing data for
scientific exploitation.

+------------------------------+-----------------------------------------------+
| Name                         | Type                                          |
+==============================+===============================================+
| ``'master_dark'``            | :class:`~megaradrp.types.MasterDark`          |
+------------------------------+-----------------------------------------------+

A bidimensional dark image, QA flag, a text log file of the processing and a
structured text file containing information about the processing.


Fiber-flat
----------

:Mode: Fiber-flat
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.flat.FiberFlatRecipe`

In fiber-fed spectrographs such as MEGARA each optical fiber behaves like a
different optical system, and therefore, its optical transmission is different
and individual, with different wavelength dependence. In the Preliminary Design
phase this mode was named "Lamp fiber flat".

Requirements
++++++++++++
This observing mode should include the actions to calibrate the low-frequency
variations in transmission in between fibers and as a function of wavelength in
MEGARA. A fiber-flat should be used to perform this correction and is the
result of illuminating the instrument focal plane with a flat source that can
be either a continuum (halogen) lamp that is part of the GTC Instrument
Calibration Module (ICM) or the twilight sky. The fiber-flat observing mode
discussed here assumes that the focal plane is illuminated with a halogen lamp
located at the ICM. The ICM beam has to have the same focal ratio arriving to
the first MEGARA optical element (the MEGARA telecentricity-correction lens in
this case) simulating as much as possible the real GTC mirrors beam at F-C.

These fiber-flat images are also used to trace the fiber spectra on the
detector for each specific spectral setup. Finally, they are also useful to
verify the status of the optical link between the F-C focal plane and the
platform where the spectrographs are located.

This mode requires having the ICM turned on, one of the halogen lamps at the
ICM also turned on, to configure the focal-plane cover (at least one of the
sides should be open), to have the instrument shutter open, to move the
pseudo-slit to that of the instrument mode of choice, to configure the VPH
wheel mechanism in order to select the grating to be used, to move the
focusing mechanism to the position pre-defined for the specific VPH of choice
and to expose a certain time and to readout the detector a series of exposures,
being this series the fiber-flat image set.

+---------------------------+---------------+------------+-------------------------------+
| Name                      | Type          | Default    | Meaning                       |
+===========================+===============+============+===============================+
| ``'obresult'``            | Product       | NA         |      Observation Result       |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_bias'``         | Product       | NA         |      Master Bias frame        |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_dark'``         | Product       | NA         |      Master Dark frame        |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_bpm'``          | Product       | NA         |      Master BPM frame         |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_slitflat'``     | Product       | NA         |      Master SlitFlat          |
+---------------------------+---------------+------------+-------------------------------+
| ``'wlcalib'``             | Product       | NA         |      WavelengthCalibration    |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_weights'``      | Product       | NA         |      MasterWeights            |
+---------------------------+---------------+------------+-------------------------------+


Procedure
+++++++++
The "User" processes an observing block obtained in the observing mode
Fiber-flat. This mode includes the required actions to obtain a master
fiber-flat field. The master fiber-flat field generated is used in other stages
of the data processing.

Products
++++++++
Fiber-flat image sets are to be obtained both as part of the activities related
to the verification of the instrument status and for processing data for
scientific exploitation.

+------------------------------+--------------------------------------------------+
| Name                         | Type                                             |
+==============================+==================================================+
| ``'fiberflat_frame'``        | :class:`~megaradrp.types.ProcessedFrame`         |
+------------------------------+--------------------------------------------------+
| ``'fiberflat_rss'``          | :class:`~megaradrp.types.ProcessedRSS`           |
+------------------------------+--------------------------------------------------+
| ``'master_fiberflat'``       | :class:`~megaradrp.types.MasterFiberFlat`        |
+------------------------------+--------------------------------------------------+


A RSS master flat field; a QA flag; a text log file of the processing; a structured text file
containing information about the processing; a reduced image and a master flat field image.


Slit-flat
---------

:Mode: Slit-flat
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.slitflat.SlitFlatRecipe`

In the case of fiber-fed spectrographs the correction for the detector
pixel-to-pixel variation of the sensibility is usually carried out using data
from laboratory, where the change in efficiency of the detector at different
wavelengths is computed and then used to correct for this effect for each
specific instrument configuration (VPH setup in the case of MEGARA).

Requeriments
++++++++++++
In the case of MEGARA we will offset the pseudo-slit from its optical focus
position to ensure that the gaps between fibers are also illuminated when a
continuum (halogen) lamp at the ICM is used. The NSC zemax model of the
spectrograph indicates that by offsetting 3mm the pseudo-slit we would already
obtain a homogenous illumination of the CCD. A series of images with different
count levels would be obtained.

The quality of present-day CCDs leads to a rather small impact of these
pixel-to-pixel variations in sensitivity on either the flux calibration and the
cosmetics of the scientific images, especially considering that not one but a
number of pixels along the spatial direction are extracted for each fiber and
at each wavelength. Therefore, we anticipate that this correction might not be
needed or that, as a maximum, a first-order correction based on laboratory data
might suffice. However, before the results of the analysis of the
pixel-to-pixel variations in sensitivity planned using our CCD230 e2V test CCD
are obtained we will consider this observing mode as TBC.

This mode requires having the ICM halogen lamp on, the instrument shutter open,
to move the pseudo-slit to the open position, to configure the VPH wheel
mechanism in order to select the grating to be used, to move the focusing
mechanism to the position pre-defined for the specific VPH of choice but offset
by 3mm and to expose a certain time and to readout the detector a series of
exposures, being this series the slit-flat image set.

+---------------------------+---------------+------------+-------------------------------+
| Name                      | Type          | Default    | Meaning                       |
+===========================+===============+============+===============================+
| ``'obresult'``            | Product       | NA         |      Observation Result       |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_bias'``         | Product       | NA         |      Master Bias frame        |
+---------------------------+---------------+------------+-------------------------------+
| ``'master_dark'``         | Product       | NA         |      Master Dark frame        |
+---------------------------+---------------+------------+-------------------------------+
| ``'window_length_x'``     | Product       | NA         |      Savitzky-Golay length    |
+---------------------------+---------------+------------+-------------------------------+
| ``'window_length_y'``     | Product       | NA         |      Savitzky-Golay length    |
+---------------------------+---------------+------------+-------------------------------+
| ``'polyorder'``           | Product       | NA         |      Savitzky-Golay order     |
+---------------------------+---------------+------------+-------------------------------+
| ``'median_window_length'``| Product       | NA         |      Median window width      |
+---------------------------+---------------+------------+-------------------------------+

Procedure
+++++++++
The "User" processes an observing block obtained in the observing mode
Slit-flat. This mode includes the required actions to obtain a master slit-flat
field. The master slit-flat field generated is used in other stages of the data
processing.

Products
++++++++
Slit-flat image sets are to be obtained both as part of the activities related
to the verification of the instrument status (such as for evaluating the status
of the MEGARA spectrograph) and also for processing data for scientific
exploitation (correction for the pixel-to-pixel variation in sensitivity). The
frequency at which these detector flat images should be acquired is TBC.
Although defined in this document as a mode to be considered part of the
"Daily Calibration Modes" if it is finally used only sporadic it should be
considered as part of the "System Calibration Modes" instead.

+------------------------------+------------------------------------------------+
| Name                         | Type                                           |
+==============================+================================================+
| ``'master_slitflat'``        | :class:`~megaradrp.types.MasterSlitFlat`       |
+------------------------------+------------------------------------------------+

A bidimensional master slit flat field, QA flag, a text log file of the
processing and a structured text file containing information about the
processing.


Trace
-----

:Mode: Trace
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.trace.TraceMapRecipe`

Although for the majority of the observing modes described elsewhere in this
document the MEGARA off-line pipeline will perform its own fiber spectra
extraction from the 2D CCD FITS frame, there are cases where an archival master
"trace map" should be used instead. Note that a different "trace map" should be
available for each pseudo-slit and VPH combination.

Requirements
++++++++++++
This observing mode should include the actions needed to obtain a series of
Fiber-flats that should be combined to generate a master "trace map". This will
be done by means of illuminating the instrument focal plane with a continuum
(halogen) lamp that is part of the GTC Instrument Calibration Module (ICM). The
use of the twilight sky is not recommended in this case as the twilight sky can
present strong absorption lines that could lead to errors in the resulting
trace map at specific wavelengths.

This mode requires having the ICM turned on, one of the halogen lamps at the
ICM also turned on, to configure the focal-plane cover (at least one of the
sides should be open), to have the instrument shutter open, to move the
pseudo-slit to that of the instrument mode of choice, to configure the VPH
wheel mechanism in order to select the grating to be used, to move the focusing
mechanism to the position pre-defined for the specific VPH of choice and to
expose a certain time and to readout the detector a series of exposures, being
this series the trace map image set.

+--------------------------+---------------+------------+-------------------------------+
| Name                     | Type          | Default    | Meaning                       |
+==========================+===============+============+===============================+
| ``'obresult'``           | Product       | NA         |      Observation Result       |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_dark'``        | Product       | NA         |      Master Dark frame        |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_bias'``        | Product       | NA         |      Master Bias frame        |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_bpm'``         | Product       | NA         |      Master BPM frame         |
+--------------------------+---------------+------------+-------------------------------+


Procedure
+++++++++
The "User" processes an observing block obtained in the observing mode Trace.
This mode includes the required actions to obtain a mapping of the trace of the
fibers. The master trace map generated is used in other stages of the data
processing.

Products
++++++++

Trace map image sets are to be obtained both as part of the activities related
to the verification of the instrument status and for processing data for
scientific exploitation. Note, however, that the use of this observing mode for
scientific exploitation should be limited as it could affect to the general
performance of the on-line quick-look software.

+------------------------------+-------------------------------------------------------+
| Name                         | Type                                                  |
+==============================+=======================================================+
| ``'fiberflat_frame'``        | :class:`~megaradrp.types.ProcessedFrame`              |
+------------------------------+-------------------------------------------------------+
| ``'master_traces'``          | :class:`~megaradrp.products.tracemap.TraceMap`        |
+------------------------------+-------------------------------------------------------+


Twilight fiber-flat
-------------------

:Mode: Twilight fiber-flat
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.twilight.TwilightFiberFlatRecipe`

Depending on the final performance of the ICM (provided by the GTC) at F-C the
twilight fiber-flat mode (proposed in this section) might be offered as
optional to the observer or a must should a proper data reduction be required.
In any case this must be always available as an observing mode.

The twilight fiber-flat observing mode should include the actions required to
calibrate the low-frequency sensitivity variation in the spatial direction of
the detector. In principle, the lamp fiber-flat should suffice to correct the
change in sensitivity along both the spatial (fiber-to-fiber relative
transmission) and the spectral direction of the system. The latter only
combined with flux standard-star observations since the spectral shape of the
ICM lamps is not known with enough accuracy.

The twilight fiber-flat is based on the observation of the blank twilight sky.
This can safely assume to homogeneously illuminate the entire MEGARA field of
view (3.5 arcmin x 3.5 arcmin).

Requeriments
++++++++++++
The focal plane should be uniformly illuminated with twilight-sky light. As the
illumination conditions change during twilight, each image set has a different
exposure time. The purpose is to obtain a similar (linear) level of DUs at the
detector (counts) under different illumination conditions.

This mode requires having the focal-plane cover configured (at least one of the
sides should be open), the instrument shutter open, the telescope tracking, to
move the pseudo-slit to that of the instrument mode of choice, to configure the
VPH wheel mechanism in order to select the grating to be used, to move the
focusing mechanism to the position pre-defined for the specific VPH of choice
and to take a series of exposures with different exposure times and to readout
the detector for this series of exposures, being these series the twilight
image set, each with a different exposure time, but with similar level of
counts.

+--------------------------+---------------+------------+-------------------------------+
| Name                     | Type          | Default    | Meaning                       |
+==========================+===============+============+===============================+
| ``'obresult'``           | Product       | NA         |      Observation Result       |
+--------------------------+---------------+------------+-------------------------------+
| ``'master_bias'``        | Product       | NA         |      Master Bias frame        |
+--------------------------+---------------+------------+-------------------------------+

Procedure
+++++++++

The "User" processes an observing block obtained in the observing mode Twilight
Fiber Flat. This mode includes the required actions to obtain a master
illumination flat field. The master illumination flat field generated is used
in other stages of the data processing.

Products
++++++++
Twilight-sky fiber-flat image sets are expected to be obtained as part of the
routine calibration activities performed by the observer since are needed for
processing any scientific-valid data. Therefore, this observing mode should be
considered as part of the "Daily Calibration Modes".

+------------------------------+-------------------------------------------------------+
| Name                         | Type                                                  |
+==============================+=======================================================+
| ``'reduced_frame'``          | :class:`~megaradrp.types.ProcessedFrame`              |
+------------------------------+-------------------------------------------------------+
| ``'reduced_rss'``            | :class:`~megaradrp.types.ProcessedRSS`                |
+------------------------------+-------------------------------------------------------+
| ``'master_twilight_flat'``   | :class:`~megaradrp.products.MasterTwilightFlat`       |
+------------------------------+-------------------------------------------------------+

A RSS master illumination flat field, QA flag, a text log file of the
processing and a structured text file containing information about the
processing.


Linearity tests
---------------

:Mode: Linearity tests
:Usage: Offline
:Recipe class: :class:`~megaradrp.recipes.calibration.LinearityTestRecipe`

Although the linearity of the MEGARA CCD are well characterized at the LICA lab
already, it might be advisable to generate linearity test frames both as part
of the AIV activities and after changes in the MEGARA DAS.

The MEGARA e2V 231-84 CCD offers a full-well capacity of 350,000 ke-. Linearity
tests carried out in instruments already using this type of CCD indicate a
linearity better than ±0.4% at 100 kpix/sec in the range between 140 to 40,000
e- (Reiss et al. 2009 for MUSE@VLT). Given these good linearity results (up to
40,000 e-) and considering the fact that at the spectral resolutions of MEGARA
we will rarely reach those signals from astronomical targets linearity can be
considered negligible. Despite these facts, it is advisable to carry out this
kind of tests both at the lab and at the telescope on the MEGARA CCD itself.

While Linearity tests will be generated as part of the characterization
activities at the lab, the use of the ICM would also allow carrying them out as
part of AIV activities and routinely as part of the "System Calibration Modes".
Therefore, we define here an observing mode that the observatory staff could
use to generate updated Linearity tests should these be needed.

In the case of fiber-fed spectrographs the fiber flats (either lamp or twilight
flats) are not optimal for carrying out Linearity tests as these leave many
regions in the CCD not exposed to light. The whole CCD should be illuminated at
different intensity levels in order for properly carrying out these tests.


Requirements
++++++++++++
In the case of MEGARA we will offset the pseudo-slit from its optical focus
position to ensure that the gaps between fibers are also illuminated when a
continuum (halogen) lamp at the ICM is used. The NSC zemax model of the
spectrograph indicates that by offsetting 3mm the pseudo-slit we would already
obtain a homogenous illumination of the CCD. A series of images with different
count levels would be obtained.

This mode requires having the ICM halogen lamp on, the instrument shutter open,
to move the pseudo-slit to the open position, to configure the VPH wheel
mechanism in order to select the grating to be used, to move the focusing
mechanism to the position pre-defined for the specific VPH of choice and to
expose a certain time and to readout the detector a series of exposures, being
this series the slit-flat image set. Note that the Linearity test will be done
using only one spectral setup as this is independent of the VPH of use. The
specific choice for the VPH will depend on the actual color of the ICM halogen
lamp and on the actual response of the VPHs. In principle, we should choose the
VPH at the peak of the lamp spectral energy distribution but we

+------------------------------+-------------------------------------------------------+
| Name                         | Type                                                  |
+==============================+=======================================================+
+------------------------------+-------------------------------------------------------+

Procedure
+++++++++

Products
++++++++

This Linearity-test observing mode will be used only sporadically as it is
considered part of the "System Calibration Modes".

+------------------------------+-------------------------------------------------------+
| Name                         | Type                                                  |
+==============================+=======================================================+
+------------------------------+-------------------------------------------------------+

