import numpy as np

from ImagingReso._utilities import checking_stack, formula_to_dictionary, get_isotope_dicts


class Resonance(object):
    
    database = 'ENDF_VIII'

    stack = {} # compound, thickness and ratio of each layer
    isotopes = {} # list of isotopes and file name for each element
    
    energy_max = np.NaN
    energy_min = np.NaN
    
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
        self.isotopes = {}

        if not stack == {}:
            # checking that every element of each stack is defined
            checking_stack(stack=stack)
            self.__retrieve_isotopes_infos_from_stack(stack=stack)
            self.stack = stack
    
        self.energy_max = energy_max
        self.energy_min = energy_min

    def __retrieve_isotopes_infos_from_stack(self, stack={}):
        '''retrieve the isotopes and isotopes file names from each element in stack'''
        for _key in stack:
            _elements = stack[_key]['elements']
            for _element in _elements:
                _dict = get_isotope_dicts(element=_element, database=self.database)
                self.isotopes = {**self.isotopes, **_dict}

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
        self.__retrieve_isotopes_infos_from_stack(stack=_new_stack)
        
        _key = list(_new_stack.keys())[0]
        _value = _new_stack[_key]
        
        self.stack[_key] = _value
        
