import analysisUtils as au
import numpy as np
import os

def getMosaicPhaseCenter(measurement_set,field):
    """
    this does not work
    """
    # initialize mosaic pointing list
    
    coords = []

    # check if measurement_set is non string iterable
    if isinstance(measurement_set,str):
        measurement_sets = [measurement_set]
    else:
        measurement_sets = measurement_set

    for ms in measurement_sets:
        # get the unique field ID for each pointing of the mosaic
        print('Measurement set: %s' % ms)
        print('Field: %s' % field)
        field_ids, _ = au.parseSingleFieldArgument(ms,field)
        print(f'Field IDs: {field_ids}')

        for field_id in field_ids:
            radec, frame = au.getRADecForField(ms,field_id,hms=True,verbose=True,returnReferenceFrame=True,blendByName=False)
            coords.append(radec)

    radec = au.getMeanPosition(coords)

    return(frame + ' ' + radec.replace(',',' '))





def estimate_cell_and_imsize2(
        infile=None,
        clean_call=None,
        oversamp=5,
        force_square=False,
):
    """
    Pick a cell and image size for a measurement set. Requests an
    oversampling factor, which is by default 5. Will pick a good size
    for the FFT and will try to pick a round number for the cell
    size. Returns variables appropriate for cell= and imsize= in
    tclean.
    """

    if not os.path.isdir(infile):
        print('Error! The input file "' + infile + '" was not found!')
        return

    # If supplied, use the clean call to determine pblevel


    pblevel = 0.2

    # These are the CASA-preferred sizes for fast FFTs

    valid_sizes = []
    for ii in range(10):
        for kk in range(3):
            for jj in range(3):
                valid_sizes.append(2 ** (ii + 1) * 5 ** jj * 3 ** kk)
    valid_sizes = sorted(valid_sizes)
    valid_sizes = np.array(valid_sizes)

    # Cell size implied by baseline distribution from analysis
    # utilities.

    au_cellsize, au_imsize, _ = au.pickCellSize(infile,
                                                imsize=True,
                                                npix=oversamp,
                                                pblevel=pblevel,
                                                )
    print('AU cell size:' , au_cellsize)
    print('AU imsize:' , au_imsize)

    xextent = au_cellsize * au_imsize[0] * 1.2
    yextent = au_cellsize * au_imsize[1] * 1.2

    # Make the cell size a nice round number

    if au_cellsize < 0.1:
        cell_size = au_cellsize
    elif 0.1 <= au_cellsize < 0.5:
        cell_size = np.floor(au_cellsize / 0.05) * 0.05
    elif 0.5 <= au_cellsize < 1.0:
        cell_size = np.floor(au_cellsize / 0.1) * 0.1
    elif 1.0 <= au_cellsize < 2.0:
        cell_size = np.floor(au_cellsize / 0.25) * 0.25
    elif 2.0 <= au_cellsize < 5.0:
        cell_size = np.floor(au_cellsize / 0.5) * 0.5
    else:
        cell_size = np.floor(au_cellsize / 1.0) * 0.5

    # Now make the image size a good number for the FFT

    need_cells_x = xextent / cell_size
    need_cells_y = yextent / cell_size

    cells_x = np.min(valid_sizes[valid_sizes > need_cells_x])
    cells_y = np.min(valid_sizes[valid_sizes > need_cells_y])

    # If requested, force the mosaic to be square. This avoids
    # pathologies in CASA versions 5.1 and 5.3.

    if force_square:
        if cells_y < cells_x:
            cells_y = cells_x
        if cells_x < cells_y:
            cells_x = cells_y

    image_size = [int(cells_x), int(cells_y)]
    cell_size_string = str(cell_size) + 'arcsec'

    return cell_size_string, image_size
