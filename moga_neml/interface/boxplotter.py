"""
 Title:         Boxplotter
 Description:   For creating boxplots
 Author:        Janzen Choi
 
"""

# Libraries
import matplotlib.pyplot as plt
import seaborn as sns

def plot_boxplots(data_list_list:list, file_path:str, title:str, colour_list:list=None,
                  limits_list:list=None, log:bool=False) -> None:
    """
    Creates multiple boxplots

    Parameters:
    * `data_list_list`: A list of datasets (list)
    * `file_path`:      The path to save the boxplots
    * `title`:          The title on top of the boxplots
    * `colour_list`:    A list of colours
    * `limits_list`:    A list of tuples (i.e., (lower, upper)) defining the scale of the boxplots
    * `log`:            Whether to apply log scale or not
    """

    # Create plots
    num_data = len(data_list_list)
    fig, axes = plt.subplots(nrows=1, ncols=num_data, figsize=(num_data*2, num_data), sharey=False)

    # Add boxplots and data points
    for i, axis in enumerate(axes):

        # Prepare the plotting
        data_list = data_list_list[i]
        x_list = [i+1] * len(data_list)

        # Plot boxplot and data points
        sns.boxplot(x=x_list, y=data_list, ax=axis, width=0.5, showfliers=False, boxprops=dict(alpha=0.5),
                    color=colour_list[i] if colour_list != None else None)
        sns.stripplot(x=x_list, y=data_list, ax=axis, color="black", alpha=0.5)

        # Apply limits and log if desired
        if limits_list != None:
            axis.set_ylim(limits_list[i])
        if log:
            axis.set_yscale("log")

    # Format and save figure
    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.tight_layout()
    plt.savefig(file_path)
