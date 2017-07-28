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
                                                        'ratio': [1,1],
                                                        },
                                                 },
                                                 {'Ag': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                         'list': ['107-Ag','109-Ag'],
                                                         'mass': [106.905093, 108.904756],
                                                         'ratio': [1,1],
                                                         },
                                                  }
                                                 ]},
                          'Ag': {'elements': ['Ag'],
                                 'ratio': [1],
                                 'thickness': 0.1,
                                 'isotopes': [{'Ag': {'file_names': ['Ag-107.csv','Ag-109.csv'],
                                                      'list': ['107-Ag','109-Ag'],
                                                      'mass': [106.905093, 108.904756],
                                                      'ratio': [1,1],
                                                      },
                                               },
                                              ]},
                          }     
        
        self.assertEqual(returned_stack, expected_stack)
        
   