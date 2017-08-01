import unittest
import numpy as np
import os
import pprint

from ImagingReso.resonance import Resonance

class TestInitialization(unittest.TestCase):

    def test_correct_initialization_of_stack(self):
        '''assert correct defined stack is correctly saved'''
        _stack = {'CoAg': {'elements': ['Co','Ag'],
                           'stochiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stochiometric_ratio': [1],
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
                                   'stochiometric_ratio': [1,1],
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
                                 'stochiometric_ratio': [1],
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
        self.assertEqual(returned_stack['CoAg']['stochiometric_ratio'], expected_stack['CoAg']['stochiometric_ratio'])
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
                           'stochiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stochiometric_ratio': [1],
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
        

class TestGetterSetter(unittest.TestCase):
    
    def setUp(self):
        _stack = {'CoAg': {'elements': ['Co','Ag'],
                               'stochiometric_ratio': [1, 2],
                                   'thickness': {'value': 0.025,
                                                 'units': 'mm'},
                                   },
                      'U': {'elements': ['U'],
                                 'stochiometric_ratio': [1],
                                 'thickness': {'value': 0.03,
                                               'units': 'mm'},
                                 },
                          }
        self.o_reso = Resonance(stack=_stack)        
        
    # stochiometric ratio
    def test_retrieve_stochiometric_ratio_raises_error_if_unknown_compound(self):
        '''assert ValueError raised if wrong compound when getting stochiometric ratio'''
        self.assertRaises(ValueError, self.o_reso.get_stochiometric_ratio, compound='unknown')
        
    def test_if_element_misssing_use_compound_and_raises_error_if_wrong(self):
        '''assert ValueError raised if element does not exist'''
        self.assertRaises(ValueError, self.o_reso.get_stochiometric_ratio, compound='CoAg')
        
    def test_stochiometric_ratio_returned(self):
        '''assert the stochiometric ratio are correctly returned'''
        _stochiometric_ratio = self.o_reso.get_stochiometric_ratio(compound='U')
        _expected_dict = {'233-U': 0.0,
                          '234-U': 5.5e-5,
                          '235-U': 0.0072,
                          '238-U': 0.992745}
        self.assertEqual(_expected_dict['233-U'], _stochiometric_ratio['233-U'])
        self.assertEqual(_expected_dict['235-U'], _stochiometric_ratio['235-U'])
        self.assertEqual(_expected_dict['238-U'], _stochiometric_ratio['238-U'])
        
    def test_list_all_stochiometric_ratio(self):
        '''assert the entire stochiometric list is returned'''
        _stochiometric_ratio = self.o_reso.get_stochiometric_ratio()
        _expected_dict = {'U': {'U': {'233-U': 0.0,
                                      '234-U': 5.5e-5,
                                      '235-U': 0.0072,
                                      '238-U': 0.992745},
                                },
                          'CoAg': {'Ag': {'107-Ag': 0.51839,
                                          '109-Ag': 0.4816},
                                   'Co': {'58-Co': 0.0,
                                          '59-Co': 1.0},
                                   },
                          }
        self.assertEqual(_expected_dict['U']['U']['233-U'], _stochiometric_ratio['U']['U']['233-U'])
        self.assertEqual(_expected_dict['U']['U']['238-U'], _stochiometric_ratio['U']['U']['238-U'])
        self.assertEqual(_expected_dict['CoAg']['Ag']['107-Ag'], _stochiometric_ratio['CoAg']['Ag']['107-Ag'])
        
    def test_set_stochiometric_ratio_raises_value_error_if_wrong_compound(self):
        '''assert ValueError raised if wrong compound in stochiometric ratio setter'''
        self.assertRaises(ValueError, self.o_reso.set_stochiometric_ratio)
        self.assertRaises(ValueError, self.o_reso.set_stochiometric_ratio, compound='unknown')
        
    def test_set_stochiometric_ratio_raises_value_error_if_wrong_element(self):
        '''assert ValueError raised if wrong element in stochiometric ratio setter'''
        self.assertRaises(ValueError, self.o_reso.set_stochiometric_ratio, compound='CoAg')
        self.assertRaises(ValueError, self.o_reso.set_stochiometric_ratio, compound='CoAg', element='unknown')
        
    def test_set_stochiometric_ratio_has_correct_new_list_size(self):
        '''assert ValueRror raised if new list of ratio does not match old list size'''
        self.assertRaises(ValueError, self.o_reso.set_stochiometric_ratio, compound='U', element='U', list_ratio=[0, 1, 2])
        
    def test_set_stochiometric_ratio_correctly_calculates_new_molar_mass(self):
        '''assert molar mass is correctly calculated for new set of stochiometric coefficient'''
        self.o_reso.set_stochiometric_ratio(compound='CoAg', element='Co', list_ratio=[0.5, 0.5])
        new_molar_mass = self.o_reso.stack['CoAg']['Co']['molar_mass']['value']
        list_isotopes_mass = self.o_reso.stack['CoAg']['Co']['isotopes']['mass']['value']
        list_isotopes_ratio = self.o_reso.stack['CoAg']['Co']['isotopes']['isotopic_ratio']
        mass_ratio = zip(list_isotopes_mass, list_isotopes_ratio)
        expected_molar_mass = np.array([_m * _r for _m, _r in mass_ratio]).sum()
        self.assertAlmostEqual(new_molar_mass, expected_molar_mass, delta=0.0001)
        
    def test_set_stochiometric_ratio_correctly_calculates_new_density(self):
        '''assert density is correctly calculated for new set of stochiometric coefficient'''
        self.o_reso.set_stochiometric_ratio(compound='CoAg', element='Co', list_ratio=[0.5, 0.5])
        new_density = self.o_reso.stack['CoAg']['Co']['density']['value']
        list_density = self.o_reso.stack['CoAg']['Co']['isotopes']['density']['value']
        list_isotopes_ratio = self.o_reso.stack['CoAg']['Co']['isotopes']['isotopic_ratio']
        density_ratio = zip(list_density, list_isotopes_ratio)
        expected_density = np.array([_d * _r for _d, _r in density_ratio]).sum()
        self.assertAlmostEqual(new_density, expected_density, delta=0.0001)    
        
    # density
    def test_retrieve_density_raises_error_if_unknown_compound(self):
        '''assert ValueError raised if wrong compound when getting density'''
        self.assertRaises(ValueError, self.o_reso.get_density, compound='unknown')
        
    def test_if_element_misssing_use_compound_and_raises_error_if_wrong_when_getting_density(self):
        '''assert ValueError raised if element does not exist when getting density'''
        self.assertRaises(ValueError, self.o_reso.get_density, compound='CoAg')        
        
    def test_density_returned(self):
        '''assert the density are correctly returned'''
        _density = self.o_reso.get_density(compound='U')
        _expected_density = 18.95
        self.assertEqual(_density, _expected_density)
        
    def test_density_returned_all(self):
        '''assert the density of all element works'''
        _density_list = self.o_reso.get_density()
        _expected_density = {'CoAg': {'Co': 8.9,
                                      'Ag': 10.5,
                                      },
                             'U': {'U': 18.95,
                                   },
                             }
        self.assertEqual(_expected_density, _density_list)
        
    def test_set_density_raises_error_if_bad_compound_element_or_density(self):
        '''assert set density raises error if any of the parameters is wrong'''
        self.assertRaises(ValueError, self.o_reso.set_density)
        self.assertRaises(ValueError, self.o_reso.set_density, compound='unknown')
        self.assertRaises(ValueError, self.o_reso.set_density, compound='CoAg', element='unknown')
        self.assertRaises(ValueError, self.o_reso.set_density, compound='CoAg', element='Co', density='not_a_number')
        
    def test_set_density_works(self):
        '''assert set density works'''
        self.o_reso.set_density(compound='CoAg', element='Ag', density=50)
        _expected_density = 50
        _returned_density = self.o_reso.get_density(compound='CoAg', element='Ag')
        self.assertEqual(_expected_density, _returned_density)