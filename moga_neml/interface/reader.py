"""
 Title:         Reader
 Description:   For reading experimental data
 Author:        Janzen Choi

"""

# Libraries
from numbers import Number
from moga_neml.maths.data import get_thinned_list
from moga_neml.maths.experiment import DATA_FIELD_DICT, DATA_DENSITY

def try_float_cast(value:str) -> float:
    """
    Tries to float cast a value

    Parameters:
    * `value`: A string to be float casted, if possible
    """
    try:
        return float(value)
    except:
        return value

def get_curve_dict(headers:list, data:list) -> dict:
    """
    Converts CSV data into a curve dict

    Parameters:
    * `headers`: A list of strings representing the keys
    * `data`:    A list of lists containing the data
    """

    # Get indexes of data
    list_indexes = [i for i in range(len(data[2])) if data[2][i] != ""]
    info_indexes = [i for i in range(len(data[2])) if data[2][i] == ""]
    
    # Create curve
    curve = {}
    for index in list_indexes:
        value_list = [float(d[index]) for d in data]
        value_list = get_thinned_list(value_list, DATA_DENSITY)
        curve[headers[index]] = value_list
    for index in info_indexes:
        curve[headers[index]] = try_float_cast(data[0][index])

    # Return curve
    return curve

def read_exp_data(file_dir:str, file_name:str) -> dict:
    """
    Reads the experimental data

    Parameters:
    * `file_dir`:  The path to the folder containing the experimental data files
    * `file_name`: The name of the file containing the experimental data
    """

    # Read data
    with open(f"{file_dir}/{file_name}", "r") as file:
        headers = file.readline().replace("\n","").split(",")
        data = [line.replace("\n","").split(",") for line in file.readlines()]
    
    # Create, check, and convert curve
    exp_data = get_curve_dict(headers, data)
    exp_data["file_name"] = file_name
    check_exp_data(exp_data)
    
    # Return curves
    return exp_data

def check_header(exp_data:dict, header:str, type:type) -> None:
    """
    Checks that a header exists and is of a correct type

    Parameters:
    * `exp_data`: The dictionary of experimental data
    * `header`:   A header in the experimental data dictionary
    * `type`:     The type of experimental data
    """
    if not header in exp_data.keys():
        raise ValueError(f"The data at '{exp_data['file_name']}' is missing a '{header}' header!")
    if not isinstance(exp_data[header], type):
        raise ValueError(f"The data at '{exp_data['file_name']}' does not have the correct '{header}' data type!")

def check_lists(exp_data:dict, header_list:list) -> None:
    """
    Checks that two lists in a curve are of correct formats

    Parameters:
    * `exp_data`:    The dictionary of experimental data
    * `header_list`: The list of headers in the dictionary
    """
    if header_list == []:
        return
    list_length = len(exp_data[header_list[0]])
    for header in header_list:
        if len(exp_data[header]) != list_length:
            raise ValueError(f"The data at '{exp_data['file_name']}' unequally sized data!")

def check_exp_data(exp_data:dict) -> None:
    """
    Checks whether the CSV files have sufficient headers and correct values;
    does not check that the 'lists' are all numbers

    Parameters:
    * `exp_data`:    The dictionary of experimental data
    """
    check_header(exp_data, "type", str)
    for data_type in ["common", exp_data["type"]]:
        data_field = DATA_FIELD_DICT[data_type]
        for list_field in data_field["lists"]:
            check_header(exp_data, list_field, list)
        check_lists(exp_data, data_field["lists"])
        for value_field in data_field["values"]:
            check_header(exp_data, value_field, Number)
