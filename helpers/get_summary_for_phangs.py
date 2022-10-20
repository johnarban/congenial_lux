# in this file we will get the important values we need
# in order to build phangsPipeline key files

import analysisUtils as au

measurement_set = 'calibrated.ms'
field = 'NGC_625'
spw = '3'  # pick the right SPW for your data. should be a string
npix = 6   # how many pixels to sample the beam

# source radial velocity so you can defined channel parameters using line freqnecy
radvel = au.radialVelocity(measurement_set, field)

# get the phase center. use this when imaging a mosaic too
coord = au.getPhaseCenterForField(measurement_set, field)

# retuns a dictionary
vel_params = au.tcleanVelocityParameters(measurement_set)

# cells size is found by the pipeline, but this is useful for imaging by hand
cells_size = au.pickCellSize(measurement_set, spw=spw, npix=npix, imsize=True)
