import unittest
import numpy as np
import os

from ImagingReso.resonance import Resonance

class TestInitialization(unittest.TestCase):
    
    def test_initialization_of_correct_elements(self):
        '''assert elements are correctly loaded'''

        # unique element
        _elements = ['Ag','Au','Hf']
        _thickness = [0.025, 0.025, 0.025]
        _o_reso = Resonance(elements=_elements, thicknesses=_thickness)
        _elements_expected = _elements.sort()
        _elements_returned = _o_reso.elements.sort()
        self.assertEqual(_elements_expected, _elements_returned)
    
        # duplicate element
        _elements = ['Ag','Au','Hf', 'Ag']
        _thickness = [0.025, 0.025, 0.025]
        _o_reso = Resonance(elements=_elements, thicknesses=_thickness)
        _elements_expected = list(set(_elements)).sort()
        _elements_returned = _o_reso.elements.sort()
        self.assertEqual(_elements_expected, _elements_returned)
        
    def test_initialization_raises_error_if_unknown_element(self):
        '''assert IOError is raised if element can not be found in database'''
        _elements = ['Unknown','Au','Hf', 'Ag']
        self.assertRaises(IOError, Resonance, elements=_elements)

    def test_initialization_must_contain_at_least_one_element(self):
        '''assert at least one element must be defined'''
        self.assertRaises(ValueError, _o_reso = Resonance)
        
    def test_initialization_must_contain_at_least_one_thickness(self):
        '''assert at least one thickness must be defined'''
        _elements = ['Ag']
        self.assertRaises(ValueError, Resonance, elements=_elements)
        
    def test_initialization_raises_error_if_elements_and_thickness_size_do_not_match(self):
        '''assert ValueError is raised when elements and thickness do not have the same size'''
        _elements = ['Ag','Au','Hf']
        _thickness = [0.025, 0.025]
        self.assertRaises(ValueError, Resonance, _elements, _thickness)
        