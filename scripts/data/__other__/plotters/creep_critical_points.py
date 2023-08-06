# Libraries
import matplotlib.pyplot as plt
import math
from copy import deepcopy
from scipy.interpolate import splev, splrep, splder

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list, y_list, resolution=50, smooth=False):
        thin_x_list = get_thinned_list(x_list, resolution)
        thin_y_list = get_thinned_list(y_list, resolution)
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(thin_x_list, thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self):
        self.spl = splder(self.spl)

    # Evaluate
    def evaluate(self, x_list):
        return list(splev(x_list, self.spl))

# For differentiating a curve
def differentiate_curve(curve, x_label, y_label):
    curve = deepcopy(curve)
    interpolator = Interpolator(curve[x_label], curve[y_label])
    interpolator.differentiate()
    curve[y_label] = interpolator.evaluate(curve[x_label])
    return curve

# Returns a thinned list
def get_thinned_list(unthinned_list:list, density:int) -> list:
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Tries to float cast a value
def try_float_cast(value:str) -> float:
    try:
        return float(value)
    except:
        return value

# Converts CSV data into a curve dict
def get_curve_dict(headers:list, data:list) -> dict:
    
    # Get indexes of data
    list_indexes = [i for i in range(len(data[2])) if data[2][i] != ""]
    info_indexes = [i for i in range(len(data[2])) if data[2][i] == ""]
    
    # Create curve
    curve = {}
    for index in list_indexes:
        value_list = [float(d[index]) for d in data]
        value_list = get_thinned_list(value_list, 200)
        curve[headers[index]] = value_list
    for index in info_indexes:
        curve[headers[index]] = try_float_cast(data[0][index])

    # Return curve
    return curve

# File names
file_path_list = [
    # "data/creep/inl_1/AirBase_900_36_G22.csv",
    "data/creep/inl_1/AirBase_900_31_G50.csv",
    # "data/creep/inl_1/AirBase_900_28_G45.csv",
    # "data/creep/inl_1/AirBase_900_26_G59_unox.csv",
]

# Iterate through curves
for file_path in file_path_list:

    # Read file
    with open(file_path, "r") as file:
        headers = file.readline().replace("\n","").split(",")
        data = [line.replace("\n","").split(",") for line in file.readlines()]
        curve = get_curve_dict(headers, data)
    
    # Get minimum creep rate
    d_curve    = differentiate_curve(curve, "time", "strain")
    mcr_value  = min(d_curve["strain"])
    index_mcr  = d_curve["strain"].index(mcr_value)
    time_mcr   = curve["time"][index_mcr]
    strain_mcr = curve["strain"][index_mcr]
    
    # Define top and bottom lines
    line_1 = lambda time : mcr_value * (time - time_mcr) + strain_mcr - 0.002
    line_2 = lambda time : mcr_value * (time - time_mcr) + strain_mcr + 0.002
    
    # Define function to get intersection
    def get_intersection(line_function, time_list, strain_list):
        initial_diff = line_function(time_list[0]) - strain_list[0]
        initial_sign = initial_diff / abs(initial_diff)
        for i in range(len(time_list)):
            value_diff = line_function(time_list[i]) - strain_list[i]
            value_sign  = value_diff / abs(value_diff)
            if initial_sign * value_sign == -1:
                return time_list[i], strain_list[i]
    
    # Get intersection values
    time_primary, strain_primary = get_intersection(line_1, curve["time"], curve["strain"])
    time_tertiary, strain_tertiary = get_intersection(line_2, curve["time"], curve["strain"])
    
    # Plot everything
    plt.xlabel("Time (h)")
    plt.ylabel("Strain (mm/mm)")
    plt.scatter(curve["time"], curve["strain"], c="gray", label="Experimental data")
    plt.scatter([time_primary], [strain_primary], label="Primary creep")
    plt.scatter([time_mcr], [strain_mcr], label="Minimum creep rate")
    plt.scatter([time_tertiary], [strain_tertiary], label="Tertiary creep")
    plt.legend()
    plt.savefig("plot")