# Code Reference

## Folders

- `new_keys`
  - key files for running the pipeline on lux. These can be found in `/data/users/joarlewis/andes/`
    - also contains a copy of `run_andes.py` which should be places in the parent directory of `new_keys`
  - I run the pipeline from within the `andes` directory. This creates the `imaging/` and `derived/` (and other `phangsPipeline` output) subfolders.

## Files
- `findclumps.py` 
  - batch run STARLINK findclumps using the starlink python wrapper [starlink-pywrapper](https://starlink-pywrapper.readthedocs.io/en/latest/)
  - a config file ([config.cf](https://github.com/johnarban/congenial_lux/blob/main/helpers/config.cf)) can be found in the helpers subfolder
  
- `process_cprops.py`
    - batch run cprops for a series of ALMA images. 
    - raw data are stored in the folder structure the comes from the ALMA archive in the my `lux` data directory. A symlink with common name of the 3 processed sources links directly to the lowest directory structure where the `script/`, `raw/`, and `calibrated/` folders are. 
    - This contains some sub functions. To run `cprops` you need to create a noise mask so the basic workflow is
    ```python
    from process_cprops import make_emission_mask
    make_emission_mask(`my_cube.fits`)
    # set cubefiles to [../relative/path/to/my_cube.fits] in process_cprops.py
    # cubefiles should be a list of files to process or can be list of single item, but must be a list
    %run -i process_cprops.py
    ```
 
- `functions.py`
    - `getMosaicPhaseCenter`
        - Find the center of a mosaic. Do not use this to set the phase center of a mosaic in the `phangsPipeline`. Just use the phase center of the first mosaic field. The pipeline will do the rest
    - `estimate_cell_and_imsize2`
        - Estime the pixel and image size for the mosaic. This is pulled from the `phangsPipeline`

- `split_convert.py`
    - concatinates a series of `*.ms.split.cal` files into a single `concat.ms` visibility file. It has reasonable frequency and direction tolerances for combining fields (1 arcsec) and spectral windows (10 MHz). 


