"""
 Title:         Curve
 Description:   For storing information about a curve
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.errors.__error__ import get_error
from moga_neml.models.__model__ import __Model__

# The Curve class
class Curve:
    
    # Constructor
    def __init__(self, type:str, exp_data:dict, model:__Model__):
        
        # Initialise inputs variables
        self.type     = type
        self.exp_data = exp_data
        self.model    = model
        
        # Initialise internal variables
        self.error_list = []
    
    # Sets the experimental data
    def set_exp_data(self, exp_data:dict) -> None:
        self.exp_data = exp_data
    
    # Gets the curve type
    def get_type(self) -> str:
        return self.type
    
    # Gets whether the curve will be used for training or validation
    def get_train(self) -> bool:
        return len(self.error_list) != 0
    
    # Gets the experimental data
    def get_exp_data(self) -> dict:
        return self.exp_data
    
    # Gets the model
    def get_model(self) -> __Model__:
        return self.model
    
    # Gets the list of errors
    def get_error_list(self) -> list:
        return self.error_list
    
    # Adds an error to the list
    def add_error(self, error_name:str, x_label:str, y_label:str, weight:float, **kwargs) -> None:
        
        # Check labels
        for label in [x_label, y_label]:
            if label != "" and not label in self.exp_data.keys():
                raise ValueError(f"Error {error_name} cannot be added because '{label}' is not a field in the data!")
        
        # Add error
        error = get_error(error_name, x_label, y_label, weight, self.exp_data, self.model, **kwargs)
        self.error_list.append(error)
    