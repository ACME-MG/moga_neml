"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import math, os, re, time
import numpy as np
import matplotlib.pyplot as plt
from moga_neml._interface.reader import read_experimental_data
from moga_neml._optimise.objective import Objective
from moga_neml._optimise.problem import Problem
from moga_neml._optimise.moga import MOGA
from moga_neml._optimise.recorder import Recorder
from moga_neml._interface.plotter import quick_plot_N, quick_subplot
from moga_neml._maths.derivative import remove_after_sp, differentiate_curve
from moga_neml._maths.general import safe_mkdir

# API Class
class API:

    # Constructor
    def __init__(self, title:str="", input_path="./data", output_path="./results"):
                
        # Prepare progressor
        title = "" if title == "" else f"_{title}"
        title = re.sub(r"[^a-zA-Z0-9_]", "", title.replace(" ", "_"))
        
        # Define input
        self.input_path  = input_path
        self.get_input   = lambda x : f"{self.input_path}/{x}"
        
        # Define output
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{output_path}/{self.output_dir}{title}"
        self.get_output   = lambda x : f"{self.output_path}/{x}"
        
        # Create directories
        safe_mkdir(output_path)
        safe_mkdir(self.output_path)
        
        # Initialise internal variables
        self.__objective__ = Objective()
        self.__plot_count__ = 1
        self.__print_count__ = 1
    
    # Displays a message before running the command
    def __print__(self, message:str) -> None:
        print(f" {self.__print_count__})\t{message}")
        self.__print_count__ += 1
    
    # Reads in the experimental data from a file
    def read_file(self, file_name:str, train:bool=True) -> None:
        data_type = "train" if train else "test"
        self.__print__(f"Reading data from '{file_name}' for {data_type}ing")
        curves = read_experimental_data([self.get_input(file_name)])
        self.__objective__.add_curves(curves, data_type)

    # Reads in the experimental data from folders
    def read_folder(self, folder_name:str, train:bool=True) -> None:
        data_type = "train" if train else "test"
        self.__print__(f"Reading data from '{folder_name}' for {data_type}ing")
        data_paths = [self.get_input(f"{folder_name}/{file}") for file in os.listdir(self.get_input(folder_name)) if file.endswith(".csv")]
        curves = read_experimental_data(data_paths)
        self.__objective__.add_curves(curves, data_type)

    # Defines the model
    def define_model(self, model_name:str, *args) -> None:
        self.__print__(f"Defining model '{model_name}'")
        self.__objective__.define_model(model_name, args)
    
    # Adds an error
    def add_error(self, error_name:str, type:str, weight:float=1) -> None:
        self.__print__(f"Adding error '{error_name}' for {type} with a weight of {weight}")
        self.__objective__.add_error(error_name, type, weight)

    # Fixes a parameter
    def fix_param(self, param_name:str, param_value:float) -> None:
        self.__print__(f"Fixed the '{param_name}' parameter to {param_value}")
        self.__objective__.fix_param(param_name, param_value)

    # Visualises teh training and testing data
    def visualise(self, file_name:str="", type:str="creep", separate:bool=False) -> None:
        file_name = f"plot_{self.__plot_count__}.png" if file_name == "" else f"{file_name}.png"
        self.__print__(f"Visualising the data at '{file_name}'")
        exp_test_curves = self.__objective__.get_exp_curves(["test"])
        exp_test_curves = [curve for curve in exp_test_curves if curve["type"] == type]
        exp_train_curves = self.__objective__.get_exp_curves(["train"])
        exp_train_curves = [curve for curve in exp_train_curves if curve["type"] == type]
        if separate:
            all_curves = exp_test_curves + exp_train_curves
            quick_subplot(self.get_output(file_name), all_curves, [curve["file_path"] for curve in all_curves])
        else:
            quick_plot_N(self.get_output(file_name), [exp_train_curves, exp_test_curves], ["Training", "Testing"], ["gray", "silver"], markers=["scat", "scat"])
        self.__plot_count__ += 1

    # Prepares the model and results recorder
    def record(self, interval:int=10, population:int=10) -> None:
        self.__print__(f"Initialising the recorder with an interval of {interval} and population of {population}")
        self.interval = interval
        self.population = population
        
    # Conducts the optimisation
    def optimise(self, num_gens:int=10000, init_pop:int=400, offspring:int=400, crossover:float=0.65, mutation:float=0.35) -> None:
        self.__print__(f"Conducting the optimisation ({num_gens}, {init_pop}, {offspring}, {crossover}, {mutation})")
        self.__objective__.define_optimisation()
        self.__recorder__ = Recorder(self.__objective__, self.get_output("moga"), self.interval, self.population)
        self.__recorder__.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.__objective__, self.__recorder__)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Plots the results of a set of parameters
    def plot_results(self, *params) -> None:
        self.__print__(f"Plotting the results for {params}")
        self.__objective__.define_optimisation()
        recorder = Recorder(self.__objective__, "", 0, 1)
        recorder.define_hyperparameters(0,0,0,0,0)
        errors = self.__objective__.get_error_values(*params)
        recorder.update_population(params, errors)
        recorder.create_record(self.get_output("results.xlsx"))

    # Removes the tertiary creep from the most recently added creep curve
    def remove_tertiary_creep(self, window:int=200, acceptance:float=0.9) -> None:
        self.__print__(f"Removing the tertiary creep")
        objective = self.__objective__.objective_list[-1]
        objective["curve"] = remove_after_sp(objective["curve"], "min", window, acceptance, 0)

    # Removes the data after the tertiary creep for the most recently added 
    def remove_oxidised_creep(self, window:int=300, acceptance:float=0.9) -> None:
        self.__print__(f"Removing the oxidised creep")
        objective = self.__objective__.objective_list[-1]
        objective["curve"] = remove_after_sp(objective["curve"], "max", window, acceptance, 0)
    
    # Visualises the work damage with the work rate of the curves
    def __visualise_work__(self) -> None:
        self.__print__("[Experimental] Visualising the work damage")
        for curve in self.__objective__.get_exp_curves(["train", "test"]):
            d_curve = differentiate_curve(curve)
            work_rate_list = [curve["stress"] * dy for dy in d_curve["y"]]
            avg_work_rate = np.average(work_rate_list)
            if avg_work_rate <= 0:
                continue
            work_failure = curve["y"][-1] * curve["stress"]
            plt.scatter([math.log10(avg_work_rate)], [work_failure])
        plt.savefig(self.get_output("work_damage.png"))