"""
 Title:         The Curve class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
from copy import deepcopy
from moga_neml.models.__model__ import __Model__, get_model
from moga_neml.errors.__error__ import __Error__
from moga_neml.interface.plotter import Plotter
from moga_neml.optimise.driver import Driver
from moga_neml.optimise.curve import Curve
from moga_neml.maths.derivative import differentiate_curve
from moga_neml.maths.experiment import DATA_FIELD_PLOT_MAP
from moga_neml.maths.general import reduce_list

# Constants
MIN_DATA  = 5
BIG_VALUE = 10000

# The Controller class
class Controller():

    def __init__(self):
        """
        Class to control all the components of the optimisation
        """
        
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
        
        # Other initialisation
        self.set_driver()
        
    def define_model(self, model_name:str, **kwargs) -> None:
        """
        Defines the model

        Parameters:
        * `model_name`: The name of the model
        """
        self.model = get_model(model_name, **kwargs)
        
    def add_curve(self, type:str, exp_data:dict) -> None:
        """
        Adds an experimental curve to the controller
        
        Parameters:
        * `type`:     The type of the curve
        * `exp_data`: The corresponding experimental data
        """
        curve = Curve(type, exp_data, self.model)
        self.curve_list.append(curve)
    
    def get_curve_list(self) -> list:
        """
        Gets the list of curves
        """
        return self.curve_list
    
    def get_last_curve(self) -> Curve:
        """
        Returns the most recently added curve
        """
        if self.curve_list == []:
            raise ValueError("No curves have been added yet!")
        return self.curve_list[-1]

    def fix_param(self, param_name:str, param_value:float) -> None:
        """
        Fixes a parameter to a value

        Parameters:
        * `param_name`:  The name of the parameter
        * `param_value`: The value to fix the parameter to 
        """
        param_dict = self.model.get_param_dict()
        pretext = f"The '{param_name}' parameter cannot be fixed because"
        if not param_name in param_dict.keys():
            raise ValueError(f"{pretext} it is not defined in {self.model.get_name()}!")
        if param_name in self.init_param_dict.keys():
            raise ValueError(f"{pretext} it has already been set!")
        self.fix_param_dict[param_name] = param_value

    def init_param(self, param_name:str, param_value:float, param_std:float) -> None:
        """
        Sets the initial value of a parameter

        Parameters:
        * `param_name`:  The name of the parameter
        * `param_value`: The value to initialise the parameter to
        * `param_std`:   The initial standard deviation of the parameter
        """
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

    def get_model(self) -> __Model__:
        """
        Returns the model
        """
        if self.model == None:
            raise ValueError("The model cannot be retrieved because it has not been defined yet!")
        return self.model

    def get_fix_param_dict(self) -> dict:
        """
        Gets information about the fixed parameters
        """
        return self.fix_param_dict

    def get_init_param_dict(self) -> dict:
        """
        Gets information about the initialised parameters
        """
        return self.init_param_dict

    def incorporate_fix_param_dict(self, *params) -> list:
        """
        Incorporates the fixed parameters

        Parameters:
        * `params`: The parameters
        """
        param_names = list(self.model.get_param_dict().keys())
        fix_indexes = [i for i in range(len(param_names)) if param_names[i] in self.fix_param_dict.keys()]
        params = list(params)
        for fix_index in fix_indexes:
            fix_value = self.fix_param_dict[param_names[fix_index]]
            params.insert(fix_index, fix_value)
        return tuple(params)

    def get_unfix_param_dict(self) -> dict:
        """
        Returns the information of unfixed parameters
        """
        unfix_param_dict = {}
        param_dict = self.model.get_param_dict()
        for param_name in param_dict.keys():
            if not param_name in self.fix_param_dict.keys():
                unfix_param_dict[param_name] = param_dict[param_name]
        return unfix_param_dict

    def set_error_reduction_method(self, method:str):
        """
        Changes the reduction method for errors

        Parameters:
        * `method`: The reduction method for the errors to change to
        """
        self.error_reduction_method = method

    def get_error_reduction_method(self) -> str:
        """
        Gets the reduction method for errors
        """
        return self.error_reduction_method
      
    def set_objective_reduction_method(self, method:str):
        """
        Changes the reduction method for objective functions

        Parameters:
        * `method`: The reduction method for the objective functions to change to
        """
        self.objective_reduction_method = method

    def get_objective_reduction_method(self) -> str:
        """
        Gets the reduction method for objective functions
        """
        return self.objective_reduction_method

    def set_error_grouping(self, group_name:bool=True, group_type:bool=True, group_labels:bool=True) -> None:
        """
        Changes the variables for grouping the errors together

        Parameters:
        * `group_name`:   Whether to group the errors by name
        * `group_type:    Whether to group the errors by curve type
        * `group_labels`: Whether to group the errors by the curve labels
        """
        self.group_name = group_name
        self.group_type = group_type
        self.group_labels = group_labels

    def set_driver(self, num_steps:int=1000, rel_tol:float=1e-6, abs_tol:float=1e-10, verbose:bool=False) -> None:
        """
        Sets some general options for the NEML driver
        
        Parameters:
        * `num_steps`: Number of steps to run
        * `rel_tol`:   Relative error tolerance
        * `abs_tol`:   Absolute error tolerance
        * `verbose`:   Whether to print updates during the driving
        """
        self.num_steps = num_steps
        self.rel_tol   = rel_tol
        self.abs_tol   = abs_tol
        self.verbose   = verbose

    def get_error_grouping(self) -> str:
        """
        Gets the error grouping approach as a string
        """
        group_str_list = [
            "name" if self.group_name else "",
            "type" if self.group_type else "",
            "labels" if self.group_labels else ""
        ]
        group_str_list = [group_str for group_str in group_str_list if group_str != ""]
        return ', '.join(group_str_list)

    def get_objective_info_list(self) -> list:
        """
        Returns information about the errors
        """
        objective_info_list = []
        for curve in self.curve_list:
            error_list = curve.get_error_list()
            for error in error_list:
                error_group_key = error.get_group_key(self.group_name, self.group_type, self.group_labels)
                objective_info_list.append(error_group_key)
        return list(set(objective_info_list))

    def get_prd_data(self, curve:Curve, *params) -> dict:
        """
        Gets the predicted curve; returns none if the data is invalid

        Parameters:
        * `curve`:  The curve to predict
        * `params`: The parameters for the prediction

        Returns the predicted data
        """
        
        # Fix parameters and calibrate the model
        params = self.incorporate_fix_param_dict(*params)
        self.model.set_exp_data(curve.get_exp_data())
        calibrated_model = self.model.get_calibrated_model(*params)
        if calibrated_model == None:
            return None
        
        # Get the driver and prediction
        model_driver = Driver(curve.get_exp_data(), calibrated_model, self.num_steps,
                              self.rel_tol, self.abs_tol, self.verbose)
        prd_data = model_driver.run()
        
        # Check data has some data points
        if prd_data == None:
            return
        for field in prd_data.keys():
            if len(prd_data[field]) < MIN_DATA:
                return
        
        # Add the latest prediction to the curve and return the data
        curve.set_prd_data(prd_data)
        return prd_data
    
    def reduce_errors(self, error_list_dict:dict) -> dict:
        """
        Defines how the errors are reduced

        Parameters:
        * `error_list_dict`: A dictionary of error values

        Returns the reduced error values
        """
        objective_info_list = self.get_objective_info_list()
        error_value_dict = {}
        for error_info in objective_info_list:
            try:
                error_value_dict[error_info] = reduce_list(error_list_dict[error_info], self.error_reduction_method)
            except OverflowError:
                error_value_dict[error_info] = BIG_VALUE
        return error_value_dict
    
    def reduce_objectives(self, objective_list:list) -> float:
        """
        Defines how the objectives are reduced

        Parameters:
        * `objective_list`: The list of objective functions
        
        Returns the reduced objective value
        """
        try:
            return reduce_list(objective_list, self.objective_reduction_method)
        except OverflowError:
            return BIG_VALUE
    
    def calculate_objectives(self, *params) -> dict:
        """
        Calculates the error values for a set of parameters

        Parameters:
        * `params`: The parameters for the prediction

        Returns a dictionary of the objectives
        """

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

    def plot_exp_curves(self, type:str, file_path:str="", x_label:str=None, y_label:str=None,
                        derivative:int=0, x_log:bool=False, y_log:bool=False) -> None:
        """
        Plots the experimental curves for a given type

        Parameters:
        * `type:`       The type of the experimental data
        * `file_path`:  The path to plot the experimental curves
        * `x_label`:    The x label for the plot
        * `y_label`:    The y label for the plot
        * `derivative`: How many derivatives to take the curves to
        * `x_log`:      Whether to log the x axis
        * `y_log`:      Whether to log the y axis
        """

        # Gets the data of defined type
        exp_data_list = [curve.get_exp_data() for curve in self.curve_list if curve.get_type() == type]
        
        # Initialise plotter
        x_label = DATA_FIELD_PLOT_MAP[type]["x"] if x_label == None else x_label
        y_label = DATA_FIELD_PLOT_MAP[type]["y"] if y_label == None else y_label
        plotter = Plotter(file_path, x_label, y_label)
        plotter.prep_plot("Experimental")
        
        # Converts the list into a derivative if desired
        for _ in range(derivative):
            exp_data_list = deepcopy(exp_data_list)
            exp_data_list = [differentiate_curve(exp_data, x_label, y_label) for exp_data in exp_data_list]
        
        # Plot the data, save, and clear for next plot
        for exp_data in exp_data_list:
            plotter.scat_plot(exp_data)
        plotter.log_scale(x_log, y_log)
        plotter.save_plot()
        plotter.clear()

    def plot_prd_curves(self, *params:tuple, type:str, file_path:str="", x_label:str=None,
                        y_label:str=None, x_log:bool=False, y_log:bool=False) -> None:
        """
        Plots the predicted curves for a given type

        Parameters:
        * `params`:     The parameters to perform the prediction
        * `type:`       The type of the experimental data
        * `file_path`:  The path to plot the experimental curves
        * `x_label`:    The x label for the plot
        * `y_label`:    The y label for the plot
        * `x_log`:      Whether to log the x axis
        * `y_log`:      Whether to log the y axis
        """
        
        # Initialise plotter
        x_label = DATA_FIELD_PLOT_MAP[type]["x"] if x_label == None else x_label
        y_label = DATA_FIELD_PLOT_MAP[type]["y"] if y_label == None else y_label
        plotter = Plotter(file_path, x_label, y_label)
        plotter.prep_plot("Predicted")
        
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
        
        # Format and save
        plotter.log_scale(x_log, y_log)
        plotter.save_plot()
        plotter.clear()
