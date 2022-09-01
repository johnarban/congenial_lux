import os



import starlink
from starlink import convert
from starlink import cupid

from astropy.io import fits
import numpy as np
import subprocess

def estimate_noise(emission_file):
    with fits.open(emission_file) as hdu:
        x = hdu[0].data[np.isfinite(hdu[0].data)]
        noise_est = np.nanmedian(np.abs(x - np.nanmedian(x))) * 1.4826
    
    return noise_est

def parse_name(path):
    # we are building from the phangs pipeline so images
    # are in directories with their names
    return os.path.dirname(path).split('/')[-1]

if os.environ.get('STARLINK_DIR') is not None:
    starlink.wrapper.change_starpath(os.environ.get('STARLINK_DIR'))
else:
    starlink.wrapper.change_starpath('/home/joarlewi/star-2021A')



    
# ================================== #
#             CONVERT                #
source = "../imaging/he210/he210_12m_co32_co10.fits"

source_name = parse_name(source)

in_ = os.path.abspath(source) # path to fits cube
out = os.path.basename(source).replace('.fits','.sdf')

os.system('rm -f ' + out)

cline1 = 'convert; fits2ndf %s %s'%(in_,out)
# prog = subprocess.Popen(cline, shell=True)

# ================================== #
#          FINDCLUMPS                #

rms = estimate_noise(in_)
in_ = out                                 # use the NDF format file we created with fits2ndf
out = source_name + '_clumps'
outcat = source_name + 'clumps.FIT'

backoff = False                           # for compatability with IDL version
method = 'ClumpFind'
shape = 'Ellipse2'
config_cf = ['ClumpFind.AllowEdge=0',     # down allow edge clumps
               'ClumpFind.DeltaT=2*RMS',
               'ClumpFind.IDLAlg=1',      # use the IDL algorigthm
               'ClumpFind.MinPix=20',
               'ClumpFind.Tlow=3*RMS']

config = '"' + (','.join(config_cf)) + '"'

os.system('rm -f ' + out)
os.system('rm -f ' + outcat)

cline2 = f"findclumps in='{in_}' out='{out}' outcat='{outcat}' backoff={str(backoff)} method={method} rms={rms} shape={shape} config=^config.cf"


cline = f'. starlink; {cline1}; cupid; {cline2}'

print('Commands:')
print(cline.replace(';','\n'))
print('')
prog = subprocess.Popen(cline, shell=True)
prog.wait()
# nclumps = cupid.findclumps(in_,out,
#                             outcat = outcat,
#                             backoff = backoff,
#                             method = method,
#                             config = config,
#                             shape = shape,
#                             rms = rms)

print(' =============== Done ==============')
