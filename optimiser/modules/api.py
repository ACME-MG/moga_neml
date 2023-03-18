"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import sys, os
from modules.reader import read_experimental_data, export_data_summary
from modules.moga.objective import Objective
from modules.moga.problem import Problem, PENALTY_FACTOR
from modules.moga.moga import MOGA
from modules.recorder import Recorder
from modules.errors.__error_factory__ import create_error, create_custom_y_area_error
from modules.constraints.__constraint_factory__ import create_constraint

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from api_template import APITemplate
from plotter import quick_plot_N, quick_subplot
from __model_factory__ import get_model
from derivative import remove_after_sp

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title:str="", display:int=2):
        super().__init__(title, display)
        self.error_list, self.constraint_list = [], []
        self.train_curves, self.test_curves = [], []
        self.plot_count = 1
        self.csv_path = self.get_output("moga")
    
    # Reads in the experimental data from a file
    def read_file(self, file_name:str, train:bool=True):
        self.add(f"Reading {'train' if train else 'test'}ing data from {file_name}")
        experimental_data = read_experimental_data([self.get_input(file_name)])
        if train:
            self.train_curves += experimental_data
        else:
            self.test_curves += experimental_data

    # Reads in the experimental data from folders
    def read_folder(self, folder_name:str, train:bool=True):
        self.add(f"Reading {'train' if train else 'test'}ing data from {folder_name}")
        data_paths = [self.get_input(f"{folder_name}/{file}") for file in os.listdir(self.get_input(folder_name)) if file.endswith(".csv")]
        experimental_data = read_experimental_data(data_paths)
        if train:
            self.train_curves += experimental_data
        else:
            self.test_curves += experimental_data

    # Exports summary about the experimental data
    def export_summary(self, file_name:str="summary.csv"):
        self.add("Exporting summaries of experimental data")
        export_data_summary(self.get_output(file_name), self.train_curves + self.test_curves)

    # Defines the model
    def define_model(self, model_name:str, args:list=[]):
        self.add(f"Defining the model ({model_name})")
        self.model_name = model_name
        self.args = args
    
    # Adds an error
    def add_error(self, error_name:str, type:str, weight:int=1):
        self.add(f"Preparing to minimise the {error_name} error")
        self.error_list.append(create_error(error_name, type, weight, self.train_curves))

    # Adds a constraint
    def add_constraint(self, constraint_name:str, type:str):
        self.add(f"Preparing to apply the {constraint_name} constraint")
        self.constraint_list.append(create_constraint(constraint_name, type, self.train_curves))

    # Prepares the model and results recorder
    def record(self, interval:int=10, population:int=10):
        self.add("Preparing the results recorder")
        self.model = get_model(self.model_name, self.train_curves, self.args)
        self.objective = Objective(self.model, self.error_list, self.constraint_list)
        self.recorder = Recorder(self.objective, self.train_curves, self.test_curves, self.csv_path, interval, population)

    # Conducts the optimisation
    def optimise(self, num_gens:int=10000, init_pop:int=400, offspring:int=400, crossover:float=0.65, mutation:float=0.35):
        self.add("Optimising the parameters of the model")
        self.recorder.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.objective, self.recorder)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Adds the vertical area error with a custom CDF (x**0.5 for right skewed, x**2 for left skewed)
    def __add_custom_y_area__(self, type:str, weight:int=1, cdf=lambda x:x):
        self.add("[Experimental] Preparing to minimise custom y_area error")
        self.error_list.append(create_custom_y_area_error(type, weight, self.train_curves, cdf))

    # Plots the results of a set of parameters
    def __plot_results__(self, params:list):
        self.add("[Experimental] Plotting experimental and predicted curves")

        # Get recorder
        objective = Objective(self.model, self.error_list, self.constraint_list)
        recorder = Recorder(objective, self.train_curves, self.test_curves, self.csv_path, 0, 1)
        recorder.define_hyperparameters(0,0,0,0,0)

        # Get errors and constraints
        prd_curves        = self.model.get_specified_prd_curves(params, self.train_curves)
        error_values      = objective.get_error_values(prd_curves)
        constraint_values = objective.get_constraint_values(prd_curves)
        feasible_list     = [constraint <= 0 for constraint in constraint_values]
        error_values      = [PENALTY_FACTOR*error for error in error_values] if False in feasible_list else error_values
        
        # Output results
        recorder.update_population(params, error_values, constraint_values)
        recorder.write_results(self.get_output("results.xlsx"))

    # Visualises the training and testing data
    def __visualise__(self, file_name:str="", separate:bool=False):
        self.add(f"[Experimental] Visualising training and testing curves {'separately' if separate else 'together'}")
        file_name = f"plot_{self.plot_count}.png" if file_name == None else f"{file_name}.png"
        if separate:
            quick_plot_N(self.get_output(file_name), [self.train_curves, self.test_curves], ["Training", "Testing"], ["gray", "silver"])
        else:
            all_curves = self.train_curves+self.test_curves
            quick_subplot(self.get_output(file_name), all_curves, [curve["file_path"] for curve in all_curves])
        self.plot_count += 1

    # Removes the tertiary creep from creep curves
    def __remove_tertiary_creep__(self, window:int=200, acceptance:float=0.9):
        self.add("[Experimental] Removing tertiary creep strain")
        self.train_curves = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.train_curves if curve["type"] == "creep"]
        self.test_curves = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.test_curves if curve["type"] == "creep"]

    # Removes the data after the tertiary creep
    def __remove_oxidised_creep__(self, window:int=300, acceptance:float=0.9):
        self.add("[Experimental] Removing oxidised creep strain")
        self.train_curves = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.train_curves if curve["type"] == "creep"]
        self.test_curves = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.test_curves if curve["type"] == "creep"]