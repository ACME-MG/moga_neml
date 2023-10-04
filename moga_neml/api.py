"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import re, time
from moga_neml.interface.reader import read_exp_data, check_exp_data
from moga_neml.maths.data import remove_data_after
from moga_neml.maths.general import safe_mkdir
from moga_neml.optimise.recorder import Recorder
from moga_neml.optimise.controller import Controller
from moga_neml.optimise.problem import Problem
from moga_neml.optimise.moga import MOGA
from moga_neml.maths.derivative import remove_after_sp
from moga_neml.maths.experiment import DATA_UNITS

# API Class
class API:

    def __init__(self, title:str="", input_path:str="./data", output_path:str="./results", verbose:bool=True, output_here:bool=False):
        """
        Class to interact with the optimisation code
        
        Parameters:
        * `title`:       Title of the output folder
        * `input_path`:  Path to the input folder
        * `output_path`: Path to the output folder
        * `verbose`:     If true, outputs messages for each function call
        * `output_here`: If true, just dumps the output in ths executing directory
        """
        
        # Initialise internal variables
        self.__controller__  = Controller()
        self.__recorder__    = None
        self.__print_index__ = 0
        self.__print_subindex__ = 0
        self.__verbose__     = verbose
        
        # Print starting message
        time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        self.__print__(f"\n  Starting on {time_str}\n", add_index=False)
        
        # Get start time
        self.__start_time__ = time.time()
        time_stamp = time.strftime("%y%m%d%H%M%S", time.localtime(self.__start_time__))
        
        # Define input and output
        self.__input_path__ = input_path
        self.__get_input__  = lambda x : f"{self.__input_path__}/{x}"
        title = "" if title == "" else f"_{title}"
        title = re.sub(r"[^a-zA-Z0-9_]", "", title.replace(" ", "_"))
        self.__output_dir__ = "." if output_here else time_stamp
        self.__output_path__ = "." if output_here else f"{output_path}/{self.__output_dir__}{title}"
        self.__get_output__ = lambda x : f"{self.__output_path__}/{x}"
        
        # Create directories
        if not output_here:
            safe_mkdir(output_path)
            safe_mkdir(self.__output_path__)
    
    def __print__(self, message:str, add_index:bool=True, sub_index:bool=False) -> None:
        """
        Displays a message before running the command (for internal use only)
        
        Parameters:
        * `message`:   the message to be displayed
        * `add_index`: if true, adds a number at the start of the message
        * `sub_index`: if true, adds a number as a decimal
        """
        
        # Special printing cases
        if not self.__verbose__:
            return
        if not add_index:
            print(message)
            return
        
        # Prints with an index / subindex
        if sub_index:
            self.__print_subindex__ += 1
            print_index = f"     {self.__print_index__}.{self.__print_subindex__}"
        else:
            self.__print_index__ += 1
            self.__print_subindex__ = 0
            print_index = f"{self.__print_index__}"
        print(f"   {print_index})\t{message} ...")
    
    def define_model(self, model_name:str, **kwargs) -> None:
        """
        Defines the model to be optimised
        
        Parameters:
        * `model_name`: The name of the model
        * `kwargs`:     Any additional keyword arguments to pass to the model
        """
        self.__print__(f"Defining model '{model_name}'")
        self.__controller__.define_model(model_name, **kwargs)
    
    def read_data(self, file_name:str) -> None:
        """
        Reads in the experimental data from a file
        
        Parameters:
        * `file_name`: The name of the file relative to the defined `input_path`
        """
        self.__print__(f"Reading data from '{file_name}'")
        exp_data = read_exp_data(self.__input_path__, file_name)
        self.__controller__.add_curve(exp_data["type"], exp_data)
    
    def add_custom_data(self, type:str, exp_data:dict) -> None:
        """
        Adds custom data; useful for defining specific test conditions
        
        Parameters:
        * `type`:      The data type (e.g., creep, tensile)
        * `exp_data`:  Information about the data
        """
        self.__print__(f"Adding custom {type} data!")
        exp_data["file_name"] = "custom"
        exp_data["type"] = type
        check_exp_data(exp_data)
        self.__controller__.add_curve(type, exp_data)
    
    def add_error(self, error_name:str, x_label:str="", y_label:str="", weight:float=1, **kwargs) -> None:
        """
        Adds an error to optimise for the most recenrtly added experimental data
        
        Parameters:
        * `error_name`: The name of the error
        * `x_label`:    The measurement on the x-axis (e.g., time, strain)
        * `y_label`:    The measurement on the y-axis (e.g., strain, stress)
        * `weight`:     The factor multipled with the error when the errors are reduced
        * `kwargs`:     Any additional keyword arguments to pass to the model
        """
        labels = f"{x_label}-{y_label}" if x_label != "" and y_label != "" else f"{x_label}" if x_label != "" else ""
        label_str = f"for {labels} " if labels != "" else ""
        weight_str = f"with a weight of {weight}" if weight != 1 else ""
        self.__print__(f"Adding '{error_name}' error {label_str}{weight_str}", sub_index=True)
        curve = self.__controller__.get_last_curve()
        curve.add_error(error_name, x_label, y_label, weight, **kwargs)

    def fix_param(self, param_name:str, param_value:float) -> None:
        """
        Fixes a parameter to a value and stops it from changing during the optimisation
        
        Parameters:
        * `param_name`:  The name of the parameter
        * `param_value`: The value the parameter will be fixed to
        """
        self.__print__("Fixing the '{}' parameter to fixed value of {:0.4}".format(param_name, float(param_value)))
        self.__controller__.fix_param(param_name, param_value)

    def init_param(self, param_name:str, param_value:float, param_std:float=0) -> None:
        """
        Gives a parameter an initial value in the initial population of the optimisation
        
        Parameters:
        * `param_name`:  The name of the parameter
        * `param_value`: The value the parameter is initialised to
        * `param_std`:   The deviation of the parameter in the initial population
        """
        message = "Setting the '{}' parameter to an initial value of {:0.4} and deviation of {:0.4}"
        self.__print__(message.format(param_name, float(param_value), float(param_std)))
        self.__controller__.init_param(param_name, param_value, param_std)

    def add_constraint(self, constraint_name:str) -> None:
        """
        Adds a constraint to all the curves that prevent a solution from being accepted

        Parameters:
        * `constraint_name`: The name of the constraint
        """
        self.__print__(f"Adding the {constraint_name} constraint to the optimisation")

    def remove_damage(self, window:int=0.1, acceptance:float=0.9) -> None:
        """
        Removes the tertiary creep from the most recently added creep curve, by removing the data
        points after the minimum creep rate
        
        Parameters:
        * `window`:     The window ratio to identify the stationary points of the derivative; the actual
                        window size is the product of `window` and the number of data points (1000)
        * `acceptance`: The acceptance value for identifying the nature of stationary points; should
                        have a value between 0.5 and 1.0
        """
        self.__print__(f"Removing the tertiary creep", sub_index=True)
        curve = self.__controller__.get_last_curve()
        if curve.get_type() != "creep":
            raise ValueError("Cannot remove damage because it can only be removed for creep curves!")
        exp_data = curve.get_exp_data()
        exp_data = remove_after_sp(exp_data, "min", "time", "strain", window, acceptance, 0)
        curve.set_exp_data(exp_data)

    def remove_oxidation(self, window:int=0.1, acceptance:float=0.9) -> None:
        """
        Removes the data after the tertiary creep for the most recently added
        
        Parameters:
        * `window`:     The window ratio to identify the stationary points of the derivative; the actual
                        window size is the product of `window` and the number of data points (1000)
        * `acceptance`: The acceptance value for identifying the nature of stationary points; should
                        have a value between 0.5 and 1.0
        """
        self.__print__(f"Removing the oxidised creep", sub_index=True)
        curve = self.__controller__.get_last_curve()
        if curve.get_type() != "creep":
            raise ValueError("Cannot remove oxidised creep because it can only be removed for creep curves!")
        exp_data = curve.get_exp_data()
        exp_data = remove_after_sp(exp_data, "max", "time", "strain", window, acceptance, 0)
        curve.set_exp_data(exp_data)
    
    def remove_manual(self, label:str, value:float) -> None:
        """
        Removes the data for a curve at a specific value
        
        Parameters:
        * `label`: The measurement corresponding to the value (e.g., strain, stress)
        * `value`: The value to start removing data
        """
        curve = self.__controller__.get_last_curve()
        units = DATA_UNITS[label]
        self.__print__(f"Removing the values after {label} of {value} ({units})", sub_index=True)
        exp_data = curve.get_exp_data()
        exp_data = remove_data_after(exp_data, value, label)
        curve.set_exp_data(exp_data)
    
    def plot_experimental(self, type:str=None, x_label:str=None, y_label:str=None,
                          derivative:int=0, x_log:bool=False, y_log:bool=False) -> None:
        """
        Visualises the experimental data
        
        Parameters:
        * `type`:       The type of data to be visualised (e.g., creep, tensile); if none is specified,
                        then the type of the most recently added curve is visualised
        * `x_label`:    The measurement to be visualised on the x-axis
        * `y_label`:    The measurement to be visualised on the y-axis
        * `derivative`: The derivative order of the data; the default is 0, meaning that the
                        visualised data is not differentiated
        * `x_log`:      Whether to log the x-axis
        * `y_log`:      Whether to log the y-axis
        """
        
        # Determine type (use type of last curve if undefined)
        type = self.__controller__.get_last_curve().get_type() if type == None else type
        
        # Determine file name
        file_name = f"exp_{type}_d{derivative}.png" if derivative > 0 else f"exp_{type}.png"
        
        # Display informative message
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        derivative_str = f" {ordinal(derivative)} derivative of the" if derivative > 0 else ""
        self.__print__(f"Visualising the{derivative_str} {type} data at '{file_name}'")
        
        # Actually plot the curves
        self.__controller__.plot_exp_curves(type, self.__get_output__(file_name), x_label,
                                            y_label, derivative, x_log, y_log)

    def plot_predicted(self, *params:tuple, type:str=None, x_label:str=None,
                       y_label:str=None, x_log:bool=False, y_log:bool=False) -> None:
        """
        Visualises the predicted curves from a set of parameters
        
        Parameters:
        * `params`:    The parameter values of the model; note that defining the parameters as
                       arguments to this function is similar to fixing the parameters via `fix_params`,
                       meaning that there will be clashes if the parameter values are defined twice.
        * `type_list`: The types of data (e.g., creep, tensile) to be visualised; if none are
                       specified, then all the possible data types will be plotted
        * `x_label`:   The measurement to be visualised on the x-axis
        * `y_label`:   The measurement to be visualised on the y-axis
        * `x_log`:     Whether to log the x-axis
        * `y_log`:     Whether to log the y-axis
        """
        
        # Convert parameters into a string and display
        param_str = ["{:0.4}".format(float(param)) for param in params]
        self.__print__("Plotting the curves for {}".format(str(param_str).replace("'", "")))

        # Get parameters and check input
        param_name_list = list(self.__controller__.get_unfix_param_dict().keys())
        if len(params) != len(param_name_list):
            raise ValueError(f"Could not plot because the number of inputs ({len(params)}) do not match the number of parameters ({len(param_name_list)})!")
        
        # Get type and plot prediction
        type = self.__controller__.get_last_curve().get_type() if type == None else type
        file_path = self.__get_output__(f"prd_{type}.png")
        self.__controller__.plot_prd_curves(*params, type=type, file_path=file_path, x_label=x_label,
                                            y_label=y_label, x_log=x_log, y_log=y_log)

    def get_results(self, *params:tuple, type_list:list=None, x_label:str=None, y_label:str=None) -> None:
        """
        Gets the optimisation, parameter, and error summary from a set of parameters
        
        Parameters:
        * `params`:    The parameter values of the model; note that defining the parameters as
                       arguments to this function is similar to fixing the parameters via `fix_params`,
                       meaning that there will be clashes if the parameter values are defined twice.
        * `type_list`: The types of data (e.g., creep, tensile) to be visualised; if none are
                       specified, then all the possible data types will be plotted
        * `x_label`:   The measurement to be visualised on the x-axis
        * `y_label`:   The measurement to be visualised on the y-axis
        """
        
        # Convert parameters into a string and display
        param_str = ["{:0.4}".format(float(param)) for param in params]
        self.__print__("Getting the results for {}".format(str(param_str).replace("'", "")))

        # Get parameters and check input
        param_name_list = list(self.__controller__.get_unfix_param_dict().keys())
        param_value_dict = {key: value for key, value in zip(param_name_list, params)}
        if len(params) != len(param_name_list):
            raise ValueError("Could not plot because the number of inputs do not match the number of parameters!")
        
        # Initialise recorder
        recorder = Recorder(self.__controller__, 0, 1, "")
        recorder.define_hyperparameters("n/a","n/a","n/a","n/a","n/a")
        
        # Add parameters and create record
        error_value_dict = self.__controller__.calculate_objectives(*params)
        recorder.update_optimal_solution(param_value_dict, error_value_dict)
        recorder.create_record(self.__get_output__("results.xlsx"), type_list, x_label, y_label)
    
    def set_driver(self, num_steps:int=1000, rel_tol:float=1e-6, abs_tol:float=1e-10, verbose:bool=False) -> None:
        """
        Sets some general options for the NEML driver
        
        Parameters:
        * `num_steps`: Number of steps to run
        * `rel_tol`:   Relative error tolerance
        * `abs_tol`:   Absolute error tolerance
        * `verbose`:   Whether to print updates during the driving
        """
        self.__print__(f"Initialising the driver")
        self.__controller__.set_driver(num_steps, rel_tol, abs_tol, verbose)
    
    def set_recorder(self, interval:int=10, population:int=10, quick_view:bool=False) -> None:
        """
        Sets the options for the results recorder
        
        Parameters:
        * `interval`:   The number of generations for which the most updated results will
                        be generated
        * `population`: The number of solutions to be stored and shown in the results
        """
        self.__print__(f"Initialising the recorder with an interval of {interval} and population of {population}")
        self.__recorder__ = Recorder(self.__controller__, interval, population, self.__get_output__("opt"), quick_view)

    def group_errors(self, name:bool=True, type:bool=True, labels:bool=True):
        """
        Sets the options for the grouping of errors into objective functions; if all the parameters
        are set to false, then the errors will be grouped into a single objective function
        
        Parameters:
        * `name`:   If true, the errors will be grouped by their names (e.g., end_value, area)
        * `type`:   If true, the errors will be grouped by the data types (e.g., creep, tensile)
        * `labels`: If true, the errors will be grouped by their measurements (e.g., strain, stress)
        """
        self.__controller__.set_error_grouping(name, type, labels)
        group_str = self.__controller__.get_error_grouping()
        group_str_out = f"based on {group_str}" if group_str != "" else "individually"
        self.__print__(f"Grouping the errors {group_str_out}") # prints after action
    
    def reduce_errors(self, method:str="average"):
        """
        Sets the reduction method to convert a list of error values into a single
        value for each objective function; the reduced values are then optimised
        by the multi-objective genetic algorithm
        
        Parameters:
        * `method`: The reduction method ("sum", "average", "square_sum", "square_average")
        """
        self.__print__(f"Reducing the errors based on {method}")
        self.__controller__.set_error_reduction_method(method)
    
    def reduce_objectives(self, method:str="average"):
        """
        Sets the reduction method to convert a list of objective function values into a
        single value; this single value is for determining the optimal solution in the
        collection of solutions during the optimisation process
        
        Parameters:
        * `method`: The reduction method ("sum", "average", "square_sum", "square_average")
        """
        self.__print__(f"Reducing the objective functions based on {method}")
        self.__controller__.set_objective_reduction_method(method)
    
    def optimise(self, num_gens:int=10000, init_pop:int=100, offspring:int=50, crossover:float=0.65, mutation:float=0.35) -> None:
        """
        Prepares and conducts the optimisation
        
        Parameters:
        * `num_gens`:  The number of generations to optimise
        * `init_pop`:  The number of solutions in the initial population
        * `offspring`: The number of solutions introduced after each generation
        * `crossover`: The crossover probability; should be between 0.0 and 1.0
        * `mutation`:  The mutation probability; should be between 0.0 and 1.0
        """
        self.__print__(f"Conducting the optimisation ({num_gens}, {init_pop}, {offspring}, {crossover}, {mutation})")
        self.__recorder__.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.__controller__, self.__recorder__)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()
        
    def __del__(self):
        """
        Prints out the final message (for internal use only)
        """
        time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        duration = round(time.time() - self.__start_time__)
        self.__print__(f"\n  Finished on {time_str} in {duration}s\n", add_index=False)
