import unittest
import numpy as np
import os

from ImagingReso._utilities import is_element_in_database
from ImagingReso._utilities import get_list_element_from_database
from ImagingReso._utilities import checking_stack
from ImagingReso._utilities import formula_to_dictionary

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
                          'ratio': [1],
                          'thickness': 0.025}}
        _result_1 = checking_stack(stack=stack_1)
        self.assertTrue(_result_1)
        
        # complex set of stacks
        stack_2 = {'Co': {'elements': ['Co'],
                          'ratio': [1],
                          'thickness': 0.03},
                   'GdEu': {'elements': ['Gd','Eu'],
                            'ratio': [1,1],
                            'thickness': 0.025}}
        _result_2 = checking_stack(stack=stack_2)
        self.assertTrue(_result_2)
        
    def test_checking_stack_raises_value_error_if_element_missing_from_database(self):
        '''assert checking_stack raises an error if elements can not be found in database'''
        stack_2 = {'Al': {'elements': ['Al'],
                          'ratio': [1],
                          'thickness': 0.03},
                       'GdEu': {'elements': ['Gd','Eu'],
                                'ratio': [1,1],
                                'thickness': 0.025}}
        self.assertRaises(ValueError, checking_stack, stack=stack_2)
        
    def test_checking_stack_raises_value_error_if_thickness_has_wrong_format(self):
        '''assert checking_stack raises an error if thickness is not a number'''
        stack_2 = {'Ag': {'elements': ['Ag'],
                          'ratio': [1],
                          'thickness': '0.025'},
                   'GdEu': {'elements': ['Gd','Eu'],
                            'ratio': [1,1],
                            'thickness': 0.025}}
        self.assertRaises(ValueError, checking_stack, stack=stack_2)
        
    def test_raises_error_when_size_ratio_is_different_from_elements(self):
        '''assert checking_stack raises error if size of ratio and elements do not match'''
        stack = {'Ag': {'elements': ['Ag'],
                        'ratio': [1],
                        'thickness': 0.025},
                 'GdEu': {'elements': ['Gd','Eu'],
                          'ratio': [1],
                          'thickness': 0.025}}
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
        _dict_expected = {'Ag': {'elements': ['Ag'], 'ratio': [1], 'thickness': np.NaN}}
        self.assertEqual(_dict_returned, _dict_expected)

        # 'Ag2Co'
        _formula_2 = 'Ag2Co'
        _dict_returned = formula_to_dictionary(formula=_formula_2)
        _dict_expected = {'Ag2Co': {'elements': ['Ag','Co'], 'ratio': [2,1], 'thickness': np.NaN}}
        self.assertEqual(_dict_returned, _dict_expected)
        
        # 'Ag2CoU3'
        _formula_3 = 'Ag2CoU3'
        _dict_returned = formula_to_dictionary(formula=_formula_3)
        _dict_expected = {'Ag2CoU3': {'elements': ['Ag','Co','U'], 'ratio': [2,1,3], 'thickness': np.NaN}}
        self.assertEqual(_dict_returned, _dict_expected)
        
        # 'Ag2Co' with thickness=0.025
        _formula_2 = 'Ag2Co'
        _dict_returned = formula_to_dictionary(formula=_formula_2, thickness=0.025)
        _dict_expected = {'Ag2Co': {'elements': ['Ag','Co'], 'ratio': [2,1], 'thickness': 0.025}}
        self.assertEqual(_dict_returned, _dict_expected)
        