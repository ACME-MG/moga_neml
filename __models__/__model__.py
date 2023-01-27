"""
 Title:         Model
 Description:   Contains the basic structure for a model class
 Author:        Janzen Choi

"""

# Libraries
import os, sys
from copy import deepcopy

# Helper libraries
sys.path += ["../__common__"]
from curve import get_curve

# The Model Class
class Model:

    # Constructor
    def __init__(self, name, param_info, exp_curves):
        self.name = name
        self.param_info = param_info
        self.exp_curves = exp_curves

    # Returns the name of the model
    def get_name(self):
        return self.name

    # Returns the parameter info
    def get_param_info(self):
        return self.param_info

    # Returns the parameter names
    def get_param_names(self):
        return [param["name"] for param in self.param_info]

    # Returns the parameter lower bounds
    def get_param_lower_bounds(self):
        return [param["min"] for param in self.param_info]

    # Returns the parameter upper bounds
    def get_param_upper_bounds(self):
        return [param["max"] for param in self.param_info]

    # Returns the experimental curves
    def get_exp_curves(self):
        return self.exp_curves
    
    # Prepares the model (placeholder)
    def prepare(self, args):
        raise NotImplementedError

    # Gets the predicted curves (to be overridden)
    def get_prd_curves(self):
        return [get_curve([], []) for _ in range(len(self.exp_curves))] # do not remove [], []

    # Gets the predicted curves for specified curves
    def get_specified_prd_curves(self, params, exp_curves):
        old_exp_curves = deepcopy(self.exp_curves)
        self.exp_curves = exp_curves
        prd_curves = self.get_prd_curves(*params)
        self.exp_curves = old_exp_curves
        return prd_curves

# For blocking prints
class BlockPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, _1, _2, _3):
        sys.stdout.close()
        sys.stdout = self._original_stdout