"""
 Title:         Plotter
 Description:   For plotting data
 Author:        Janzen Choi
 
"""

# Libraries
import matplotlib.pyplot as plt
import matplotlib.colors as mcolours
from moga_neml.maths.experiment import DATA_UNITS

# Constants
DEFAULT_PATH    = "./plot"
EXP_DATA_COLOUR = "darkgrey"
PRD_DATA_COLOUR = "r"
ALL_COLOURS     = list(mcolours.TABLEAU_COLORS) + list(mcolours.BASE_COLORS) + list(mcolours.CSS4_COLORS)

# Plotter class
class Plotter:

    def __init__(self, path:str=DEFAULT_PATH, x_label:str="x", y_label:str="y"):
        """
        Class for plotting data

        Parameters:
        * `path`:    The path to save the plot
        * `x_label`: The label for the x axis
        * `y_label`: The label for the y axis
        """
        self.path = path
        self.x_label = x_label
        self.y_label = y_label

    def prep_plot(self, title:str="", size:int=15) -> None:
        """
        Prepares the plot
        
        Parameters:
        * `title`: The title of the plot
        * `size`:  The size of the font
        """

        # Set figure size and title
        plt.figure(figsize=(8,8))
        plt.title(title, fontsize=size)

        # Set x and y labels
        x_units = f" ({DATA_UNITS[self.x_label]})" if self.x_label in DATA_UNITS.keys() else ""
        y_units = f" ({DATA_UNITS[self.y_label]})" if self.y_label in DATA_UNITS.keys() else ""
        plt.xlabel(f"{self.x_label.capitalize()}{x_units}", fontsize=size)
        plt.ylabel(f"{self.y_label.capitalize()}{y_units}", fontsize=size)
    
    def set_limits(self, x_limits:float=None, y_limits:float=None) -> None:
        """
        Sets the limits of the x and y scales

        Parameters:
        * `x_limits`: The upper and lower bounds of the plot for the x scale
        * `y_limits`: The upper and lower bounds bound of the plot for the y scale
        """
        if x_limits != None:
            plt.xlim(*x_limits)
        if y_limits != None:
            plt.ylim(*y_limits)

    def set_log_scale(self, x_log:bool=False, y_log:bool=False) -> None:
        """
        Changes the scale of the plot
        
        Parameters:
        * `x_log`: Whether to log the x scale
        * `y_log`: Whether to log the y scale
        """
        if x_log:
            plt.xscale("log")
        if y_log:
            plt.yscale("log")
    
    def scat_plot(self, data_dict:dict, colour:str=EXP_DATA_COLOUR, size:int=5) -> None:
        """
        Plots the experimental data using a scatter plot

        Parameters:
        * `data_dict`: The dictionary to store the data
        * `colour`:    The colour to plot the data
        * `size`:      The size of the curve
        """
        plt.scatter(data_dict[self.x_label], data_dict[self.y_label],
                    s=size**2, marker="o", color=colour, linewidth=1)
        
    def line_plot(self, data_dict:dict, colour=PRD_DATA_COLOUR) -> None:
        """
        Plots the experimental data using a line plot

        Parameters:
        * `data_dict`: The dictionary to store the data
        * `colour`:    The colour to plot the data
        """
        plt.plot(data_dict[self.x_label], data_dict[self.y_label], colour)

    def define_legend(self, keys:list) -> None:
        """
        Defines the plot legend
        
        Parameters:
        * `keys`: The keys to add to the legend
        """
        plt.legend(keys)

    def save_plot(self) -> None:
        """
        Saves the plot
        """
        plt.savefig(self.path)
    
    def clear(self) -> None:
        """
        Clears the plot
        """
        plt.clf()
