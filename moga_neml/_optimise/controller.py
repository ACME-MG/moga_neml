"""
 Title:         The Curve class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
from copy import deepcopy
from moga_neml.models.__model__ import __Model__, get_model
from moga_neml.errors.__error__ import __Error__
from moga_neml._interface.plotter import Plotter
from moga_neml._optimise.driver import Driver
from moga_neml._optimise.curve import Curve
from moga_neml._maths.derivative import differentiate_curve
from moga_neml._maths.experiment import DATA_FIELD_PLOT_MAP
from moga_neml._maths.general import reduce_list

# Constants
MIN_DATA  = 5
BIG_VALUE = 10000

# The Controller class
class Controller():

    # Constructor
    def __init__(self):
        
        # Initialise internal variables
        self.model = None
        self.curve_list = []
        self.fix_param_dict = {}
        self.init_param_dict = {}
        
        # Initialise variables for grouping errors
        self.group_name = True
        self.group_type = True
        self.group_labels = True
        
        # Initialise variables for reducing errors
        self.error_reduction_method = "average"
        self.objective_reduction_method = "average"
        
    # Defines the model
    def define_model(self, model_name:str, model_args:tuple) -> None:
        self.model = get_model(model_name, model_args)
        
    # Adds experimental data
    def add_curve(self, type:str, exp_data:dict) -> None:
        curve = Curve(type, exp_data, self.model)
        self.curve_list.append(curve)
    
    # Gets the list of curves
    def get_curve_list(self) -> list:
        return self.curve_list
    
    # Returns the most recently added curve
    def get_last_curve(self) -> Curve:
        if self.curve_list == []:
            raise ValueError("No curves have been added yet!")
        return self.curve_list[-1]
    
    # Fixes a parameter to a value
    def fix_param(self, param_name:str, param_value:float) -> None:
        param_dict = self.model.get_param_dict()
        pretext = f"The '{param_name}' parameter cannot be fixed because"
        if not param_name in param_dict.keys():
            raise ValueError(f"{pretext} it is not defined in {self.model.get_name()}!")
        if param_name in self.init_param_dict.keys():
            raise ValueError(f"{pretext} it has already been set!")
        self.fix_param_dict[param_name] = param_value

    # Sets the initial value of a parameter
    def init_param(self, param_name:str, param_value:float, param_std:float) -> None:
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
        self.init_param_dict[param_name] = {"value": param_value, "std": param_std}

    # Returns the model
    def get_model(self) -> __Model__:
        if self.model == None:
            raise ValueError("The model cannot be retrieved because it has not been defined yet!")
        return self.model

    # Gets information about the fixed parameters
    def get_fix_param_dict(self) -> dict:
        return self.fix_param_dict

    # Gets information about the initialised parameters
    def get_init_param_dict(self) -> dict:
        return self.init_param_dict

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

    # Changes the reduction method for errors
    def set_error_reduction_method(self, method:str):
        self.error_reduction_method = method

    # Gets the reduction method for errors
    def get_error_reduction_method(self) -> str:
        return self.error_reduction_method
        
    # Changes the reduction method for objective functions
    def set_objective_reduction_mtehod(self, method:str):
        self.objective_reduction_method = method

    # Gets the reduction method for objective functions
    def get_objective_reduction_method(self) -> str:
        return self.objective_reduction_method

    # Changes the variables for grouping the errors together
    def set_error_grouping(self, group_name:bool=True, group_type:bool=True, group_labels:bool=True):
        self.group_name = group_name
        self.group_type = group_type
        self.group_labels = group_labels

    # Gets the error grouping approach as a string
    def get_error_grouping(self) -> str:
        group_str_list = [
            "name" if self.group_name else "",
            "type" if self.group_type else "",
            "labels" if self.group_labels else ""
        ]
        group_str_list = [group_str for group_str in group_str_list if group_str != ""]
        return ', '.join(group_str_list)

    # Returns information about the errors
    def get_objective_info_list(self) -> list:
        objective_info_list = []
        for curve in self.curve_list:
            error_list = curve.get_error_list()
            for error in error_list:
                error_group_key = error.get_group_key(self.group_name, self.group_type, self.group_labels)
                objective_info_list.append(error_group_key)
        return list(set(objective_info_list))

    # Gets the predicted curve
    #   Returns none if the data is invalid
    def get_prd_data(self, curve:Curve, *params):
        
        # Fix parameters and calibrate the model
        params = self.incorporate_fix_param_dict(*params)
        self.model.set_exp_data(curve.get_exp_data())
        calibrated_model = self.model.get_calibrated_model(*params)
        if calibrated_model == None:
            return None
        
        # Get the driver and prediction
        model_driver = Driver(curve.get_exp_data(), calibrated_model)
        prd_data = model_driver.run()
        
        # Check data has some data points
        if prd_data == None:
            return
        for field in prd_data.keys():
            if len(prd_data[field]) < MIN_DATA:
                return
        return prd_data
    
    # Defines how the errors are reduced
    def reduce_errors(self, error_list_dict:dict) -> dict:
        objective_info_list = self.get_objective_info_list()
        error_value_dict = {}
        for error_info in objective_info_list:
            error_value = reduce_list(error_list_dict[error_info], self.error_reduction_method)
            error_value_dict[error_info] = error_value
        return error_value_dict
    
    # Defines how the objectives are reduced
    def reduce_objectives(self, objective_list:list) -> float:
        objective_value = reduce_list(objective_list, self.objective_reduction_method)
        return objective_value
    
    # Calculates the error values for a set of parameters
    def calculate_objectives(self, *params) -> dict:
        
        # Create a dictionary of errors
        objective_info_list = self.get_objective_info_list()
        empty_list_list = [[] for _ in range(len(objective_info_list))]
        error_list_dict = {key: value for key, value in zip(objective_info_list, empty_list_list)}
        
        # Iterate through experimental data
        for curve in self.curve_list:
            
            # Ignore validation data
            error_list = curve.get_error_list()
            if len(error_list) == 0:
                continue
            
            # Get prediction for training data
            prd_data = self.get_prd_data(curve, *params)
            if prd_data == None:
                return {key: value for key, value in zip(objective_info_list, [BIG_VALUE] * len(objective_info_list))}
        
            # Gets all the errors and add to dictionary
            for error in error_list:
                error_value = error.get_value(prd_data)
                error_value = error_value * error.get_weight() if error_value != None else BIG_VALUE
                error_group_key = error.get_group_key(self.group_name, self.group_type, self.group_labels)
                error_list_dict[error_group_key].append(error_value)
        
        # Reduce and return errors
        objective_dict = self.reduce_errors(error_list_dict)
        return objective_dict

    # Plots the curves for a given type
    def plot_exp_curves(self, type:str, file_path:str="", x_label:str=None, y_label:str=None, derivative:int=0):
        
        # Gets the data of defined type
        exp_data_list = [curve.get_exp_data() for curve in self.curve_list if curve.get_type() == type]
        
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

    # Plots the curves for a given type
    def plot_prd_curves(self, *params:tuple, type:str, file_path:str="", x_label:str=None, y_label:str=None):
        
        # Initialise plotter
        x_label = DATA_FIELD_PLOT_MAP[type]["x"] if x_label == None else x_label
        y_label = DATA_FIELD_PLOT_MAP[type]["y"] if y_label == None else y_label
        plotter = Plotter(file_path, x_label, y_label)
        
        # Plot experimental and predicted data
        for curve in self.curve_list:
            if curve.get_type() != type:
                continue
            exp_data = curve.get_exp_data()
            prd_data = self.get_prd_data(curve, *params)
            if prd_data == None:
                raise ValueError("The model is unable to run with the parameters!")
            plotter.scat_plot(exp_data)
            plotter.line_plot(prd_data)
        plotter.save_plot()
        plotter.clear()
    