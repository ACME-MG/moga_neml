"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import re, time
from moga_neml._interface.reader import read_exp_data
from moga_neml._maths.curve import remove_data_after
from moga_neml._maths.general import safe_mkdir
from moga_neml._optimise.recorder import Recorder
from moga_neml._optimise.controller import Controller
from moga_neml._optimise.problem import Problem
from moga_neml._optimise.moga import MOGA
from moga_neml._maths.derivative import remove_after_sp
from moga_neml._maths.experiment import DATA_UNITS

# API Class
class API:

    # Constructor
    def __init__(self, title:str="", input_path="./data", output_path="./results"):
        
        # Print starting message
        time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        print(f"\n  Starting on {time_str}\n")
                
        # Prepare progressor
        title = "" if title == "" else f"_{title}"
        title = re.sub(r"[^a-zA-Z0-9_]", "", title.replace(" ", "_"))
        
        # Define input
        self.input_path  = input_path
        self.get_input   = lambda x : f"{self.input_path}/{x}"
        
        # Define output
        self.start_time  = time.time()
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(self.start_time))
        self.output_path = f"{output_path}/{self.output_dir}{title}"
        self.get_output  = lambda x : f"{self.output_path}/{x}"
        
        # Create directories
        safe_mkdir(output_path)
        safe_mkdir(self.output_path)
        
        # Initialise internal variables
        self.__controller__  = Controller()
        self.__recorder__    = None
        self.__print_count__ = 1
    
    # Displays a message before running the command
    def __print__(self, message:str) -> None:
        print(f"   {self.__print_count__})\t{message}")
        self.__print_count__ += 1
    
    # Defines the model
    def def_model(self, model_name:str, *args) -> None:
        self.__print__(f"Defining model '{model_name}'")
        self.__controller__.define_model(model_name, args)
    
    # Reads in the experimental data from a file
    def read_file(self, file_name:str) -> None:
        self.__print__(f"Reading data from '{file_name}'")
        exp_data = read_exp_data(self.input_path, file_name)
        self.__controller__.add_objective(exp_data["type"], exp_data)
    
    # Adds an error
    def add_error(self, error_name:str, x_label:str, y_label:str="", weight:float=1) -> None:
        labels = f"{x_label}-{y_label}" if y_label != "" else x_label
        self.__print__(f"Adding error '{error_name}' for {labels} with a weight of {weight}")
        objective = self.__controller__.get_last_objective()
        objective.add_error(error_name, x_label, y_label, weight)

    # Fixes a parameter
    def fix_param(self, param_name:str, param_value:float) -> None:
        self.__print__("Fixing the '{}' parameter to fixed value of {:0.4}".format(param_name, float(param_value)))
        self.__controller__.fix_param(param_name, param_value)

    # Initialises a parameter
    def set_param(self, param_name:str, param_value:float, param_std:float=0) -> None:
        message = "Setting the '{}' parameter to an initial value of {:0.4} and deviation of {:0.4}"
        self.__print__(message.format(param_name, float(param_value), float(param_std)))
        self.__controller__.set_param(param_name, param_value, param_std)

    # Prepares the results recorder
    def start_rec(self, interval:int=10, population:int=10) -> None:
        self.__print__(f"Initialising the recorder with an interval of {interval} and population of {population}")
        self.__recorder__ = Recorder(self.__controller__, interval, population, self.get_output("out"))

    # Prepares and conducts the optimisation
    def start_opt(self, num_gens:int=10000, init_pop:int=100, offspring:int=50, crossover:float=0.65, mutation:float=0.35) -> None:
        self.__print__(f"Conducting the optimisation ({num_gens}, {init_pop}, {offspring}, {crossover}, {mutation})")
        self.__recorder__.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.__controller__, self.__recorder__)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Removes the tertiary creep from the most recently added creep curve
    def rm_damage(self, window:int=0.1, acceptance:float=0.9) -> None:
        self.__print__(f"Removing the tertiary creep")
        objective = self.__controller__.get_last_objective()
        if objective.get_type() != "creep":
            raise ValueError("Cannot remove damage because it can only be removed for creep curves!")
        exp_data = objective.get_exp_data()
        exp_data = remove_after_sp(exp_data, "min", "time", "strain", window, acceptance, 0)
        objective.set_exp_data(exp_data)

    # Removes the data after the tertiary creep for the most recently added 
    def rm_ocreep(self, window:int=0.1, acceptance:float=0.9) -> None:
        self.__print__(f"Removing the oxidised creep")
        objective = self.__controller__.get_last_objective()
        if objective.get_type() != "creep":
            raise ValueError("Cannot remove oxidised creep because it can only be removed for creep curves!")
        exp_data = objective.get_exp_data()
        exp_data = remove_after_sp(objective["curve"], "max", "time", "strain", window, acceptance, 0)
        objective.set_exp_data(exp_data)
    
    # Removes the data for a curve at a specific x value
    def rm_manual(self, x_value:float, x_label:str) -> None:
        objective = self.__controller__.get_last_objective()
        x_units = DATA_UNITS[x_label]
        self.__print__(f"Removing the values after {x_label} of {x_value} ({x_units})")
        objective["curve"] = remove_data_after(objective["curve"], x_value)
    
    # Visualises the experimental data
    def visualise(self, type:str=None, file_name:str="", x_label:str=None, y_label:str=None, derivative:int=0) -> None:
        
        # Determine type (use type of last curve if undefined)
        type = self.__controller__.get_last_objective().get_type() if type == None else type
        
        # Determine file name
        default_file_name = f"exp_{type}_d{derivative}.png" if derivative > 0 else f"exp_{type}.png"
        file_name = default_file_name if file_name == "" else f"{file_name}.png"
        
        # Display informative message
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        derivative_str = f" {ordinal(derivative)} derivative of the" if derivative > 0 else ""
        self.__print__(f"Visualising the{derivative_str} {type} data at '{file_name}'")
        
        # Actually plot the curves
        self.__controller__.plot_curves(type, self.get_output(file_name), x_label, y_label, derivative)

    # Plots the results of a set of parameters
    def fast_plot(self, *params:tuple, type_list:list=None, x_label:str=None, y_label:str=None) -> None:
        param_str = ["{:0.4}".format(float(param)) for param in params]
        self.__print__("Plotting the results for {}".format(str(param_str).replace("'", "")))

        # Get parameters and check input
        param_name_list = list(self.__controller__.get_model().get_param_dict().keys())
        param_value_dict = {key: value for key, value in zip(param_name_list, params)}
        if len(params) != len(param_name_list):
            raise ValueError("Could not plot because the number of inputs do not match the number of parameters!")
        
        # Initialise recorder
        recorder = Recorder(self.__controller__, 0, 1, "")
        recorder.define_hyperparameters("n/a","n/a","n/a","n/a","n/a")
        
        # Add parameters and create record
        error_value_dict = self.__controller__.calculate_error_value_dict(*params)
        recorder.update_optimal_solution(param_value_dict, error_value_dict)
        recorder.create_record(self.get_output("results.xlsx"), type_list, x_label, y_label)

    # Prints out the final messaeg
    def __del__(self):
        time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        duration = round(time.time() - self.start_time)
        print(f"\n  Finished on {time_str} in {duration}s\n")