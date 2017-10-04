import os
import sys
import re
import pprint
import numpy as np
from ImagingReso.resonance import Resonance

root_folder = os.path.dirname(os.getcwd())
sys.path.append(root_folder)

_energy_min = 0.0001
_energy_max = 300
_energy_step = 0.1

_layer_1 = 'Co'
_thickness_1 = 0.025  # mm
_density_1 = 8  # g/cm3 deviated due to porosity

_layer_2 = 'Ag'
_thickness_2 = 0.03  # mm

_layer_3 = 'UO3'
_thickness_3 = 0.3  # mm
_density_3 = 0.7875  # g/cm3

o_reso = Resonance(energy_min=_energy_min, energy_max=_energy_max, energy_step=_energy_step)
o_reso.add_layer(formula=_layer_1, thickness=_thickness_1, density=_density_1)
o_reso.add_layer(formula=_layer_2, thickness=_thickness_2)
o_reso.add_layer(formula=_layer_3, thickness=_thickness_3, density=_density_3)

# o_reso.export(to_csv=True, mixed=True, transmission=True)
# o_reso.export(x_axis='lambda', mixed=True, transmission=True)
# o_reso.export(mixed=True, all_layers=True, transmission=False)
# o_reso.export(mixed=True, all_elements=True, transmission=False)
# o_reso.export(mixed=True, all_isotopes=True, transmission=False)
o_reso.export(items_to_export=[['UO3'], ['UO3', 'U', '233-U'], ['UO3', 'U', '238-U']])
# o_reso.export(items_to_plot=[['Co'], ['Ag'], ['Ag', 'Ag', '107-Ag'], ['Co', 'Co', '58-Co']])
