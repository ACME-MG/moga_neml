"""
 Title:         Recorder
 Description:   For recording results periodically
 Author:        Janzen Choi

"""

# Libraries
import time
from moga_neml._optimise.objective import BIG_VALUE, Objective
from moga_neml._interface.spreadsheet import Spreadsheet
from moga_neml._maths.general import DATA_LABELS, DATA_UNITS, get_thinned_list

# Constants
CURVE_DENSITY = 100

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, objective:Objective, path:str, interval:int, population:int):

        # Initialise
        self.objective    = objective
        self.train_curves = self.objective.get_exp_curves("train")
        self.test_curves  = self.objective.get_exp_curves("test")
        self.all_types    = list(set([curve["type"] for curve in self.train_curves+self.test_curves]))
        self.path         = path
        self.interval     = interval
        self.population   = population

        # Define parameter information
        fixed_params = self.objective.get_fixed_params()
        self.fixed_param_info = [f"{param_name} ({fixed_params[param_name]})"
                                 for param_name in self.objective.get_fixed_params().keys()]
        self.unfixed_param_info = ["{} ([{:0.3}, {:0.3}])".format(param["name"], param["min"], param["max"])
                                   for param in self.objective.get_unfixed_param_info()]

        # Define error information
        self.error_names   = objective.get_error_names()
        self.error_types   = objective.get_error_types()
        self.error_weights = objective.get_error_weights()
        self.error_info = [f"{self.error_names[i]} ({self.error_types[i]}) ({self.error_weights[i]})" for i in range(len(self.error_names))]

        # Track optimisation progress
        self.start_time = time.time()
        self.update_time = self.start_time
        self.start_time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        self.num_evals_completed, self.num_gens_completed = 0, 0
        self.opt_params, self.opt_errors = [], []

    # Define MOGA hyperparameters
    def define_hyperparameters(self, num_gens:int, init_pop:int, offspring:int, crossover:float, mutation:float) -> None:
        self.num_gens  = num_gens
        self.init_pop  = init_pop
        self.offspring = offspring
        self.crossover = crossover
        self.mutation  = mutation
        hp_names = ["num_gens", "init_pop", "offspring", "crossover", "mutation"]
        hp_values = [num_gens, init_pop, offspring, crossover, mutation]
        self.moga_summary = [f"{hp_names[i]} ({hp_values[i]})" for i in range(len(hp_names))]

    # Updates the results after X iterations
    def update_results(self, params:list, errors:list) -> None:

        # Update optimisation progress
        self.num_evals_completed += 1
        self.num_gens_completed = (self.num_evals_completed - self.init_pop) / self.offspring + 1
        
        # If parameters are valid, update the population
        if not BIG_VALUE in errors:
            self.update_population(params, errors)

        # Record results after X generations
        if self.num_gens_completed > 0 and self.num_gens_completed % self.interval == 0:

            # Get time since previous update in seconds
            current_time = time.time()
            update_duration = round(current_time - self.update_time)
            self.update_time = current_time

            # Display output
            num_gens_completed_padded = str(round(self.num_gens_completed)).zfill(len(str(self.num_gens)))
            file_path = f"{self.path}_{num_gens_completed_padded} ({update_duration}s).xlsx"
            self.create_record(file_path)

            # Display progress in console
            progress = f"{num_gens_completed_padded}/{self.num_gens}"
            index = round(self.num_gens_completed//self.interval)
            print(f"  {index}]\tRecorded ({progress} in {update_duration}s)")
    
    # Updates the population
    def update_population(self, params:tuple, errors:tuple) -> None:
        params, errors = list(params), list(errors)
        err_sqr_sum = sum([error**2 for error in errors])

        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == self.population:
            if self.opt_errors[-1][-1] < err_sqr_sum:
                return
            self.opt_params.pop()
            self.opt_errors.pop()
        
        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if err_sqr_sum < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, errors + [err_sqr_sum])
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(errors + [err_sqr_sum])

    # Returns a dictionary of optimisation summary
    def get_summary(self) -> dict:
        return {
            "Progress":       [f"{round(self.num_gens_completed)}/{self.num_gens}"],
            "Start / End":    [self.start_time_str, time.strftime("%A, %D, %H:%M:%S", time.localtime())],
            "Model":          [self.objective.get_model_name()],
            "Fixed Params":   self.fixed_param_info,
            "Unfixed Params": self.unfixed_param_info,
            "Errors":         self.error_info,
            "Training Data":  [f"{train_curve['file_path']}" for train_curve in self.train_curves],
            "Testing Data":   [f"{test_curve['file_path']}" for test_curve in self.test_curves],
            "Hyperparams":    self.moga_summary,
        }

    # Gets a dictionary of the optimisation results
    def get_results(self) -> dict:
        
        # Initialise
        results = {}
        sf_format = lambda x : float("{:0.3}".format(float(x)))
        param_info = self.objective.get_unfixed_param_info()
        
        # Add parameters and errors
        for i in range(len(param_info)):
            results[param_info[i]["name"]] = [sf_format(params[i]) for params in self.opt_params]
        for i in range(len(self.error_names)):
            results[self.error_info[i]] = [sf_format(errors[i]) for errors in self.opt_errors]
        
        # Add total error and return
        results["sqr_sum"] = [sf_format(errors[-1]) for errors in self.opt_errors]
        return results

    # Gets the curves for a curve type
    def get_curves(self, type:str) -> dict:

        # If there are no optimal parameters / curves, leave
        if len(self.opt_params) == 0 or not type in self.all_types:
            return
        
        # Otherwise, get the curves
        test_curves = [curve for curve in self.test_curves if curve["type"] == type]
        train_curves = [curve for curve in self.train_curves if curve["type"] == type]
        prd_test_curves = self.objective.get_prd_curves(["test"], type, *self.opt_params[0])
        prd_train_curves = self.objective.get_prd_curves(["train"], type, *self.opt_params[0])
        
        # Flatten the curves
        test_x_flat, test_y_flat = thin_and_flatten(test_curves)
        train_x_flat, train_y_flat = thin_and_flatten(train_curves)
        prd_test_x_flat, prd_test_y_flat = thin_and_flatten(prd_test_curves)
        prd_train_x_flat, prd_train_y_flat = thin_and_flatten(prd_train_curves)
        prd_x_flat = prd_test_x_flat + prd_train_x_flat
        prd_y_flat = prd_test_y_flat + prd_train_y_flat
        
        # Create dictionary
        data_dict = {}
        if test_x_flat != []:
            data_dict["testing"]   = {"x": test_x_flat,  "y": test_y_flat,  "size": 5, "colour": "silver"}
        if train_x_flat != []:
            data_dict["training"]  = {"x": train_x_flat, "y": train_y_flat, "size": 5, "colour": "gray"}
        if prd_x_flat != []:
            data_dict["predicted"] = {"x": prd_x_flat,   "y": prd_y_flat,   "size": 3, "colour": "red"}
        return data_dict

    # Returns a writer object
    def create_record(self, file_path:str) -> None:
        
        # Get record information
        spreadsheet = Spreadsheet(file_path)
        summary = self.get_summary()
        spreadsheet.write_data(summary, "summary")
        results = self.get_results()
        spreadsheet.write_data(results, "results")
        for type in self.all_types:
            curves = self.get_curves(type)
            if curves == None:
                continue
            x_label = DATA_LABELS[type]["x"]
            y_label = DATA_LABELS[type]["y"]
            spreadsheet.write_plot(
                data_dict_dict = curves,
                sheet_name     = f"plot_{type}",
                x_label        = f"{x_label} ({DATA_UNITS[x_label]})",
                y_label        = f"{y_label} ({DATA_UNITS[y_label]})",
                plot_type      = "scatter"
            )
        spreadsheet.close()

# For thinning and flattening data
def thin_and_flatten(curves:list) -> tuple:
    x_data = [get_thinned_list(curve["x"], CURVE_DENSITY) for curve in curves]
    y_data = [get_thinned_list(curve["y"], CURVE_DENSITY) for curve in curves]
    x_data_flat = [x for x_list in x_data for x in x_list]
    y_data_flat = [y for y_list in y_data for y in y_list]
    return x_data_flat, y_data_flat
