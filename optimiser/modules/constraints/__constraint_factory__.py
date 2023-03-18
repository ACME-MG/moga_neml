"""
 Title:         The Constraint Factory
 Description:   For creating and returning constraint objects
 Author:        Janzen Choi

"""

# Constraints
from modules.constraints.dec_x_end import DecXEnd
from modules.constraints.inc_y_end import IncYEnd

# Returns a constraint given a name
def create_constraint(constraint_name, type, penalty, exp_curves):
    constraint_list = (
        DecXEnd(type, penalty, exp_curves),
        IncYEnd(type, penalty, exp_curves),
    )
    constraint = [constraint for constraint in constraint_list if constraint.get_name() == constraint_name][0]
    return constraint