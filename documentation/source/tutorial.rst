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
is defined by a dictionary  where the
thickness is defined in mm, the density in g/cm3 and the ratio is the stochiometric coefficient of each element. 

example:
--------

>>> _stack = {'CoAg': {'elements': ['Co','Ag'],
                   'stochiometric_ratio': [1,1],
                   'thickness': {'value': 0.025,
                                'units': 'mm'},
                   'density': {'value': 0.5,
                              'units': 'g/cm3'},
                  },
         'U': {'elements': ['U'],
               'stochiometric_ratio': [1],
              'thickness': {'value': 0.3,
                            'units': 'mm'},
                'density': {'value': np.NaN,
                            'units': 'g/cm3'},
              },
         }
         
Then you can now initialize the object as followed, in this case we use a energy range of 0 to 300 eV with 
10 eV of energy step.

As noted that if the density is omitted, the program will use the stochiometri_ratio and theoretical density of each element to 
estimage the density of the compound (layer)

>>> o_reso = ImagingReso.Resonance(stack = _stack, energy_min=0, energy_max=300, energy_step=10)

It is also possible to define the layers (stack) one by one using their formula as demonstrated here

>>> o_reso = ImagingReso.Resonance(energy_min=0, energy_max=300, energy_step=10)
>>> stack1 = 'CoAg'
>>> thickness1 = 0.025 #mm
>>> density1 = 0.5 #g/cm3
>>> o_reso.add_layer(formula=stack1, thickness=thickness1, density=density1)
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
          'atoms_per_cm3': {'Ag': 1.8051829472054791e+21,
                            'Co': 1.8051829472054791e+21},
          'density': {'units': 'g/cm3', 'value': 0.5},
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
       'atoms_per_cm3': {'U': 4.7943575106128917e+22},
       'density': {'units': 'g/cm3', 'value': 18.949999999999999},
       'elements': ['U'],
       'stochiometric_ratio': [1],
       'thickness': {'units': 'mm', 'value': 0.3}}}       

The energy range defined

>>> print("Energy min {} eV".format(o_reso.energy_min))
Energy min 0 eV
>>> print("Energy max {} eV".format(o_reso.energy_max))
Energy max 300 eV
>>> print("Energy step {} eV".format(o_reso.energy_step))
Energy step 10 eV

During the initialization process, the following things take place behind the scene
- the number of atoms per cm3 of each element is calculated
- the density of each layer (if not provided is estimated)
- the arrays of Sigma (barns) vs Energy for each isotope is retrieved

>>> pprint.pprint(o_reso.stack_sigma)
{'CoAg': {'Ag': {'107-Ag': {'energy_eV': array([  1.00000000e-05,   1.03401821e+01,   2.06803541e+01,
         ...
         2.79184656e+02,   2.89524828e+02,   2.99865000e+02]),
                            'sigma_b': array([ 1938.91      ,     6.69765395,     6.9742027 ,     5.28153402,
         ...
         4.73100823,     4.11286   ])},
                 '109-Ag': {'energy_eV': array([  1.00000000e-05,   1.03446648e+01,   2.06893197e+01,
         ...
         2.79305690e+02,   2.89650345e+02,   2.99995000e+02]),
                            'sigma_b': array([  4.51167000e+03,   1.19932847e+01,   5.51138934e+00,
         ...
         4.32864623e+00,   1.19208304e+01,   5.41247000e+00])},
                 'energy_ev': array([  1.00000000e-05,   1.03424234e+01,   2.06848369e+01,
         ...
         2.79245173e+02,   2.89587587e+02,   2.99930000e+02]),
                 'sigma': array([ 3177.9769436 ,     9.24808268,     6.26969716,    64.29044465,
         ...
         8.19369849,     4.73876517])},
         
         ...
         
          }}}

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
          'atoms_per_cm3': {'Ag': 1.8051829472054791e+21,
                            'Co': 1.8051829472054791e+21},
          'density': {'units': 'g/cm3', 'value': 0.5},
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
       'atoms_per_cm3': {'U': 4.7943575106128917e+22},
       'density': {'units': 'g/cm3', 'value': 18.949999999999999},
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




