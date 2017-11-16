from ImagingReso.resonance import Resonance
import numpy as np
import pprint
# Global parameters
_energy_min = 1
_energy_max = 200
_energy_step = 0.01
# Input sample name or names as str, case sensitive
layer_1 = 'U'
thickness_1 = 0.01
density_1 = None
layer_2 = 'Gd'
thickness_2 = 0.009
density_2 = None

o_reso = Resonance(energy_min=_energy_min, energy_max=_energy_max, energy_step=_energy_step)
o_reso.add_layer(formula=layer_1, thickness=thickness_1)
o_reso.add_layer(formula=layer_2, thickness=thickness_2)

# o_reso.plot(all_elements=True, transmission=False, x_axis='time')
# o_reso.plot(all_elements=True, transmission=False, x_axis='lambda')
pprint.pprint(o_reso.stack_sigma)
o_reso.plot(mixed=True, y_axis='attenuation', x_axis='energy', offset_us=0, time_resolution_us=0.16,
            all_elements=True,
            all_isotopes=False,
            source_to_detector_m=16,
            lambda_max_angstroms=0.1)
