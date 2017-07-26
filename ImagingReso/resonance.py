from ImagingReso._utilities import checking_stack


class Resonance(object):
    
    database = 'ENDF_VIII'

    stack = {}
    
    def __init__(self, stack={}):
        if stack == {}:
            raise ValueError("You need to define at least one stack!")

        # checking that every element of each stack is defined
        checking_stack(stack=stack)
        self.stack = stack

        #elements = list(set(elements))
        #for _element in elements:
            #if not is_element_in_database(element=_element, database=self.database):
                #raise IOError("Element {} can not be found in database!".format(_element))
            
        #if thicknesses == []:
            #raise ValueError("You need to define at least 1 thickness!")
            
        #if not (len(thicknesses) == len(elements)):
            #raise ValueError("Thickness and Elements arrays must have the same size!")
    
        #self.elements = elements
        #self.thicknesses = thicknesses
        
