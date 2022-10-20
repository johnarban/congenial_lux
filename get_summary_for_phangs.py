# in this file we will get the important values we need
# in order to build phangsPipeline key files

import analysisUtils as au

# Get the system velocity for the field

# Get the phase center for the field

# get bandwidth for the SPW in velocity

measurement_set = 'calibrated.ms'

au.radialVelocity('measurement_set','NGC_625')
# 14/74: coord = au.getPhaseCenterForField('measurement_set','NGC_625')
# au.tcleanVelocityParameters('measurement_set')
# a = au.pickCellSize('measurement_set',spw='3',npix=6,imsize=True)
measurement_set = 'calibrated.ms'
field = 'NGC_625'


