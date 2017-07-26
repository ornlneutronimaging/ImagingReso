from ImagingReso._utilities import is_element_in_database


class Resonance(object):
    
    database = 'ENDF_VIII'
    
    def __init__(self, elements=[]):
        if not (elements == []):
            elements = list(set(elements))
            for _element in elements:
                if not is_element_in_database(element=_element, database=self.database):
                    raise IOError("Element {} can not be found in database!".format(_element))
            self.elements = elements
            
    
    
    