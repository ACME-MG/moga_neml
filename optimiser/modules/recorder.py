"""
 Title:         Recorder
 Description:   For recording results periodically
 Author:        Janzen Choi

"""

# Libraries
import time, math, sys
import pandas as pd
from modules.moga.objective import BIG_VALUE

# Helper libraries
sys.path += ["../__common__"]
from derivative import differentiate_curve

# Constants
CURVE_DENSITY = 100

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, objective, train_curves, test_curves, path, interval, population):

        # Initialise
        self.model            = objective.get_model()
        self.error_names      = objective.get_error_names()
        self.constraint_names = objective.get_constraint_names()
        self.train_curves     = train_curves
        self.test_curves      = test_curves
        self.path             = path
        self.interval         = interval
        self.population       = population

        # Track optimisation progress
        self.start_time = time.time()
        self.update_time = self.start_time
        self.start_time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        self.num_evals_completed, self.num_gens_completed = 0, 0
        self.opt_params, self.opt_errors, self.opt_constraints = [], [], []

    # Define MOGA hyperparameters
    def define_hyperparameters(self, num_gens, init_pop, offspring, crossover, mutation):
        self.num_gens   = num_gens
        self.init_pop   = init_pop
        self.offspring  = offspring
        self.crossover  = crossover
        self.mutation   = mutation

    # Updates the results after X iterations
    def update_results(self, params, errors, constraints):

        # Update optimisation progress
        self.num_evals_completed += 1
        self.num_gens_completed = (self.num_evals_completed - self.init_pop) / self.offspring + 1
        
        # If parameters are valid, update the population
        if not BIG_VALUE in errors:
            self.update_population(params, errors, constraints)

        # Record results after X generations
        if self.num_gens_completed > 0 and self.num_gens_completed % self.interval == 0:

            # Get time since previous update in seconds
            current_time = time.time()
            update_duration = round(current_time - self.update_time)
            self.update_time = current_time

            # Prepare CSV output
            num_gens_completed_padded = str(round(self.num_gens_completed)).zfill(len(str(self.num_gens)))
            file_path = f"{self.path}_{num_gens_completed_padded} ({update_duration}s).xlsx"

            # Write to CSV
            writer = pd.ExcelWriter(file_path, engine = "xlsxwriter")
            self.record_settings(writer)
            self.record_results(writer)
            self.record_plot(writer)
            writer.save()

            # Display progress in console
            progress = f"{num_gens_completed_padded}/{self.num_gens}"
            index = round(self.num_gens_completed//self.interval)
            print(f"  {index}]\tRecorded ({progress} in {update_duration}s)")
    
    # Updates the population
    def update_population(self, params, errors, constraints):
        params, errors = list(params), list(errors)
        constraints = [constraint <= 0 for constraint in constraints]
        err_sqr_sum = sum([error**2 for error in errors])

        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == self.population:
            if self.opt_errors[-1][-1] < err_sqr_sum:
                return
            self.opt_params.pop()
            self.opt_errors.pop()
            self.opt_constraints.pop()
        
        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if err_sqr_sum < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, errors + [err_sqr_sum])
                self.opt_constraints.insert(i, constraints)
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(errors + [err_sqr_sum])
            self.opt_constraints.append(constraints)

    # Records the settings
    def record_settings(self, writer):

        # Settings Data
        settings = {
            "Status":               ["Complete" if self.num_gens_completed == self.num_gens else "Incomplete"],
            "Progress":             [f"{round(self.num_gens_completed)}/{self.num_gens}"],
            "Start Time":           [self.start_time_str],
            "End Time":             [time.strftime("%A, %D, %H:%M:%S", time.localtime())],
            "Time Elapsed":         [f"{round(time.time() - self.start_time)}s"],
            "Model":                [self.model.get_name()],
            "Params":               self.model.get_param_names(),
            "Lower Bound":          self.model.get_param_lower_bounds(),
            "Upper Bound":          self.model.get_param_upper_bounds(),
            "Errors":               self.error_names,
            "Constraints":          self.constraint_names,
            "Training Data":        [f"{train_curve['temp']}/{train_curve['stress']}" for train_curve in self.train_curves],
            "Testing Data":         [f"{test_curve['temp']}/{test_curve['stress']}" for test_curve in self.test_curves],
            "num_gens":             [self.num_gens],
            "init_pop":             [self.init_pop],
            "offspring":            [self.offspring],
            "crossover":            [self.crossover],
            "mutation":             [self.mutation],
        }

        # Change format of data
        columns = list(settings.keys())
        data = zip_longest([settings[column] for column in columns])
        data = list(map(list, zip(*data)))
        settings_dataframe = pd.DataFrame(data, columns = columns)

        # Write settings
        settings_dataframe.style.apply(centre_align, axis = 0).to_excel(writer, "settings", index = False)
        sheet = writer.sheets["settings"]
        for column in settings_dataframe:
            column_length = max(settings_dataframe[column].astype(str).map(len).max(), len(column)) + 1
            column_index = settings_dataframe.columns.get_loc(column)
            sheet.set_column(column_index, column_index, column_length)
    
    # Records the results
    def record_results(self, writer):
        columns = [param["name"] for param in self.model.param_info] + self.error_names + ["err_sqr_sum"] + self.constraint_names
        data = [self.opt_params[i] + self.opt_errors[i] + self.opt_constraints[i] for i in range(0,len(self.opt_params))]
        results = pd.DataFrame(data, columns = columns)
        results.to_excel(writer, "results", index = False)

    # Records the plot
    def record_plot(self, writer):

        # If there are no optimal parameters, leave
        if len(self.opt_params) == 0:
            return
        
        # Create plot for curves
        prd_test_curves = self.model.get_specified_prd_curves(self.opt_params[0], self.test_curves)
        prd_train_curves = self.model.get_specified_prd_curves(self.opt_params[0], self.train_curves)
        add_plot_sheet(writer, "plot_y", self.test_curves, self.train_curves, prd_test_curves, prd_train_curves)

        # Create plot for derivative of curves
        test_d_curves       = [differentiate_curve(curve) for curve in self.test_curves]
        train_d_curves      = [differentiate_curve(curve) for curve in self.train_curves]
        prd_test_curves     = self.model.get_specified_prd_curves(self.opt_params[0], self.test_curves)
        prd_test_d_curves   = [differentiate_curve(curve) for curve in prd_test_curves]
        prd_train_curves    = self.model.get_specified_prd_curves(self.opt_params[0], self.train_curves)
        prd_train_d_curves  = [differentiate_curve(curve) for curve in prd_train_curves]
        add_plot_sheet(writer, "plot_dy", test_d_curves, train_d_curves, prd_test_d_curves, prd_train_d_curves)

# For creating a sheet for a plot
def add_plot_sheet(writer, sheet_name, test_curves, train_curves, prd_test_curves, prd_train_curves):
    
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
    worksheet = writer.sheets[sheet_name]
    chart = writer.book.add_chart({"type": "scatter"})

    # Add curves to chart
    add_series(chart, sheet_name, "Testing", 0, len(test_x_flat), "circle", 5, "silver")
    add_series(chart, sheet_name, "Training", 2, len(train_x_flat), "circle", 5, "gray")
    add_series(chart, sheet_name, "Predicted", 4, len(prd_x_flat), "circle", 2, "red")

    # Insert chart into worksheet
    chart.set_x_axis({"name": "x", "major_gridlines": {"visible": True}})
    chart.set_y_axis({"name": "y", "major_gridlines": {"visible": True}})
    worksheet.insert_chart("A1", chart)

# For adding series to a chart
def add_series(chart, sheet_name, series_name, col_num, curve_length, type, size, colour):
    if curve_length > 0:
        chart.add_series({
            "name":       series_name,
            "categories": [sheet_name, 1, col_num, curve_length, col_num],
            "values":     [sheet_name, 1, col_num+1, curve_length, col_num+1],
            "marker":     {"type": type, "size": size, "border": {"color": colour}, "fill": {"color": colour}}
        })

# For thinning and flattening data
def thin_and_flatten(curves):
    x_data = [get_thinned_list(curve["x"]) for curve in curves]
    y_data = [get_thinned_list(curve["y"]) for curve in curves]
    x_data_flat = [x for x_list in x_data for x in x_list]
    y_data_flat = [y for y_list in y_data for y in y_list]
    return x_data_flat, y_data_flat

# For centre-aligning the cellss
def centre_align(x):
    return ["text-align: center" for _ in x]

# Returns a thinned list
def get_thinned_list(unthinned_list):
    src_data_size = len(unthinned_list)
    step_size = src_data_size / CURVE_DENSITY
    thin_indexes = [math.floor(step_size*i) for i in range(1, CURVE_DENSITY - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Imitates zip longest but for a list of lists
def zip_longest(list_list):
    max_values = max([len(list) for list in list_list])
    new_list_list = []
    for list in list_list:
        new_list = list + [None] * (max_values - len(list))
        new_list_list.append(new_list)
    return new_list_list