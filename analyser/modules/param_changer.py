"""
 Title:         Parameter Changer
 Description:   For investigating the effects of changing parameters
 Author:        Janzen Choi
 
"""

# Libraries
from copy import deepcopy
import matplotlib.pyplot as plt

# Changes the parameters and plots the results
def investigate_params(model, change_params, base_params, change, steps, output_path):

    # Initialise model
    param_names = model.get_param_names()
    model_name = model.get_name()
    num_params = len(param_names)

    # Initialise plots
    figure, axis = plt.subplots(1, num_params)
    axes = [axis] if num_params == 1 else axis
    figure.set_size_inches(6*num_params-1, 6)
    figure.suptitle(f"Changes to Parameters for {model_name}\n(red=100%, green={(1+change)*100}%)")
    [axes[i].set_title(f"{param_names[i]}") for i in range(num_params)]
    [axes[i].set_xlabel("x") for i in range(num_params)]
    [axes[i].set_ylabel("y") for i in range(num_params)]

    # Iterate through the parameters
    for i in range(len(param_names)):
        if not param_names[i] in change_params:
            continue

        # Gets a list of the changed values
        params_list = [deepcopy(base_params) for _ in range(steps+1)]
        for j in range(steps+1):
            params_list[j][i] = base_params[i] * (1 + j * change / steps)
        
        # Gets the corresponding curves
        print("====================================================================================================")
        curve_list_list = []
        for j in range(len(params_list)):
            rounded_params = [round(param, 4) for param in params_list[j]]
            print(f"  Changing {param_names[i]}\t({j+1}/{steps+1})\t{rounded_params}")
            curve_list = model.get_prd_curves(*params_list[j])
            curve_list_list.append(curve_list)
        
        # Plot the data
        for j in range(1,len(curve_list_list)-1):
            for curve in curve_list_list[j]:
                axes[i].plot(curve["x"], curve["y"], color="silver")
        for curve in curve_list_list[0]:
            axes[i].plot(curve["x"], curve["y"], color="r")
        for curve in curve_list_list[-1]:
            axes[i].plot(curve["x"], curve["y"], color="g")
    
    # Format and save
    for i in range(num_params):
        axes[i].locator_params(axis='x', nbins=7)
    figure.tight_layout(pad=1.0)
    figure.savefig(output_path)