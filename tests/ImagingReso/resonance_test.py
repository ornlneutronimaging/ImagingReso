import unittest
import numpy as np
import os

from ImagingReso.resonance import Resonance

class TestInitialization(unittest.TestCase):

    def test_correct_initialization_of_stack(self):
        '''assert correct defined stack is correctly saved'''
        _stack = {'CoAg': {'elements': ['Co','Ag'],
                           'ratio': [1, 2],
                           'thickness': 0.025},
                  'Ag': {'elements': ['Ag'],
                         'ratio': [1],
                         'thickness': 0.03}}
        o_reso = Resonance(stack=_stack)
        _stack_returned = o_reso.stack
        self.assertEqual(_stack, _stack_returned)
    
    def test_adding_layer(self):
        '''assert adding_layer works'''
        o_reso = Resonance()
        
        # layer 1
        layer1 = 'CoAg'
        thickness1 = 0.025
        o_reso.add_layer(formula=layer1, thickness=thickness1)
        
        # layer 2
        layer2 = 'Ag'
        thickness2 = 0.1
        o_reso.add_layer(formula=layer2, thickness=thickness2)        
        
        returned_stack = o_reso.stack
        expected_stack = {'CoAg': {'elements':['Co','Ag'],
                                   'ratio': [1,1],
                                   'thickness': 0.025},
                          'Ag': {'elements': ['Ag'],
                                 'ratio': [1],
                                 'thickness': 0.1}}
        self.assertEqual(returned_stack, expected_stack)
        
    def test_listing_isotopes_via_init_method(self):
        '''assert list of isotopes and database file names correctly retrieved via init method'''
        _stack = {'CoAg': {'elements': ['Co','Ag'],
                               'ratio': [1, 2],
                               'thickness': 0.025},
                      'Ag': {'elements': ['Ag'],
                             'ratio': [1],
                             'thickness': 0.03}}
        o_reso = Resonance(stack=_stack)
        _isotopes_returned = o_reso.isotopes
        _isotopes_expected = {'Co': {'isotopes': ['58-Co','59-Co'],
                                     'file_names': ['Co-58.csv','Co-59.csv']},
                              'Ag': {'isotopes': ['107-Ag','109-Ag'],
                                     'file_names': ['Ag-107.csv','Ag-109.csv']}}
        self.assertEqual(_isotopes_returned, _isotopes_expected)
        
    def test_listing_isotopes_via_add_layer_method(self):
        '''assert list of isotopes and database file names correctly retrieved via add_layer'''
        o_reso = Resonance()
    
        # layer 1
        layer1 = 'CoAg'
        thickness1 = 0.025
        o_reso.add_layer(formula=layer1, thickness=thickness1)
    
        # layer 2
        layer2 = 'Ag'
        thickness2 = 0.1
        o_reso.add_layer(formula=layer2, thickness=thickness2)             
        
        _isotopes_retuned = o_reso.isotopes
        _isotopes_expected = {'Co': {'isotopes': ['58-Co','59-Co'],
                                         'file_names': ['Co-58.csv','Co-59.csv']},
                                  'Ag': {'isotopes': ['107-Ag','109-Ag'],
                                         'file_names': ['Ag-107.csv','Ag-109.csv']}}
        self.assertEqual(_isotopes_expected, _isotopes_retuned)