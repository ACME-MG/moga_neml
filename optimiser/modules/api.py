"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import os, math
import numpy as np
import matplotlib.pyplot as plt
from modules.reader import read_experimental_data
from modules.moga.objective import Objective
from modules.moga.problem import Problem
from modules.moga.moga import MOGA
from modules.recorder import Recorder

# Helper libraries
import sys; sys.path += ["../__common__"]
from api_template import APITemplate
from plotter import quick_plot_N, quick_subplot
from derivative import remove_after_sp, differentiate_curve

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title:str="", display:int=2):
        super().__init__(title, display)
        self.__objective__ = Objective()
        self.__plot_count__ = 1
    
    # Reads in the experimental data from a file
    def read_file(self, file_name:str, train:bool=True) -> None:
        data_type = "train" if train else "test"
        self.add(f"Reading {data_type}ing data from {file_name}")
        curves = read_experimental_data([self.get_input(file_name)])
        self.__objective__.add_curves(curves, data_type)

    # Reads in the experimental data from folders
    def read_folder(self, folder_name:str, train:bool=True) -> None:
        data_type = "train" if train else "test"
        self.add(f"Reading {data_type}ing data from {folder_name}")
        data_paths = [self.get_input(f"{folder_name}/{file}") for file in os.listdir(self.get_input(folder_name)) if file.endswith(".csv")]
        curves = read_experimental_data(data_paths)
        self.__objective__.add_curves(curves, data_type)

    # Defines the model
    def define_model(self, model_name:str, *args) -> None:
        self.add(f"Defining the model ({model_name})")
        self.__objective__.define_model(model_name, args[0])
    
    # Adds an error
    def add_error(self, error_name:str, type:str, weight:float=1) -> None:
        self.add(f"Preparing to minimise the {error_name} error")
        self.__objective__.add_error(error_name, type, weight)

    # Fixes a parameter
    def fix_param(self, param_name:str, param_value:float) -> None:
        self.add(f"Fixing the {param_name} to {param_value}")
        self.__objective__.fix_param(param_name, param_value)

    # Visualises teh training and testing data
    def visualise(self, file_name:str="", separate:bool=False) -> None:
        self.add(f"[Experimental] Visualising training and testing curves {'separately' if separate else 'together'}")
        file_name = f"plot_{self.__plot_count__}.png" if file_name == "" else f"{file_name}.png"
        exp_test_curves = self.__objective__.get_exp_curves(["test"])
        exp_train_curves = self.__objective__.get_exp_curves(["train"])
        if separate:
            all_curves = exp_test_curves + exp_train_curves
            quick_subplot(self.get_output(file_name), all_curves, [curve["file_path"] for curve in all_curves])
        else:
            quick_plot_N(self.get_output(file_name), [exp_train_curves, exp_test_curves], ["Training", "Testing"], ["gray", "silver"], markers=["scat", "scat"])
        self.__plot_count__ += 1

    # Prepares the model and results recorder
    def record(self, interval:int=10, population:int=10) -> None:
        self.add("Preparing the results recorder")
        self.interval = interval
        self.population = population
        
    # Conducts the optimisation
    def optimise(self, num_gens:int=10000, init_pop:int=400, offspring:int=400, crossover:float=0.65, mutation:float=0.35) -> None:
        self.add("Optimising the parameters of the model")
        self.__objective__.define_optimisation()
        self.__recorder__ = Recorder(self.__objective__, self.get_output("moga"), self.interval, self.population)
        self.__recorder__.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.__objective__, self.__recorder__)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Plots the results of a set of parameters
    def plot_results(self, *params) -> None:
        self.add("Plotting experimental and predicted curves")
        self.__objective__.define_optimisation()
        recorder = Recorder(self.__objective__, "", 0, 1)
        recorder.define_hyperparameters(0,0,0,0,0)
        errors = self.__objective__.get_error_values(*params)
        recorder.update_population(params, errors)
        recorder.write_results(self.get_output("results.xlsx"))

    # Removes the tertiary creep from creep curves
    def __remove_tertiary_creep__(self, window:int=200, acceptance:float=0.9) -> None:
        self.add("[Experimental] Removing tertiary creep strain")
        for objective in self.__objective__.objective_list:
            objective["curve"] = remove_after_sp(objective["curve"], "min", window, acceptance, 0)

    # Removes the data after the tertiary creep
    def __remove_oxidised_creep__(self, window:int=300, acceptance:float=0.9) -> None:
        self.add("[Experimental] Removing oxidised creep strain")
        for objective in self.__objective__.objective_list:
            objective["curve"] = remove_after_sp(objective["curve"], "max", window, acceptance, 0)
    
    # Visualises the work damage with the work rate of the curves
    def __visualise_work__(self) -> None:
        self.add("[Experimental] Plotting the work damage against the average work rate")
        for curve in self.__objective__.get_exp_curves(["train", "test"]):
            d_curve = differentiate_curve(curve)
            work_rate_list = [curve["stress"] * dy for dy in d_curve["y"]]
            avg_work_rate = np.average(work_rate_list)
            if avg_work_rate <= 0:
                continue
            work_failure = curve["y"][-1] * curve["stress"]
            plt.scatter([math.log10(avg_work_rate)], [work_failure])
        plt.savefig(self.get_output("work_damage.png"))