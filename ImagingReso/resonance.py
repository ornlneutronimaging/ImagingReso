import numpy as np
import numbers
import os
import matplotlib.pyplot as plt
import json

from ImagingReso import _utilities


class Resonance(object):
    
    database = 'ENDF_VIII'

    E_MIN = 1e-5
    E_MAX = 3e3

    stack = {}  # compound, thickness, atomic_ratio of each layer with isotopes information
    stack_sigma = {}  # all the energy and sigma of the isotopes and compounds
    stack_signal = {}  # transmission and attenuation signal for every isotope and compound
    total_signal = {}  # transmission and attenuation of the entire sample
    
    density_lock = {}  # dictionary that will defined the densities locked
    
    energy_max = np.NaN
    energy_min = np.NaN
    energy_step = np.NaN

    def __init__(self, stack={}, energy_max=1, energy_min=0.001, energy_step=0.001):
        """initialize resonance object
        
        Paramters:
        ==========
        stack: dictionary 
          example: {'layer1': {'elements':['Ag','Si], 
                               'atomic_ratio': [1, 2],
                               'thickness': {'value': 0.025,
                                             'units': 'mm',
                                             },
                               'density': {'units': 'g/cm3',
                                           'value': 0.5,
                                           },
                                }
        energy_max: float (default 300) max energy in eV to use in calculation
        energy_min: float (default 0) min energy in eV to use in calculation
        energy_step: float (default 0.1) energy step to use in extrapolation of sigma data
        """
        self.__element_metadata = {}
        
        if energy_min < self.E_MIN:
            raise ValueError("Energy min (eV) must be >= {}".format(self.E_MIN))
        self.energy_min = energy_min

        if energy_max > self.E_MAX:
            raise ValueError("Energy max (eV) must be <= {}".format(self.E_MAX))
        self.energy_max = energy_max

        self.energy_step = energy_step

        if not stack == {}:
            # checking that every element of each stack is defined
            _utilities.checking_stack(stack=stack)
            new_stack = self.__update_stack_with_isotopes_infos(stack=stack)
            self.stack = new_stack
            
            # if layer density has been defined, lock it
            self.__lock_density_if_defined(stack=self.stack)
            
            # calculate stack_sigma, layer density, atoms_per_cm3 ...
            self.__math_on_stack()
              
    def __str__(self):
        '''what to display if user does
        
        >>> o_reso = Resolution()
        >>> print(o_reso)
        '''
        return json.dumps(self.stack, indent=4)
    
    def __repr__(self):
        '''what to display if user does
        
        >>> o_reso = Resolution()
        >>> o_reso
        '''
        return json.dumps(self.stack, indent=4)    
                
    def add_layer(self, formula='', thickness=np.NaN, density=np.NaN): 
        """provide another way to define the layers (stack)
        
        Parameters:
        ===========
        formula: string
           ex: 'CoAg2'
           ex: 'Al'
        thickness: float (in mm) 
        density: float (g/cm3)
        """
        if formula == '':
            return
        
        _new_stack = _utilities.formula_to_dictionary(formula=formula, 
                                                      thickness=thickness, 
                                                      density=density,
                                                      database=self.database)      
        # check if density has been defined
        self.__lock_density_if_defined(stack=_new_stack)
        
        new_stack = self.__update_stack_with_isotopes_infos(stack=_new_stack)
        self.stack = {**self.stack, **new_stack}
        
        # calculate stack_sigma, layer density, atoms_per_cm3 ...
        self.__math_on_stack()

    def get_isotopic_ratio(self, compound='', element=''):
        """returns the list of isotopes for the element of the compound defined with their stoichiometric values
        
        Parameters:
        ===========
        compound: string (default is empty). If empty, all the stoichiometric will be displayed
        element: string (default is same as compound). 
        
        Raises:
        =======
        ValueError if element is not defined in the stack
        """
        _stack = self.stack
        compound = str(compound)
        
        if compound == '':
            _list_compounds = _stack.keys()
            list_all_dict = {}
            for _compound in _list_compounds:
                _compound = str(_compound)
                _list_element = _stack[_compound]['elements']
                list_all_dict[_compound] = {}
                for _element in _list_element:
                    list_all_dict[_compound][_element] = self.get_isotopic_ratio(
                        compound=_compound,
                        element=_element)
            return list_all_dict
        
        # checking compound is valid
        list_compounds = _stack.keys()
        if not compound in list_compounds:
            list_compounds_joined = ', '.join(list_compounds)
            raise ValueError("Compound '{}' could not be find in {}".format(compound, list_compounds_joined))
        
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
        
        _stoichiometric_ratio = {}
        for _iso, _ratio in iso_ratio:
            _stoichiometric_ratio[_iso] = _ratio
            
        return _stoichiometric_ratio
        
    def set_isotopic_ratio(self, compound='', element='', list_ratio=[]):
        """defines the new set of ratio of the compound/element and trigger the calculation to update the density
        
        Parameters:
        ===========
        compound: string (default is ''). Name of compound
        elememnt: string (defualt is ''). Name of element
        list_ratio: list (default is []). list of new stoichiometric_ratio
        
        Raises:
        =======
        ValueError if compound does not exist
        ValueError if element does not exist
        ValueError if list_ratio does not have the right format
        """
        _stack = self.stack
        
        list_compounds = _stack.keys()
        if not compound in _stack.keys():
            list_compounds_joined = ', '.join(list_compounds)
            raise ValueError("Compound '{}' could not be find in {}".format(compound, list_compounds_joined))

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

        # update entire stack
        self.__math_on_stack()

    def get_density(self, compound='', element=''):
        """returns the list of isotopes for the element of the compound defined with their density
        
        Parameters:
        ===========
        compound: string (default is empty). If empty, all the stoichiometric will be displayed
        element: string (default is same as compound). 
        
        Raises:
        =======
        ValueError if element is not defined in the stack
        """
        _stack = self.stack
        
        if compound == '':
            _list_compounds = _stack.keys()
            list_all_dict = {}
            for _compound in _list_compounds:
                _list_element = _stack[_compound]['elements']
                list_all_dict[_compound] = {}
                for _element in _list_element:
                    list_all_dict[_compound][_element] = self.get_density(
                        compound=_compound,
                        element=_element)
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

    def __set_density(self, compound='', element='', density=np.NaN, debug=False):
        '''defines the new density of the compound/element 
        
        Parameters:
        ===========
        compound: string (default is ''). Name of compound
        element: string (defualt is ''). Name of element
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
        
        _density_lock = self.density_lock
        if _density_lock[compound]: 
            raise IOError("You are not authorized to change the density!")

        self.stack[compound]['density']['value'] = density
    
        # populate atoms_per_cm3
        self.__calculate_atoms_per_cm3(used_lock=True)

        # calculate transmission and attenuation
        self.__calculate_transmission_attenuation()
        
    def __math_on_stack(self, used_lock=False):
        """will perform all the various update of the stack, such as populating the stack_sigma, caluclate the density of the
        layers....etc. """

        # populate stack_sigma (Sigma vs Energy for every element)
        self.__get_sigmas()

        # populate compound density (if none provided)
        self.__update_layer_density()

        # populate atoms_per_cm3
        self.__calculate_atoms_per_cm3(used_lock=used_lock)
        
        # calculate transmission and attenuation
        self.__calculate_transmission_attenuation()

    def __lock_density_if_defined(self, stack={}):
        '''lock (True) the density lock if the density has been been defined during initialization
        Store the resulting dictionary into density_lock

        Parameters:
        ===========
        stack: dictionary (optional)
          if not provided, the entire stack will be used
        '''
          
        if self.stack == {}:
            density_lock = {}
        else:
            density_lock = self.density_lock
        
        for _compound in stack.keys():
            _density = stack[_compound]['density']['value']
            if np.isnan(_density):
                density_lock[_compound] = False
            else:
                density_lock[_compound] = True
        self.density_lock = density_lock

    def __calculate_transmission_attenuation(self):
        """  """
        stack = self.stack
        stack_sigma = self.stack_sigma
        stack_signal = {}
        
        total_signal = {}
        total_transmisison = 1.

        # compound level
        for _name_of_compound in stack.keys():
            stack_signal[_name_of_compound] = {}
            transmission_compound = 1.
            energy_compound = []
            
            _list_element = stack[_name_of_compound]['elements']
            _thickness_cm = _utilities.set_distance_units(value=stack[_name_of_compound]['thickness']['value'],
                                                          from_units=stack[_name_of_compound]['thickness']['units'],
                                                          to_units='cm')

            # element level
            for _element in _list_element:
                stack_signal[_name_of_compound][_element] = {}
                _atoms_per_cm3 = stack[_name_of_compound]['atoms_per_cm3'][_element]

                # isotope level
                for _iso in stack[_name_of_compound][_element]['isotopes']['list']:
                    stack_signal[_name_of_compound][_element][_iso] = {}
                    _sigma_iso = stack_sigma[_name_of_compound][_element][_iso]['sigma_b']
                    _transmission_iso = _utilities.calculate_transmission(
                        thickness_cm=_thickness_cm, 
                        atoms_per_cm3=_atoms_per_cm3,
                        sigma_b=_sigma_iso)
                    stack_signal[_name_of_compound][_element][_iso]['transmission'] = _transmission_iso
                    stack_signal[_name_of_compound][_element][_iso]['attenuation'] = 1. - _transmission_iso
                    stack_signal[_name_of_compound][_element][_iso]['energy_eV'] = stack_sigma[_name_of_compound][_element][_iso]['energy_eV']
                
                _sigma_ele = stack_sigma[_name_of_compound][_element]['sigma_b']
                _transmission_ele = _utilities.calculate_transmission(
                    thickness_cm=_thickness_cm, 
                    atoms_per_cm3=_atoms_per_cm3, 
                    sigma_b=_sigma_ele)
                stack_signal[_name_of_compound][_element]['transmission'] = _transmission_ele
                stack_signal[_name_of_compound][_element]['attenuation'] = 1. - _transmission_ele
                stack_signal[_name_of_compound][_element]['energy_eV'] = stack_sigma[_name_of_compound][_element]['energy_eV']

                transmission_compound *= _transmission_ele
                if energy_compound == []:
                    energy_compound = stack_sigma[_name_of_compound][_element]['energy_eV']

            stack_signal[_name_of_compound]['transmission'] = transmission_compound
            stack_signal[_name_of_compound]['attenuation'] = 1. - transmission_compound
            stack_signal[_name_of_compound]['energy_eV'] = energy_compound
            
            total_transmisison *= transmission_compound
        
        total_attenuation = 1. - total_transmisison

        self.stack_signal = stack_signal
        total_signal['transmission'] = total_transmisison
        total_signal['attenuation'] = total_attenuation
        total_signal['energy_eV'] = energy_compound
        self.total_signal = total_signal
        
    def __calculate_atoms_per_cm3(self, used_lock=False):
        """calculate for each element, the atoms per cm3"""
        stack = self.stack
        _density_lock = self.density_lock
        
        for _name_of_compound in stack.keys():
            if used_lock and _density_lock[_name_of_compound]:
                continue
            atoms_per_cm3 = _utilities.get_atoms_per_cm3_of_layer(compound_dict=stack[_name_of_compound])
            stack[_name_of_compound]['atoms_per_cm3'] = atoms_per_cm3
        self.stack = stack

    def __fill_missing_keys(self, stack={}):
        _list_key_to_check = ['density']
        _list_key_value = [{'value': np.NaN,
                            'units': 'g/cm3'}]

        list_compound = stack.keys()
        for _key in list_compound:
            _inside_keys = stack[_key].keys()
            _key_value_to_search = zip(_list_key_to_check, _list_key_value)
            for _key_to_find, _value_to_add in _key_value_to_search:
                if not (_key_to_find in _inside_keys):
                    stack[_key][_key_to_find] = _value_to_add.copy()

        return stack
        
    def __update_layer_density(self, debug=False):
        '''calculate or update the layer density'''
        _stack = self.stack
        
        _density_lock = self.density_lock

        list_compound = _stack.keys()
        for _key in list_compound:
            if _density_lock[_key]:
                continue
            
            #if np.isnan(_stack[_key]['density']['value']):
                
            _list_ratio = _stack[_key]['stoichiometric_ratio']
            _list_density = []
            for _element in _stack[_key]['elements']:
                _list_density.append(_stack[_key][_element]['density']['value'])
                _compound_density = _utilities.get_compound_density(list_density=_list_density, 
                                                                    list_ratio=_list_ratio)   

            _stack[_key]['density']['value'] = _compound_density
        self.stack = _stack
                
    def __update_stack_with_isotopes_infos(self, stack={}):
        """retrieve the isotopes, isotopes file names, mass and atomic_ratio from each element in stack"""
        for _key in stack:
            isotopes_array = []
            _elements = stack[_key]['elements']
            for _element in _elements:
                _dict = _utilities.get_isotope_dicts(element=_element, database=self.database)
                stack[_key][_element] = _dict    
        
        stack = self.__fill_missing_keys(stack=stack)
        return stack

    def __update_density(self, compound='', element=''):
        """Re-calculate the density of the element given due to stoichiometric changes as
        well as the compound density (if density is not locked)
        
        Parameters:
        ===========
        compound: string (default is '') name of compound
        element: string (default is '') name of element
        """
        _density_element = 0
        list_ratio = self.stack[compound][element]['isotopes']['isotopic_ratio']
        list_density = self.stack[compound][element]['isotopes']['density']['value']
        ratio_density = zip(list_ratio, list_density)
        for _ratio, _density in ratio_density:
            _density_element += np.float(_ratio) * np.float(_density)
        self.stack[compound][element]['density']['value'] = _density_element
        
        _density_lock = self.density_lock
        if not _density_lock[compound]:
            self.__update_layer_density()
        
    def __update_molar_mass(self, compound='', element=''):
        """Re-calculate the molar mass of the element given due to stoichiometric changes

        Parameters:
        ==========
        compound: string (default is '') name of compound
        element: string (default is '') name of element
        """
        _molar_mass_element = 0
        list_ratio = self.stack[compound][element]['isotopes']['isotopic_ratio']
        list_mass = self.stack[compound][element]['isotopes']['mass']['value']
        ratio_mass = zip(list_ratio, list_mass)
        for _ratio, _mass in ratio_mass:
            _molar_mass_element += np.float(_ratio) * np.float(_mass)
        self.stack[compound][element]['molar_mass']['value'] = _molar_mass_element
        
    def __get_sigmas(self):
        """will populate the stack_sigma dictionary with the energy and sigma array
        for all the compound/element and isotopes"""
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
                _list_isotopic_ratio = _stack[_compound][_element]['isotopes']['isotopic_ratio']
                _iso_file_ratio = zip(_list_isotopes, _list_file_names, _list_isotopic_ratio)
                
                # _dict_sigma_isotopes_sum = {}
                _sigma_all_isotopes = 0
                _energy_all_isotpes = 0
                
                for _iso, _file, _ratio in _iso_file_ratio:
                    stack_sigma[_compound][_element][_iso] = {}
                    _file = os.path.join(_database_folder, _file)
                    _dict = _utilities.get_sigma(database_file_name=_file, 
                                                 E_min=self.energy_min,
                                                 E_max=self.energy_max,
                                                 E_step=self.energy_step)
                    stack_sigma[_compound][_element][_iso]['energy_eV'] = _dict['energy_eV']
                    stack_sigma[_compound][_element][_iso]['sigma_b'] = _dict['sigma_b'] * _ratio

                    # sigma for all isotopes with their isotopic ratio
                    _sigma_all_isotopes += _dict['sigma_b'] * _ratio
                    _energy_all_isotpes += _dict['energy_eV']

                # energy axis (x-axis) is averaged to take into account differences between x-axis of isotopes
                _mean_energy_all_isotopes = _energy_all_isotpes/len(_list_isotopes)
                stack_sigma[_compound][_element]['energy_eV'] = _mean_energy_all_isotopes
                stack_sigma[_compound][_element]['sigma_b'] = _sigma_all_isotopes
                    
        self.stack_sigma = stack_sigma

    def plot(self, transmission=False, x_axis='energy', mixed=True, all_layers=False, all_elements=False,
             all_isotopes=False, items_to_plot=[], time_unit='us', offset_us=2.99, time_resolution_us=0.16, source_to_detector_m=16.125):
        # offset delay values is normal 2.99 us with NONE actual MCP delay settings
        """display the transmission or attenuation of compound, element and/or isotopes specified

        Parameters:
        ===========
        transmission: boolean. True -> display transmission signal
                               False -> display the attenuation signal
        x_axis: string. Must be either 'energy' or 'lambda'
        mixed: boolean. True -> display the total of each layer
                        False -> not displayed
        all_layers: boolean. True -> display all layers
                             False -> not displayed
        all_elements: boolean. True -> display all elements signal
                               False -> not displayed
        all_isotopes: boolean. True -> display all isotopes signal
                               False -> not displayed
        items_to_plot: array that descibes what to plot
            ex:
                [['CoAg','Ag','107-Ag'], ['CoAg']]
            if the dictionary is empty, everything is plotted
        """
        plt.figure(figsize=[8, 8])

        _stack_signal = self.stack_signal
        _stack = self.stack
        _x_axis = self.total_signal['energy_eV']

        '''X-axis'''
        # determine values and labels for x-axis with options from
        # 'energy(eV)' & 'lambda(A)' & 'time(us)' & 'image number(#)'
        if x_axis == 'energy':
            x_axis_label = 'Energy (eV)'
        if x_axis == 'lambda':
            x_axis_label = u"Wavelength (\u212B)"
            _x_axis = _utilities.ev_to_angstroms(array=_x_axis)
            # plt.xlim(0, 1)
        if x_axis == 'time':
            if time_unit == 's':
                x_axis_label = 'Time (s)'
                _x_axis = _utilities.ev_to_s(array=_x_axis,
                                             source_to_detector_m=source_to_detector_m,
                                             offset_us=offset_us)
            if time_unit == 'us':
                x_axis_label = 'Time (us)'
                _x_axis = 1e6 * _utilities.ev_to_s(array=_x_axis,
                                                   source_to_detector_m=source_to_detector_m,
                                                   offset_us=offset_us)
            if time_unit == 'ns':
                x_axis_label = 'Time (ns)'
                _x_axis = 1e9 * _utilities.ev_to_s(array=_x_axis,
                                                   source_to_detector_m=source_to_detector_m,
                                                   offset_us=offset_us)
        if x_axis == 'number':
            x_axis_label = 'Image number (#)'
            _x_axis = _utilities.ev_to_image_number(array=_x_axis,
                                                    source_to_detector_m=source_to_detector_m,
                                                    offset_us=offset_us,
                                                    time_resolution_us=time_resolution_us)

        '''Y-axis'''
        # determine to plot transmission or attenuation
        # determine to put transmission or attenuation words for y-axis
        if transmission:
            y_axis_label = 'Neutron Transmission'
            y_axis_tag = 'transmission'
        else:
            y_axis_label = 'Neutron Attenuation'
            y_axis_tag = 'attenuation'

        if mixed:
            _y_axis = self.total_signal[y_axis_tag]
            plt.plot(_x_axis, _y_axis, label="Total")

        if all_layers:
            for _compound in _stack.keys():
                _y_axis = _stack_signal[_compound][y_axis_tag]
                plt.plot(_x_axis, _y_axis, label=_compound)

        if all_elements:
            for _compound in _stack.keys():
                for _element in _stack[_compound]['elements']:
                    _y_axis = _stack_signal[_compound][_element][y_axis_tag]
                    plt.plot(_x_axis, _y_axis, label="{}/{}".format(_compound, _element))

        if all_isotopes:
            for _compound in _stack.keys():
                for _element in _stack[_compound]['elements']:
                    for _isotope in _stack[_compound][_element]['isotopes']['list']:
                        _y_axis = _stack_signal[_compound][_element][_isotope][y_axis_tag]
                        plt.plot(_x_axis, _y_axis, label="{}/{}/{}".format(_compound, _element, _isotope))

        '''Y-axis for specified items_to_plot'''
        for _path_to_plot in items_to_plot:
            _path_to_plot = list(_path_to_plot)
            _live_path = _stack_signal
            _label = "/".join(_path_to_plot)
            while _path_to_plot:
                _item = _path_to_plot.pop(0)
                _live_path = _live_path[_item]
            _y_axis = _live_path[y_axis_tag]
            plt.plot(_x_axis, _y_axis, label=_label)

        plt.ylim(-0.01, 1.01)
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)
        plt.legend(loc='best')
        plt.show()
