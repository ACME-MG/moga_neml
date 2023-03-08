"""
 Title:         The Error Factory
 Description:   For creating and returning error objects
 Author:        Janzen Choi

"""

# Errors
from modules.errors.dy_area import DyArea
from modules.errors.x_area import XArea
from modules.errors.y_area import YArea
from modules.errors.x_end import XEnd
from modules.errors.y_end import YEnd

# Returns a list of errors
def get_error_list(type, error_names, exp_curves):
    error_list = (
        DyArea(type, exp_curves),
        XArea(type, exp_curves),
        YArea(type, exp_curves),
        XEnd(type, exp_curves),
        YEnd(type, exp_curves),
    )
    error_list = [error for error in error_list if error.get_name() in error_names]
    [error.prepare() for error in error_list]
    return error_list