"""
 Title:         The Objective class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
from modules.errors.__error__ import get_error
from modules.models.__model__ import get_model

# Constants
MIN_DATA = 50
BIG_VALUE = 10000

# The Objective class
class Objective():

    # Constructor
    def __init__(self):
        self.objective_list = []
        self.model_name = ""
        self.model_args = ()
        self.error_info_list = []
        self.fixed_params = {}
    
    # Adds experimental curves to the optimisation information list
    def add_curves(self, curves:list, data_type:str) -> None:
        for curve in curves:
            self.objective_list.append({
                "curve": curve,
                "data_type": data_type
            })

    # Defines the model's name
    def define_model(self, model_name:str, *model_args) -> None:
        print(model_name, model_args)
        self.model_name = model_name
        self.model_args = model_args

    # Adds error to optimisation
    def add_error(self, error_name:str, type:str, weight:float) -> None:
        self.error_info_list.append({"name": error_name, "type": type, "weight": weight})
    
    # Fixes a parameter
    def fix_param(self, param_name:str, param_value:float) -> None:
        self.fixed_params[param_name] = param_value

    # Defines everything based on curves, model, errors, and fixed parameters
    def define_optimisation(self):

        # Check that curves have been added
        if len(self.objective_list) == []:
            raise ValueError("No curves have been added to the optimisation!")

        # Add data to optimisation
        for objective in self.objective_list:
            objective["model"] = get_model(self.model_name, objective["curve"], self.model_args)
            objective["errors"] = {}
            for error_info in self.error_info_list:
                if objective["curve"]["type"] == error_info["type"]:
                    objective["errors"][error_info["name"]] = get_error(error_info["name"], objective["curve"], error_info["weight"])
        
        # Check that fixed parameters exist
        param_names = [param["name"] for param in self.get_param_info()]
        for fixed_param in self.fixed_params:
            if not fixed_param["name"] in param_names:
                raise ValueError(f"'{fixed_param['name']}' cannot be fixed because it is not defined in the model!")

    # Returns the model's name
    def get_model_name(self):
        return self.model_name

    # Returns the error names
    def get_error_names(self) -> list:
        return [error_info["name"] for error_info in self.error_info_list]

    # Returns the error types
    def get_error_types(self) -> list:
        return [error_info["type"] for error_info in self.error_info_list]

    # Returns the error weights
    def get_error_weights(self) -> list:
        return [error_info["weight"] for error_info in self.error_info_list]

    # Gets the experimental curves
    def get_exp_curves(self, data_types:list=["train", "test"]):
        return [objective["curve"] for objective in self.objective_list if objective["data_type"] in data_types]

    # Gets the parameter information from the model
    def get_param_info(self) -> dict:
        model = self.objective_list[0]["model"] # assume curves >= 1
        return model.get_param_info()

    # Gets information about the fixed parameters
    def get_fixed_params(self) -> dict:
        return self.fixed_params

    # Incorporates the fixed parameters
    def incorporate_fixed_params(self, *params) -> list:
        param_names = [param["name"] for param in self.get_param_info()]
        fixed_indexes = [i for i in range(len(param_names)) if param_names[i] in self.fixed_params.keys()]
        params = list(params)
        for fixed_index in fixed_indexes:
            fixed_value = self.fixed_params[param_names[fixed_index]]
            params.insert(fixed_index, fixed_value)
        return tuple(params)

    # Returns the information of unfixed parameters
    def get_unfixed_param_info(self) -> list:
        unfixed_param_info = []
        for param in self.get_param_info():
            if not param["name"] in self.fixed_params.keys():
                unfixed_param_info.append(param)
        return unfixed_param_info

    # Gets the predicted curves
    def get_prd_curves(self, data_types:list=["train", "test"], curve_type:str="all", *params) -> list:
        
        # Iterate through curves
        prd_curves = []
        for objective in self.objective_list:
            
            # Ignore if not applicable
            if (not objective["data_type"] in data_types
            or (curve_type != "all" and objective["curve"]["type"] != curve_type)):
                continue

            # Fix parameters and get curves
            params = self.incorporate_fixed_params(*params)
            prd_curve = objective["model"].get_prd_curve(*params)
            if prd_curve == None or len(prd_curve["x"]) < MIN_DATA:
                return []
            prd_curve["objective"] = objective
            prd_curves.append(prd_curve)
        
        # Return predicted curves
        return prd_curves

    # Gets the error values
    def get_error_values(self, *params) -> list:

        # Gets the predicted curves and check
        prd_curves = self.get_prd_curves(["train"], "all", *params)
        if prd_curves == []:
            return [BIG_VALUE] * len(self.error_info_list)

        # Get errors from predicted curves and append
        error_values = []
        for error_info in self.error_info_list:
            error_value_list = []

            # Iterate through predicted curves
            for prd_curve in prd_curves:
                objective = prd_curve["objective"]
                if objective["curve"]["type"] == error_info["type"]:
                    error = objective["errors"][error_info["name"]]
                    error_value = error.get_value(prd_curve) * error.get_weight()
                    error_value_list.append(error_value)
            
            # Average errors and append
            avg_error_value = np.average(error_value_list)
            error_values.append(avg_error_value)

        # Return errors
        return error_values