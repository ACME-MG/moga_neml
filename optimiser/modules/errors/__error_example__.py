"""
 Title:         Error Example
 Description:   Follow this structure when creating custom errors
 Author:        Janzen Choi

 """

# Libraries
import modules.errors.__error__ as error

# The Error class
class Error(error.ErrorTemplate):
    
    # Runs at the start, once (optional)
    def prepare(self):
        exp_curve = self.get_exp_curve()

    # Computes the error value
    def get_value(self, prd_curve:dict) -> float:
        return 100