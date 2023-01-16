"""
 Title:         Reader
 Description:   For reading experimental data
 Author:        Janzen Choi

"""

# Libraries
import sys
sys.path += ["../__models__"]
from __model__ import get_curve

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
        
        # Get indexes of data 
        x_index      = headers.index("x")
        y_index      = headers.index("y")
        type_index   = headers.index("type")
        temp_index   = headers.index("temp")
        stress_index = headers.index("stress")

        # Create curve and append
        exp_curve = get_curve(
            x_list  = [float(d[x_index]) for d in data],
            y_list  = [float(d[y_index]) for d in data],
            file    = file_path,
            type    = data[0][type_index],
            stress  = float(data[0][stress_index]),
            temp    = float(data[0][temp_index]),
        )
        exp_curves.append(exp_curve)
    return exp_curves