import numpy as np
import numbers
import os

from ImagingReso import _utilities


class Resonance(object):
    
    database = 'ENDF_VIII'

    stack = {} # compound, thickness, atomic_ratio of each layer with isotopes information
    stack_sigma = {} # all the energy and sigma of the isotopes and compounds 
    
    energy_max = np.NaN
    energy_min = np.NaN
    energy_step = np.NaN
    
    def __init__(self, stack={}, energy_max=300, energy_min=0, energy_step=0.1):
        '''initialize resonance object
        
        Paramters:
        ==========
        stack: dictionary 
          example: {'layer1': {'elements':['Ag','Si], 
                               'atomic_ratio': [1, 2],
                               'thickness': 0.025}}
        energy_max: float (default 300) max energy in eV to use in calculation
        energy_min: float (default 0) min energy in eV to use in calculation
        energy_step: float (default 0.1) energy step to use in extrapolation of sigma data
        '''
        self.__element_metadata = {}
        
        self.energy_max = energy_max
        self.energy_min = energy_min
        self.energy_step = energy_step

        if not stack == {}:
            # checking that every element of each stack is defined
            _utilities.checking_stack(stack=stack)
            new_stack = self.__update_stack_with_isotopes_infos(stack=stack)
            self.stack = new_stack
            
            # populate stack_sigma
            self.__get_sigmas()
    
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
        
        _new_stack = _utilities.formula_to_dictionary(formula=formula, 
                                           thickness=thickness, 
                                           database=self.database)
        new_stack = self.__update_stack_with_isotopes_infos(stack=_new_stack)
        self.stack = {**self.stack, **new_stack}
        
        # populate stack_sigma
        self.__get_sigmas()

    def get_stochiometric_ratio(self, compound='', element=''):
        '''returns the list of isotopes for the element of the compound defined with their stochiometric values
        
        Parameters:
        ===========
        compound: string (default is empty). If empty, all the stochiometric will be displayed
        element: string (default is same as compound). 
        
        Raises:
        =======
        ValueError if element is not defined in the stack
        '''
        _stack = self.stack
        
        if compound == '':
            _list_compounds = _stack.keys()
            list_all_dict = {}
            for _compound in _list_compounds:
                _list_element = _stack[_compound]['elements']
                list_all_dict[_compound] = {}
                for _element in _list_element:
                    list_all_dict[_compound][_element] = self.get_stochiometric_ratio(
                        compound = _compound, 
                        element = _element)     
            return list_all_dict
        
        # checking compound is valid
        list_compounds = _stack.keys()
        if not compound in list_compounds:
            list_compounds_joined = ', '.join(list_compounds)
            raise ValueError("Compound '{}' could not be find in {}".format(compile, list_compounds_joined))
        
        # checking element is valid
        if element == '': 
            # we assume that the element and compounds names matched
            element = compound
        list_element = _stack[compound].keys()
        if not element in list_element:
            list_element_joined = ', '.join(list_element)
            raise ValueError("Element '{}' should be any of those elements: {}".format(element, list_element_joined))
        
        list_istopes = _stack[compound][element]['isotopes']['list']
        list_ratio = _stack[compound][element]['isotopes']['isotopic_ratio']
        iso_ratio = zip(list_istopes, list_ratio)
        
        _stochiometric_ratio = {}
        for _iso, _ratio in iso_ratio:
            _stochiometric_ratio[_iso] = _ratio
            
        return _stochiometric_ratio
        
    def set_stochiometric_ratio(self, compound='', element='', list_ratio=[]):
        '''defines the new set of ratio of the compound/element and trigger the calculation to update the density
        
        Parameters:
        ===========
        compound: string (default is ''). Name of compound
        elememnt: string (defualt is ''). Name of element
        list_ratio: list (default is []). list of new stochiometric_ratio
        
        Raises:
        =======
        ValueError if compound does not exist
        ValueError if element does not exist
        ValueError if list_ratio does not have the right format
        '''
        _stack = self.stack
        
        list_compounds = _stack.keys()
        if not compound in _stack.keys():
            list_compounds_joined = ', '.join(list_compounds)
            raise ValueError("Compound '{}' could not be find in {}".format(compile, list_compounds_joined))

        if element == '': 
            # we assume that the element and compounds names matched
            element = compound
        list_element = _stack[compound].keys()
        if not element in list_element:
            list_element_joined = ', '.join(list_element)
            raise ValueError("Element '{}' should be any of those elements: {}".format(element, list_element_joined))
        
        old_list_ratio = _stack[compound][element]['isotopes']['list']
        if not (len(old_list_ratio) == len(list_ratio)):
            raise ValueError("New list of ratio ({} elements) does not match old list size ({} elements!".format(len(
                list_ratio), len(old_list_ratio)))
        
        self.stack[compound][element]['isotopes']['isotopic_ratio'] = list_ratio
        self.__update_molar_mass(compound=compound, element=element)
        self.__update_density(compound=compound, element=element)

    def get_density(self, compound='', element=''):
        '''returns the list of isotopes for the element of the compound defined with their density
        
        Parameters:
        ===========
        compound: string (default is empty). If empty, all the stochiometric will be displayed
        element: string (default is same as compound). 
        
        Raises:
        =======
        ValueError if element is not defined in the stack
        '''
        _stack = self.stack
        
        if compound == '':
            _list_compounds = _stack.keys()
            list_all_dict = {}
            for _compound in _list_compounds:
                _list_element = _stack[_compound]['elements']
                list_all_dict[_compound] = {}
                for _element in _list_element:
                    list_all_dict[_compound][_element] = self.get_density(
                        compound = _compound, 
                        element = _element)     
            return list_all_dict
        
        # checking compound is valid
        list_compounds = _stack.keys()
        if not compound in list_compounds:
            list_compounds_joined = ', '.join(list_compounds)
            raise ValueError("Compound '{}' could not be find in {}".format(compile, list_compounds_joined))
        
        # checking element is valid
        if element == '': 
            # we assume that the element and compounds names matched
            element = compound
        list_element = _stack[compound].keys()
        if not element in list_element:
            list_element_joined = ', '.join(list_element)
            raise ValueError("Element '{}' should be any of those elements: {}".format(element, list_element_joined))
        
        return _stack[compound][element]['density']['value']

    def set_density(self, compound='', element='', density=np.NaN):
        '''defines the new density f the compound/element 
        
        Parameters:
        ===========
        compound: string (default is ''). Name of compound
        elememnt: string (defualt is ''). Name of element
        density: float (default is np.NaN). New density
        
        Raises:
        =======
        ValueError if compound does not exist
        ValueError if element does not exist
        ValueError if density is not a number
        '''
        _stack = self.stack
        
        list_compounds = _stack.keys()
        if not compound in _stack.keys():
            list_compounds_joined = ', '.join(list_compounds)
            raise ValueError("Compound '{}' could not be find in {}".format(compile, list_compounds_joined))

        if element == '': 
            # we assume that the element and compounds names matched
            element = compound
        list_element = _stack[compound].keys()
        if not element in list_element:
            list_element_joined = ', '.join(list_element)
            raise ValueError("Element '{}' should be any of those elements: {}".format(element, list_element_joined))
        
        if not isinstance(density, numbers.Number):
            raise ValueError("Density '{}' must be a number!".format(density))
        
        self.stack[compound][element]['density']['value'] = density

    def __update_stack_with_isotopes_infos(self, stack={}):
        '''retrieve the isotopes, isotopes file names, mass and atomic_ratio from each element in stack'''
        for _key in stack:
            isotopes_array = []
            _elements = stack[_key]['elements']
            for _element in _elements:
                _dict = _utilities.get_isotope_dicts(element=_element, database=self.database)
                stack[_key][_element] = _dict    
        return stack

    def __update_density(self, compound='', element=''):
        '''Re-calculate the density of the compound / element given due to stochiometric changes
        
        Parameters:
        ===========
        compound: string (default is '') name of compound
        element: string (default is '') name of element
        '''
        _density_element = 0
        list_ratio = self.stack[compound][element]['isotopes']['isotopic_ratio']
        list_density = self.stack[compound][element]['isotopes']['density']['value']
        ratio_density = zip(list_ratio, list_density)
        for _ratio, _density in ratio_density:
            _density_element += np.float(_ratio) * np.float(_density)
        self.stack[compound][element]['density']['value'] = _density_element
        
    def __update_molar_mass(self, compound='', element=''):
        '''Re-calculate the molar moass of the compound / element given due to stochiometric changes
        
        Parameters:
        ==========
        compound: string (default is '') name of compound
        element: string (default is '') name of element
        '''
        _molar_mass_element = 0
        list_ratio = self.stack[compound][element]['isotopes']['isotopic_ratio']
        list_mass = self.stack[compound][element]['isotopes']['mass']['value']
        ratio_mass = zip(list_ratio, list_mass)
        for _ratio, _mass in ratio_mass:
            _molar_mass_element += np.float(_ratio) * np.float(_mass)
        self.stack[compound][element]['molar_mass']['value'] = _molar_mass_element
        
    def __get_sigmas(self):
        '''will populate the stack_sigma dictionary with the energy and sigma array
        for all the compound/element and isotopes'''
        stack_sigma = {}
        _stack = self.stack

        _file_path = os.path.abspath(os.path.dirname(__file__))
        _database_folder = os.path.join(_file_path, 'reference_data', self.database)

        _list_compounds = _stack.keys()
        for _compound in _list_compounds:
            _list_element = _stack[_compound]['elements']
            stack_sigma[_compound] = {}
            
            for _element in _list_element:
                stack_sigma[_compound][_element] = {}
                _list_isotopes = _stack[_compound][_element]['isotopes']['list']
                _list_file_names = _stack[_compound][_element]['isotopes']['file_names']
                _iso_file = zip(_list_isotopes, _list_file_names)
                for _iso, _file in _iso_file:
                    stack_sigma[_compound][_element][_iso] = {}
                    _file = os.path.join(_database_folder, _file)
                    _dict = _utilities.get_sigma(database_file_name=_file, 
                                                E_min=self.energy_min, 
                                                E_max=self.energy_max, 
                                                E_step=self.energy_step)
                    stack_sigma[_compound][_element][_iso]['energy_eV'] = _dict['energy']
                    stack_sigma[_compound][_element][_iso]['sigma_b'] = _dict['sigma']
                    
        self.stack_sigma = stack_sigma
                    
                
        