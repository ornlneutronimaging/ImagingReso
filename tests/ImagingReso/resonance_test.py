import unittest
import numpy as np
import os

from ImagingReso.resonance import Resonance

class TestInitialization(unittest.TestCase):
    
    def test_initialization_of_correct_elements(self):
        '''assert elements are correctly loaded'''
        _elements = ['Co','Al','Fe']
        _o_reso = Resonance(elements=_elements)
        self.assertEqual(_elements, _o_reso.elements)
    
