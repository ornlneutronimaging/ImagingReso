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

>>> _stack = {'name_of_stack1': {'elements': ['Ag','Si'], 'ratio': [1,1], thickness': 0.025}, 'namee_of_stack2': {'elements': ['Co'], 'ratio': [1], thickness': 0.3}}

Then you can now initialize the object

>>> o_reso = ImagingReso.Resonance(stack = _stack)

It is also possible to define the layers (stack) one by one using their formula as demonstrated here

>>> o_reso = ImagingReso.Resonance()
>>> stack1 = 'AgSi'
>>> thickness1 = 0.025
>>> o_reso.add_layer(formula=stack1, thickness=thickness1)
>>> stack2 = 'Co'
>>> thcikness2 = 0.3
>>> o_reso.add_layer(formula=stack2, thcikness=thickness2)

The global material can then be checked usign the **slack** parameter

>>> print(o_reso.slack)
{'AgSi': {'elements': ['Ag','Si'], 'ratio':[1,1], 'thickness':0.025}, 'Co': {'elements':['Co'], 'ratio':[1], 'thickness': 0.3}}

