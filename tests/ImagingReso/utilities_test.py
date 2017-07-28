import unittest
import numpy as np
import os
import pprint

from ImagingReso._utilities import is_element_in_database
from ImagingReso._utilities import get_list_element_from_database
from ImagingReso._utilities import checking_stack
from ImagingReso._utilities import formula_to_dictionary
from ImagingReso._utilities import get_isotope_dicts
from ImagingReso._utilities import get_mass
from ImagingReso._utilities import get_density


class TestUtilities(unittest.TestCase):
    
    def test_is_element_in_database(self):
        '''assert is_element_in_database works correctly for good and bad input elements'''

        # empty element
        _element = ''
        _answer = is_element_in_database(element=_element)
        self.assertFalse(_answer)
    
        # element not in database
        _element = 'Fe'
        _answer = is_element_in_database(element=_element)
        self.assertFalse(_answer)
        
        # element in database
        _element = 'Co'
        _answer = is_element_in_database(element=_element)
        self.assertTrue(_answer)
        
    def test_get_list_element_from_database(self):
        '''assert the correct list of element is retrieved from the database'''

        # ENDF_VIII
        _database_1 = 'ENDF_VIII'
        list_elements = get_list_element_from_database(database=_database_1)
        _expected_list = ['Pb','Cd','Gd','Ta','Au','Ag','Eu','Sm','Co','O','Hf','B','In','W','U']
        _expected_list = set([_element.lower() for _element in _expected_list])
        self.assertEqual(_expected_list, list_elements)
        
        # ENDF_VII
        _database_1 = 'ENDF_VII'
        list_elements = get_list_element_from_database(database=_database_1)
        _expected_list = ['Ag','Gd','U','Au','O','Co']
        _expected_list = set([_element.lower() for _element in _expected_list])
        self.assertEqual(_expected_list, list_elements)
        
    def test_get_list_of_element_raise_error_if_wrong_database(self):
        '''assert ValueError if wrong database passed to get_list_element_from_database'''
        _database_1 = 'do_not_exist'
        self.assertRaises(ValueError, get_list_element_from_database, database=_database_1)
        
    def test_checking_stack(self):
        '''assert checking_stack_works in all good cases (1 or more stacks)'''
        
        # normal simple stack
        stack_1 = {'Ag': {'elements': ['Ag'],
                          'atomic_ratio': [1],
                          'thickness': {'value': 0.025,
                                        'units': 'mm'},
                          },
                   }
        _result_1 = checking_stack(stack=stack_1)
        self.assertTrue(_result_1)
        
        # complex set of stacks
        stack_2 = {'Co': {'elements': ['Co'],
                          'atomic_ratio': [1],
                          'thickness': {'value': 0.03,
                                        'units': 'mm'},
                          },
                   'GdEu': {'elements': ['Gd','Eu'],
                            'atomic_ratio': [1,1],
                            'thickness': {'value': 0.025,
                                          'units': 'mm'},
                            },
                   }
        _result_2 = checking_stack(stack=stack_2)
        self.assertTrue(_result_2)
        
    def test_checking_stack_raises_value_error_if_element_missing_from_database(self):
        '''assert checking_stack raises an error if elements can not be found in database'''
        stack_2 = {'Al': {'elements': ['Al'],
                          'atomic_ratio': [1],
                          'thickness': {'value': 0.03,
                                        'units': 'mm'},
                          },
                       'GdEu': {'elements': ['Gd','Eu'],
                                'atomic_ratio': [1,1],
                                'thickness': {'value': 0.025,
                                              'units': 'mm'},
                                },
                       }
        self.assertRaises(ValueError, checking_stack, stack=stack_2)
        
    def test_checking_stack_raises_value_error_if_thickness_has_wrong_format(self):
        '''assert checking_stack raises an error if thickness is not a number'''
        stack_2 = {'Ag': {'elements': ['Ag'],
                          'atomic_ratio': [1],
                          'thickness': {'value': '0.025',
                                        'units': 'mm'},
                          },
                   'GdEu': {'elements': ['Gd','Eu'],
                            'atomic_ratio': [1,1],
                            'thickness': {'value': 0.025,
                                          'units': 'mm'},
                            },
                   }
        self.assertRaises(ValueError, checking_stack, stack=stack_2)
        
    def test_raises_error_when_size_atomic_ratio_is_different_from_elements(self):
        '''assert checking_stack raises error if size of atomic_ratio and elements do not match'''
        stack = {'Ag': {'elements': ['Ag'],
                        'atomic_ratio': [1],
                        'thickness': {'value': 0.025,
                                      'units': 'mm'},
                        },
                 'GdEu': {'elements': ['Gd','Eu'],
                          'atomic_ratio': [1],
                          'thickness': {'value': 0.025,
                                        'units': 'mm'},
                          },
                 }
        self.assertRaises(ValueError, checking_stack, stack=stack)
        
    def test_formula_to_dictionary_raises_error_when_unknow_element(self):
        '''assert formula_to_dictionary raises error if element is unknown'''
        _formula = 'AlCo'
        self.assertRaises(ValueError, formula_to_dictionary, formula=_formula)
        
    def test_formula_to_dictionary_works_with_various_cases(self):
        '''assert formulla_to_dictionary works in all cases'''
        
        # 'Ag'
        _formula_1 = 'Ag'
        _dict_returned = formula_to_dictionary(formula=_formula_1)
        _dict_expected = {'Ag': {'elements': ['Ag'], 'atomic_ratio': [1], 'thickness': {'value': np.NaN, 'units': 'mm'}}}
        self.assertEqual(_dict_returned, _dict_expected)

        # 'Ag2Co'
        _formula_2 = 'Ag2Co'
        _dict_returned = formula_to_dictionary(formula=_formula_2)
        _dict_expected = {'Ag2Co': {'elements': ['Ag','Co'], 'atomic_ratio': [2,1], 'thickness': {'value': np.NaN, 'units': 'mm'}}}
        self.assertEqual(_dict_returned, _dict_expected)
        
        # 'Ag2CoU3'
        _formula_3 = 'Ag2CoU3'
        _dict_returned = formula_to_dictionary(formula=_formula_3)
        _dict_expected = {'Ag2CoU3': {'elements': ['Ag','Co','U'], 'atomic_ratio': [2,1,3], 'thickness': {'value': np.NaN, 'units': 'mm'}}}
        self.assertEqual(_dict_returned, _dict_expected)
        
        # 'Ag2Co' with thickness=0.025
        _formula_2 = 'Ag2Co'
        _dict_returned = formula_to_dictionary(formula=_formula_2, thickness=0.025)
        _dict_expected = {'Ag2Co': {'elements': ['Ag','Co'], 'atomic_ratio': [2,1], 'thickness': {'value': 0.025, 'units': 'mm'}}}
        self.assertEqual(_dict_returned, _dict_expected)
        
    def test_get_isotope_dicts_returns_correct_dictionary(self):
        '''assert get_isotope_dict works with typical entry element Ag'''
        _element = 'Ag'
        _dict_returned = get_isotope_dicts(element=_element)
        _dict_expected = {'density': {'value': 10.5,
                                      'units': 'g/mol'},
                          'isotopes': {'list': ['107-Ag','109-Ag'],
                                       'file_names': ['Ag-107.csv','Ag-109.csv'],
                                       'mass': {'value': [106.905093, 108.904756],
                                                'units': 'g/mol'},
                                       'atomic_ratio': [0.51839, 0.481610]},
                          'molar_mass': {'value': 107.8682,
                                         'units': 'g/cm3'},
                          }
        # list of isotopes
        self.assertEqual(_dict_returned['isotopes']['list'], _dict_expected['isotopes']['list'])
        # names of isotopes
        self.assertEqual(_dict_returned['isotopes']['file_names'], _dict_expected['isotopes']['file_names'])
        # mass of isotopes
        self.assertEqual(_dict_returned['isotopes']['mass']['value'], _dict_expected['isotopes']['mass']['value'])
        # atomic_ratio
        self.assertAlmostEqual(_dict_returned['isotopes']['atomic_ratio'][0], _dict_expected['isotopes']['atomic_ratio'][0], delta=0.0001)
        self.assertAlmostEqual(_dict_returned['isotopes']['atomic_ratio'][1], _dict_expected['isotopes']['atomic_ratio'][1], delta=0.0001)
        # density
        self.assertEqual(_dict_returned['density']['value'], _dict_expected['density']['value'])
        # molar mass
        self.assertEqual(_dict_returned['molar_mass']['value'], _dict_expected['molar_mass']['value'])
        
    def test_get_isotope_returns_empty_dict_if_missing_element(self):
        '''assert get_isotopes_dict returns empty dict if element can not be found such as Al'''
        _element = 'Al'
        _dict_returned = get_isotope_dicts(element=_element)
        _dict_expected = {'isotopes': {'list': [],
                                       'file_names': [],
                                       'mass': {'value': [],
                                                'units': 'g/mol',
                                                },
                                       'atomic_ratio': []},
                          'density': {'value': np.NaN,
                                      'units': 'g/cm3'},
                          'molar_mass': {'value': np.NaN,
                                         'units': 'g/mol',
                                         },
                          }
        self.assertEqual(_dict_returned, _dict_expected)
        
    def test_get_mass(self):
        '''assert get_mass works for isotopes and elements'''
        _isotope = '107-Ag'
        _returned_mass = get_mass(_isotope)
        _expected_mass = 106.905093
        self.assertAlmostEqual(_returned_mass, _expected_mass, delta=0.00001)
        
        _element = 'Ag'
        _returned_mass = get_mass(_element)
        _expected_mass = 107.8682
        self.assertEqual(_returned_mass, _expected_mass)
        
    def test_get_density(self):
        '''assert get_density works'''
        _element = 'Ag'
        _returned_density = get_density(_element)
        _expected_density = 10.5
        self.assertEqual(_returned_density, _expected_density)