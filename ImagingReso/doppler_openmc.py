import os
from pprint import pprint
import shutil
import subprocess
import urllib.request

import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
from matplotlib.patches import Rectangle

import openmc.data

# Download ENDF file
# url = 'https://t2.lanl.gov/nis/data/data/ENDFB-VII.1-neutron/U/238'
# filename, headers = urllib.request.urlretrieve(url, 'u238.endf')

# Load into memory
# u238_endf = openmc.data.IncidentNeutron.from_endf('u238.endf')
u238_endf = openmc.data.IncidentNeutron.from_hdf5('/Users/y9z/Documents/GitHub/openmc/scripts/nndc_hdf5/U238.h5')
# u238_endf.from_njoy('u238.endf',
#                     temperatures=[300.],
#                     njoy_exec='/Users/y9z/Documents/Softwares/NJOY2016/bin/njoy',
#                     stdout=True)
u238_multipole = openmc.data.WindowedMultipole.from_hdf5('/Users/y9z/Documents/GitHub/openmc/scripts/nndc_hdf5/U238.h5')

