"""
 Title:         Reader
 Description:   For reading experimental data
 Author:        Janzen Choi

"""

# Libraries
import sys
sys.path += ["../__common__"]
from curve import get_curve

# For reading experimental data
def read_experimental_data(file_paths):
    exp_curves = []

    # Get experimental data for each path
    for file_path in file_paths:

        # Read data
        file = open(file_path, "r")
        headers = file.readline().replace("\n","").split(",")
        data = [line.replace("\n","").split(",") for line in file.readlines()]
        file.close()
        
        # Get x and y data
        x_index = headers.index("x")
        y_index = headers.index("y")
        x_list = [float(d[x_index]) for d in data]
        y_list = [float(d[y_index]) for d in data]

        # Get auxiliary information
        info_dict = {}
        for i in range(len(headers)):
            if not headers[i] in ["x", "y"]:
                try:
                    value = float(data[0][i])
                except:
                    value = data[0][i]
                info_dict[headers[i]] = value

        # Create curve and append
        exp_curve = get_curve(x_list, y_list, info_dict)
        exp_curves.append(exp_curve)
    return exp_curves

# Removes values of a curve after a specific x value
def prematurely_end_curve(curve, x_value):
    curve["y"] = [curve["y"][i] for i in range(len(curve["x"])) if curve["y"][i] < x_value]
    curve["x"] = [curve["x"][i] for i in range(len(curve["x"])) if curve["x"][i] < x_value]
    return curve