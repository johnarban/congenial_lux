files = glob.glob('*.ms')

# for f in files:
#     split(f, outputvis = f+'.split.cal', spw = '25', datacolumn='corrected')

newfiles = glob.glob('*.ms.split.cal')

concat(vis = newfiles, concatvis = 'concat.ms', freqtol='10MHz', dirtol='1arcsec', copypointing=True)
