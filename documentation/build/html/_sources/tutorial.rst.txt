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

>>> _stack = {'CoAg': {'elements': ['Co', Ag'], 'ratio': [1,1], thickness': 0.025}, 'U': {'elements': ['U'], 'ratio': [1], thickness': 0.3}}

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
{'CoAg': {'elements': ['Co', 'Ag'],
          'isotopes': [{'Co': {'file_names': ['Co-58.csv', 'Co-59.csv'],
                               'list': ['58-Co', '59-Co'],
                               'mass': [57.9357576, 58.9332002],
                               'ratio': [1, 1]}},
                       {'Ag': {'file_names': ['Ag-107.csv', 'Ag-109.csv'],
                               'list': ['107-Ag', '109-Ag'],
                               'mass': [106.905093, 108.904756],
                               'ratio': [1, 1]}}],
          'ratio': [1, 1],
          'thickness': 0.025},
 'U': {'elements': ['U'],
       'isotopes': [{'U': {'file_names': ['U-233.csv',
                                          'U-234.csv',
                                          'U-235.csv',
                                          'U-238.csv'],
                           'list': ['233-U', '234-U', '235-U', '238-U'],
                           'mass': [233.039628,
                                    234.0409456,
                                    235.0439231,
                                    238.0507826],
                           'ratio': [1, 1, 1, 1]}}],
       'ratio': [1],
       'thickness': 0.3}}
       
The energy range defined

>>> print("Energy min {} eV".format(o_reso.energy_min))
Energy min 0 eV
>>> print("Energy max {} eV".format(o_reso.energy_max))
Energy max 300 eV

Metadata concerning the element defined can also be retrieved this way

>>> pprint.pprint(o_reso.get_element_infos())
{'Ag': {'density': 10.5, 'molar_mass': 107.8682},
 'Co': {'density': 8.9, 'molar_mass': 58.9332},
 'U': {'density': 18.95, 'molar_mass': 238.02891}}
 