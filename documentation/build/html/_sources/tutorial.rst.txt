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
                 'isotopes': {'density': {'units': 'g/cm3',
                                          'value': [10.406250187729098,
                                                    10.600899412431097]},
                              'file_names': ['Ag-107.csv', 'Ag-109.csv'],
                              'isotopic_ratio': [0.51839, 0.48161000000000004],
                              'list': ['107-Ag', '109-Ag'],
                              'mass': {'units': 'g/mol',
                                       'value': [106.905093, 108.904756]}},
                 'molar_mass': {'units': 'g/mol', 'value': 107.8682}},
          'Co': {'density': {'units': 'g/cm3', 'value': 8.9},
                 'isotopes': {'density': {'units': 'g/cm3',
                                          'value': [8.749367803547068,
                                                    8.900000030203689]},
                              'file_names': ['Co-58.csv', 'Co-59.csv'],
                              'isotopic_ratio': [0.0, 1.0],
                              'list': ['58-Co', '59-Co'],
                              'mass': {'units': 'g/mol',
                                       'value': [57.9357576, 58.9332002]}},
                 'molar_mass': {'units': 'g/mol', 'value': 58.9332}},
          'elements': ['Co', 'Ag'],
          'stochiometric_ratio': [1, 1],
          'thickness': {'units': 'mm', 'value': 0.025}},
 'U': {'U': {'density': {'units': 'g/cm3', 'value': 18.95},
             'isotopes': {'density': {'units': 'g/cm3',
                                      'value': [18.552792392319066,
                                                18.632509467526443,
                                                18.712358690988417,
                                                18.951741325328925]},
                          'file_names': ['U-233.csv',
                                         'U-234.csv',
                                         'U-235.csv',
                                         'U-238.csv'],
                          'isotopic_ratio': [0.0,
                                             5.4999999999999995e-05,
                                             0.0072,
                                             0.992745],
                          'list': ['233-U', '234-U', '235-U', '238-U'],
                          'mass': {'units': 'g/mol',
                                   'value': [233.039628,
                                             234.0409456,
                                             235.0439231,
                                             238.0507826]}},
             'molar_mass': {'units': 'g/mol', 'value': 238.02891}},
       'elements': ['U'],
       'stochiometric_ratio': [1],
       'thickness': {'units': 'mm', 'value': 0.3}}}
       
The energy range defined

>>> print("Energy min {} eV".format(o_reso.energy_min))
Energy min 0 eV
>>> print("Energy max {} eV".format(o_reso.energy_max))
Energy max 300 eV

Modify Isotopic Ratio
#####################

Let's presume that the U layer of our sample does not have the default isotopic_ratio reported

```
U-233 -> 0
U-234 -> 5.5e-5
U-235 -> 0.007
U-238 -> 0.99
```

but instead

```
U-233 -> 0
U-234 -> 0
U-235 -> 0.15
U-238 -> 085
```

Display current isotopic ratio
------------------------------

It's possible to display the current list of isotopic ratio

To display the entire list

>>> pprint.pprint(o_reso.get_stochiometric_ratio())
{'CoAg': {'Ag': {'107-Ag': 0.51839, '109-Ag': 0.48161000000000004},
          'Co': {'58-Co': 0.0, '59-Co': 1.0}},
 'U': {'U': {'233-U': 0.0,
             '234-U': 5.4999999999999995e-05,
             '235-U': 0.0072,
             '238-U': 0.992745}}}
             
From there, it's possible to narrow down the search to the compound and element we are looking for

>>> pprint.pprint(o_reso.get_stochiometric_ratio(compound='U', element='U'))  
{'233-U': 0.0,
 '234-U': 5.4999999999999995e-05,
 '235-U': 0.0072,
 '238-U': 0.992745}
 
if compound is composed of only 1 element, **element** paremeter can be omitted
>>> pprint.pprint(o_reso.get_stochiometric_ratio(compound='U'))
{'233-U': 0.0,
 '234-U': 5.4999999999999995e-05,
 '235-U': 0.0072,
 '238-U': 0.992745}
 
Define new set of isotopic ratio
--------------------------------

Let's presume our new set of 'U' ratio is

>>> new_list_ratio = [0.2, 0.3, 0.4, 0.1]

Let's define the new stochiomettric ratio

>>> o_reso.set_stochiometric_ratio(compound='U', list_ratio=new_list_ratio)
>>> pprint.pprint(o_reso.stack)
{'CoAg': {'Ag': {'density': {'units': 'g/cm3', 'value': 10.5},
                 'isotopes': {'density': {'units': 'g/cm3',
                                          'value': [10.406250187729098,
                                                    10.600899412431097]},
                              'file_names': ['Ag-107.csv', 'Ag-109.csv'],
                              'isotopic_ratio': [0.51839, 0.48161000000000004],
                              'list': ['107-Ag', '109-Ag'],
                              'mass': {'units': 'g/mol',
                                       'value': [106.905093, 108.904756]}},
                 'molar_mass': {'units': 'g/mol', 'value': 107.8682}},
          'Co': {'density': {'units': 'g/cm3', 'value': 8.9},
                 'isotopes': {'density': {'units': 'g/cm3',
                                          'value': [8.749367803547068,
                                                    8.900000030203689]},
                              'file_names': ['Co-58.csv', 'Co-59.csv'],
                              'isotopic_ratio': [0.0, 1.0],
                              'list': ['58-Co', '59-Co'],
                              'mass': {'units': 'g/mol',
                                       'value': [57.9357576, 58.9332002]}},
                 'molar_mass': {'units': 'g/mol', 'value': 58.9332}},
          'elements': ['Co', 'Ag'],
          'stochiometric_ratio': [1, 1],
          'thickness': {'units': 'mm', 'value': 0.025}},
 'U': {'U': {'density': {'units': 'g/cm3', 'value': 18.680428927650006},
             'isotopes': {'density': {'units': 'g/cm3',
                                      'value': [18.552792392319066,
                                                18.632509467526443,
                                                18.712358690988417,
                                                18.951741325328925]},
                          'file_names': ['U-233.csv',
                                         'U-234.csv',
                                         'U-235.csv',
                                         'U-238.csv'],
                          'isotopic_ratio': [0.2, 0.3, 0.4, 0.1],
                          'list': ['233-U', '234-U', '235-U', '238-U'],
                          'mass': {'units': 'g/mol',
                                   'value': [233.039628,
                                             234.0409456,
                                             235.0439231,
                                             238.0507826]}},
             'molar_mass': {'units': 'g/mol', 'value': 234.64285678}},
       'elements': ['U'],
       'stochiometric_ratio': [1],
       'thickness': {'units': 'mm', 'value': 0.3}}}
       
As you can see, the **density** and **molar_mass** values of the *U* compound/element have been updated.

Let's assume that the **Ag** element is not perfect and has some voids that changes its density to 8.5 (instead of 10.5). 
We need to change this value. 

First, we can have the current density value for this element

>>> print(o_reso.get_density(compound='CoAg', element='Co'))
10.5

or of all the compounds

>>> pprint.pprint(o_reso.get_density())
{'CoAg': {'Ag': 10.5, 'Co': 8.9}, 'U': {'U': 18.680428927650006}}

And now we can change the value of the density for the **Co** element

>>> o_reso.set_density(compound='CoAg', element='Co', density=8.5)
>>> pprint.pprint(o_reso.get_density())
{'CoAg': {'Ag': 10.5, 'Co': 20}, 'U': {'U': 18.680428927650006}}




