"""
 Title:         Constraint
 Description:   Contains the basic structure for a constraints class
 Author:        Janzen Choi

"""

# The Constraint Class
class Constraint:

    # Constructor
    def __init__(self, name, type, exp_curves):
        self.name = name
        self.type = type
        self.exp_curves = exp_curves

    # Returns the name of the constraint
    def get_name(self):
        return self.name

    # Returns the type of the constraint
    def get_type(self):
        return self.type

    # Returns the experimental curve
    def get_exp_curves(self):
        return self.exp_curves
    
    # Returns a constraint (placeholder)
    #   Constraint is violated if value > 0
    def get_value(self):
        raise NotImplementedError

# Returns the stress from a curve
def get_stress(curve):
    return curve["stress"]

# Groups creep curves by temperature and orders them by stress
def get_curve_map(exp_curves):
    
    # Get unique temperatures
    temp_list = [exp_curve["temp"] for exp_curve in exp_curves if exp_curve["type"] == "creep"]
    temp_list = list(set(temp_list))
    
    # Group curves by temperature
    curve_dict = {}
    for temp in temp_list:

        # Sort curves by stress
        curve_list = [exp_curve for exp_curve in exp_curves if exp_curve["type"] == "creep" and exp_curve["temp"] == temp]
        curve_list.sort(key=get_stress)
        
        # Get their indexes and add to map
        index_list = [exp_curves.index(temp_curve) for temp_curve in curve_list]
        curve_dict[temp] = index_list
    
    # Return the mapping
    return curve_dict