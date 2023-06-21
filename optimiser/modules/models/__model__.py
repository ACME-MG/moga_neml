"""
 Title:         Model Template
 Description:   Contains the basic structure for a model class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os

# Constants
MIN_DATA = 10
PATH_TO_MODELS = "modules/models"
EXCLUSION_LIST = ["__model__", "__pycache__"]

# The Model Template Class
class ModelTemplate:

    # Constructor
    def __init__(self):
        self.param_info = []
        self.exp_curve = None
        self.args = ()

    # Adds a parameter and bounds
    def add_param(self, name:str, min:float=0.0e0, max:float=1.0e0) -> None:
        self.param_info += [{"name": name, "min": min, "max": max}]

    # Sets the name
    def set_name(self, name:str) -> None:
        self.name = name

    # Sets the experimental curve
    def set_exp_curve(self, exp_curve:dict) -> None:
        self.exp_curve = exp_curve
    
    # Sets a list of arguments
    def set_args(self, args) -> None:
        self.args = args

    # Gets the name
    def get_name(self) -> str:
        return self.name

    # Returns the experimental curve
    def get_exp_curve(self) -> list:
        return self.exp_curve

    # Returns the parameter info
    def get_param_info(self) -> list:
        return self.param_info
        
    # Gets a list of arguments
    def get_args(self) -> tuple:
        return self.args

    # Runs at the start, once (must be overridden)
    def prepare(self) -> None:
        raise NotImplementedError

    # Gets a predicted curve (must be overridden)
    def get_prd_curve(self, _1, _2) -> dict:
        raise NotImplementedError

# Creates and return a model
def get_model(model_name:str, exp_curve:dict, args:list=[]) -> ModelTemplate:

    # Get available models in current folder
    files = os.listdir(PATH_TO_MODELS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if model name not in available models
    if not model_name in files:
        raise NotImplementedError(f"The model '{model_name}' has not been implemented")

    # Import and initialise model
    module = f"{PATH_TO_MODELS}/{model_name}".replace("/", ".")
    model_file = importlib.import_module(module)
    model = model_file.Model()

    # Prepare and return model
    model.set_name(model_name)
    model.set_exp_curve(exp_curve)
    model.set_args(args)
    model.prepare()
    return model