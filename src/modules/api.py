"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import time
from modules.reader import read_experimental_data
from modules.errors.__error__ import get_bfd
from modules.moga.objective import Objective
from modules.moga.problem import Problem
from modules.moga.moga import MOGA
from modules.recorder import Recorder
from modules.models.__model_factory__ import get_model
from modules.errors.__error_factory__ import get_error_list
from modules.constraints.__constraint_factory__ import get_constraint_list
from modules.helper.progressor import Progressor
from modules.helper.plotter import Plotter
from modules.helper.general import safe_mkdir

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

        # Initialise paths
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_dir  = self.output_dir if title == "" else f"{self.output_dir} ({title})"
        self.output_path = "{}/{}".format(RESULTS_DIR, self.output_dir)
        self.csv_path    = "{}/{}".format(self.output_path, "moga")

        # Set up environment
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)
    
    # Reads in the experimental data
    def read_data(self, file_names):
        self.prog.add(f"Reading experimental data from {len(file_names)} files")
        file_paths = [f"{INPUT_DIR}/{file_name}" for file_name in file_names]
        self.exp_curves = read_experimental_data(file_paths)

    # Removes data past the minimum rate value
    def remove_damage(self):
        self.prog.add("Removing creep damage")
        for i in range(len(self.exp_curves)):
            _, exp_y_fd = get_bfd(self.exp_curves[i]["x"], self.exp_curves[i]["y"])
            min_index = exp_y_fd.index(min(exp_y_fd))
            self.exp_curves[i]["x"] = [self.exp_curves[i]["x"][j] for j in range(min_index)]
            self.exp_curves[i]["y"] = [self.exp_curves[i]["y"][j] for j in range(min_index)]

    # Initialising the model
    def define_model(self, model_name, args=[]):
        self.prog.add("Defining the model")
        self.model = get_model(model_name, self.exp_curves, args)
    
    # Defining the errors
    def define_errors(self, error_names):
        self.prog.add("Defining the errors to minimise")
        self.error_list = get_error_list(error_names, self.exp_curves)

    # Defining the constraints
    def define_constraints(self, constraint_names):
        self.prog.add("Defining the constraints to adhere")
        self.constraint_list = get_constraint_list(constraint_names, self.exp_curves)

    # Prepares the recorder
    def define_recorder(self, interval=10, population=10):
        self.prog.add("Preparing the results recorder")
        self.objective = Objective(self.model, self.error_list, self.constraint_list)
        self.recorder = Recorder(self.objective, self.exp_curves, self.csv_path, interval, population)

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
        plotter = Plotter(self.output_path)
        plotter.scat_plot(self.exp_curves)
        prd_curves = self.model.get_prd_curves(*params)
        plotter.line_plot(prd_curves)
        plotter.save_plot()

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
