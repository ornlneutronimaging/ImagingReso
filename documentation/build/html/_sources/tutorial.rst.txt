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
is defined by a dictionary  {'elements': [list_of_elements_as_string'], 'thickness', 0.025} where the
thickness is defined in mm.

example:
--------

>>> _stack = {'name_of_stack1': {'elements': ['Ag','Si'], 'thickness': 0.025}, 'namee_of_stack2': {'elements': ['Co'], 'thickness': 0.3}}

Then you can now initialize the object

>>> o_reso = ImagingReso.Resonance(stack = _stack)

