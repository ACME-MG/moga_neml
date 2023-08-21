"""
 Title:         Plotter
 Description:   For plotting data
 Author:        Janzen Choi
 
"""

# Libraries
import matplotlib.pyplot as plt
from moga_neml.maths.experiment import DATA_UNITS

# Constants
DEFAULT_PATH    = "./plot"
EXP_DATA_COLOUR = "darkgrey"
PRD_DATA_COLOUR = "r"

# Class for plotting
class Plotter:

    # Constructor
    def __init__(self, path:str=DEFAULT_PATH, x_label:str="x", y_label:str="y"):
        self.path = path
        self.x_label = x_label
        self.y_label = y_label

    # Prepares the plot
    def prep_plot(self, title:str="", size:int=15):
        # plt.figure(figsize=(8,8))
        plt.xlabel(f"{self.x_label} ({DATA_UNITS[self.x_label]})", fontsize=size)
        plt.ylabel(f"{self.y_label} ({DATA_UNITS[self.y_label]})", fontsize=size)
        plt.title(title, fontsize=size)
    
    # Changes the scale of the plot
    def log_scale(self, x_log:bool=False, y_log:bool=False):
        if x_log:
            plt.xscale("log")
        if y_log:
            plt.yscale("log")
    
    # Plots the experimental data using a scatter plot
    def scat_plot(self, data_dict:dict, colour:str=EXP_DATA_COLOUR, size:int=5):
        plt.scatter(data_dict[self.x_label], data_dict[self.y_label], s=size**2, marker="o", color=colour, linewidth=1)
        
    # Plots the predicted data using a line plot
    def line_plot(self, data_dict:dict, colour=PRD_DATA_COLOUR):
        plt.plot(data_dict[self.x_label], data_dict[self.y_label], colour)

    # Defines the plot legend
    def define_legend(self, keys):
        plt.legend(keys)

    # Saves the plot
    def save_plot(self):
        plt.savefig(self.path)
    
    # CLears the plot
    def clear(self):
        plt.clf()