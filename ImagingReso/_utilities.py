import glob
import numbers
import os
import re
import zipfile

import numpy as np
import pandas as pd
import periodictable as pt
from scipy.constants import Avogadro
from scipy.interpolate import interp1d

from six.moves import input
from six.moves.urllib.request import urlopen
import sys


def download_from_github(fname, path):
    """
    Download database from GitHub

    :param fname: file name with extension ('.zip') of the target item
    :type fname: str
    :param path: path to save unzipped files
    :type path: str

    :return: database folder
    :rtype: folder
    """
    base_url = 'https://github.com/ornlneutronimaging/ImagingReso/blob/master/ImagingReso/reference_data/'
    # Add GitHub junk to the file name for downloading.
    f = fname + '?raw=true'
    url = base_url + f
    block_size = 16384
    req = urlopen(url)

    # Get file size from header
    if sys.version_info[0] < 3:
        file_size = int(req.info().getheaders('Content-Length')[0])
    else:
        file_size = req.length
    # downloaded = 0

    # Check if file already downloaded
    if os.path.exists(fname):
        if os.path.getsize(fname) == file_size:
            print("Skipping downloading '{}'".format(fname))
        else:
            overwrite = input("File size changed, overwrite '{}'? ([y]/n) ".format(fname))
            if overwrite.lower().startswith('n'):
                print("Local file '{}' kept without overwriting.".format(fname))

    # Copy file to disk
    print("Downloading '{}'... ".format(fname))
    with open(fname, 'wb') as fh:
        while True:
            chunk = req.read(block_size)
            if not chunk:
                break
            fh.write(chunk)
            # downloaded += len(chunk)
        print('')
    print('Download completed.')
    print("Unzipping '{}'... ".format(fname))

    _database_zip = zipfile.ZipFile(fname)
    _database_zip.extractall(path=path)
    print("'{}' has been unzipped and database '{}' is ready to use.".format(fname, fname.replace('.zip', '')))

    os.remove(fname)
    print("'{}' has been deleted".format(fname))


def get_list_element_from_database(database='ENDF_VII'):
    """return a string array of all the element from the database

    Parameters:
    ==========
    database: string. Name of database

    Raises:
    ======
    ValueError if database can not be found

    """
    _file_path = os.path.abspath(os.path.dirname(__file__))
    _ref_data_folder = os.path.join(_file_path, 'reference_data')
    _database_folder = os.path.join(_ref_data_folder, database)

    if not os.path.exists(_ref_data_folder):
        os.makedirs(_ref_data_folder)
        print("Folder to store database files has been created: '{}'".format(_ref_data_folder))

    if not os.path.exists(_database_folder):
        print("First time using database '{}'? ".format(database))
        print("I will retrieve and store a local copy of database'{}': ".format(database))
        download_from_github(fname=database + '.zip', path=_ref_data_folder)

    # if '/_elements_list.csv' NOT exist
    if not os.path.exists(_database_folder + '/_elements_list.csv'):
        # glob all .csv files
        _list_files = glob.glob(_database_folder + '/*.csv')

        # glob all .h5 files if NO .csv file exist
        if not _list_files:
            _list_files = glob.glob(_database_folder + '/*.h5')

        # test if files globed
        _empty_list_boo = not _list_files
        if _empty_list_boo is True:
            raise ValueError("'{}' does not contain any '*.csv' or '*.h5' file.".format(_database_folder))

        # convert path/to/file to filename only
        _list_short_filename_without_extension = [os.path.splitext(os.path.basename(_file))[0] for _file in _list_files]

        # isolate element names and output as list
        if '-' in _list_short_filename_without_extension[0]:
            _list_element = list(set([_name.split('-')[0] for _name in _list_short_filename_without_extension]))
        else:
            _list_letter_part = list(
                set([re.split(r'(\d+)', _name)[0] for _name in _list_short_filename_without_extension]))
            _list_element = []
            for each_letter_part in _list_letter_part:
                if len(each_letter_part) <= 2:
                    _list_element.append(each_letter_part)
        # save to current dir
        _list_element.sort()
        df_to_save = pd.DataFrame()
        df_to_save['elements'] = _list_element
        df_to_save.to_csv(_database_folder + '/_elements_list.csv')
        # print("NOT FOUND '{}'".format(_database_folder + '/_elements_list.csv'))
        # print("SAVED '{}'".format(_database_folder + '/_elements_list.csv'))

    # '/_elements_list.csv' exist
    else:
        df_to_read = pd.read_csv(_database_folder + '/_elements_list.csv')
        _list_element = list(df_to_read['elements'])
        # print("FOUND '{}'".format(_database_folder + '/_elements_list.csv'))
        # print("READ '{}'".format(_database_folder + '/_elements_list.csv'))

    return _list_element


def is_element_in_database(element='', database='ENDF_VII'):
    """will try to find the element in the folder (database) specified

    Parameters:
    ==========
    element: string. Name of the element. Not case sensitive
    database: string (default is 'ENDF_VII'). Name of folder that has the list of elements

    Returns:
    =======
    bool: True if element was found in the database
          False if element could not be found
    """
    if element == '':
        return False

    list_entry_from_database = get_list_element_from_database(database=database)
    if element in list_entry_from_database:
        return True
    return False


def checking_stack(stack, database='ENDF_VII'):
    """This method makes sure that all the elements from the various stacks are
    in the database and that the thickness has the correct format (float)

    Parameters:
    ==========
    stack: dictionary that defines the various stacks
    database: string (default is 'ENDF_VII') name of database
    
    Raises:
    ======
    ValueError if one of the element in one of the stack can not be found 
    ValueError if thickness is not a float
    ValueError if elements and stoichiometric ratio arrays do not have the same size
    
    Return:
    ======
    True: for testing purpose only
    """
    for _keys in stack:
        _elements = stack[_keys]['elements']
        for _element in _elements:
            if not is_element_in_database(element=_element, database=database):
                raise ValueError("Element {} can not be found in the database".format(_element))

        _thickness = stack[_keys]['thickness']['value']
        if not isinstance(_thickness, numbers.Number):
            raise ValueError("Thickness {} should be a number!".format(_thickness))

        _stoichiometric_ratio = stack[_keys]['stoichiometric_ratio']
        if len(_stoichiometric_ratio) != len(_elements):
            raise ValueError("stoichiometric Ratio and Elements should have the same size!")

    return True


def formula_to_dictionary(formula='', thickness=np.NaN, density=np.NaN, database='ENDF_VII'):
    """create dictionary based on formula given
    
    Parameters:
    ===========
    formula: string
       ex: 'AgCo2'
       ex: 'Ag'
    thickness: float (in mm) default is np.NaN
    density: float (in g/cm3) default is np.NaN
    database: string (default is ENDV_VIII). Database where to look for elements
    
    Raises:
    =======
    ValueError if one of the element is missing from the database
    
    Return:
    =======
    the dictionary of the elements passed
      ex: {'AgCo2': {'elements': ['Ag','Co'],
                     'stoichiometric_ratio': [1,2],
                     'thickness': {'value': thickness,
                                   'units': 'mm'},
                     'density': {'value': density,
                                 'units': 'g/cm3'},
                     'molar_mass': {'value': np.nan,
                                    'units': 'g/mol'},
                    }
    """

    if '.' in formula:
        raise ValueError("formula '{}' is invalid, containing symbol '{}' !".format(formula, '.'))
    _formula_parsed = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    if len(_formula_parsed) == 0:
        raise ValueError("formula '{}' is invalid !".format(formula))

    # _dictionary = {}
    _elements_array = []
    _atomic_ratio_array = []
    for _element in _formula_parsed:
        [_single_element, _atomic_ratio] = list(_element)
        if not is_element_in_database(element=_single_element, database=database):
            raise ValueError("element '{}' not found in the database '{}'!".format(_single_element, database))

        if _atomic_ratio == '':
            _atomic_ratio = 1

        _atomic_ratio_array.append(int(_atomic_ratio))
        _elements_array.append(_single_element)
    _dict = {formula: {'elements': _elements_array,
                       'stoichiometric_ratio': _atomic_ratio_array,
                       'thickness': {'value': thickness,
                                     'units': 'mm'},
                       'density': {'value': density,
                                   'units': 'g/cm3'},
                       'molar_mass': {'value': np.nan,
                                      'units': 'g/mol'}
                       }
             }
    return _dict


def get_isotope_dicts(element='', database='ENDF_VII'):
    """return a dictionary with list of isotopes found in database and name of database files
    
    Parameters:
    ===========
    element: string. Name of the element
      ex: 'Ag'
    database: string (default is ENDF_VII)
    
    Returns:
    ========
    dictionary with isotopes and files 
      ex: {'Ag': {'isotopes': ['107-Ag','109-Ag'],
                  'file_names': ['Ag-107.csv','Ag-109.csv']}}
    
    """
    _file_path = os.path.abspath(os.path.dirname(__file__))
    _database_folder = os.path.join(_file_path, 'reference_data', database)
    _element_search_path = os.path.join(_database_folder, element + '-*.csv')

    list_files = glob.glob(_element_search_path)
    if not list_files:
        raise ValueError("File names contains NO '-', the name should in the format of 'Cd-115_m1' or 'Cd-114'")
    list_files.sort()
    isotope_dict = {'isotopes': {'list': [],
                                 'file_names': [],
                                 'density': {'value': np.NaN,
                                             'units': 'g/cm3'},
                                 'mass': {'value': [],
                                          'units': 'g/mol',
                                          },
                                 'isotopic_ratio': [], },
                    'density': {'value': np.NaN,
                                'units': 'g/cm3'},
                    'molar_mass': {'value': np.NaN,
                                   'units': 'g/mol'},
                    }

    # isotope_dict_mirror = {}
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
        filename = os.path.splitext(_basename)[0]
        if '-' in filename:
            [_name, _number] = filename.split('-')
            if '_' in _number:
                [aaa, meta] = _number.split('_')
                _number = aaa[:]
        else:
            _split_list = re.split(r'(\d+)', filename)
            if len(_split_list) == 2:
                [_name, _number] = _split_list
            else:
                _name = _split_list[0]
                _number = _split_list[1]
        if _number == '0':
            _number = '12'
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
    """return the abundance [0.,1.] of the defined element
    
    Parameters:
    ===========
    element: (sting)
    
    Returns:
    ========
    the abundance of the elemenet (value between 0 and 1)
    """
    return pt.elements.isotope(element).abundance / 100.


def get_mass(element):
    """return the molar mass (SI units) of an given isotope, or element
    
    Parameters:
    ===========
    element: string. Element or isotopes to get the mass from
    
    Returns:
    ========
    the molar mass of the element/isotope in SI units
    """
    return pt.elements.isotope(element).mass


def get_density(element):
    """return the density (g.cm-3) of the element
    
    Paramters:
    ==========
    element: string. Name of element
    
    Returns:
    ========
    the density of the element in g.cm-3 units
    """
    return pt.elements.isotope(element).density


def get_compound_density(list_density: list, list_ratio: list):
    """"""
    _ratio_density = zip(list_ratio, list_density)
    _density_compound = 0

    _sum_ratio = np.array(list_ratio).sum()

    for _ratio, _density in _ratio_density:
        _density_compound += (_ratio * _density) / _sum_ratio
    return _density_compound


def get_compound_molar_mass(list_molar_mass: list, list_ratio: list):
    """"""
    _ratio_density = zip(list_ratio, list_molar_mass)
    _molar_mass_compound = 0
    for _i, _mass in enumerate(list_molar_mass):
        _molar_mass_compound += _mass * list_ratio[_i]
    return _molar_mass_compound


def get_database_data(file_name=''):
    """return the energy (eV) and Sigma (barn) from the file_name
    
    Parameters:
    ===========
    file_name: string ('' by default) name of csv file
    
    Returns:
    ========
    pandas dataframe
    
    Raises:
    =======
    IOError if file does not exist
    """
    if not os.path.exists(file_name):
        raise IOError("File {} does not exist!".format(file_name))
    df = pd.read_csv(file_name, header=1)
    return df


def get_interpolated_data(df: pd.DataFrame, e_min=np.nan, e_max=np.nan, e_step=np.nan):
    """return the interpolated x and y axis for the given x range [e_min, e_max] with step defined

    :param df: input data frame
    :type df: pandas.DataFrame
    :param e_min: left energy range in eV of new interpolated data
    :type e_min: float
    :param e_max: right energy range in eV of new interpolated data
    :type e_max: float
    :param e_step: energy step in eV for interpolation
    :type e_step: float

    :return: x_axis and y_axis of interpolated data over specified range
    :rtype: dict
    """
    nbr_point = int((e_max - e_min) / e_step + 1)
    x_axis = np.linspace(e_min, e_max, nbr_point).round(6)
    y_axis_function = interp1d(x=df['E_eV'], y=df['Sig_b'], kind='linear')
    y_axis = y_axis_function(x_axis)

    return {'x_axis': x_axis, 'y_axis': y_axis}


def get_sigma(database_file_name='', e_min=np.NaN, e_max=np.NaN, e_step=np.NaN, t_kelvin=None):
    """retrieve the Energy and sigma axis for the given isotope

    :param database_file_name: path/to/file with extension
    :type database_file_name: string
    :param e_min: left energy range in eV of new interpolated data
    :type e_min: float
    :param e_max: right energy range in eV of new interpolated data
    :type e_max: float
    :param e_step: energy step in eV for interpolation
    :type e_step: float
    :param t_kelvin: temperature in Kelvin
    :type t_kelvin: float

    :return: {'energy': np.array, 'sigma': np.array}
    :rtype: dict
    """

    file_extension = os.path.splitext(database_file_name)[1]

    if t_kelvin is None:
        # '.csv' files
        if file_extension != '.csv':
            raise IOError("Cross-section File type must be '.csv'")
        else:
            _df = get_database_data(file_name=database_file_name)
            _dict = get_interpolated_data(df=_df, e_min=e_min, e_max=e_max,
                                          e_step=e_step)
            return {'energy_eV': _dict['x_axis'],
                    'sigma_b': _dict['y_axis']}
    else:
        raise ValueError("Doppler broadened cross-section in not yet supported in current version.")


# # '.h5' files
# if file_extension == '.h5':
#     dir_to_read = os.path.dirname(database_file_name)
#     basename = os.path.basename(database_file_name)
#     name_no_extension = os.path.splitext(basename)[0]
#     _split = re.split(r'(\d+)', name_no_extension)
#     name_only = _split[0]
#     aaa = _split[1]
#     filename_to_save = name_only + '-' + aaa
#
#     if len(_split) == 5:
#         meta_str = _split[2] + _split[3]
#         filename_to_save += meta_str
#
#     dir_to_save = os.path.join(dir_to_read, 'cached_csv')
#     if not os.path.exists(dir_to_save):
#         os.makedirs(dir_to_save)
#
#     fullpath_to_save = os.path.join(dir_to_save, filename_to_save + '.csv')
#     if os.path.exists(fullpath_to_save):
#         _df = get_database_data(file_name=filename_to_save)
#         _dict = get_interpolated_data(df=_df, e_min=e_min, e_max=e_max,
#                                       e_step=e_step)
#         return {'energy_eV': _dict['x_axis'],
#                 'sigma_b': _dict['y_axis']}
#
#     else:
#         _reactions = openmc.data.IncidentNeutron.from_hdf5(database_file_name)
#         total_xs = _reactions[1].xs['294K']
#         nbr_point = int((e_max - e_min) / e_step + 1)
#         x_axis = np.linspace(e_min, e_max, nbr_point)
#         y_axis = total_xs(x_axis)
#
#         _energies_list = list(_reactions.energy['294K'])
#         _xs_list = list(total_xs(_energies_list))
#         _energies_list.insert(0, 'E_eV')
#         _energies_list.insert(0, name_only)
#         _xs_list.insert(0, 'Sig_b')
#         _xs_list.insert(0, aaa)
#         _df_to_save = pd.DataFrame(_xs_list, index=_energies_list)
#         _df_to_save.to_csv(fullpath_to_save, header=False)
#         print("Saving '{}'".format(fullpath_to_save))
#
#         return {'energy_eV': x_axis,
#                 'sigma_b': y_axis}


def get_atoms_per_cm3_of_layer(compound_dict: dict):
    """
    calculate the atoms per cm3 of the given compound (layer)
    :param compound_dict: compound infomation to pass
    :type compound_dict: dict
    :return: molar mass and atom density for layer
    :rtype: float
    """
    # atoms_per_cm3 = {}

    _list_of_elements = compound_dict['elements']
    _stoichiometric_list = compound_dict['stoichiometric_ratio']

    _element_stoichio = zip(_list_of_elements, _stoichiometric_list)
    _molar_mass_sum = 0
    for _element, _stoichio in _element_stoichio:
        _molar_mass_sum += _stoichio * compound_dict[_element]['molar_mass']['value']

    atoms_per_cm3 = Avogadro * compound_dict['density']['value'] / _molar_mass_sum
    # _element_stoichio = zip(_list_of_elements, _stoichiometric_list)
    # for _element, _stoichio in _element_stoichio:
    #     _step1 = (compound_dict['density']['value'] * _stoichio) / _molar_mass_sum
    #     atoms_per_cm3[_element] = Avogadro * _step1

    return _molar_mass_sum, atoms_per_cm3


def calculate_linear_attenuation_coefficient(atoms_per_cm3: np.float, sigma_b: np.array):
    """calculate the transmission signal using the formula

    transmission = exp( - thickness_cm * atoms_per_cm3 * 1e-24 * sigma_b)

    Parameters:
    ===========
    thickness: float (in cm)
    atoms_per_cm3: float (number of atoms per cm3 of element/isotope)
    sigma_b: np.array of sigma retrieved from database

    Returns:
    ========
    transmission array
    """
    miu_per_cm = 1e-24 * sigma_b * atoms_per_cm3
    return np.array(miu_per_cm)


def calculate_trans(thickness_cm: np.float, miu_per_cm: np.array):
    """calculate the transmission signal using the formula

    transmission = exp( - thickness_cm * atoms_per_cm3 * 1e-24 * sigma_b)

    Parameters:
    ===========
    thickness: float (in cm)
    atoms_per_cm3: float (number of atoms per cm3 of element/isotope)
    sigma_b: np.array of sigma retrieved from database

    Returns:
    ========
    transmission array
    """
    transmission = np.exp(-thickness_cm * miu_per_cm)
    return np.array(transmission)


def calculate_transmission(thickness_cm: np.float, atoms_per_cm3: np.float, sigma_b: np.array):
    """calculate the transmission signal using the formula
    
    transmission = exp( - thickness_cm * atoms_per_cm3 * 1e-24 * sigma_b)
    
    Parameters:
    ===========
    thickness: float (in cm)
    atoms_per_cm3: float (number of atoms per cm3 of element/isotope)
    sigma_b: np.array of sigma retrieved from database
    
    Returns:
    ========
    transmission array
    """
    miu_per_cm = calculate_linear_attenuation_coefficient(atoms_per_cm3=atoms_per_cm3, sigma_b=sigma_b)
    transmission = calculate_trans(thickness_cm=thickness_cm, miu_per_cm=miu_per_cm)
    return miu_per_cm, transmission


def set_distance_units(value=np.NaN, from_units='mm', to_units='cm'):
    """convert distance into new units
    
    Parameters:
    ===========
    value: float. value to convert
    from_units: string. Must be 'mm', 'cm' or 'm'
    to_units: string. must be 'mm','cm' or 'm'
    
    Returns:
    ========
    converted value
    
    Raises:
    =======
    ValueError if from_units is not a valid unit (see above)
    ValueError if to_units is not a valid unit
    """
    if from_units == to_units:
        return value

    if from_units == 'cm':
        if to_units == 'mm':
            coeff = 10
        elif to_units == 'm':
            coeff = 0.01
        else:
            raise ValueError("to_units not supported ['cm','m','mm']!")
    elif from_units == 'mm':
        if to_units == 'cm':
            coeff = 0.1
        elif to_units == 'm':
            coeff = 0.001
        else:
            raise ValueError("to_units not supported ['cm','m','mm']!")
    elif from_units == 'm':
        if to_units == 'mm':
            coeff = 1000
        elif to_units == 'cm':
            coeff = 100
        else:
            raise ValueError("to_units not supported ['cm','m','mm']!")
    else:
        raise ValueError("to_units not supported ['cm','m','mm']!")

    return coeff * value


def ev_to_angstroms(array):
    """convert into lambda from the energy array

    Parameters:
    ===========
    array: array or number to convert (in eV)

    Returns:
    ========
    numpy array or value of lambda in Angstroms
    """
    return np.sqrt(81.787 / (array * 1000.))  # 1000 is used to convert eV to meV


def angstroms_to_ev(array):
    """convert lambda array in angstroms to energy in eV
    
    Parameters:
    ===========
    array: numpy array or number in Angstroms
    
    Returns:
    ========
    numpy array or value of energy in eV
    """
    return 81.787 / (1000. * array ** 2)  # 1000 is used to convert meV to eV


def ev_to_s(offset_us, source_to_detector_m, array):
    # delay values is normal 2.99 us with NONE actual MCP delay settings
    """convert energy (eV) to time (us)

    Parameters:
    ===========
    array: array (in eV)
    offset_us: float. Delay of detector in us
    source_to_detector_m: float. Distance source to detector in m

    Returns:
    ========
    time: array in s 
    """
    # 1000 is used to convert eV to meV
    time_s = np.sqrt(81.787 / (array * 1000.)) * source_to_detector_m / 3956.
    time_record_s = time_s - offset_us * 1e-6
    return time_record_s


def s_to_ev(offset_us, source_to_detector_m, array):
    """convert time (s) to energy (eV)
    Parameters:
    ===========
    numpy array of time in s
    offset_us: float. Delay of detector in us
    source_to_detector_m: float. Distance source to detector in m

    Returns:
    ========
    numpy array of energy in eV
    """
    lambda_a = 3956. * (array + offset_us * 1e-6) / source_to_detector_m
    return (81.787 / pow(lambda_a, 2)) / 1000.  # 1000 is used to convert meV to eV


def angstroms_to_s(offset_us, source_to_detector_m, array):
    """convert array in angstroms into s

    Parameters:
    ===========
    numpy array of lambda in angstroms
    offset_us: float. Delay of detector in us
    source_to_detector_m: float. Distance source to detector in m

    Returns:
    ========
    numpy array of time in s
    """
    return (source_to_detector_m * array / 3956.) - offset_us * 1e-6


def s_to_angstroms(offset_us, source_to_detector_m, array):
    """convert s to angstroms arrays

    Parameters:
    ===========
    array: array in s
    offset_us: float. Delay of detector in mocros
    source_to_detector_m: float. Distance source to detector in m

    Returns:
    ========
    array in angstroms
    """
    return 3956. * (array + offset_us * 1e-6) / source_to_detector_m


def ev_to_image_number(offset_us, source_to_detector_m, time_resolution_us, t_start_us, array):
    # delay values is normal 2.99 us with NONE actual MCP delay settings
    """convert energy (eV) to image numbers (#)

    Parameters:
    ===========
    numpy array of energy in eV
    offset_us: float. Delay of detector in us
    source_to_detector_m: float. Distance source to detector in m

    Returns:
    ========
    image numbers: array of image number
    """
    time_tot_us = np.sqrt(81.787 / (array * 1000)) * source_to_detector_m * 100 / 0.3956
    time_record_us = (time_tot_us + offset_us)
    image_number = (time_record_us - t_start_us) / time_resolution_us
    return image_number
