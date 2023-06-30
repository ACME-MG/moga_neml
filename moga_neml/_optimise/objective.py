"""
 Title:         The Objective class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import moga_neml.errors.__error__ as __error__
import moga_neml.models.__model__ as __model__
import moga_neml._optimise.driver as driver


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
        self.fix_param_dict = {}
        self.init_param_dict = {}
    
    # Adds experimental curves to the optimisation information list
    def add_curves(self, curves:list, data_type:str) -> None:
        for curve in curves:
            self.objective_list.append({
                "curve": curve,
                "data_type": data_type
            })

    # Defines the model's name
    def def_model(self, model_name:str, *model_args) -> None:
        self.model_name = model_name
        self.model_args = model_args

    # Adds error to optimisation
    def add_error(self, error_name:str, type:str, weight:float) -> None:
        self.error_info_list.append({"name": error_name, "type": type, "weight": weight})
    
    # Fixes a parameter
    def fix_param(self, param_name:str, param_value:float) -> None:
        self.fix_param_dict[param_name] = param_value

    # Initialises a parameter
    def init_param(self, param_name:str, param_value:float) -> None:
        self.init_param_dict[param_name] = param_value

    # Defines everything based on curves, model, errors, and fixed parameters
    def define_optimisation(self):

        # Check that curves have been added
        if len(self.objective_list) == []:
            raise ValueError("No curves have been added to the optimisation!")

        # Add data to optimisation
        for objective in self.objective_list:
            objective["model"] = __model__.get_model(self.model_name, objective["curve"], *self.model_args)
            objective["errors"] = {}
            for error_info in self.error_info_list:
                if objective["curve"]["type"] == error_info["type"]:
                    objective["errors"][error_info["name"]] = __error__.get_error(error_info["name"], objective["curve"], error_info["weight"])
        
        # Initialise parameter checking
        param_dict = self.get_param_dict()
        param_names = param_dict.keys()
        
        # Check that fixed parameters exist
        for param_name in self.fix_param_dict.keys():
            if not param_name in param_names:
                raise ValueError(f"'{param_name}' cannot be fixed because it is not defined in the {self.model_name} model!")

        # Check that initialised parameters exist, have not been fixed, and are within the bounds
        for param_name in self.init_param_dict.keys():
            if not param_name in param_names:
                raise ValueError(f"'{param_name}' cannot be initialised because it is not defined in the {self.model_name} model!")
            if param_name in self.fix_param_dict.keys():
                raise ValueError(f"'{param_name}' cannot be both fixed and initialised!")
            if self.init_param_dict[param_name] > param_dict[param_name]["u_bound"]:
                raise ValueError(f"'{param_name}' has been initialised with a value greater than the defined upper bound!")
            if self.init_param_dict[param_name] < param_dict[param_name]["l_bound"]:
                raise ValueError(f"'{param_name}' has been initialised with a value less than the defined upper bound!")

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

    # Gets the model
    def get_model(self) -> dict:
        if len(self.objective_list) == 0:
            raise ValueError("No data has been added! Can't retrieve model!")
        model = self.objective_list[0]["model"] # assume curves >= 1
        return model

    # Gets the parameter information from the model
    def get_param_dict(self) -> dict:
        model = self.get_model()
        return model.get_param_dict()

    # Gets information about the fixed parameters
    def get_fix_param_dict(self) -> dict:
        return self.fix_param_dict

    # Gets information about the initialised parameters
    def get_init_param_dict(self) -> dict:
        return self.init_param_dict

    # Incorporates the fixed parameters
    def incorporate_fix_param_dict(self, *params) -> list:
        param_names = list(self.get_param_dict().keys())
        fix_indexes = [i for i in range(len(param_names)) if param_names[i] in self.fix_param_dict.keys()]
        params = list(params)
        for fix_index in fix_indexes:
            fix_value = self.fix_param_dict[param_names[fix_index]]
            params.insert(fix_index, fix_value)
        return tuple(params)

    # Returns the information of unfixed parameters
    def get_unfix_param_dict(self) -> dict:
        unfix_param_dict = {}
        param_dict = self.get_param_dict()
        for param_name in param_dict.keys():
            if not param_name in self.fix_param_dict.keys():
                unfix_param_dict[param_name] = param_dict[param_name]
        return unfix_param_dict

    # Gets the predicted curves
    def get_prd_curves(self, data_types:list=["train", "test"], curve_type:str="all", *params) -> list:
        
        # Iterate through curves
        prd_curves = []
        for objective in self.objective_list:
            
            # Ignore if not applicable
            if (not objective["data_type"] in data_types
            or (curve_type != "all" and objective["curve"]["type"] != curve_type)):
                continue

            # Fix parameters and calibrate model
            params = self.incorporate_fix_param_dict(*params)
            calibrated_model = objective["model"].get_model(*params)
            if calibrated_model == None:
                return []
            
            # Get driver and get curve
            model_driver = driver.Driver(objective["curve"], calibrated_model)
            prd_curve = model_driver.run()
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