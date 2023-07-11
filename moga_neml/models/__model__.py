"""
 Title:         Model Template
 Description:   Contains the basic structure for a model class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, pathlib, sys

# The Model Template Class
class __Model__:

    # Constructor
    def __init__(self, name:str, args:tuple):
        
        # Initialise input variables
        self.name = name
        self.args = args
        
        # Initialise internal variables
        self.param_dict = {}
        self.exp_data = {}
        self.args = ()

    # Adds a parameter and bounds
    def add_param(self, name:str, l_bound:float=0.0e0, u_bound:float=1.0e0) -> None:
        if name in self.param_dict.keys():
            raise ValueError("The parameter has already been defined!")
        self.param_dict[name] = {"l_bound": l_bound, "u_bound": u_bound}

    # Sets the experimental data
    def set_exp_data(self, exp_data:dict) -> None:
        self.exp_data = exp_data

    # Gets the name
    def get_name(self) -> str:
        return self.name

    # Returns the experimental data
    def get_exp_data(self) -> list:
        return self.exp_data

    # Returns a field of the experimental data
    def get_data(self, field:str):
        if not field in self.exp_data.keys():
            raise ValueError(f"The experimental data does not contain the {field} field")
        return self.exp_data[field]

    # Returns the parameter info
    def get_param_dict(self) -> dict:
        return self.param_dict
        
    # Gets an argument
    def get_arg(self, index) -> tuple:
        return self.args[index]

    # Gets the calibrated model
    def get_calibrated_model(self, *params): # -> NEML Model
        self.calibrated_model = self.calibrate_model(*params)
        return self.calibrated_model

    # Gets the last calibrated model
    def get_last_calibrated_model(self):
        if self.calibrated_model == None:
            raise ValueError("Could not get the calibrated model because it has not been calibrated yet!")
        return self.calibrated_model

    # Runs at the start, once (must be overridden)
    def initialise(self) -> None:
        raise NotImplementedError
        
    # Gets the model (must be overridden)
    #   Returns None if the parameter set / model is invalid
    def calibrate_model(self, *params): # -> NEML Model
        raise NotImplementedError

# Creates and return a model
def get_model(model_name:str, args:tuple=()) -> __Model__:

    # Get available models in current folder
    models_dir = pathlib.Path(__file__).parent.resolve()
    files = os.listdir(models_dir)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in ["__model__", "__pycache__"]]
    
    # Raise error if model name not in available models
    if not model_name in files:
        raise NotImplementedError(f"The model '{model_name}' has not been implemented")

    # Prepare dynamic import
    module_path = f"{models_dir}/{model_name}.py"
    spec = importlib.util.spec_from_file_location("model_file", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    
    # Initialise and return the model
    from model_file import Model
    model = Model(model_name, args)
    model.initialise()
    return model