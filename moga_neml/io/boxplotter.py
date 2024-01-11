"""
 Title:         Boxplotter
 Description:   For creating boxplots
 Author:        Janzen Choi
 
"""

# Libraries
import matplotlib.pyplot as plt
import seaborn as sns

def plot_boxplots(data_list_list:list, file_path:str, title:str, colour_list:list=None,
                  limits_dict:list=None, log:bool=False) -> None:
    """
    Creates multiple boxplots

    Parameters:
    * `data_list_list`: A list of datasets (list)
    * `file_path`:      The path to save the boxplots
    * `title`:          The title on top of the boxplots
    * `colour_list`:    A list of colours
    * `limits_dict`:    A dictionary of tuples (i.e., (lower, upper)) defining the scale of the boxplots
    * `log`:            Whether to apply log scale or not
    """

    # Create plots
    num_data = len(data_list_list)
    fig, axes = plt.subplots(nrows=num_data, ncols=1, figsize=(5, num_data*0.8), sharex=False)

    # Add horizontal boxplots and data points
    for i, axis in enumerate(axes):

        # Create boxplot
        data_list = data_list_list[i]
        y_list = [i + 1] * len(data_list)
        sns.boxplot(x=data_list, y=y_list, ax=axis, width=0.5, showfliers=False, boxprops=dict(alpha=0.5),
                    color=colour_list[i] if colour_list is not None else None, orient="h")

        # Format ticks
        axis.tick_params(axis="x", labelsize=14)
        axis.set_yticks([])
        axis.set_ylabel("")

        # Apply limits and log if desired
        if limits_dict != None:
            limits = list(limits_dict.values())[i]
            axis.set_xlim(limits)
        if log:
            axis.set_xscale("log")

    # Format and save figure
    # fig.suptitle(title, fontsize=14, fontweight="bold") # uncomment me
    fig.tight_layout()
    plt.savefig(file_path)
