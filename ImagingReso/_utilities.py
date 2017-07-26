import glob
import os


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
    '''return a string array of all the element from the database'''
    _file_path = os.path.abspath(os.path.dirname(__file__))
    _database_folder = os.path.join(_file_path, 'reference_data', database)
    _list_files = glob.glob(_database_folder + '/*.csv')
    _list_short_files = [os.path.basename(_file) for _file in _list_files]
    _list_element = set([_name.split('-')[0].lower() for _name in _list_short_files])
    return _list_element
    
    