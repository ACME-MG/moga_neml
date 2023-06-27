"""
 Title:         Helper
 Description:   General helper functions
 Author:        Janzen Choi

"""

# Libraries
import csv, inspect, math, os, subprocess
import numpy as np

# Stores x and y labels
DATA_LABELS = {
    "creep":                {"x": "type",   "y": "strain"},
    "tensile":              {"x": "strain", "y": "stress"},
    "cyclic-time-strain":   {"x": "time",   "y": "strain"},
    "cyclic-time-stress":   {"x": "time",   "y": "stress"},
    "cyclic-strain-stress": {"x": "strain", "y": "stress"},
}

# Stores all the units
DATA_UNITS = {
    "stress": "MPa",
    "strain": "mm/mm",
    "temperature": "°C",
    "time": "s",
}

# For safely making a directory
def safe_mkdir(dir_path:str) -> None:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# For quickly writing to a file
def quick_write(file_name:str, content:list) -> None:
    with open(file_name, "w+") as file:
        file.write(content)
        
# Converts a list of dictionaries to a CSV format
def dict_list_to_csv(dictionary_list:list) -> tuple:
    headers = list(dictionary_list[0].keys())
    data = [[d[1] for d in dictionary.items()] for dictionary in dictionary_list]
    return headers, data

# For writing to CSV files
def write_to_csv(path:str, data:list) -> None:
    with open(path, "w+") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Runs a command using a single thread
def run(command, shell:bool=True, check:bool=True) -> None:
    subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = shell, check = check)

# Performs a 3x3 matrix multiplication
def get_matrix_product(matrix_1:list, matrix_2:list) -> list:
    result = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += matrix_1[i][k] * matrix_2[k][j]
    return result

# Inverts a matrix
def get_inverted(matrix:list) -> list:
    matrix = np.array(matrix)
    inverted = [list(i) for i in np.linalg.inv(matrix)]
    return inverted

# Inserts a commas and a conjunction into a list of strings
def conjunct(str_list:list, conjunction:list) -> str:
    if len(str_list) == 1:
        return str_list[0]
    elif len(str_list) == 2:
        return "{} {} {}".format(str_list[0], conjunction, str_list[1])
    conjuncted = ", ".join(str_list[:-1])
    conjuncted += ", {} {}".format(conjunction, str_list[-1])
    return conjuncted

# Silently raises an exception
def silent_raise(exception:Exception, caller:str="") -> None:
    caller = inspect.stack()[1][3] if caller == "" else caller
    print("\n  Error in '{}':\n".format(caller))
    print("  {}\n".format(exception))
    exit()

# Checks whether a variable is a number
def is_number(variable) -> bool:
    return isinstance(variable, float) or isinstance(variable, int)

# Transposes a 2D list of lists
def transpose(list_of_lists) -> list:
    transposed = np.array(list_of_lists).T.tolist()
    return transposed

# Returns a thinned list
def get_thinned_list(unthinned_list:list, density:int) -> list:
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]