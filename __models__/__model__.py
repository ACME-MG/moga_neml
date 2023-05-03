"""
 Title:         Model Template
 Description:   Contains the basic structure for a model class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, sys
from copy import deepcopy
sys.path += ["../__common__"]
from curve import get_curve

# Constants
MIN_DATA = 10
PATH_TO_MODELS = "../__models__"
EXCLUSION_LIST = ["__model__", "__model__", "__pycache__"]

# The Model Template Class
class ModelTemplate:

    # Constructor
    def __init__(self, param_info:dict) -> None:
        self.param_info = param_info
   
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
    def get_param_info(self) -> dict:
        return self.param_info

    # Returns the parameter names
    def get_param_names(self) -> list[str]:
        return [param["name"] for param in self.param_info]

    # Returns the parameter lower bounds
    def get_param_lower_bounds(self) -> list[float]:
        return [param["min"] for param in self.param_info]

    # Returns the parameter upper bounds
    def get_param_upper_bounds(self) -> list[float]:
        return [param["max"] for param in self.param_info]

    # Returns the experimental curves
    def get_exp_curves(self) -> list[dict]:
        return self.exp_curves
    
    # Prepares the model (placeholder)
    def prepare(self, args) -> None:
        raise NotImplementedError

    # Gets the predicted curves (to be overridden)
    def get_prd_curves(self) -> list[dict]:
        return [get_curve([], []) for _ in range(len(self.exp_curves))] # do not remove [], []

    # Gets the predicted curves for specified curves
    def get_specified_prd_curves(self, params:list, exp_curves:list[dict]) -> list[dict]:
        old_exp_curves = deepcopy(self.exp_curves)
        self.exp_curves = exp_curves
        prd_curves = self.get_prd_curves(*params)
        self.exp_curves = old_exp_curves
        return prd_curves

    # For checking the validity of a predicted curve
    def ensure_validity(self, prd_curves:list[dict]) -> list[dict]:
        for prd_curve in prd_curves:
            if len(prd_curve["x"]) != len(prd_curve["y"]) or len(prd_curve["x"]) < MIN_DATA:
                return []
        return prd_curves

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
    model_file = importlib.import_module(model_name)
    model = model_file.Model()
    model.set_name(model_name)
    model.set_exp_curves(exp_curves)
    model.prepare(args)

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