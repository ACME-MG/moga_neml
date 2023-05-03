"""
 Title:         Error Template
 Description:   Contains the basic structure for an error class
 Author:        Janzen Choi

"""

# Libraries
import importlib, os

# Constants
PATH_TO_ERRORS = "modules/errors"
EXCLUSION_LIST = ["__error__", "__pycache__"]

# The Error Template Class
class ErrorTemplate:

    # Sets values
    def set_vals(self, name:str, type:str, weight:float, exp_curves:list[dict]) -> None:
        self.name = name
        self.type = type
        self.weight = weight
        self.exp_curves = exp_curves

    # Returns the name of the error
    def get_name(self) -> str:
        return self.name

    # Returns the type of the error
    def get_type(self) -> str:
        return self.type

    # Returns the weight of the error
    def get_weight(self) -> float:
        return self.weight

    # Returns the experimental curve
    def get_exp_curves(self) -> list[dict]:
        return self.exp_curves

    # Prepares the object for evaluation (optional placeholder)
    def prepare(self) -> None:
        pass
    
    # Returns an error (placeholder)
    def get_value(self) -> None:
        raise NotImplementedError

# Creates and return a error
def get_error(error_name:str, type:str, weight:float, exp_curves:list[dict]) -> ErrorTemplate:

    # Get available errors in current folder
    files = os.listdir(PATH_TO_ERRORS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if error name not in available errors
    if not error_name in files:
        raise NotImplementedError(f"The error '{error_name}' has not been implemented")

    # Import and prepare error
    module = f"{PATH_TO_ERRORS}/{error_name}".replace("/", ".")
    error_file = importlib.import_module(module)
    error = error_file.Error()
    error.set_vals(error_name, type, weight, exp_curves)
    error.prepare()

    # Return the error
    return error