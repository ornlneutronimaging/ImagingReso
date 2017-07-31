import unittest
import numpy as np
import os
import pprint

from ImagingReso.resonance import Resonance

class TestInitialization(unittest.TestCase):

    def test_correct_initialization_of_stack(self):
        '''assert correct defined stack is correctly saved'''
        _stack = {'CoAg': {'elements': ['Co','Ag'],
                           'atomic_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'atomic_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
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
                                   'atomic_ratio': [1,1],
                                   'thickness': {'value': 0.025,
                                                 'units': 'mm'},
                                   'Co': {'isotopes': {'file_names':['Co-58.csv','Co-59.csv'],
                                                       'list': ['58-Co','59-Co'],
                                                       'mass': {'value': [57.9357576, 58.9332002],
                                                                'units': 'g/mol',
                                                                },
                                                       'isotopic_ratio': [0.0,1.0],
                                                       },
                                          'density': {'value': 8.9,
                                                      'units': 'g/cm3'},
                                          'molar_mass': {'value': 58.9332,
                                                         'units': 'g/mol'},
                                          },
                                   'Ag': {'isotopes': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                       'list': ['107-Ag','109-Ag'],
                                                       'mass': {'value': [106.905093, 108.904756],
                                                                'units': 'g/mol',
                                                                },
                                                       'isotopic_ratio': [0.51839,0.48161000],
                                                       },
                                          'density': {'value': 10.5,
                                                      'units': 'g/cm3'},
                                          'molar_mass': {'value': 107.8682,
                                                         'units': 'g/cm3'},
                                          },
                                   },
                          'Ag': {'elements': ['Ag'],
                                 'atomic_ratio': [1],
                                 'thickness': {'value': 0.1,
                                               'units': 'mm'},
                                 'Ag': {'isotopes': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                     'list': ['107-Ag','109-Ag'],
                                                     'mass': {'value': [106.905093, 108.904756],
                                                              'units': 'g/mol',
                                                              },
                                                      'isotopic_ratio': [0.51839,0.48161000],
                                                      },
                                        'density': {'value': 10.5,
                                                    'units': 'g/cm3'},
                                        'molar_mass': {'value': 107.8682,
                                                       'units': 'g/mol'},
                                        },
                                 },
                          }         

        # CoAg
        # elements
        self.assertEqual(returned_stack['CoAg']['elements'], expected_stack['CoAg']['elements'])
        # atomic_atomic_ratio
        self.assertEqual(returned_stack['CoAg']['atomic_ratio'], expected_stack['CoAg']['atomic_ratio'])
        # thickness
        self.assertEqual(returned_stack['CoAg']['thickness']['value'], expected_stack['CoAg']['thickness']['value'])
        self.assertEqual(returned_stack['CoAg']['thickness']['units'], expected_stack['CoAg']['thickness']['units'])
        # isotopes Co
        # file names
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['file_names'], 
                         expected_stack['CoAg']['Co']['isotopes']['file_names'])
        # list
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['list'], 
                         expected_stack['CoAg']['Co']['isotopes']['list'])
        # mass
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['mass']['value'], 
                         expected_stack['CoAg']['Co']['isotopes']['mass']['value'])
        self.assertEqual(returned_stack['CoAg']['Co']['isotopes']['mass']['units'], 
                         expected_stack['CoAg']['Co']['isotopes']['mass']['units'])
        # atomic_ratio Co
        self.assertAlmostEqual(returned_stack['CoAg']['Co']['isotopes']['isotopic_ratio'][0],
                               expected_stack['CoAg']['Co']['isotopes']['isotopic_ratio'][0],
                               delta=0.0001)
        self.assertAlmostEqual(returned_stack['CoAg']['Co']['isotopes']['isotopic_ratio'][1],
                               expected_stack['CoAg']['Co']['isotopes']['isotopic_ratio'][1],
                               delta=0.0001)
        # isotopic_ratio Ag
        self.assertAlmostEqual(returned_stack['CoAg']['Ag']['isotopes']['isotopic_ratio'][0],
                                   expected_stack['CoAg']['Ag']['isotopes']['isotopic_ratio'][0],
                                   delta=0.0001)
        self.assertAlmostEqual(returned_stack['CoAg']['Ag']['isotopes']['isotopic_ratio'][1],
                                   expected_stack['CoAg']['Ag']['isotopes']['isotopic_ratio'][1],
                                   delta=0.0001)
        
        # density
        self.assertEqual(returned_stack['CoAg']['Ag']['density']['value'], 
                         expected_stack['CoAg']['Ag']['density']['value'])
        self.assertEqual(returned_stack['CoAg']['Co']['density']['value'], 
                         expected_stack['CoAg']['Co']['density']['value'])
        # molar mass
        self.assertEqual(returned_stack['CoAg']['Ag']['molar_mass']['value'], 
                         expected_stack['CoAg']['Ag']['molar_mass']['value'])
        self.assertEqual(returned_stack['CoAg']['Co']['molar_mass']['value'], 
                         expected_stack['CoAg']['Co']['molar_mass']['value'])
        
    def test_element_metadata_via_stack_initialization(self):
        '''assert __element_metadata is correctly populated using stack initialization'''

        _stack = {'CoAg': {'elements': ['Co','Ag'],
                           'atomic_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'atomic_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        o_reso = Resonance(stack=_stack)        
        
        # molar mass
        stack = o_reso.stack
        co_mass_expected = 58.9332
        ag_mass_expected = 107.8682
        self.assertEqual(co_mass_expected, stack['CoAg']['Co']['molar_mass']['value'])
        self.assertEqual(ag_mass_expected, stack['Ag']['Ag']['molar_mass']['value'])
        
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
        self.assertEqual(co_mass_expected, stack['CoAg']['Co']['molar_mass']['value'])
        self.assertEqual(ag_mass_expected, stack['CoAg']['Ag']['molar_mass']['value'])
        self.assertEqual(ag_mass_expected, stack['Ag']['Ag']['molar_mass']['value'])
        
        # density
        co_density_expected = 8.9
        ag_density_expected = 10.5
        self.assertEqual(co_density_expected, stack['CoAg']['Co']['density']['value'])
        self.assertEqual(ag_density_expected, stack['Ag']['Ag']['density']['value'])