import unittest
import numpy as np
import os

from ImagingReso._utilities import is_element_in_database, get_list_element_from_database

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
        print(_expected_list)
        self.assertEqual(_expected_list, list_elements)
        
        # ENDF_VII
        _database_1 = 'ENDF_VII'
        list_elements = get_list_element_from_database(database=_database_1)
        _expected_list = ['Ag','Gd','U','Au','O','Co']
        _expected_list = set([_element.lower() for _element in _expected_list])
        self.assertEqual(_expected_list, list_elements)
        