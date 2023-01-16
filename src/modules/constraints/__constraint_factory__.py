"""
 Title:         The Constraint Factory
 Description:   For creating and returning constraint objects
 Author:        Janzen Choi

"""

# Constraints
from modules.constraints.dec_x_end import DecXEnd
from modules.constraints.inc_y_end import IncYEnd

# Returns a list of constraints
def get_constraint_list(constraint_names, exp_curves):
    constraint_list = (
        DecXEnd(exp_curves),
        IncYEnd(exp_curves),
    )
    constraint_list = [constraint for constraint in constraint_list if constraint.get_name() in constraint_names]
    return constraint_list