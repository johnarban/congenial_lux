import pycprops
import astropy.units as u
import re
from astropy.io import fits
import numpy as np

def get_distance(ecsv_file, name):
    """
    Get distance from row corresponding to name
    """
    with open(ecsv_file) as f:
        for line in f:
            if re.sub('[^a-zA-Z0-9]','',name.lower()) in re.sub('[^a-zA-Z0-9]','',line.lower()):
                return float(line.split(",")[1])
        return None


def mad_std(x):
    y = x[np.isfinite(x)]
    return np.nanmedian(np.abs(y - np.nanmedian(y))) * 1.4826


def estimate_noise(emission_file):
    with fits.open(emission_file) as hdu:
        # use MAD std as noise level
        print("========= estimaing noise level ========")
        x = hdu[0].data[np.isfinite(hdu[0].data)]
        noise_est = np.nanmedian(np.abs(x - np.nanmedian(x))) * 1.4826
    
    return noise_est
    
# create emission mask
def make_emission_mask(emission_file, n = 3., level = None, label=''):
    """
    Make emission mask from cube

    Parameters
    ----------
    emission_file : str
        File name of emission cube
    n : float or int
        sigma clipping n parameter (n * sigma)
    level : float
        user provided level for clipping data
        
    the mask will be saved to the current (not the emission cube's) directory
    """
    outfile = emission_file.split('/')[-1].replace('.fits','.emission_mask'+label+'.fits')

    # estimate noise using median absolute deviation

    with fits.open(emission_file) as hdu:

        # mask noise
        if level is None:
            # use MAD std as noise level
            print("========= estimaing noise level ========")
            x = hdu[0].data[np.isfinite(hdu[0].data)]
            noise_est = np.nanmedian(np.abs(x - np.nanmedian(x))) * 1.4826
            print("noise:   {:0.3g}".format(noise_est))

            # Rosolowsky & Leroy 06 : use Tpeak / noise > 3
            mask = hdu[0].data.max(axis=0)/noise_est > n
            mask = (hdu[0].data/noise_est > n) & mask

        else:
            mask = hdu[0].data.max(axis=0) > level
            mask = (hdu[0].data > level) & mask
        
        hdu[0].data[mask] = 1
        hdu[0].data[np.logical_not(mask)] = np.nan


        # print out the fraction of unmasked pixels
        fraction_not_masked = np.nansum(mask)/np.prod(mask.shape)
        print("Fraction of '{}' not masked: {:0.1f}%".format(emission_file.split('/')[-1],fraction_not_masked*100))
        
        hdu[0].header['HISTORY'] = 'RMS = %0.6f' % (level or noise_est)

        hdu.writeto(outfile, overwrite=True)

    return outfile, level or noise_est


# Begin pycprops scripts

cubefiles = ["../imaging/he210/he210_12m_co32_co10.fits",
            "../imaging/ngc625/ngc625_12m_co32_co10.fits",
            "../imaging/sextansA_1/sextansA_1_7m_co10.fits"]

cubefile = cubefiles[0]


distance = get_distance("~/andes/new_keys/distance_key.txt", cubefile.split('/')[-2])

# needed because of some deprecation errors
np.asscalar = np.ndarray.item

pycprops.fits2props(cubefile,
                    mask_file=cubefile.split('/')[-1].replace('.fits','.emission_mask.fits'),
                    distance=distance * u.Mpc,
                    asgnname=cubefile.split('/')[-1].replace('.fits','_new.asgn.fits'),
                    propsname=cubefile.split('/')[-1].replace('.fits','_new.props.fits'),
                    allow_huge=True,
                    alphaCO=1, # just give me luminosity and ignore the bad units it gives you.
                   )

