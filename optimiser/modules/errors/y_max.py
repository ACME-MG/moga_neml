"""
 Title:         The y_max objective function
 Description:   The objective function for calculating the maximum y magnitude of two curves
 Author:        Janzen Choi

"""

# Libraries
import modules.errors.__error__ as error

# The YArea class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once
    def prepare(self):
        exp_curve = self.get_exp_curve()
        self.y_max = abs(max(exp_curve["y"]))
            
    # Computing the error
    def get_value(self, prd_curve:list) -> float:
        return abs(self.y_max - max(prd_curve["y"])) / self.y_max