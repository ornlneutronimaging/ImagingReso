********
Tutorial
********

In a first time, you need to install the library

$ pip install ImagingReso

then you need to import it

>>> import ImagingReso

Initialization
##############

we first define our stack of elements. Each layer of the stack can be a single element, or a compound and
is defined by a dictionary  {'elements': [list_of_elements_as_string'], 'ratio': [1], thickness', 0.025} where the
thickness is defined in mm and the ratio is the stochiometric coefficient of each element. 

example:
--------

>>> _stack = _stack = {'CoAg': {'elements': ['Co','Ag'],
                   'atomic_ratio': [1,1],
                   'thickness': {'value': 0.025,
                                'units': 'mm'},
                  },
         'U': {'elements': ['U'],
               'atomic_ratio': [1],
              'thickness': {'value': 0.3,
                           'units': 'mm'},
              },
         }
         
Then you can now initialize the object as followed, in this case we use a energy range of 0 to 300 eV

>>> o_reso = ImagingReso.Resonance(stack = _stack, energy_min=0, energy_max=300)

It is also possible to define the layers (stack) one by one using their formula as demonstrated here

>>> o_reso = ImagingReso.Resonance()
>>> stack1 = 'CoAg'
>>> thickness1 = 0.025
>>> o_reso.add_layer(formula=stack1, thickness=thickness1)
>>> stack2 = 'U'
>>> thcikness2 = 0.3
>>> o_reso.add_layer(formula=stack2, thcikness=thickness2)

**All the parameters defined can be checked as followed**

The list of stack displays the input information, but also reported the list of isotopes, mass, etc, for
the elements you defined, for each layer.

>>> import pprint
>>> pprint.pprint(o_reso.slack)
{'CoAg': {'Ag': {'density': {'units': 'g/cm3', 'value': 10.5},
                 'isotopes': {'atomic_ratio': [0.51839, 0.48161000000000004],
                              'file_names': ['Ag-107.csv', 'Ag-109.csv'],
                              'list': ['107-Ag', '109-Ag'],
                              'mass': {'units': 'g/mol',
                                       'value': [106.905093, 108.904756]}},
                 'molar_mass': {'units': 'g/mol', 'value': 107.8682}},
          'Co': {'density': {'units': 'g/cm3', 'value': 8.9},
                 'isotopes': {'atomic_ratio': [0.0, 1.0],
                              'file_names': ['Co-58.csv', 'Co-59.csv'],
                              'list': ['58-Co', '59-Co'],
                              'mass': {'units': 'g/mol',
                                       'value': [57.9357576, 58.9332002]}},
                 'molar_mass': {'units': 'g/mol', 'value': 58.9332}},
          'atomic_ratio': [1, 1],
          'elements': ['Co', 'Ag'],
          'thickness': {'units': 'mm', 'value': 0.025}},
 'U': {'U': {'density': {'units': 'g/cm3', 'value': 18.95},
             'isotopes': {'atomic_ratio': [0.0,
                                           5.4999999999999995e-05,
                                           0.0072,
                                           0.992745],
                          'file_names': ['U-233.csv',
                                         'U-234.csv',
                                         'U-235.csv',
                                         'U-238.csv'],
                          'list': ['233-U', '234-U', '235-U', '238-U'],
                          'mass': {'units': 'g/mol',
                                   'value': [233.039628,
                                             234.0409456,
                                             235.0439231,
                                             238.0507826]}},
             'molar_mass': {'units': 'g/mol', 'value': 238.02891}},
       'atomic_ratio': [1],
       'elements': ['U'],
       'thickness': {'units': 'mm', 'value': 0.3}}}
       
The energy range defined

>>> print("Energy min {} eV".format(o_reso.energy_min))
Energy min 0 eV
>>> print("Energy max {} eV".format(o_reso.energy_max))
Energy max 300 eV

