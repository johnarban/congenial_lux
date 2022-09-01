import glob
SPACESAVING = 3
DOSPLIT = True # split out science SPWs

# scriptforpi = 'member.uid___A001_X133d_X4145.scriptForPI.py'

scriptforpi = glob.glob('*scriptForPI.py')[0]

execfile(scriptforpi)

scriptforim = glob.globg('*scriptForImag*.py')
if len(scriptforim) > 0:
	print('Doing imaging to')
	execfile(scriptforim[0])
	
