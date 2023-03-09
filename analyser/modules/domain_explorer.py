"""
 Title:         Domain Explorer
 Description:   For exploring the parameter space of a model
 Author:        Janzen Choi
 
"""

# Libraries
import math, random
import matplotlib.pyplot as plt

# Assesses the values of individual parameters
def assess_individual(model, output_path, trials=10):

    # Get model information
    param_names = model.get_param_names()
    model_name = model.get_name()
    l_bounds = model.get_param_lower_bounds()
    u_bounds = model.get_param_upper_bounds()

    # Create the plots
    num_params = len(param_names)
    plot_length = math.ceil(math.sqrt(num_params))
    figure, axis = plt.subplots(plot_length, plot_length)
    figure.set_size_inches(20, 10)
    figure.suptitle(f"Individual Parameter Assessment for {model_name}")

    # Set titles
    for i in range(num_params):
        x_index, y_index = i//plot_length, i%plot_length
        axis[x_index, y_index].set_title(param_names[i])

    # Explore X points in the parameter space
    for trial in range(trials):
        
        # Generate random curve
        params = [random.uniform(l_bounds[i], u_bounds[i]) for i in range(len(l_bounds))]
        curve = model.get_prd_curves(*params)
        curve = {"x": curve[0]["x"], "y": curve[0]["y"]} if curve != [] else {"x": [], "y": []}

        # Test validity of curve
        if curve["x"] == [] or curve["y"] == []: # or curve["y"][-1] < 0.01:
            valid = False
        else:
            valid_list = [y >= 0 and y <= 1 for y in curve["y"]]
            valid = False not in valid_list
        
        # Plot parameter values
        for i in range(num_params):
            x_index, y_index = i//plot_length, i%plot_length
            value = 1 if valid else 0
            colour = "g" if valid else "r"
            axis[x_index, y_index].scatter([params[i]], [value], marker="o", color=colour, linewidth=1)
        
        # Save results
        figure.savefig(output_path)
        print(f"  Explored {trial+1}/{trials}\t({'SUCCESS' if valid else 'FAILURE'})")

# Assesses the parameter dependencies
def assess_dependency(model, output_path, trials=10):

    # Get model information
    param_names = model.get_param_names()
    model_name = model.get_name()
    l_bounds = model.get_param_lower_bounds()
    u_bounds = model.get_param_upper_bounds()

    # Create the plots
    num_params = len(param_names)
    figure, axis = plt.subplots(num_params, num_params)
    figure.set_size_inches(40, 40)
    figure.suptitle(f"Parameter Dependency Assessment for {model_name}")

    # Set titles
    for i in range(num_params):
        for j in range(num_params):
            axis[i, j].set_title(f"{param_names[i]} : {param_names[j]}")

    # Explore X points in the parameter space
    for trial in range(trials):
        
        # Generate random curve
        params = [random.uniform(l_bounds[i], u_bounds[i]) for i in range(len(l_bounds))]
        curve = model.get_prd_curves(*params)
        curve = {"x": curve[0]["x"], "y": curve[0]["y"]} if curve != [] else {"x": [], "y": []}

        # Test validity of curve
        if curve["x"] == [] or curve["y"] == []: # or curve["y"][-1] < 0.01:
            valid = False
        else:
            valid_list = [y >= 0 and y <= 1 for y in curve["y"]]
            valid = False not in valid_list
        
        # Plot parameter values
        for i in range(num_params):
            for j in range(num_params):
                colour = "g" if valid else "r"
                axis[i, j].scatter([params[i]], [params[j]], marker="o", color=colour, linewidth=1)
        
        # Save results
        figure.savefig(output_path)
        print(f"  Explored {trial+1}/{trials}\t({'SUCCESS' if valid else 'FAILURE'})")
