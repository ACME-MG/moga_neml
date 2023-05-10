"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import sys, os, math
import numpy as np
import matplotlib.pyplot as plt
from modules.reader import read_experimental_data
from modules.moga.objective import Objective
from modules.moga.problem import Problem
from modules.moga.moga import MOGA
from modules.recorder import Recorder
from modules.errors.__error__ import get_error
from modules.constraints.__constraint__ import get_constraint
from modules.models.__model__ import get_model

# Helper libraries
sys.path += ["../__common__"]
from api_template import APITemplate
from plotter import quick_plot_N, quick_subplot
from derivative import remove_after_sp, differentiate_curve

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title:str="", display:int=2):
        super().__init__(title, display)
        self.__error_list__, self.__constraint_list__ = [], []
        self.__train_curves__, self.__test_curves__ = [], []
        self.__plot_count__ = 1
        self.__csv_path__ = self.get_output("moga")
    
    # Reads in the experimental data from a file
    def read_file(self, file_name:str, train:bool=True) -> None:
        self.add(f"Reading {'train' if train else 'test'}ing data from {file_name}")
        experimental_data = read_experimental_data([self.get_input(file_name)])
        if train:
            self.__train_curves__ += experimental_data
        else:
            self.__test_curves__ += experimental_data

    # Reads in the experimental data from folders
    def read_folder(self, folder_name:str, train:bool=True) -> None:
        self.add(f"Reading {'train' if train else 'test'}ing data from {folder_name}")
        data_paths = [self.get_input(f"{folder_name}/{file}") for file in os.listdir(self.get_input(folder_name)) if file.endswith(".csv")]
        experimental_data = read_experimental_data(data_paths)
        if train:
            self.__train_curves__ += experimental_data
        else:
            self.__test_curves__ += experimental_data

    # Visualises the training and testing data
    def visualise(self, file_name:str="", separate:bool=False) -> None:
        self.add(f"[Experimental] Visualising training and testing curves {'separately' if separate else 'together'}")
        file_name = f"plot_{self.__plot_count__}.png" if file_name == "" else f"{file_name}.png"
        if separate:
            all_curves = self.__train_curves__+self.__test_curves__
            quick_subplot(self.get_output(file_name), all_curves, [curve["file_path"] for curve in all_curves])
        else:
            quick_plot_N(self.get_output(file_name), [self.__train_curves__, self.__test_curves__], ["Training", "Testing"], ["gray", "silver"], markers=["scat", "scat"])
        self.__plot_count__ += 1

    # Defines the model
    def define_model(self, model_name:str, *args) -> None:
        self.add(f"Defining the model ({model_name})")
        self.__model_name__ = model_name
        self.__fixed_params__ = {}
        self.__args__ = args
    
    # Adds an error
    def add_error(self, error_name:str, type:str, weight:float=1) -> None:
        self.add(f"Preparing to minimise the {error_name} error")
        error = get_error(error_name, type, weight, self.__train_curves__)
        self.__error_list__.append(error)

    # Adds a constraint
    def add_constraint(self, constraint_name:str, type:str, penalty:float=1) -> None:
        self.add(f"Preparing to apply the {constraint_name} constraint")
        constraint = get_constraint(constraint_name, type, penalty, self.__train_curves__)
        self.__constraint_list__.append(constraint)

    # Fixes a parameter
    def fix_param(self, param_name:str, param_value:float) -> None:
        self.add(f"Fixing the {param_name} to {param_value}")
        self.__fixed_params__[param_name] = param_value

    # Prepares the model and results recorder
    def record(self, interval:int=10, population:int=10) -> None:
        self.add("Preparing the results recorder")
        self.__model__ = get_model(self.__model_name__, self.__train_curves__, self.__args__)
        [self.__model__.fix_param(name, self.__fixed_params__[name]) for name in self.__fixed_params__.keys()]
        if len(self.__model__.get_fixed_params()) == len(self.__model__.get_param_info()):
            raise ValueError("All parameters have been fixed so no parameters need to be calibrated!")
        self.__objective__ = Objective(self.__model__, self.__error_list__, self.__constraint_list__)
        self.__recorder__ = Recorder(self.__objective__, self.__train_curves__, self.__test_curves__, self.__csv_path__, interval, population)

    # Conducts the optimisation
    def optimise(self, num_gens:int=10000, init_pop:int=400, offspring:int=400, crossover:float=0.65, mutation:float=0.35) -> None:
        self.add("Optimising the parameters of the model")
        self.__recorder__.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.__objective__, self.__recorder__)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Plots the results of a set of parameters
    def __plot_results__(self, params:list[float]) -> None:
        self.add("[Experimental] Plotting experimental and predicted curves")

        # Get recorder
        self.__model__ = get_model(self.__model_name__, self.__train_curves__, self.__args__)
        objective = Objective(self.__model__, self.__error_list__, self.__constraint_list__)
        recorder = Recorder(objective, self.__train_curves__, self.__test_curves__, self.__csv_path__, 0, 1)
        recorder.define_hyperparameters(0,0,0,0,0)

        # Get errors and constraints
        prd_curves        = self.__model__.get_specified_prd_curves(params, self.__train_curves__)
        error_values      = objective.get_error_values(prd_curves)
        constraint_values = objective.get_constraint_values(prd_curves)
        error_values      = objective.get_penalised_error_values(error_values, constraint_values)
        
        # Output results
        recorder.update_population(params, error_values, constraint_values)
        recorder.write_results(self.get_output("results.xlsx"))

    # Removes the tertiary creep from creep curves
    def __remove_tertiary_creep__(self, window:int=200, acceptance:float=0.9) -> None:
        self.add("[Experimental] Removing tertiary creep strain")
        self.__train_curves__ = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.__train_curves__ if curve["type"] == "creep"]
        self.__test_curves__ = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.__test_curves__ if curve["type"] == "creep"]

    # Removes the data after the tertiary creep
    def __remove_oxidised_creep__(self, window:int=300, acceptance:float=0.9) -> None:
        self.add("[Experimental] Removing oxidised creep strain")
        self.__train_curves__ = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.__train_curves__ if curve["type"] == "creep"]
        self.__test_curves__ = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.__test_curves__ if curve["type"] == "creep"]
    
    # Visualises the work damage with the work rate of the curves
    def __visualise_work__(self) -> None:
        self.add("[Experimental] Plotting the work damage against the average work rate")
        for curve in self.__train_curves__ + self.__test_curves__:
            d_curve = differentiate_curve(curve)
            work_rate_list = [curve["stress"] * dy for dy in d_curve["y"]]
            avg_work_rate = np.average(work_rate_list)
            if avg_work_rate <= 0:
                continue
            work_failure = curve["y"][-1] * curve["stress"]
            plt.scatter([math.log10(avg_work_rate)], [work_failure])
        plt.savefig(self.get_output("work_damage.png"))