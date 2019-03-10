import unittest
import numpy as np

from ImagingReso.resonance import Resonance


class TestInitialization(unittest.TestCase):
    database = '_data_for_unittest'

    def test_E_min(self):
        """assert E can not be set below a given threshold"""
        energy_min = 1e-6
        self.assertRaises(ValueError, Resonance, energy_min=energy_min, database=self.database)

    def test_E_max(self):
        """assert E can not be set above a given threshold"""
        energy_max = 1e9
        self.assertRaises(ValueError, Resonance, energy_max=energy_max, database=self.database)

    def test_database(self):
        """assert ValueError if unsupported or wrong database passed to Resonance()"""
        self.assertRaises(ValueError, Resonance, database='_do_not_exist')

    def test_str(self):
        """assert print(object) works"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        energy_min = 10
        energy_max = 150
        energy_step = 1
        o_reso = Resonance(stack=_stack, energy_max=energy_max, energy_min=energy_min,
                           energy_step=energy_step, database=self.database)
        self.assertIsInstance(o_reso.__str__(), str)

    def test_repr(self):
        """assert object works"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        energy_min = 10
        energy_max = 150
        energy_step = 1
        o_reso = Resonance(stack=_stack, energy_max=energy_max, energy_min=energy_min,
                           energy_step=energy_step, database=self.database)
        self.assertIsInstance(o_reso.__repr__(), str)

    def test_initialization_of_object(self):
        """assert object is correctly initialized with energy min, max and step"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        energy_min = 10
        energy_max = 150
        energy_step = 1
        o_reso = Resonance(stack=_stack, energy_max=energy_max, energy_min=energy_min,
                           energy_step=energy_step, database=self.database)
        self.assertEqual(o_reso.energy_max, energy_max)
        self.assertEqual(o_reso.energy_min, energy_min)
        self.assertEqual(o_reso.energy_step, energy_step)

    def test_initialization_with_same_E_min_and_max_raises_error(self):
        """assert ValueError is raised if E_min == E_max"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        energy_min = 150
        energy_max = 150
        energy_step = 1
        self.assertRaises(ValueError, Resonance, stack=_stack, energy_max=energy_max, energy_min=energy_min,
                          energy_step=energy_step, database=self.database)

    def test_initialization_E_step_bigger_than_E_range_raises_error(self):
        """assert ValueError is raised if E_min == E_max"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        energy_min = 1
        energy_max = 10
        energy_step = 11
        self.assertRaises(ValueError, Resonance, stack=_stack, energy_max=energy_max, energy_min=energy_min,
                          energy_step=energy_step, database=self.database)

    def test_get_sigma_isotopes(self):
        """assert get_sigma works"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        energy_min = 10
        energy_max = 150
        energy_step = 1
        o_reso = Resonance(stack=_stack, energy_max=energy_max, energy_min=energy_min,
                           energy_step=energy_step, database=self.database)
        stack_sigma = o_reso.stack_sigma

        # for isotopes
        self.assertEqual(len(stack_sigma), 2)
        self.assertEqual(stack_sigma['Ag']['Ag']['107-Ag']['energy_eV'][0], 10)
        self.assertEqual(stack_sigma['Ag']['Ag']['107-Ag']['energy_eV'][-1], 150)

        # for elements
        self.assertEqual(stack_sigma['Ag']['Ag']['energy_eV'][0], 10)

    def test_correct_initialization_of_stack(self):
        """assert correct defined stack is correctly saved"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        o_reso = Resonance(stack=_stack, database=self.database)
        _stack_returned = o_reso.stack
        self.assertEqual(_stack, _stack_returned)

    def test_adding_layer(self):
        """assert adding_layer works"""
        o_reso = Resonance(database=self.database)

        # layer 1
        layer1 = 'CoAg'
        thickness1 = 0.025
        o_reso.add_layer(formula=layer1, thickness=thickness1)

        # layer 2
        layer2 = 'Ag'
        thickness2 = 0.1
        density2 = 0.5
        o_reso.add_layer(formula=layer2, thickness=thickness2, density=density2)

        returned_stack = o_reso.stack
        expected_stack = {'CoAg': {'elements': ['Co', 'Ag'],
                                   'stoichiometric_ratio': [1, 1],
                                   'thickness': {'value': 0.025,
                                                 'units': 'mm'},
                                   'density': {'value': 9.7,
                                               'units': 'g/cm3'},
                                   'Co': {'isotopes': {'file_names': ['Co-58.csv', 'Co-59.csv'],
                                                       'list': ['58-Co', '59-Co'],
                                                       'mass': {'value': [57.9357576, 58.9332002],
                                                                'units': 'g/mol',
                                                                },
                                                       'isotopic_ratio': [0.0, 1.0],
                                                       },
                                          'density': {'value': 8.9,
                                                      'units': 'g/cm3'},
                                          'molar_mass': {'value': 58.9332,
                                                         'units': 'g/mol'},
                                          },
                                   'Ag': {'isotopes': {'file_names': ['Ag-107.csv', 'Ag-109.csv'],
                                                       'list': ['107-Ag', '109-Ag'],
                                                       'mass': {'value': [106.905093, 108.904756],
                                                                'units': 'g/mol',
                                                                },
                                                       'isotopic_ratio': [0.51839, 0.48161000],
                                                       },
                                          'density': {'value': 10.5,
                                                      'units': 'g/cm3'},
                                          'molar_mass': {'value': 107.8682,
                                                         'units': 'g/cm3'},
                                          },
                                   },
                          'Ag': {'elements': ['Ag'],
                                 'stoichiometric_ratio': [1],
                                 'thickness': {'value': 0.1,
                                               'units': 'mm'},
                                 'density': {'value': 0.5,
                                             'units': 'g/cm3'},
                                 'Ag': {'isotopes': {'file_names': ['Ag-107.csv', 'Ag-109.csv'],
                                                     'list': ['107-Ag', '109-Ag'],
                                                     'mass': {'value': [106.905093, 108.904756],
                                                              'units': 'g/mol',
                                                              },
                                                     'isotopic_ratio': [0.51839, 0.48161000],
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
        self.assertEqual(returned_stack['CoAg']['stoichiometric_ratio'], expected_stack['CoAg']['stoichiometric_ratio'])
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

        # layer density
        self.assertEqual(returned_stack['Ag']['density']['value'],
                         expected_stack['Ag']['density']['value'])
        self.assertAlmostEqual(returned_stack['CoAg']['density']['value'],
                               expected_stack['CoAg']['density']['value'],
                               delta=0.1)

        # element density
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
        """assert __element_metadata is correctly populated using stack initialization"""

        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         },
                  }
        o_reso = Resonance(stack=_stack, database=self.database)

        # molar mass
        stack = o_reso.stack
        co_mass_expected = 58.9332
        ag_mass_expected = 107.8682
        self.assertEqual(co_mass_expected, stack['CoAg']['Co']['molar_mass']['value'])
        self.assertEqual(ag_mass_expected, stack['Ag']['Ag']['molar_mass']['value'])

    def test_element_metadata_via_add_layer_initialization(self):
        """assert __element_metadata is correctly populated using add layer initialization"""
        o_reso = Resonance(database=self.database)

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

    def test_layer_density_locked_if_defined_during_initialization_init(self):
        """assert the layer density is locked if defined at the beginning using init"""
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           'density': {'value': 8.9,
                                       'units': 'g/cm3'},
                           },
                  'Ag': {'elements': ['Ag'],
                         'stoichiometric_ratio': [1],
                         'thickness': {'value': 0.03,
                                       'units': 'mm'},
                         'density': {'value': np.NaN,
                                     'units': 'g/cm3'},
                         },
                  }
        o_reso = Resonance(stack=_stack, database=self.database)

        density_lock_before = 8.9
        density_lock_after = o_reso.stack['CoAg']['density']['value']
        self.assertEqual(density_lock_after, density_lock_before)

        density_unlock_expected = 10.5
        density_unlock_after = o_reso.stack['Ag']['density']['value']
        self.assertEqual(density_unlock_after, density_unlock_expected)

    def test_layer_density_locked_if_defined_during_initialization_add_layer(self):
        """assert the layer density is locked if defined at the beginning using add_layer"""
        o_reso = Resonance(database=self.database)

        # layer 1
        layer1 = 'CoAg'
        thickness1 = 0.025
        density = 8.9
        o_reso.add_layer(formula=layer1, thickness=thickness1, density=density)

        # layer 2
        layer2 = 'Ag'
        thickness2 = 0.1
        o_reso.add_layer(formula=layer2, thickness=thickness2)

        density_lock_before = 8.9
        density_lock_after = o_reso.stack['CoAg']['density']['value']
        self.assertEqual(density_lock_after, density_lock_before)

        density_unlock_expected = 10.5
        density_unlock_after = o_reso.stack['Ag']['density']['value']
        self.assertEqual(density_unlock_after, density_unlock_expected)


class TestGetterSetter(unittest.TestCase):
    database = '_data_for_unittest'

    def setUp(self):
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           'density': {'value': np.NaN,
                                       'units': 'g/cm3'},
                           },
                  'U': {'elements': ['U'],
                        'stoichiometric_ratio': [1],
                        'thickness': {'value': 0.03,
                                      'units': 'mm'},
                        'density': {'value': np.NaN,
                                    'units': 'g/cm3'},
                        },
                  }
        self.o_reso = Resonance(stack=_stack, database=self.database)

        # stoichiometric ratio

    def test_retrieve_stoichiometric_of_uo3_sample(self):
        """assert retrieve stoichiometric work for complex sample such as UO3"""
        o_reso = self.o_reso
        o_reso.add_layer(formula='UO3', thickness=0.25, density=0.5)
        o_reso.add_layer(formula='AgCo', thickness=0.5, density=0.8)
        _stoichiometric_ratio = o_reso.get_isotopic_ratio(compound='UO3', element='U')
        self.assertEqual(_stoichiometric_ratio['238-U'], 0.992745)

    def test_retrieve_stoichiometric_ratio_raises_error_if_unknown_compound(self):
        """assert ValueError raised if wrong compound when getting stoichiometric ratio"""
        self.assertRaises(ValueError, self.o_reso.get_isotopic_ratio, compound='unknown')

    def test_if_element_misssing_use_compound_and_raises_error_if_wrong(self):
        """assert ValueError raised if element does not exist"""
        self.assertRaises(ValueError, self.o_reso.get_isotopic_ratio, compound='CoAg')

    def test_stoichiometric_ratio_returned(self):
        """assert the stoichiometric ratio are correctly returned"""
        _stoichiometric_ratio = self.o_reso.get_isotopic_ratio(compound='U')
        _expected_dict = {'233-U': 0.0,
                          '234-U': 5.5e-5,
                          '235-U': 0.0072,
                          '238-U': 0.992745}
        self.assertEqual(_expected_dict['233-U'], _stoichiometric_ratio['233-U'])
        self.assertEqual(_expected_dict['235-U'], _stoichiometric_ratio['235-U'])
        self.assertEqual(_expected_dict['238-U'], _stoichiometric_ratio['238-U'])

    def test_list_all_stoichiometric_ratio(self):
        """assert the entire stoichiometric list is returned"""
        _stoichiometric_ratio = self.o_reso.get_isotopic_ratio()
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
        self.assertEqual(_expected_dict['U']['U']['233-U'], _stoichiometric_ratio['U']['U']['233-U'])
        self.assertEqual(_expected_dict['U']['U']['238-U'], _stoichiometric_ratio['U']['U']['238-U'])
        self.assertEqual(_expected_dict['CoAg']['Ag']['107-Ag'], _stoichiometric_ratio['CoAg']['Ag']['107-Ag'])

    def test_set_stoichiometric_ratio_raises_value_error_if_wrong_compound(self):
        """assert ValueError raised if wrong compound in stoichiometric ratio setter"""
        self.assertRaises(ValueError, self.o_reso.set_isotopic_ratio)
        self.assertRaises(ValueError, self.o_reso.set_isotopic_ratio, compound='unknown')

    def test_set_stoichiometric_ratio_raises_value_error_if_wrong_element(self):
        """assert ValueError raised if wrong element in stoichiometric ratio setter"""
        self.assertRaises(ValueError, self.o_reso.set_isotopic_ratio, compound='CoAg')
        self.assertRaises(ValueError, self.o_reso.set_isotopic_ratio, compound='CoAg', element='unknown')

    def test_set_stoichiometric_ratio_has_correct_new_list_size(self):
        """assert ValueRror raised if new list of ratio does not match old list size"""
        self.assertRaises(ValueError, self.o_reso.set_isotopic_ratio, compound='U', element='U', list_ratio=[0, 1, 2])

    def test_set_stoichiometric_ratio_correctly_calculates_new_molar_mass(self):
        """assert molar mass is correctly calculated for new set of stoichiometric coefficient"""
        self.o_reso.set_isotopic_ratio(compound='CoAg', element='Co', list_ratio=[0.5, 0.5])
        new_molar_mass = self.o_reso.stack['CoAg']['Co']['molar_mass']['value']
        list_isotopes_mass = self.o_reso.stack['CoAg']['Co']['isotopes']['mass']['value']
        list_isotopes_ratio = self.o_reso.stack['CoAg']['Co']['isotopes']['isotopic_ratio']
        mass_ratio = zip(list_isotopes_mass, list_isotopes_ratio)
        expected_molar_mass = np.array([_m * _r for _m, _r in mass_ratio]).sum()
        self.assertAlmostEqual(new_molar_mass, expected_molar_mass, delta=0.0001)

    def test_set_stoichiometric_ratio_correctly_calculates_new_density(self):
        """assert density is correctly calculated for new set of stoichiometric coefficient"""
        self.o_reso.set_isotopic_ratio(compound='CoAg', element='Co', list_ratio=[0.5, 0.5])
        new_density = self.o_reso.stack['CoAg']['Co']['density']['value']
        list_density = self.o_reso.stack['CoAg']['Co']['isotopes']['density']['value']
        list_isotopes_ratio = self.o_reso.stack['CoAg']['Co']['isotopes']['isotopic_ratio']
        density_ratio = zip(list_density, list_isotopes_ratio)
        expected_density = np.array([_d * _r for _d, _r in density_ratio]).sum()
        self.assertAlmostEqual(new_density, expected_density, delta=0.0001)

        # density

    def test_retrieve_density_raises_error_if_unknown_compound(self):
        """assert ValueError raised if wrong compound when getting density"""
        self.assertRaises(ValueError, self.o_reso.get_density, compound='unknown')

    def test_if_element_misssing_use_compound_and_raises_error_if_wrong_when_getting_density(self):
        """assert ValueError raised if element does not exist when getting density"""
        self.assertRaises(ValueError, self.o_reso.get_density, compound='CoAg')

    def test_density_returned(self):
        """assert the density are correctly returned"""
        _density = self.o_reso.get_density(compound='U')
        _expected_density = 18.95
        self.assertEqual(_density, _expected_density)

    def test_density_returned_all(self):
        """assert the density of all element works"""
        _density_list = self.o_reso.get_density()
        _expected_density = {'CoAg': {'Co': 8.9,
                                      'Ag': 10.5,
                                      },
                             'U': {'U': 18.95,
                                   },
                             }
        self.assertEqual(_expected_density, _density_list)


class TestTransmissionAttenuation(unittest.TestCase):
    database = '_data_for_unittest'

    def setUp(self):
        _stack = {'CoAg': {'elements': ['Co', 'Ag'],
                           'stoichiometric_ratio': [1, 2],
                           'thickness': {'value': 0.025,
                                         'units': 'mm'},
                           'density': {'value': np.NaN,
                                       'units': 'g/cm3'},
                           },
                  'U': {'elements': ['U'],
                        'stoichiometric_ratio': [1],
                        'thickness': {'value': 0.03,
                                      'units': 'mm'},
                        'density': {'value': np.NaN,
                                    'units': 'g/cm3'},
                        },
                  }
        self.o_reso = Resonance(stack=_stack, database=self.database)

    def test_calculate_transmission_isotopes(self):
        """assert calculation of transmission for isotopes works"""
        energy_ev = self.o_reso.stack_signal['CoAg']['Ag']['107-Ag']['energy_eV']
        transmission = self.o_reso.stack_signal['CoAg']['Ag']['107-Ag']['transmission']

        expected_ev_0 = 0.0001
        expected_ev_1 = 0.002001
        expected_ev_2 = 0.003002

        expected_tran_0 = 0.98884717
        expected_tran_1 = 0.99199331
        expected_tran_2 = 0.99338488

        self.assertAlmostEqual(expected_ev_0, energy_ev[0], delta=0.001)
        self.assertAlmostEqual(expected_ev_1, energy_ev[1], delta=0.001)
        self.assertAlmostEqual(expected_ev_2, energy_ev[2], delta=0.001)
        self.assertAlmostEqual(expected_tran_0, transmission[0], delta=0.001)
        self.assertAlmostEqual(expected_tran_1, transmission[1], delta=0.001)
        self.assertAlmostEqual(expected_tran_2, transmission[2], delta=0.001)

    def test_calculate_attenuation_isotopes(self):
        """assert calculation of attenuation for isotopes works"""
        energy_ev = self.o_reso.stack_signal['CoAg']['Ag']['107-Ag']['energy_eV']
        attenuation = self.o_reso.stack_signal['CoAg']['Ag']['107-Ag']['attenuation']

        expected_ev_0 = 0.0001
        expected_ev_1 = 0.002001
        expected_ev_2 = 0.003002

        expected_attenu_0 = 1. - 0.98884717
        expected_attenu_1 = 1. - 0.99199331
        expected_attenu_2 = 1. - 0.99338488

        self.assertAlmostEqual(expected_ev_0, energy_ev[0], delta=0.001)
        self.assertAlmostEqual(expected_ev_1, energy_ev[1], delta=0.001)
        self.assertAlmostEqual(expected_ev_2, energy_ev[2], delta=0.001)
        self.assertAlmostEqual(expected_attenu_0, attenuation[0], delta=0.001)
        self.assertAlmostEqual(expected_attenu_1, attenuation[1], delta=0.001)
        self.assertAlmostEqual(expected_attenu_2, attenuation[2], delta=0.001)

    def test_calculate_transmission_element(self):
        """assert calculation of transmission for element works"""
        energy_ev = self.o_reso.stack_signal['CoAg']['Ag']['energy_eV']
        transmission = self.o_reso.stack_signal['CoAg']['Ag']['transmission']

        expected_ev_0 = 0.0001
        expected_ev_1 = 0.002001
        expected_ev_2 = 0.003002

        expected_tran_0 = 0.96556401
        expected_tran_1 = 0.97538374
        expected_tran_2 = 0.9797517

        self.assertAlmostEqual(expected_ev_0, energy_ev[0], delta=0.001)
        self.assertAlmostEqual(expected_ev_1, energy_ev[1], delta=0.001)
        self.assertAlmostEqual(expected_ev_2, energy_ev[2], delta=0.001)
        self.assertAlmostEqual(expected_tran_0, transmission[0], delta=0.001)
        self.assertAlmostEqual(expected_tran_1, transmission[1], delta=0.001)
        self.assertAlmostEqual(expected_tran_2, transmission[2], delta=0.001)

    def test_calculate_attenuation_element(self):
        """assert calculation of attenuation for element works"""
        energy_ev = self.o_reso.stack_signal['CoAg']['Ag']['energy_eV']
        attenuation = self.o_reso.stack_signal['CoAg']['Ag']['attenuation']

        expected_ev_0 = 0.0001
        expected_ev_1 = 0.002001
        expected_ev_2 = 0.003002

        expected_tran_0 = 1. - 0.96556401
        expected_tran_1 = 1. - 0.97538374
        expected_tran_2 = 1. - 0.9797517

        self.assertAlmostEqual(expected_ev_0, energy_ev[0], delta=0.001)
        self.assertAlmostEqual(expected_ev_1, energy_ev[1], delta=0.001)
        self.assertAlmostEqual(expected_ev_2, energy_ev[2], delta=0.001)
        self.assertAlmostEqual(expected_tran_0, attenuation[0], delta=0.001)
        self.assertAlmostEqual(expected_tran_1, attenuation[1], delta=0.001)
        self.assertAlmostEqual(expected_tran_2, attenuation[2], delta=0.001)

    def test_calculate_transmission_compound(self):
        """assert calculation of transmission for compounds works"""
        energy_ev = self.o_reso.stack_signal['CoAg']['energy_eV']
        transmission = self.o_reso.stack_signal['CoAg']['transmission']

        expected_ev_0 = 0.0001
        expected_ev_1 = 0.002001
        expected_ev_2 = 0.003002

        expected_tran_0 = 0.95537379
        expected_tran_1 = 0.96801669
        expected_tran_2 = 0.97365037

        self.assertAlmostEqual(expected_ev_0, energy_ev[0], delta=0.001)
        self.assertAlmostEqual(expected_ev_1, energy_ev[1], delta=0.001)
        self.assertAlmostEqual(expected_ev_2, energy_ev[2], delta=0.001)
        self.assertAlmostEqual(expected_tran_0, transmission[0], delta=0.001)
        self.assertAlmostEqual(expected_tran_1, transmission[1], delta=0.001)
        self.assertAlmostEqual(expected_tran_2, transmission[2], delta=0.001)

    def test_calculate_attenuation_compound(self):
        """assert calculation of attenuation for compounds works"""
        energy_ev = self.o_reso.stack_signal['CoAg']['energy_eV']
        attenuation = self.o_reso.stack_signal['CoAg']['attenuation']

        expected_ev_0 = 0.0001
        expected_ev_1 = 0.002001
        expected_ev_2 = 0.003002

        expected_tran_0 = 1. - 0.95537379
        expected_tran_1 = 1. - 0.96801669
        expected_tran_2 = 1. - 0.97365037

        self.assertAlmostEqual(expected_ev_0, energy_ev[0], delta=0.001)
        self.assertAlmostEqual(expected_ev_1, energy_ev[1], delta=0.001)
        self.assertAlmostEqual(expected_ev_2, energy_ev[2], delta=0.001)
        self.assertAlmostEqual(expected_tran_0, attenuation[0], delta=0.001)
        self.assertAlmostEqual(expected_tran_1, attenuation[1], delta=0.001)
        self.assertAlmostEqual(expected_tran_2, attenuation[2], delta=0.001)


class TestPlot(unittest.TestCase):
    database = '_data_for_unittest'

    def setUp(self):
        _energy_min = 1
        _energy_max = 50
        _energy_step = 0.1
        _layer_1 = 'Co'
        _thickness_1 = 0.025  # mm

        o_reso = Resonance(energy_min=_energy_min, energy_max=_energy_max, energy_step=_energy_step,
                           database=self.database)
        o_reso.add_layer(formula=_layer_1, thickness=_thickness_1)
        self.o_reso = o_reso

    def test_axis_type_and_time_unit(self):
        self.assertRaises(ValueError, self.o_reso.plot, x_axis='wrong_x_word')
        self.assertRaises(ValueError, self.o_reso.plot, time_unit='wrong_unit')
        self.assertRaises(ValueError, self.o_reso.plot, y_axis='wrong_y_word')


class TestExport(unittest.TestCase):
    database = '_data_for_unittest'

    def setUp(self):
        _energy_min = 1
        _energy_max = 50
        _energy_step = 0.1
        _layer_1 = 'Co'
        _thickness_1 = 0.025  # mm

        o_reso = Resonance(energy_min=_energy_min, energy_max=_energy_max, energy_step=_energy_step,
                           database=self.database)
        o_reso.add_layer(formula=_layer_1, thickness=_thickness_1)
        self.o_reso = o_reso

    def test_axis_type_and_time_unit(self):
        self.assertRaises(ValueError, self.o_reso.export, x_axis='wrong_x_word')
        self.assertRaises(ValueError, self.o_reso.export, time_unit='wrong_unit')
        self.assertRaises(ValueError, self.o_reso.export, y_axis='wrong_y_word')
