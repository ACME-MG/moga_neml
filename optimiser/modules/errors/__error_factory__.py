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

# Helper libraries
import sys
sys.path += ["../__common__"]
from curve import get_custom_thin_indexes

# Returns an error given a name
def create_error(error_name, type, weight, exp_curves):
    error_list = (
        DyArea(type, weight, exp_curves),
        XArea(type, weight, exp_curves),
        YArea(type, weight, exp_curves),
        XEnd(type, weight, exp_curves),
        YEnd(type, weight, exp_curves),
    )
    error = [error for error in error_list if error.get_name() == error_name][0]
    error.prepare()
    return error

# Returns the YArea error with a custom CDF
def create_custom_y_area_error(type, weight, exp_curves, cdf):
    y_area = YArea(type, weight, exp_curves)
    def get_thin_indexes(src_data_size, dst_data_size):
        return get_custom_thin_indexes(src_data_size, dst_data_size, cdf)
    y_area.prepare(get_thin_indexes)
    return y_area