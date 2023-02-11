"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import time, sys, os
from modules.reader import read_experimental_data, export_data_summary, prematurely_end_curve
from modules.moga.objective import Objective
from modules.moga.problem import Problem
from modules.moga.moga import MOGA
from modules.recorder import Recorder
from modules.errors.__error_factory__ import get_error_list
from modules.constraints.__constraint_factory__ import get_constraint_list

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from progressor import Progressor
from plotter import quick_plot_N, quick_subplot
from general import safe_mkdir
from __model_factory__ import get_model
from derivative import remove_after_sp

# Input / Output
INPUT_DIR   = "input"
RESULTS_DIR = "results"

# API Class
class API:

    # Constructor
    def __init__(self, fancy=False, title="", verbose=False):
        
        # Initialise
        self.prog = Progressor(fancy, title, verbose)
        self.constraint_list = []
        self.train_curves = []
        self.test_curves = []
        self.plot_count = 1

        # Initialise paths
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_dir  = self.output_dir if title == "" else f"{self.output_dir} ({title})"
        self.output_path = "{}/{}".format(RESULTS_DIR, self.output_dir)
        self.csv_path    = "{}/{}".format(self.output_path, "moga")

        # Set up environment
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)
    
    # Reads in the experimental data from files
    def read_files(self, train_files=[], test_files=[]):
        self.prog.add(f"Reading experimental data from files ({len(train_files)}/{len(test_files)})")
        self.train_file_paths = [f"{INPUT_DIR}/{file}" for file in train_files]
        self.train_curves = read_experimental_data(self.train_file_paths)
        self.test_file_paths = [f"{INPUT_DIR}/{file}" for file in test_files]
        self.test_curves = read_experimental_data(self.test_file_paths)

    # Reads in the experimental data from folders
    def read_folder(self, train_folder="", test_folder=""):
        self.prog.add(f"Reading experimental data from folders")
        self.train_file_paths = [f"{INPUT_DIR}/{train_folder}/{file}" for file in os.listdir(f"{INPUT_DIR}/{train_folder}") if file.endswith(".csv")]
        self.train_curves = read_experimental_data(self.train_file_paths)
        self.test_file_paths = [f"{INPUT_DIR}/{test_folder}/{file}" for file in os.listdir(f"{INPUT_DIR}/{test_folder}") if file.endswith(".csv")]
        self.test_curves = read_experimental_data(self.test_file_paths)

    # Exports summary about the experimental data
    def export_summary(self, file_name="summary.csv"):
        self.prog.add("Exporting summaries of experimental data")
        export_data_summary(f"{self.output_path}/{file_name}", self.train_curves + self.test_curves)

    # Visualises the training and testing curves
    def visualise_data(self, file_name=None, separate=False):
        self.prog.add("Visualising training and testing curves")
        file_name = f"plot_{self.plot_count}" if file_name == None else file_name
        if separate:
            quick_subplot(f"{self.output_path}/{file_name}.png", self.train_curves+self.test_curves, self.train_file_paths+self.test_file_paths)
        else:
            quick_plot_N(f"{self.output_path}/{file_name}.png", [self.train_curves, self.test_curves], ["Training", "Testing"], ["gray", "silver"])
        self.plot_count += 1

    # Prematurely ends the creep curves
    def remove_manual(self, train_ruptures=[], test_ruptures=[]):
        self.prog.add(f"Removing creep after custom rupture times")
        self.train_curves = [prematurely_end_curve(self.train_curves[i], train_ruptures[i]) for i in range(len(self.train_curves))]
        self.test_curves = [prematurely_end_curve(self.test_curves[i], test_ruptures[i]) for i in range(len(self.test_curves))]

    # Removes the tertiary creep from creep curves
    def remove_tertiary_creep(self, window=200, acceptance=0.9):
        self.prog.add("Removing tertiary creep strain")
        self.train_curves = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.train_curves if curve["type"] == "creep"]
        self.test_curves = [remove_after_sp(curve, "min", window, acceptance, 0) for curve in self.test_curves if curve["type"] == "creep"]

    # Removes the data after the tertiary creep
    def remove_oxidised_creep(self, window=300, acceptance=0.9):
        self.prog.add("Removing oxidised creep strain")
        self.train_curves = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.train_curves if curve["type"] == "creep"]
        self.test_curves = [remove_after_sp(curve, "max", window, acceptance, 0) for curve in self.test_curves if curve["type"] == "creep"]

    # Initialising the model
    def define_model(self, model_name, args=[]):
        self.prog.add(f"Defining the model ({model_name})")
        self.model = get_model(model_name, self.train_curves, args)
    
    # Defining the errors
    def define_errors(self, error_names):
        self.prog.add(f"Defining the errors to minimise ({len(error_names)})")
        self.error_list = get_error_list(error_names, self.train_curves)

    # Defining the constraints
    def define_constraints(self, constraint_names):
        self.prog.add(f"Defining the constraints to adhere ({len(constraint_names)})")
        self.constraint_list = get_constraint_list(constraint_names, self.train_curves)

    # Prepares the recorder
    def define_recorder(self, interval=10, population=10):
        self.prog.add("Preparing the results recorder")
        self.objective = Objective(self.model, self.error_list, self.constraint_list)
        self.recorder = Recorder(self.objective, self.train_curves, self.test_curves, self.csv_path, interval, population)

    # Conducts the optimisation
    def optimise(self, num_gens=10000, init_pop=400, offspring=400, crossover=0.65, mutation=0.35):
        self.prog.add("Optimising the parameters of the model")
        self.recorder.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.objective, self.recorder)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        moga.optimise()

    # Plots the results
    def plot_results(self, params):
        self.prog.add("Plotting the results")
        prd_train_curves = self.model.get_specified_prd_curves(params, self.train_curves)
        prd_test_curves = self.model.get_specified_prd_curves(params, self.test_curves)
        quick_plot_N(
            path=f"{self.output_path}/predicted.png",
            curve_lists=[self.train_curves, self.test_curves, prd_train_curves, prd_test_curves],
            labels=["Training", "Testing", "Predicted", "Predicted"],
            colours=["gray", "silver", "red", "red"],
            markers=["scat", "scat", "line", "line"],
        )

    # Returns the error values of the objective functions
    def get_errors(self, params):
        self.prog.add("Obtaining error values")
        prd_curves  = self.model.get_prd_curves(*params)
        objective   = Objective(self.model, self.error_list)
        error_names = objective.get_error_names()
        error_values = objective.get_error_values(prd_curves)
        with open(f"{self.output_path}/errors.csv", "w+") as file:
            for i in range(len(error_names)):
                file.write(f"{error_names[i]},{error_values[i]}\n")
            file.write(f"err_sqr_sum,{sum([err**2 for err in error_values])}")
