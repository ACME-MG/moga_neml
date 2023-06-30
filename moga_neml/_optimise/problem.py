"""
 Title:         Problem
 Description:   For defining the MOGA problem
 Author:        Janzen Choi

"""

# Libraries
import warnings
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from moga_neml._optimise.objective import Objective
from moga_neml._optimise.recorder import Recorder

# The Problem class
class Problem(ElementwiseProblem):

    # Constructor
    def __init__(self, objective:Objective, recorder:Recorder):
        
        # Initialise
        self.objective = objective
        self.recorder  = recorder
        
        # Get unfixed parameter information
        unfix_param_dict = self.objective.get_unfix_param_dict()
        l_bound_list = [unfix_param_dict[param_name]["l_bound"] for param_name in unfix_param_dict.keys()]
        u_bound_list = [unfix_param_dict[param_name]["u_bound"] for param_name in unfix_param_dict.keys()]
        
        # Define the element wise problem
        super().__init__(
            n_var = len(unfix_param_dict.keys()),
            n_obj = len(self.objective.get_error_names()),
            xl    = np.array(l_bound_list),
            xu    = np.array(u_bound_list),
        )
    
    # Gets the objective
    def get_objective(self) -> Objective:
        return self.objective
    
    # Gets the recorder
    def get_recorder(self) -> Recorder:
        return self.recorder
    
    # Minimises expression "F" such that the expression "G <= 0" is satisfied
    def _evaluate(self, params:list, out:dict, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore") # ignore warnings
            error_values = self.objective.get_error_values(*params)
            self.recorder.update_results(params, error_values)
            out["F"] = error_values