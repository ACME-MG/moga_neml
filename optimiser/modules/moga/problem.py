"""
 Title:         Problem
 Description:   For defining the MOGA problem
 Author:        Janzen Choi

"""

# Libraries
import warnings
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from modules.moga.objective import Objective
from modules.recorder import Recorder

# The Problem class
class Problem(ElementwiseProblem):

    # Constructor
    def __init__(self, objective:Objective, recorder:Recorder):
        
        # Initialise
        self.objective = objective
        self.recorder  = recorder
        
        # Define the element wise problem
        unfixed_params = self.objective.get_unfixed_param_info()
        super().__init__(
            n_var = len(unfixed_params),
            n_obj = len(self.objective.get_error_names()),
            xl    = np.array([param["min"] for param in unfixed_params]),
            xu    = np.array([param["max"] for param in unfixed_params]),
        )
    
    # Minimises expression "F" such that the expression "G <= 0" is satisfied
    def _evaluate(self, params:list[float], out:dict, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore") # ignore warnings
            error_values = self.objective.get_error_values(*params)
            self.recorder.update_results(params, error_values)
            out["F"] = error_values