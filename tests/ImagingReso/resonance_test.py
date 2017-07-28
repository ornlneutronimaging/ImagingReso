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
                                   'isotopes': [{'Co': {'file_names':['Co-58.csv','Co-59.csv'],
                                                        'list': ['58-Co','59-Co'],
                                                        'mass': [57.9357576, 58.9332002],
                                                        'ratio': [0.0,1.0],
                                                        },
                                                 },
                                                 {'Ag': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                         'list': ['107-Ag','109-Ag'],
                                                         'mass': [106.905093, 108.904756],
                                                         'ratio': [0.51839,0.48161000],
                                                         },
                                                  }
                                                 ]},
                          'Ag': {'elements': ['Ag'],
                                 'ratio': [1],
                                 'thickness': 0.1,
                                 'isotopes': [{'Ag': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                      'list': ['107-Ag','109-Ag'],
                                                      'mass': [106.905093, 108.904756],
                                                      'ratio': [0.51839,0.48161000],
                                                      },
                                               },
                                              ]},
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
        self.assertEqual(returned_stack['CoAg']['isotopes'][0]['Co']['file_names'], 
                         expected_stack['CoAg']['isotopes'][0]['Co']['file_names'])
        # list
        self.assertEqual(returned_stack['CoAg']['isotopes'][0]['Co']['list'], 
                         expected_stack['CoAg']['isotopes'][0]['Co']['list'])
        # mass
        self.assertEqual(returned_stack['CoAg']['isotopes'][0]['Co']['mass'], 
                         expected_stack['CoAg']['isotopes'][0]['Co']['mass'])
        # ratio Co
        self.assertAlmostEqual(returned_stack['CoAg']['isotopes'][0]['Co']['ratio'][0],
                               expected_stack['CoAg']['isotopes'][0]['Co']['ratio'][0],
                               delta=0.0001)
        self.assertAlmostEqual(returned_stack['CoAg']['isotopes'][0]['Co']['ratio'][1],
                               expected_stack['CoAg']['isotopes'][0]['Co']['ratio'][1],
                               delta=0.0001)
        # ratio Ag
        self.assertAlmostEqual(returned_stack['CoAg']['isotopes'][1]['Ag']['ratio'][0],
                                   expected_stack['CoAg']['isotopes'][1]['Ag']['ratio'][0],
                                   delta=0.0001)
        self.assertAlmostEqual(returned_stack['CoAg']['isotopes'][1]['Ag']['ratio'][1],
                                   expected_stack['CoAg']['isotopes'][1]['Ag']['ratio'][1],
                                   delta=0.0001)
        

        
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
        element_infos = o_reso.get_element_infos()
        co_mass_expected = 58.9332
        ag_mass_expected = 107.8682
        self.assertEqual(co_mass_expected, element_infos['Co']['molar_mass'])
        self.assertEqual(ag_mass_expected, element_infos['Ag']['molar_mass'])
        
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
    
        element_infos = o_reso.get_element_infos()

        # molar mass
        co_mass_expected = 58.9332
        ag_mass_expected = 107.8682
        self.assertEqual(co_mass_expected, element_infos['Co']['molar_mass'])
        self.assertEqual(ag_mass_expected, element_infos['Ag']['molar_mass'])
        
        # density
        co_density_expected = 8.9
        ag_density_expected = 10.5
        self.assertEqual(co_density_expected, element_infos['Co']['density'])
        self.assertEqual(ag_density_expected, element_infos['Ag']['density'])