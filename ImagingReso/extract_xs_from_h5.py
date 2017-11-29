import glob
from ImagingReso._utilities import get_sigma


h5 = glob.glob('/Users/y9z/Documents/GitHub/ImagingReso/ImagingReso/reference_data/nndc_hdf5/*.h5')
for each_path in h5:
    dict_ = get_sigma(each_path, 1, 200, 0.01)
