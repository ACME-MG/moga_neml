"""
 Title:         Error Template
 Description:   Contains the basic structure for an error class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os, pathlib, sys

# Constants
EXCLUSION_LIST = ["__error__", "__error_example__", "__pycache__"]

# The Error Template Class
class ErrorTemplate:

    # Sets the name
    def set_name(self, name:str) -> None:
        self.name = name

    # Sets the experimental curve
    def set_exp_curve(self, exp_curve:dict) -> None:
        self.exp_curve = exp_curve

    # Sets the weight
    def set_weight(self, weight:float) -> None:
        self.weight = weight

    # Returns the name of the error
    def get_name(self) -> str:
        return self.name

    # Returns the weight of the error
    def get_weight(self) -> float:
        return self.weight

    # Returns the experimental curve
    def get_exp_curve(self) -> dict:
        return self.exp_curve

    # Returns an error (must be overridden)
    def get_value(self) -> float:
        raise NotImplementedError

    # Runs at the start, once (optional placeholder)
    def prepare(self) -> None:
        pass

# Creates and return a error
def get_error(error_name:str, exp_curve:dict, weight:float) -> ErrorTemplate:

    # Get available errors in current folder
    errors_dir = pathlib.Path(__file__).parent.resolve()
    files = os.listdir(errors_dir)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if error name not in available errors
    if not error_name in files:
        raise NotImplementedError(f"The error '{error_name}' has not been implemented")

    # Prepare dynamic import
    module_path = f"{errors_dir}/{error_name}.py"
    spec = importlib.util.spec_from_file_location("error_file", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    
    # Import and initialise error
    from error_file import Error
    error = Error()
    
    # Prepare and return error
    error.set_name(error_name)
    error.set_exp_curve(exp_curve)
    error.set_weight(weight)
    error.prepare()
    return error