"""
 Title:         Plotter
 Description:   For plotting data
 Author:        Janzen Choi
 
"""

# Libraries
import matplotlib.pyplot as plt

# Constants
DEFAULT_PATH    = "./"
DEFAULT_PLOT    = "plot"
EXP_DATA_COLOUR = "darkgrey"
PRD_DATA_COLOUR = "r"

# Class for plotting
class Plotter:

    # Constructor
    def __init__(self, path = DEFAULT_PATH, plot = DEFAULT_PLOT):
        self.path = path
        self.plot = plot

    # Prepares the plot
    def prep_plot(self, title = "", xlabel = "x", ylabel = "y"):
        plt.figure(figsize=(8,8))
        plt.xlabel(xlabel, fontsize=20)
        plt.ylabel(ylabel, fontsize=20)
        plt.title(title, fontsize=20)
        
    # Plots the experimental data using a scatter plot
    def scat_plot(self, exp_curves, colour = EXP_DATA_COLOUR):
        for i in range(0, len(exp_curves)):
            plt.scatter(exp_curves[i]["x"], exp_curves[i]["y"], marker="o", color=colour, linewidth=1)
        
    # Plots the predicted data using a line plot
    def line_plot(self, prd_curves, colour = PRD_DATA_COLOUR):
        for i in range(0, len(prd_curves)):
            plt.plot(prd_curves[i]["x"], prd_curves[i]["y"], colour)

    # Defines the plot legend
    def define_legend(self, keys):
        plt.legend(keys)

    # Saves the plot
    def save_plot(self, path = "", plot = ""):
        path = self.path if path == "" else path
        plot = self.plot if plot == "" else plot
        plt.savefig(path + "/" + plot)
    
    # CLears the plot
    def clear(self):
        plt.clf()

# Plots a single curve
def quick_plot(path, file, curves):
    if curves == []:
        return
    plt = Plotter(path, file)
    plt.line_plot(curves, "r")
    plt.save_plot()
    plt.clear()

# Plots N sets of curves
def quick_plot_N(path, file, curve_lists=[], labels=[], colours=[], markers=[]):
    
    # Ensure there exists one non-empty curve
    is_empty = [curves == [] for curves in curve_lists]
    if curve_lists == [] or not False in is_empty:
        return

    # Define default values
    labels  = labels if labels != [] else list(range(len(curve_lists)))
    colours = colours if colours != [] else ["r"]*len(curve_lists)
    markers = markers if markers != [] else ["line"]*len(curve_lists)

    # Commence plotting
    plt = Plotter(path, file)
    for i in range(len(curve_lists)):
        if markers[i] == "line":
            plt.line_plot(curve_lists[i], colours[i])
        else:
            plt.scat_plot(curve_lists[i], colours[i])
    plt.define_legend(labels)
    plt.save_plot()
    plt.clear()