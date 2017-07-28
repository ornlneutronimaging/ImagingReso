import unittest
import numpy as np
import os
import pprint

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
                                   'thickness': 0.025,
                                   'Co': {'isotopes': {'file_names':['Co-58.csv','Co-59.csv'],
                                                       'list': ['58-Co','59-Co'],
                                                       'mass': [57.9357576, 58.9332002],
                                                       'ratio': [0.0,1.0],
                                                       },
                                          'density': 8.9,
                                          'molar_mass': 58.9332,
                                          },
                                   'Ag': {'isotopes': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                       'list': ['107-Ag','109-Ag'],
                                                       'mass': [106.905093, 108.904756],
                                                       'ratio': [0.51839,0.48161000],
                                                       },
                                          'density': 10.5,
                                          'molar_mass': 107.8682,
                                          },
                                   },
                          'Ag': {'elements': ['Ag'],
                                 'ratio': [1],
                                 'thickness': 0.1,
                                 'Ag': {'isotopes': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                     'list': ['107-Ag','109-Ag'],
                                                     'mass': [106.905093, 108.904756],
                                                      'ratio': [0.51839,0.48161000],
                                                      },
                                        'density': 10.5,
                                        'molar_mass': 107.8682,
                                        },
                                 },
                          }         

        # CoAg
        # elements
        self.assertEqual(returned_stack['CoAg']['elements'], expected_stack['CoAg']['elements'])
        # ratio
        self.assertEqual(returned_stack['CoAg']['ratio'], expected_stack['CoAg']['ratio'])
        # thickness
        self.assertEqual(returned_stack['CoAg']['thickness'], expected_stack['CoAg']['thickness'])
        # isotopes Co
        # file names
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['file_names'], 
                         expected_stack['CoAg']['Co']['isotopes']['file_names'])
        # list
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['list'], 
                         expected_stack['CoAg']['Co']['isotopes']['list'])
        # mass
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['mass'], 
                         expected_stack['CoAg']['Co']['isotopes']['mass'])
        # ratio Co
        self.assertAlmostEqual(returned_stack['CoAg']['Co']['isotopes']['ratio'][0],
                               expected_stack['CoAg']['Co']['isotopes']['ratio'][0],
                               delta=0.0001)
        self.assertAlmostEqual(returned_stack['CoAg']['Co']['isotopes']['ratio'][1],
                               expected_stack['CoAg']['Co']['isotopes']['ratio'][1],
                               delta=0.0001)
        # ratio Ag
        self.assertAlmostEqual(returned_stack['CoAg']['Ag']['isotopes']['ratio'][0],
                                   expected_stack['CoAg']['Ag']['isotopes']['ratio'][0],
                                   delta=0.0001)
        self.assertAlmostEqual(returned_stack['CoAg']['Ag']['isotopes']['ratio'][1],
                                   expected_stack['CoAg']['Ag']['isotopes']['ratio'][1],
                                   delta=0.0001)
        
        # density
        self.assertEqual(returned_stack['CoAg']['Ag']['density'], 
                         expected_stack['CoAg']['Ag']['density'])
        self.assertEqual(returned_stack['CoAg']['Co']['density'], 
                         expected_stack['CoAg']['Co']['density'])
        # molar mass
        self.assertEqual(returned_stack['CoAg']['Ag']['molar_mass'], 
                         expected_stack['CoAg']['Ag']['molar_mass'])
        self.assertEqual(returned_stack['CoAg']['Co']['molar_mass'], 
                         expected_stack['CoAg']['Co']['molar_mass'])
        
    def test_element_metadata_via_stack_initialization(self):
        '''assert __element_metadata is correctly populated using stack initialization'''

        _stack = {'CoAg': {'elements': ['Co','Ag'],
                           'ratio': [1, 2],
                           'thickness': 0.025},
                  'Ag': {'elements': ['Ag'],
                         'ratio': [1],
                         'thickness': 0.03}}
        o_reso = Resonance(stack=_stack)        
        
        # molar mass
        stack = o_reso.stack
        co_mass_expected = 58.9332
        ag_mass_expected = 107.8682
        self.assertEqual(co_mass_expected, stack['CoAg']['Co']['molar_mass'])
        self.assertEqual(ag_mass_expected, stack['Ag']['Ag']['molar_mass'])
        
    def test_element_metadata_via_add_layer_initialization(self):
        '''assert __element_metadata is correctly populated using add layer initialization'''
        o_reso = Resonance()
        
        # layer 1
        layer1 = 'CoAg'
        thickness1 = 0.025
        o_reso.add_layer(formula=layer1, thickness=thickness1)
        
        # layer 2
        layer2 = 'Ag'
        thickness2 = 0.1
        o_reso.add_layer(formula=layer2, thickness=thickness2)        
    
        stack = o_reso.stack

        # molar mass
        co_mass_expected = 58.9332
        ag_mass_expected = 107.8682
        self.assertEqual(co_mass_expected, stack['CoAg']['Co']['molar_mass'])
        self.assertEqual(ag_mass_expected, stack['CoAg']['Ag']['molar_mass'])
        self.assertEqual(ag_mass_expected, stack['Ag']['Ag']['molar_mass'])
        
        # density
        co_density_expected = 8.9
        ag_density_expected = 10.5
        self.assertEqual(co_density_expected, stack['CoAg']['Co']['density'])
        self.assertEqual(ag_density_expected, stack['Ag']['Ag']['density'])