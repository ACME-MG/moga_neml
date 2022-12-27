"""
 Title:         Results plotter
 Description:   For plotting the results of the optibrated model
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Parameters
PARAM_STR   = "1.40324E-17	6.908798612	1.00741E-11	9.019906173	3.751674397"
PARAM_LIST  = [float(param) for param in PARAM_STR.split("\t")]

# Code
api = API(True)
api.read_data(["G32", "G33", "G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# api.remove_damage()
api.define_model("evpwd")
api.plot_results(PARAM_LIST)
# api.define_errors(["y_area", "dy_area"])
# api.get_errors(PARAM_LIST)