"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import sys, os
from modules.reader import read_experimental_data, export_data_summary, prematurely_end_curve
from modules.moga.objective import Objective
from modules.moga.problem import Problem, PENALTY_FACTOR
from modules.moga.moga import MOGA
from modules.recorder import Recorder
from modules.errors.__error_factory__ import get_error_list
from modules.constraints.__constraint_factory__ import get_constraint_list

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from api_template import APITemplate
from plotter import quick_plot_N, quick_subplot
from __model_factory__ import get_model
from derivative import remove_after_sp

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title="", display=2):
        super().__init__(title, display)
        self.error_list, self.constraint_list = [], []
        self.train_curves, self.test_curves = [], []
        self.plot_count = 1
        self.csv_path = self.get_output("moga")
    
    # Reads in the experimental data from files
    def read_files(self, train_files=[], test_files=[]):
        self.add(f"Reading experimental data from files ({len(train_files)}/{len(test_files)})")
        train_file_paths = [f"{self.get_input(file)}" for file in train_files]
        test_file_paths = [f"{self.get_input(file)}" for file in test_files]
        self.train_curves += read_experimental_data(train_file_paths)
        self.test_curves += read_experimental_data(test_file_paths)

    # Reads in the experimental data from folders
    def read_folder(self, train_folder="", test_folder=""):
        self.add(f"Reading experimental data from folders")
        train_file_paths = [self.get_input(f"{train_folder}/{file}") for file in os.listdir(self.get_input(train_folder)) if file.endswith(".csv")]
        test_file_paths = [self.get_input(f"{test_folder}/{file}") for file in os.listdir(self.get_input(test_folder)) if file.endswith(".csv")]
        self.train_curves = read_experimental_data(train_file_paths)
        self.test_curves = read_experimental_data(test_file_paths)

    # Exports summary about the experimental data
    def export_summary(self, file_name="summary.csv"):
        self.add("Exporting summaries of experimental data")
        export_data_summary(self.get_output(file_name), self.train_curves + self.test_curves)

    # Visualises the training and testing data together
    def visualise_together(self, file_name=None):
        self.add("Visualising training and testing curves together")
        file_name = f"plot_{self.plot_count}.png" if file_name == None else f"{file_name}.png"
        quick_plot_N(self.get_output(file_name), [self.train_curves, self.test_curves], ["Training", "Testing"], ["gray", "silver"])
        self.plot_count += 1

    # Visualises the training and testing data separately
    def visualise_separately(self, file_name=None):
        self.add("Visualising training and testing curves separately")
        file_name = f"plot_{self.plot_count}.png" if file_name == None else f"{file_name}.png"
        all_curves = self.train_curves+self.test_curves
        quick_subplot(self.get_output(file_name), all_curves, [curve["file_path"] for curve in all_curves])
        self.plot_count += 1

    # Prematurely ends the creep curves
    def remove_manual(self, train_ruptures=[], test_ruptures=[]):
        self.add(f"Removing creep after custom rupture times")
        self.train_curves = [prematurely_end_curve(self.train_curves[i], train_ruptures[i]) for i in range(len(self.train_curves))]
        self.test_curves = [prematurely_end_curve(self.test_curves[i], test_ruptures[i]) for i in range(len(self.test_curves))]

    # Removes the tertiary creep from creep curves
    def remove_tertiary_creep(self, window=200, acceptance=0.9):
        self.add("Removing tertiary creep strain")
        self.train_curves = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.train_curves if curve["type"] == "creep"]
        self.test_curves = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.test_curves if curve["type"] == "creep"]

    # Removes the data after the tertiary creep
    def remove_oxidised_creep(self, window=300, acceptance=0.9):
        self.add("Removing oxidised creep strain")
        self.train_curves = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.train_curves if curve["type"] == "creep"]
        self.test_curves = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.test_curves if curve["type"] == "creep"]

    # Initialising the model
    def define_model(self, model_name, args=[]):
        self.add(f"Defining the model ({model_name})")
        self.model = get_model(model_name, self.train_curves, args)
    
    # Defining the errors
    def define_errors(self, type, error_names):
        self.add(f"Defining the errors to minimise ({len(error_names)})")
        self.error_list += get_error_list(type, error_names, self.train_curves)

    # Defining the constraints
    def define_constraints(self, type, constraint_names):
        self.add(f"Defining the constraints to adhere ({len(constraint_names)})")
        self.constraint_list += get_constraint_list(type, constraint_names, self.train_curves)

    # Prepares the recorder
    def define_recorder(self, interval=10, population=10):
        self.add("Preparing the results recorder")
        self.objective = Objective(self.model, self.error_list, self.constraint_list)
        self.recorder = Recorder(self.objective, self.train_curves, self.test_curves, self.csv_path, interval, population)

    # Conducts the optimisation
    def optimise(self, num_gens=10000, init_pop=400, offspring=400, crossover=0.65, mutation=0.35):
        self.add("Optimising the parameters of the model")
        self.recorder.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.objective, self.recorder)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Plots the results of a set of parameters
    def plot_results(self, params):
        self.add("Plotting experimental and predicted curves")

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
