import unittest
import numpy as np
import os

from ImagingReso._utilities import is_element_in_database
from ImagingReso._utilities import get_list_element_from_database
from ImagingReso._utilities import checking_stack

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
                          'thickness': 0.025}}
        _result_1 = checking_stack(stack=stack_1)
        self.assertTrue(_result_1)
        
        # complex set of stacks
        stack_2 = {'Co': {'elements': ['Co'],
                          'thickness': 0.03},
                   'GdEu': {'elements': ['Gd','Eu'],
                            'thickness': 0.025}}
        _result_2 = checking_stack(stack=stack_2)
        self.assertTrue(_result_2)
        
    def test_checking_stack_raises_value_error_if_element_missing_from_database(self):
        '''assert checking_stack raises an error if elements can not be found in database'''
        stack_2 = {'Al': {'elements': ['Al'],
                              'thickness': 0.03},
                       'GdEu': {'elements': ['Gd','Eu'],
                                'thickness': 0.025}}
        self.assertRaises(ValueError, checking_stack, stack=stack_2)
        
    def test_checking_stack_raises_value_error_if_thickness_has_wrong_format(self):
        '''assert checking_stack raises an error if thickness is not a number'''
        stack_2 = {'Ag': {'elements': ['Ag'],
                              'thickness': '0.025'},
                       'GdEu': {'elements': ['Gd','Eu'],
                                    'thickness': 0.025}}
        self.assertRaises(ValueError, checking_stack, stack=stack_2)
        