"""
 Title:         Material Modelling Surrogate for VSHAI
 Description:   Generates VSHAI parameters and corresponding output
 Author:        Janzen Choi

"""

# Libraries
import itertools, numpy as np
from _evp import Model
# from _vshai import Model

# Surrogate Modelling Constants
NUM_STRAINS = 25

# Rounds a float to a number of significant figures
def round_sf(value:float, sf:int) -> float:
    format_str = "{:." + str(sf) + "g}"
    rounded_value = float(format_str.format(value))
    return rounded_value

# Transposes a 2D list of lists
def transpose(list_of_lists:float) -> list:
    transposed = np.array(list_of_lists).T.tolist()
    return transposed

# Converts a dictionary into a CSV file
def dict_to_csv(data_dict:dict, csv_path:str) -> None:
    
    # Extract headers and turn all values into lists
    headers = data_dict.keys()
    for header in headers:
        if not isinstance(data_dict[header], list):
            data_dict[header] = [data_dict[header]]
    
    # Open CSV file and write headers
    csv_fh = open(csv_path, "w+")
    csv_fh.write(",".join(headers) + "\n")
    
    # Write data and close
    max_list_size = max([len(data_dict[header]) for header in headers])
    for i in range(max_list_size):
        row_list = [str(data_dict[header][i]) if i < len(data_dict[header]) else "" for header in headers]
        row_str = ",".join(row_list)
        csv_fh.write(row_str + "\n")
    csv_fh.close()

# Finds the index corresponding to the nearest value
def find_nearest(array, value):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return index

# Initialise model
model = Model()

# Initialise parameter values
value_dict = model.get_value_dict()

# Get all combinations
value_grid   = list(value_dict.values())
combinations = list(itertools.product(*value_grid))
combinations = [list(c) for c in combinations]
print(f"Generated {len(combinations)} combinations")

# Prepare parameter dictionary
transposed_combinations = transpose(combinations)
param_dict = {key: value for key, value in zip(list(value_dict.keys()), transposed_combinations)}

# Prepare combined dictionary
headers = list(param_dict.keys()) + ["x_end"] + [f"y_{i+1}" for i in range(NUM_STRAINS)]
empty_lists = [[] for _ in range(len(headers))]
combined_dict = {key: value for key, value in zip(headers, empty_lists)}

# Iterate through parameters
fail_count = 0
for params in combinations:
    
    # Get prediction
    try:
        result = model.get_prediction(*params)
    except:
        fail_count += 1
        continue
    
    # Add parameters
    for i in range(len(params)):
        param_name = list(param_dict.keys())[i]
        combined_dict[param_name].append(params[i])
    
    # Add end point
    x_end = result["strain"][-1]
    combined_dict["x_end"].append(x_end)
    
    # Define x values
    # start_num_strains = 5
    # end_num_strains = NUM_STRAINS - start_num_strains
    # x_list  = [x_end/10/start_num_strains*(i+1) for i in range(start_num_strains)]
    # x_list += [x_end/end_num_strains*(i+1) for i in range(start_num_strains, NUM_STRAINS)]
    x_list = [x_end/NUM_STRAINS*(i+1) for i in range(NUM_STRAINS)]
    
    # Add strain values
    for i in range(NUM_STRAINS):
        y_index = find_nearest(result["strain"], x_list[i])
        y_value = round_sf(result["stress"][y_index], 5)
        combined_dict[f"y_{i+1}"].append(y_value)

# Write results
print(f"Results failed = {fail_count}")
dict_to_csv(combined_dict, "params.csv")
