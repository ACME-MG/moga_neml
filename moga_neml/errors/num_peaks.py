"""
 Title:         The n_cycles objective function
 Description:   The objective function for calculating the number of cycles in a periodic curve
 Author:        Janzen Choi

 """

# Libraries
from moga_neml.errors.__error__ import __Error__
from moga_neml.maths.derivative import get_stationary_points

# The Error class
class Error(__Error__):
    
    # Runs at the start, once (optional)
    def initialise(self):
        self.enforce_data_type("cyclic")
        exp_data = self.get_exp_data()
        self.x_label = self.get_x_label()
        self.y_label = self.get_y_label()
        self.exp_num_cycles = get_cycle(exp_data, self.x_label, self.y_label)

    # Computes the error value
    def get_value(self, prd_data:dict) -> float:
        prd_num_cycles = get_cycle(prd_data, self.x_label, self.y_label)
        return abs(self.exp_num_cycles - prd_num_cycles) / self.exp_num_cycles

# Gets the number of cycles
def get_cycle(data_dict:dict, x_label:str, y_label:str) -> int:
    return len(get_stationary_points(data_dict, x_label, y_label, 0.2, 0.9))
