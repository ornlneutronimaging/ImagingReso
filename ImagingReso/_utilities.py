import glob
import os
import numbers
import re
import numpy as np
import periodictable as pt


def is_element_in_database(element='', database='ENDF_VIII'):
    '''will try to find the element in the folder (database) specified
    
    Parameters:
    ==========
    element: string. Name of the element. Not case sensitive
    database: string (default is 'ENDF_VIII'). Name of folder that has the list of elements
    
    Returns:
    =======
    bool: True if element was found in the database
          False if element could not be found
    '''
    if element == '':
        return False
    
    list_entry_from_database = get_list_element_from_database(database=database)
    if element.lower() in list_entry_from_database:
        return True
    return False    
    
def get_list_element_from_database(database=''):
    '''return a string array of all the element from the database
    
    Parameters:
    ==========
    database: string. Name of database
    
    Raises:
    ======
    ValueError if database can not be found
    
    '''
    _file_path = os.path.abspath(os.path.dirname(__file__))
    _database_folder = os.path.join(_file_path, 'reference_data', database)

    if not os.path.exists(_database_folder):
        raise ValueError("Database {} does not exist!".format(database))
    
    _list_files = glob.glob(_database_folder + '/*.csv')
    _list_short_files = [os.path.basename(_file) for _file in _list_files]
    _list_element = set([_name.split('-')[0].lower() for _name in _list_short_files])
    return _list_element
    
def checking_stack(stack={}, database='ENDF_VIII'):
    '''This method makes sure that all the elements from the various stacks are 
    in the database and that the thickness has the correct format (float)
    
    Parameters:
    ==========
    stack: dictionary that defines the various stacks
    database: string (default is 'ENDF_VIII') name of database
    
    Raises:
    ======
    ValueError if one of the element in one of the stack can not be found 
    ValueError if thickness is not a float
    ValueError if elements and stochiometric ratio arrays do not have the same size
    
    Return:
    ======
    True: for testing purpose only
    '''
    for _keys in stack:
        _elements = stack[_keys]['elements']
        for _element in _elements:
            if not is_element_in_database(element=_element):
                raise ValueError("Element {} can not be found in the database".format(_element))

        _thickness = stack[_keys]['thickness']['value']
        if not isinstance(_thickness, numbers.Number):
            raise ValueError("Thickness {} should be a number!".format(_thickness))
    
        _stochiometric_ratio = stack[_keys]['stochiometric_ratio']
        if len(_stochiometric_ratio) != len(_elements):
            raise ValueError("Stochiometric Ratio and Elements should have the same size!")
    
    return True    

def formula_to_dictionary(formula='', thickness=np.NaN, database='ENDF_VIII'):
    '''create dictionary based on formula given
    
    Parameters:
    ===========
    formula: string
       ex: 'AgCo2'
       ex: 'Ag'
    thickness: float (in mm) default is np.NaN
    database: string (default is ENDV_VIII). Database where to look for elements
    
    Raises:
    =======
    ValueError if one of the element is missing from the database
    
    Return:
    =======
    the dictionary of the elements passed
      ex: {'AgCo2': {'elements': ['Ag','Co'],
                     'stochiometric_ratio': [1,2],
                     'thickness': thickness}}
    '''
    _formula_parsed = re.findall(r'([A-Z][a-z]*)(\d*)', formula)

    _dictionary = {}
    _elements_array = []
    _atomic_ratio_array = []
    for _element in _formula_parsed:
        [_single_element, _atomic_ratio] = list(_element)
        if not is_element_in_database(element=_single_element, database=database):
            raise ValueError("element {} not found in database!".format(_single_element))

        if _atomic_ratio == '':
            _atomic_ratio = 1

        _atomic_ratio_array.append(int(_atomic_ratio))
        _elements_array.append(_single_element)

    return {formula: {'elements': _elements_array,
                      'stochiometric_ratio': _atomic_ratio_array,
                      'thickness': {'value': thickness,
                                    'units': 'mm'},
                      },
            }

def get_isotope_dicts(element='', database='ENDF_VIII'):
    '''return a dictionary with list of isotopes found in database and name of database files
    
    Parameters:
    ===========
    element: string. Name of the element
      ex: 'Ag'
    database: string (default is ENDF_VIII)
    
    Returns:
    ========
    dictionary with isotopes and files 
      ex: {'Ag': {'isotopes': ['107-Ag','109-Ag'],
                  'file_names': ['Ag-107.csv','Ag-109.csv']}}
    
    '''
    _file_path = os.path.abspath(os.path.dirname(__file__))
    _database_folder = os.path.join(_file_path, 'reference_data', database)
    _element_search_path = os.path.join(_database_folder, element + '*.csv')
    list_files = glob.glob(_element_search_path)
    isotope_dict = {'isotopes': {'list': [], 
                                 'file_names': [],
                                 'density': {'value': np.NaN,
                                             'units': 'g/cm3'},
                                 'mass': {'value': [],
                                          'units': 'g/mol',
                                 },
                                 'isotopic_ratio': [],},
                    'density': {'value': np.NaN,
                                'units': 'g/cm3'},
                    'molar_mass': {'value': np.NaN,
                                   'units': 'g/mol'},
                    } 

    isotope_dict_mirror = {}
    _isotopes_list = []
    _isotopes_list_files = []
    _isotopes_mass = []
    _isotopes_density = []
    _isotopes_atomic_ratio = []
    _density = np.NaN
    _molar_mass = np.NaN
    
    for file in list_files:

        # Obtain element, z number from the basename
        _basename = os.path.basename(file)
        [filename, file_extension] = os.path.splitext(_basename)
        [_name, _number] = filename.split('-')
        _symbol = _number + '-' + _name
        isotope = str(_symbol)

        _isotopes_list.append(isotope)
        _isotopes_list_files.append(_basename)
        _isotopes_mass.append(get_mass(isotope))
        _isotopes_atomic_ratio.append(get_abundance(isotope))
        _isotopes_density.append(get_density(isotope))
        _density = get_density(element)
        _molar_mass = get_mass(element)
                                        
    isotope_dict['isotopes']['list'] = _isotopes_list
    isotope_dict['isotopes']['file_names'] = _isotopes_list_files              
    isotope_dict['isotopes']['mass']['value'] = _isotopes_mass
    isotope_dict['isotopes']['isotopic_ratio'] = _isotopes_atomic_ratio
    isotope_dict['isotopes']['density']['value'] = _isotopes_density
    isotope_dict['density']['value'] = _density
    isotope_dict['molar_mass']['value'] = _molar_mass
                    
    return isotope_dict   

def get_abundance(element):
    '''return the abundance [0.,1.] of the defined element
    
    Parameters:
    ===========
    element: (sting)
    
    Returns:
    ========
    the abundance of the elemenet (value between 0 and 1)
    '''
    return pt.elements.isotope(element).abundance / 100.

def get_mass(element):
    '''return the molar mass (SI units) of an given isotope, or element
    
    Parameters:
    ===========
    element: string. Element or isotopes to get the mass from
    
    Returns:
    ========
    the molar mass of the element/isotope in SI units
    '''
    return pt.elements.isotope(element).mass

def get_density(element):
    '''return the density (g.cm-3) of the element
    
    Paramters:
    ==========
    element: string. Name of element
    
    Returns:
    ========
    the density of the element in g.cm-3 units
    '''
    return pt.elements.isotope(element).density