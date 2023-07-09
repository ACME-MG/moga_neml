"""
 Title:         Recorder
 Description:   For recording results periodically
 Author:        Janzen Choi

"""

# Libraries
import time
from moga_neml._interface.spreadsheet import Spreadsheet
from moga_neml._maths.curve import  get_thinned_list
from moga_neml._maths.experiment import DATA_DENSITY, DATA_FIELD_PLOT_MAP, DATA_UNITS
from moga_neml._optimise.controller import Controller

# The Recorder class
class Recorder:
    
    # Constructor
    def __init__(self, controller:Controller, interval:int, population:int, result_path:str):
        
        # Initialise inputs
        self.controller  = controller
        self.interval    = interval
        self.result_path = result_path
        self.population  = population
        
        # Initialise internal variables
        self.curve_list          = controller.get_curve_list()
        self.num_evals_completed = 0
        self.num_gens_completed  = 0
        self.start_time          = time.time()
        self.update_time         = self.start_time
        self.start_time_str      = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        
        # Get parameter information
        param_dict      = self.controller.get_model().get_param_dict()
        fix_param_dict  = self.controller.get_fix_param_dict()
        init_param_dict = self.controller.get_init_param_dict()
        
        # Summarise parameter information
        self.param_info_list = []
        for param_name in param_dict.keys():
            param_info = param_name
            if param_name in fix_param_dict.keys():
                param_info += " (fixed={:0.4})".format(float(fix_param_dict[param_name]))
            elif param_name in init_param_dict.keys():
                param_info += " (init={:0.4})".format(float(init_param_dict[param_name]["value"]))
            self.param_info_list.append(param_info)
        
        # Summarise parameter bound information
        self.param_bound_info_list = []
        for param_name in param_dict.keys():
            l_bound = float(param_dict[param_name]["l_bound"])
            u_bound = float(param_dict[param_name]["u_bound"])
            self.param_bound_info_list.append("[{:0.4}, {:0.4}]".format(l_bound, u_bound))
        
        # Summarise data information
        self.data_info_list = []
        for curve in self.curve_list:
            status = "training" if curve.get_train() else "validation"
            data_info = "{} ({})".format(curve.get_exp_data()["file_name"], status)
            self.data_info_list.append(data_info)
        
        # Initialise optimal solution
        self.optimal_solution_list = []
    
    # Define MOGA hyperparameters
    def define_hyperparameters(self, num_gens:int, init_pop:int, offspring:int, crossover:float, mutation:float) -> None:
        self.num_gens  = num_gens
        self.init_pop  = init_pop
        self.offspring = offspring
        hp_names = ["num_gens", "init_pop", "offspring", "crossover", "mutation"]
        hp_values = [num_gens, init_pop, offspring, crossover, mutation]
        self.moga_summary = [f"{hp_names[i]} ({hp_values[i]})" for i in range(len(hp_names))]
    
    # Updates the population
    def update_optimal_solution(self, param_dict:dict, objective_dict:dict):
        
        
        # Get the solution
        reduction_method = self.controller.get_objective_reduction_method()
        objective_values = list(objective_dict.values())
        reduced_value = self.controller.reduce_objectives(objective_values)
        solution = {"params": param_dict, "objectives": objective_dict, reduction_method: reduced_value}
        
        # If the stored parameters exceed the limit, remove the worst
        if len(self.optimal_solution_list) == self.population:
            if self.optimal_solution_list[-1][reduction_method] < solution[reduction_method]:
                return
            self.optimal_solution_list.pop()
        
        # Adds new solution in order
        for i in range(len(self.optimal_solution_list)):
            if solution[reduction_method] < self.optimal_solution_list[i][reduction_method]:
                self.optimal_solution_list.insert(i, solution)
                return
        self.optimal_solution_list.append(solution)
    
    # Updates the results after a MOGA iteration
    def update_iteration(self, param_dict:dict, objective_dict:dict):
        
        # Update optimisation progress
        print() if self.num_evals_completed == 0 else None
        self.num_evals_completed += 1
        self.num_gens_completed = (self.num_evals_completed - self.init_pop) / self.offspring + 1
        self.update_optimal_solution(param_dict, objective_dict)
        
        # Record results after X generations
        if self.num_gens_completed > 0 and self.num_gens_completed % self.interval == 0:
            
            # Get time since previous update in seconds
            current_time = time.time()
            update_duration = round(current_time - self.update_time)
            self.update_time = current_time

            # Display output
            num_gens_completed_padded = str(round(self.num_gens_completed)).zfill(len(str(self.num_gens)))
            file_path = f"{self.result_path}_{num_gens_completed_padded} ({update_duration}s).xlsx"
            self.create_record(file_path)

            # Display progress in console
            progress = f"{num_gens_completed_padded}/{self.num_gens}"
            index = round(self.num_gens_completed//self.interval)
            print(f"      {index}]\tRecorded ({progress} in {update_duration}s)")
        
    # Gets the optimisation summary
    def get_summary_dict(self):
        return {
            "Progress":     [f"{round(self.num_gens_completed)}/{self.num_gens}"],
            "Start / End":  [self.start_time_str, time.strftime("%A, %D, %H:%M:%S", time.localtime())],
            "Model":        [self.controller.get_model().get_name()],
            "Params":       self.param_info_list,
            "Bounds":       self.param_bound_info_list,
            "Experimental Data": self.data_info_list,
            "Objectives":   self.controller.get_objective_info_list(),
            "MOGA Summary": self.moga_summary,
        }
    
    # Gets a dictionary of the optimisation results
    def get_result_dict(self) -> dict:
        
        # Initialise
        results = {}
        sf_format = lambda x : float("{:0.5}".format(float(x)))
        
        # Add parameter information
        unfix_param_names = list(self.controller.get_unfix_param_dict().keys())
        for param_name in unfix_param_names:
            results[param_name] = [sf_format(o_sol["params"][param_name]) for o_sol in self.optimal_solution_list]
        
        # Add objective information
        objective_info_list = self.controller.get_objective_info_list()
        for objective_info in objective_info_list:
            results[objective_info] = [sf_format(o_sol["objectives"][objective_info]) for o_sol in self.optimal_solution_list]
        
        # Reduce objective values and return
        reduction_method = self.controller.get_objective_reduction_method()
        results[reduction_method] = [sf_format(o_sol[reduction_method]) for o_sol in self.optimal_solution_list]
        return results
    
    # Gets the curves for a curve type
    #   Returns None if predicted data is invalid
    def get_plot_dict(self, type:str, x_label:str, y_label:str) -> dict:

        # If there are no optimal parameters, leave
        if len(self.optimal_solution_list) == 0:
            return
        optimal_solution = self.optimal_solution_list[0]
        
        # Initialise data structure
        train_dict = {"exp_x": [], "exp_y": [], "prd_x": [], "prd_y": []}
        valid_dict = {"exp_x": [], "exp_y": [], "prd_x": [], "prd_y": []}
        
        # Get the experimental training and validation data
        for curve in self.curve_list:
            
            # Ignore data not of desired type
            if curve.get_type() != type:
                continue
            
            # Get experimental data and thin
            exp_data = curve.get_exp_data()
            exp_x_list, exp_y_list = process_data_dict(exp_data, x_label, y_label)
            
            # Get predicted data and thin
            opt_params = optimal_solution["params"].values()
            prd_data = self.controller.get_prd_data(curve, *opt_params)
            if prd_data == None:
                return None
            prd_x_list, prd_y_list = process_data_dict(prd_data, x_label, y_label)
            
            # Add to data structure
            data_dict = train_dict if curve.get_train() else valid_dict
            data_dict["exp_x"] += exp_x_list
            data_dict["exp_y"] += exp_y_list
            data_dict["prd_x"] += prd_x_list
            data_dict["prd_y"] += prd_y_list

        # Prepare dict for plotting data
        plot_dict = {}
        if train_dict["exp_x"] != []:
            plot_dict["training"] = {"x": train_dict["exp_x"], "y": train_dict["exp_y"], "size": 5, "colour": "silver"}
        if valid_dict["exp_x"] != []:
            plot_dict["validation"] = {"x": valid_dict["exp_x"], "y": valid_dict["exp_y"], "size": 5, "colour": "gray"}
        all_x = train_dict["prd_x"] + valid_dict["prd_x"]
        all_y = train_dict["prd_y"] + valid_dict["prd_y"]
        plot_dict["prediction"] = {"x": all_x , "y": all_y, "size": 2, "colour": "red"}
        return plot_dict

    # Returns a writer object
    def create_record(self, file_path:str, type_list:list=None, in_x_label:str=None, in_y_label:str=None) -> None:
        
        # Get summary and results
        spreadsheet = Spreadsheet(file_path)
        spreadsheet.write_data(self.get_summary_dict(), "summary")
        spreadsheet.write_data(self.get_result_dict(), "results")

        # Gets all the types if necessary
        all_types = list(set([curve.get_type() for curve in self.curve_list]))
        type_list = all_types if type_list == None else type_list

        # Get plots
        for type in type_list:
            x_label = DATA_FIELD_PLOT_MAP[type]["x"] if in_x_label == None else in_x_label
            y_label = DATA_FIELD_PLOT_MAP[type]["y"] if in_y_label == None else in_y_label
            plot_dict = self.get_plot_dict(type, x_label, y_label)
            if plot_dict == None:
                continue
            spreadsheet.write_plot(
                data_dict_dict = plot_dict,
                sheet_name     = f"plot_{type}",
                x_label        = f"{x_label} ({DATA_UNITS[x_label]})",
                y_label        = f"{y_label} ({DATA_UNITS[y_label]})",
                plot_type      = "scatter"
            )
        spreadsheet.close()

# For thinning data
def process_data_dict(data_dict:dict, x_label:str, y_label:str) -> tuple:
    data_dict[x_label] = get_thinned_list(data_dict[x_label], DATA_DENSITY)
    data_dict[y_label] = get_thinned_list(data_dict[y_label], DATA_DENSITY)
    return data_dict[x_label], data_dict[y_label]
