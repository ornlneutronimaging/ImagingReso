import numpy as np

from ImagingReso._utilities import checking_stack, formula_to_dictionary


class Resonance(object):
    
    database = 'ENDF_VIII'

    stack = {}
    
    def __init__(self, stack={}, energy_max=300, energy_min=0):
        '''initialize resonance object
        
        Paramters:
        ==========
        stack: dictionary 
          example: {'layer1': {'elements':['Ag','Si], 
                               'ratio': [1, 2],
                               'thickness': 0.025}}
        energy_max: float (default 300) max energy in eV to use in calculation
        energy_min: float (default 0) min energy in eV to use in calculation
        '''
        if not stack == {}:
            # checking that every element of each stack is defined
            checking_stack(stack=stack)
            self.stack = stack
    
        self.energy_max = energy_max
        self.energy_min = energy_min

    def add_layer(self, formula='', thickness=np.NaN): 
        '''provide another way to define the layers (stack)
        
        Parameters:
        ===========
        formula: string
           ex: 'CoAg2'
           ex: 'Al'
        thickness: float (in mm) 
        '''
        if formula == '':
            return
        
        _new_stack = formula_to_dictionary(formula=formula, 
                                           thickness=thickness, 
                                           database=self.database)
        
        _key = list(_new_stack.keys())[0]
        _value = _new_stack[_key]
        
        self.stack[_key] = _value
        
