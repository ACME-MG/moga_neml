"""
 Title:         The Objective class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
from copy import deepcopy
from moga_neml.models.__model__ import __Model__, get_model
from moga_neml._interface.plotter import Plotter
from moga_neml._maths.experiment import DATA_FIELD_PLOT_MAP
from moga_neml._optimise.driver import Driver
from moga_neml._optimise.objective import Objective
from moga_neml._maths.derivative import differentiate_curve

# Constants
MIN_DATA = 50
BIG_VALUE = 10000

# The Controller class
class Controller():

    # Constructor
    def __init__(self):
        self.model = None
        self.objective_list = []
        self.fix_param_dict = {}
        self.set_param_dict = {}
        
    # Defines the model
    def define_model(self, model_name:str, *model_args:tuple) -> None:
        self.model = get_model(model_name, *model_args)
        
    # Adds experimental data
    def add_objective(self, type:str, exp_data:dict) -> None:
        objective = Objective(type, exp_data)
        self.objective_list.append(objective)
    
    # Gets the list of objectives
    def get_objective_list(self) -> list:
        return self.objective_list
    
    # Returns the most recently added objective
    def get_last_objective(self) -> Objective:
        if self.objective_list == []:
            raise ValueError("No objectives have been added yet!")
        return self.objective_list[-1]
    
    # Fixes a parameter to a value
    def fix_param(self, param_name:str, param_value:float) -> None:
        param_dict = self.model.get_param_dict()
        pretext = f"The '{param_name}' parameter cannot be fixed because"
        if not param_name in param_dict.keys():
            raise ValueError(f"{pretext} it is not defined in {self.model.get_name()}!")
        if param_name in self.set_param_dict.keys():
            raise ValueError(f"{pretext} it has already been set!")
        self.fix_param_dict[param_name] = param_value

    # Sets the initial value of a parameter
    def set_param(self, param_name:str, param_value:float, param_std:float) -> None:
        param_dict = self.model.get_param_dict()
        pretext = f"The '{param_name}' parameter cannot be set because"
        if not param_name in param_dict.keys():
            raise ValueError(f"{pretext} it is not defined in {self.model.get_name()}!")
        if param_name in self.fix_param_dict.keys():
            raise ValueError(f"{pretext} it has already been fixed!")
        if param_value - param_std < param_dict[param_name]["l_bound"]:
            raise ValueError(f"{pretext} has been set an initial 'value + deviation' smaller than its lower bound!")
        if param_value + param_std > param_dict[param_name]["u_bound"]:
            raise ValueError(f"{pretext} has been set an initial 'value + deviation' larger than its upper bound!")
        self.set_param_dict[param_name] = {"value": param_value, "std": param_std}

    # Returns the model
    def get_model(self) -> __Model__:
        if self.model == None:
            raise ValueError("The model cannot be retrieved because it has not been defined yet!")
        return self.model

    # Gets information about the fixed parameters
    def get_fix_param_dict(self) -> dict:
        return self.fix_param_dict

    # Gets information about the initialised parameters
    def get_set_param_dict(self) -> dict:
        return self.set_param_dict

    # Incorporates the fixed parameters
    def incorporate_fix_param_dict(self, *params) -> list:
        param_names = list(self.model.get_param_dict().keys())
        fix_indexes = [i for i in range(len(param_names)) if param_names[i] in self.fix_param_dict.keys()]
        params = list(params)
        for fix_index in fix_indexes:
            fix_value = self.fix_param_dict[param_names[fix_index]]
            params.insert(fix_index, fix_value)
        return tuple(params)

    # Returns the information of unfixed parameters
    def get_unfix_param_dict(self) -> dict:
        unfix_param_dict = {}
        param_dict = self.model.get_param_dict()
        for param_name in param_dict.keys():
            if not param_name in self.fix_param_dict.keys():
                unfix_param_dict[param_name] = param_dict[param_name]
        return unfix_param_dict

    # Returns information about the errors
    def get_error_info_list(self) -> list:
        error_info_list = []
        for objective in self.objective_list:
            error_list = objective.get_error_list()
            for error in error_list:
                error_info_list.append(error.get_summary())
        return list(set(error_info_list))

    # Gets the predicted curve
    #   Returns none if the data is invalid
    def get_prd_data(self, objective:Objective, *params):
        
        # Fix parameters and calibrate the model
        params = self.incorporate_fix_param_dict(*params)
        self.model.set_exp_data(objective.get_exp_data())
        calibrated_model = self.model.get_model(*params)
        
        # Get the driver and get the curve
        model_driver = Driver(objective.get_exp_data(), calibrated_model)
        prd_data = model_driver.run()

        # Only return if data contains sufficient points
        if prd_data == None:
            return
        for data_key in prd_data.keys():
            if len(prd_data[data_key]) < MIN_DATA:
                return None
        return prd_data
    
    # Calculates the error values for a set of parameters
    def calculate_error_value_dict(self, *params) -> dict:
        
        # Create a dictionary of errors
        error_info_list = self.get_error_info_list()
        empty_list_list = [[] for _ in range(len(error_info_list))]
        error_list_dict = {key: value for key, value in zip(error_info_list, empty_list_list)}
        
        # Iterate through experimental data
        for objective in self.objective_list:
            
            # Ignore validation data
            error_list = objective.get_error_list()
            if len(error_list) == 0:
                continue
            
            # Get prediction for training data
            prd_data = self.get_prd_data(objective, *params)
            if prd_data == None:
                return {key: value for key, value in zip(error_info_list, [BIG_VALUE] * len(error_info_list))}
        
            # Gets all the errors and add to dictionary
            for error in error_list:
                error_value = error.get_value(prd_data) * error.get_weight()
                error_key = error.get_summary()
                error_list_dict[error_key].append(error_value)
        
        # Sum the errors and return
        error_value_dict = {}
        for error_info in error_info_list:
            error_value_dict[error_info] = sum(error_list_dict[error_info])
        return error_value_dict

    # Plots the curves for a given type
    def plot_curves(self, type:str, file_path:str="", x_label:str=None, y_label:str=None, derivative:int=0):
        
        # Gets the data of defined type
        exp_data_list = [objective.get_exp_data() for objective in self.objective_list if objective.get_type() == type]
        
        # Initialise plotter
        x_label = DATA_FIELD_PLOT_MAP[type]["x"] if x_label == None else x_label
        y_label = DATA_FIELD_PLOT_MAP[type]["y"] if y_label == None else y_label
        plotter = Plotter(file_path, x_label, y_label)
        
        # Converts the list into a derivative if desired
        for _ in range(derivative):
            exp_data_list = deepcopy(exp_data_list)
            exp_data_list = [differentiate_curve(exp_data, x_label, y_label) for exp_data in exp_data_list]
        
        # Plot the data, save, and clear for next plot
        for exp_data in exp_data_list:
            plotter.scat_plot(exp_data)
        plotter.save_plot()
        plotter.clear()
