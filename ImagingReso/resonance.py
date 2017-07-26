from ImagingReso._utilities import is_element_in_database


class Resonance(object):
    
    database = 'ENDF_VIII'
    
    def __init__(self, elements=[], thicknesses=[]):
        if elements == []:
            raise ValueError("You need to define at least one element!")

        elements = list(set(elements))
        for _element in elements:
            if not is_element_in_database(element=_element, database=self.database):
                raise IOError("Element {} can not be found in database!".format(_element))
            
        if thicknesses == []:
            raise ValueError("You need to define at least 1 thickness!")
            
        if not (len(thicknesses) == len(elements)):
            raise ValueError("Thickness and Elements arrays must have the same size!")
    
        self.elements = elements
        self.thickness = thickness