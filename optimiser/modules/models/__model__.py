"""
 Title:         Model Template
 Description:   Contains the basic structure for a model class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, sys
from copy import deepcopy

# Constants
MIN_DATA = 10
PATH_TO_MODELS = "modules/models"
EXCLUSION_LIST = ["__model__", "__pycache__"]

# The Model Template Class
class ModelTemplate:

    # Constructor
    def __init__(self):
        self.param_info = []
        self.fixed_params = {}

    # Adds a parameter and bounds
    def add_param(self, name:str, min:float=0.0e0, max:float=1.0e0) -> None:
        self.param_info += [{"name": name, "min": min, "max": max}]
    
    # Fixes a parameter
    def fix_param(self, name:str, value:float) -> None:
        all_param_names = [param["name"] for param in self.param_info]
        if name in all_param_names:
            self.fixed_params[name] = value

    # Sets a list of arguments
    def set_args(self, args) -> None:
        self.args = args

    # Sets the name
    def set_name(self, name:str) -> None:
        self.name = name

    # Gets the name
    def get_name(self) -> str:
        return self.name

    # Sets the experimental curves
    def set_exp_curves(self, exp_curves:list[dict]) -> None:
        self.exp_curves = exp_curves

    # Returns the parameter info
    def get_param_info(self) -> list[dict]:
        return self.param_info
    
    # Returns a dict of the fixed parameters
    def get_fixed_params(self) -> dict:
        return self.fixed_params

    # Returns the information of unfixed parameters
    def get_unfixed_param_info(self) -> list[dict]:
        unfixed_param_info = []
        for param in self.param_info:
            if not param["name"] in self.fixed_params.keys():
                unfixed_param_info.append(param)
        return unfixed_param_info

    # Incorporates the fixed parameters
    def incorporate_fixed_params(self, *params) -> list[float]:
        param_names = [param["name"] for param in self.param_info]
        fixed_indexes = [i for i in range(len(param_names)) if param_names[i] in self.fixed_params.keys()]
        params = list(params)
        for fixed_index in fixed_indexes:
            fixed_value = self.fixed_params[param_names[fixed_index]]
            params.insert(fixed_index, fixed_value)
        return tuple(params)

    # Returns the experimental curves
    def get_exp_curves(self) -> list[dict]:
        return self.exp_curves

    # Gets a predicted curve (must be overridden)
    def get_prd_curve(self, _1, _2) -> dict:
        raise NotImplementedError

    # Gets the predicted curves
    def get_prd_curves(self, *params) -> list[dict]:
        params = self.incorporate_fixed_params(*params)
        prd_curves = []
        for exp_curve in self.exp_curves:
            try:
                prd_curve = self.get_prd_curve(exp_curve, *params)
                if prd_curve != None:
                    prd_curves.append(prd_curve)
            except:
                return []
        return prd_curves

    # Gets the predicted curves for specified curves
    def get_specified_prd_curves(self, params:list, exp_curves:list[dict]) -> list[dict]:
        old_exp_curves = deepcopy(self.exp_curves)
        self.exp_curves = exp_curves
        prd_curves = self.get_prd_curves(*params)
        self.exp_curves = old_exp_curves
        return prd_curves

    # For checking the validity of a curve
    def ensure_validity(self, curves:list[dict]) -> list[dict]:
        for curve in curves:
            list_values = [key for key in curve.keys() if len(curve[key]) > 1]
            if len(list_values) == 0 or False in [len(list_values[0]) == len(lv) for lv in list_values]:
                return []
        return curves

    # Runs at the start, once (placeholder)
    def prepare(self):
        raise NotImplementedError

# Creates and return a model
def get_model(model_name:str, exp_curves:list[dict], args:list=[]) -> ModelTemplate:

    # Get available models in current folder
    files = os.listdir(PATH_TO_MODELS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if model name not in available models
    if not model_name in files:
        raise NotImplementedError(f"The model '{model_name}' has not been implemented")

    # Import and prepare model
    module = f"{PATH_TO_MODELS}/{model_name}".replace("/", ".")
    model_file = importlib.import_module(module)
    model = model_file.Model()
    model.set_name(model_name)
    model.set_exp_curves(exp_curves)
    model.set_args(args)
    model.prepare()

    # Return the model
    return model

# For blocking prints
class BlockPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, _1, _2, _3):
        sys.stdout.close()
        sys.stdout = self._original_stdout