"""
 Title:         Reader
 Description:   For reading experimental data
 Author:        Janzen Choi

"""

# Libraries
from numbers import Number

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
        curve[headers[index]] = [float(d[index]) for d in data]
    for index in info_indexes:
        curve[headers[index]] = try_float_cast(data[0][index])

    # Return curve
    return curve

# For reading experimental data
def read_experimental_data(file_paths:list) -> list[dict]:
    exp_curves = []

    # Get experimental data for each path
    for file_path in file_paths:

        # Read data
        with open(file_path, "r") as file:
            headers = file.readline().replace("\n","").split(",")
            data = [line.replace("\n","").split(",") for line in file.readlines()]
        
        # Create, check, convert, and append curve
        exp_curve = get_curve_dict(headers, data)
        exp_curve["file_path"] = file_path
        check_exp_curve(exp_curve)
        exp_curve = convert_exp_curve(exp_curve)
        exp_curves.append(exp_curve)
    
    # Return curves
    return exp_curves

# Checks that a header exists and is of a correct type
def check_header(exp_curve:dict, key:str, type:type):
    if not key in exp_curve.keys():
        raise ValueError(f"'{exp_curve['file_path']}' is missing a '{key}' header!")
    if not isinstance(exp_curve[key], type):
        raise ValueError(f"'{exp_curve['file_path']}' does not have the correct '{key}' data type!")

# Checks that two lists in a curve are of correct formats
def check_lists(exp_curve:dict, key_1:str, key_2:str):
    if len(exp_curve[key_1]) == 0 or len(exp_curve[key_2]) == 0:
        raise ValueError(f"'{exp_curve['file_path']}' does not have any {key_1} or {key_2} data!")
    elif len(exp_curve[key_1]) != len(exp_curve[key_2]):
        raise ValueError(f"'{exp_curve['file_path']}' has unequal {key_1} and {key_2} data!")

# Checks whether the CSV files have sufficient headers and correct values
#   Does not check that the 'lists' are all numbers
def check_exp_curve(exp_curve:dict):
    check_header(exp_curve, "type", str)
    check_header(exp_curve, "temp", Number)
    check_header(exp_curve, "youngs", Number)
    check_header(exp_curve, "poissons", Number)
    if exp_curve["type"] == "creep":
        check_header(exp_curve, "time", list)
        check_header(exp_curve, "strain", list)
        check_header(exp_curve, "stress", Number)
        check_lists(exp_curve, "time", "strain")
    elif exp_curve["type"] == "tensile":
        check_header(exp_curve, "strain", list)
        check_header(exp_curve, "stress", list)
        check_header(exp_curve, "strain_rate", Number)
        check_lists(exp_curve, "strain", "stress")
    elif exp_curve["type"] == "cyclic-time-strain":
        check_header(exp_curve, "time", list)
        check_header(exp_curve, "strain", list)
        check_header(exp_curve, "num_cycles", Number)
        check_header(exp_curve, "strain_rate", Number)
        check_lists(exp_curve, "time", "strain")
    elif exp_curve["type"] == "cyclic-time-stress":
        check_header(exp_curve, "time", list)
        check_header(exp_curve, "stress", list)
        check_header(exp_curve, "num_cycles", Number)
        check_header(exp_curve, "strain_rate", Number)
        check_lists(exp_curve, "time", "stress")
    elif exp_curve["type"] == "cyclic-strain-stress":
        check_header(exp_curve, "strain", list)
        check_header(exp_curve, "stress", list)
        check_header(exp_curve, "num_cycles", Number)
        check_header(exp_curve, "strain_rate", Number)
        check_lists(exp_curve, "strain", "stress")

# Converts an experimental curve into a suitable format
def convert_exp_curve(exp_curve:dict) -> list[dict]:
    if exp_curve["type"] == "creep":
        exp_curve["x"] = exp_curve.pop("time")
        exp_curve["y"] = exp_curve.pop("strain")
    elif exp_curve["type"] == "tensile":
        exp_curve["x"] = exp_curve.pop("strain")
        exp_curve["y"] = exp_curve.pop("stress")
    elif exp_curve["type"] == "cyclic-time-strain":
        exp_curve["x"] = exp_curve.pop("time")
        exp_curve["y"] = exp_curve.pop("strain")
    elif exp_curve["type"] == "cyclic-time-stress":
        exp_curve["x"] = exp_curve.pop("time")
        exp_curve["y"] = exp_curve.pop("stress")
    elif exp_curve["type"] == "cyclic-strain-stress":
        exp_curve["x"] = exp_curve.pop("strain")
        exp_curve["y"] = exp_curve.pop("stress")
    return exp_curve