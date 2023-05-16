"""
 Title:         Recorder
 Description:   For recording results periodically
 Author:        Janzen Choi

"""

# Libraries
import time, math, sys
import pandas as pd
from modules.moga.objective import BIG_VALUE, Objective

# Helper libraries
import sys; sys.path += ["../__common__"]
from derivative import differentiate_curve

# Constants
CURVE_DENSITY = 500

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, objective:Objective, train_curves:list[dict], test_curves:list[dict], path:str, interval:int, population:int):

        # Initialise
        self.model            = objective.get_model()
        self.train_curves     = train_curves
        self.test_curves      = test_curves
        self.path             = path
        self.interval         = interval
        self.population       = population

        # Define errors
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

    # Returns a writer object
    def write_results(self, file_path:str) -> None:
        writer = pd.ExcelWriter(file_path, engine = "xlsxwriter")
        self.record_settings(writer)
        self.record_results(writer)
        all_types = list(set([curve["type"] for curve in self.train_curves + self.test_curves]))
        for type in all_types:
            self.record_plot(writer, type)
        writer.close()

    # Updates the results after X iterations
    def update_results(self, params:list[float], errors:list[float]) -> None:

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
            self.write_results(file_path)

            # Display progress in console
            progress = f"{num_gens_completed_padded}/{self.num_gens}"
            index = round(self.num_gens_completed//self.interval)
            print(f"  {index}]\tRecorded ({progress} in {update_duration}s)")
    
    # Updates the population
    def update_population(self, params:tuple[float], errors:tuple[float]) -> None:
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

    # Records the settings
    def record_settings(self, writer:pd.ExcelWriter):
        unfixed_params = self.model.get_unfixed_param_info()
        curr_time = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        settings = {
            "Progress":           [f"{round(self.num_gens_completed)}/{self.num_gens}"],
            "Start / End Time":   [self.start_time_str, curr_time],
            "Model":              [self.model.get_name()],
            "Fixed Parameters":   list(self.model.fixed_params.keys()),
            "Fixed Values":       list(self.model.fixed_params.values()),
            "Unfixed Parameters": [param["name"] for param in unfixed_params],
            "Unfixed Bounds":     [f"[{param['min']}, {param['max']}]" for param in unfixed_params],
            "Errors":             self.error_info,
            "Training Data":      [f"{train_curve['file_path']}" for train_curve in self.train_curves],
            "Testing Data":       [f"{test_curve['file_path']}" for test_curve in self.test_curves],
            "Hyperparameters":    self.moga_summary,
        }
        write_with_fit_column_widths(settings, writer, "settings")
    
    # Records the results
    def record_results(self, writer:pd.ExcelWriter):
        results = {}
        
        # Add parameters
        param_info = self.model.get_unfixed_param_info()
        for i in range(len(param_info)):
            results[param_info[i]["name"]] = [params[i] for params in self.opt_params]
        
        # Add errors (and total error)
        if len(self.error_names) > 0:
            results["|"] = ["|" for _ in range(len(self.opt_errors))]
        for i in range(len(self.error_names)):
            error_id = f"{self.error_names[i]}_{self.error_types[i]}"
            results[error_id] = [errors[i] for errors in self.opt_errors]
        results["error_sqr_sum"] = [errors[-1] for errors in self.opt_errors]
        
        # Write all results
        write_with_fit_column_widths(results, writer, "results")

    # Records the plot
    def record_plot(self, writer:pd.ExcelWriter, type:str):

        # If there are no optimal parameters / curves, leave
        if len(self.opt_params) == 0 or not type in [curve["type"] for curve in self.train_curves+self.test_curves]:
            return
        
        # Create plot for curves
        test_curves = [curve for curve in self.test_curves if curve["type"] == type]
        train_curves = [curve for curve in self.train_curves if curve["type"] == type]
        prd_test_curves = self.model.get_specified_prd_curves(self.opt_params[0], test_curves)
        prd_train_curves = self.model.get_specified_prd_curves(self.opt_params[0], train_curves)
        add_plot_sheet(writer, f"{type}_y", test_curves, train_curves, prd_test_curves, prd_train_curves)

        # Create plot for derivative of curves
        test_d_curves       = [differentiate_curve(curve) for curve in test_curves]
        train_d_curves      = [differentiate_curve(curve) for curve in train_curves]
        prd_test_curves     = self.model.get_specified_prd_curves(self.opt_params[0], test_curves)
        prd_test_d_curves   = [differentiate_curve(curve) for curve in prd_test_curves]
        prd_train_curves    = self.model.get_specified_prd_curves(self.opt_params[0], train_curves)
        prd_train_d_curves  = [differentiate_curve(curve) for curve in prd_train_curves]
        add_plot_sheet(writer, f"{type}_dy", test_d_curves, train_d_curves, prd_test_d_curves, prd_train_d_curves)

# For creating a sheet for a plot
def add_plot_sheet(writer:pd.ExcelWriter, sheet_name:str, test_curves:list[dict], train_curves:list[dict], prd_test_curves:list[dict], prd_train_curves:list[dict]):
    
    # Flatten data
    test_x_flat, test_y_flat = thin_and_flatten(test_curves)
    train_x_flat, train_y_flat = thin_and_flatten(train_curves)
    prd_test_x_flat, prd_test_y_flat = thin_and_flatten(prd_test_curves)
    prd_train_x_flat, prd_train_y_flat = thin_and_flatten(prd_train_curves)
    prd_x_flat = prd_test_x_flat + prd_train_x_flat
    prd_y_flat = prd_test_y_flat + prd_train_y_flat

    # Write the data
    data = zip_longest([test_x_flat, test_y_flat, train_x_flat, train_y_flat, prd_x_flat, prd_y_flat])
    data = list(map(list, zip(*data)))
    pd.DataFrame(data).to_excel(writer, sheet_name, index=False)
    sheet = writer.sheets[sheet_name]
    chart = writer.book.add_chart({"type": "scatter"})

    # Add curves to chart
    add_series(chart, sheet_name, "Testing", 0, len(test_x_flat), "circle", 5, "silver")
    add_series(chart, sheet_name, "Training", 2, len(train_x_flat), "circle", 5, "gray")
    add_series(chart, sheet_name, "Predicted", 4, len(prd_x_flat), "circle", 2, "red")

    # Insert chart into worksheet
    chart.set_x_axis({"name": "x", "major_gridlines": {"visible": True}})
    chart.set_y_axis({"name": "y", "major_gridlines": {"visible": True}})
    sheet.insert_chart("A1", chart)

# For adding series to a chart
def add_series(chart, sheet_name:str, series_name:str, col_num:int, curve_length:float, type:str, size:float, colour:str):
    if curve_length > 0:
        chart.add_series({
            "name":       series_name,
            "categories": [sheet_name, 1, col_num, curve_length, col_num],
            "values":     [sheet_name, 1, col_num+1, curve_length, col_num+1],
            "marker":     {"type": type, "size": size, "border": {"color": colour}, "fill": {"color": colour}}
        })

# For thinning and flattening data
def thin_and_flatten(curves:list[dict]):
    x_data = [get_thinned_list(curve["x"]) for curve in curves]
    y_data = [get_thinned_list(curve["y"]) for curve in curves]
    x_data_flat = [x for x_list in x_data for x in x_list]
    y_data_flat = [y for y_list in y_data for y in y_list]
    return x_data_flat, y_data_flat

# For writing to a sheet with fitted column widths
def write_with_fit_column_widths(data_dict:dict, writer:pd.ExcelWriter, sheet_name:str):

    # Convert dictionary to dataframe
    columns = list(data_dict.keys())
    data = zip_longest([data_dict[column] for column in columns])
    data = list(map(list, zip(*data)))
    dataframe = pd.DataFrame(data, columns = columns)
    
    # Apply fit column widths
    dataframe.style.apply(centre_align, axis=0).to_excel(writer, sheet_name, index = False)
    sheet = writer.sheets[sheet_name]
    for column in dataframe:
        column_length = max(dataframe[column].astype(str).map(len).max(), len(column)) + 1
        column_index = dataframe.columns.get_loc(column)
        sheet.set_column(column_index, column_index, column_length)

# For centre-aligning the cellss
def centre_align(x:float):
    return ["text-align: center" for _ in x]

# Returns a thinned list
def get_thinned_list(unthinned_list:list[int]):
    src_data_size = len(unthinned_list)
    step_size = src_data_size / CURVE_DENSITY
    thin_indexes = [math.floor(step_size*i) for i in range(1, CURVE_DENSITY - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Imitates zip longest but for a list of lists
def zip_longest(list_list:list[dict]):
    max_values = max([len(list) for list in list_list])
    new_list_list = []
    for list in list_list:
        new_list = list + [None] * (max_values - len(list))
        new_list_list.append(new_list)
    return new_list_list