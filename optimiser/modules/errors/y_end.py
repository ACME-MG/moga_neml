"""
 Title:         The y_end objective function
 Description:   The objective function for calculating the vertical distance in which two curves end
 Author:        Janzen Choi

"""

# Libraries
import modules.errors.__error__ as error

# The YEnd class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.exp_y_end = abs(exp_curve["y"][-1])

    # Computing the error
    def get_value(self, prd_curve:list) -> float:
        return abs(prd_curve["y"][-1] - self.exp_y_end) / self.exp_y_end