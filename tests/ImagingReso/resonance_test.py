import unittest
import numpy as np
import os

from ImagingReso.resonance import Resonance

class TestInitialization(unittest.TestCase):
    
    def test_initialization_of_correct_elements(self):
        '''assert elements are correctly loaded'''

        # unique element
        _elements = ['Ag','Au','Hf']
        _o_reso = Resonance(elements=_elements)
        _elements_expected = _elements.sort()
        _elements_returned = _o_reso.elements.sort()
        self.assertEqual(_elements_expected, _elements_returned)
    
        # duplicate element
        _elements = ['Ag','Au','Hf', 'Ag']
        _o_reso = Resonance(elements=_elements)
        _elements_expected = list(set(_elements)).sort()
        _elements_returned = _o_reso.elements.sort()
        self.assertEqual(_elements_expected, _elements_returned)
        
    def test_initialization_raises_error_if_unknown_element(self):
        '''assert IOError is raised if element can not be found in database'''
        _elements = ['Unknown','Au','Hf', 'Ag']
        self.assertRaises(IOError, Resonance, elements=_elements)

