import glob
import os
import numbers
import re
import numpy as np


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
    
    Return:
    ======
    True: for testing purpose only
    '''
    for _keys in stack:
        _elements = stack[_keys]['elements']
        for _element in _elements:
            if not is_element_in_database(element=_element):
                raise ValueError("Element {} can not be found in the database".format(_element))

        _thickness = stack[_keys]['thickness']
        if not isinstance(_thickness, numbers.Number):
            raise ValueError("Thickness {} should be a number!".format(_thickness))
    
        _ratio = stack[_keys]['ratio']
        if len(_ratio) != len(_elements):
            raise ValueError("Ratio and Elements should have the same size!")
    
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
                     'ratio': [1,2],
                     'thickness': thickness}}
    '''
    _formula_parsed = re.findall(r'([A-Z][a-z]*)(\d*)', formula)

    _dictionary = {}
    _elements_array = []
    _ratio_array = []
    for _element in _formula_parsed:
        [_single_element, _ratio] = list(_element)
        if not is_element_in_database(element=_single_element, database=database):
            raise ValueError("element {} not found in database!".format(_single_element))

        if _ratio == '':
            _ratio = 1

        _ratio_array.append(int(_ratio))
        _elements_array.append(_single_element)

    return {formula: {'elements': _elements_array,
                      'ratio': _ratio_array,
                      'thickness': thickness}}
