"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
thread = 8
api = API(False, f"vshai {thread} threads", True)
api.read_files(["other/t_800_.csv"])
api.define_model("vshai", ["other/input_orientations.csv", 1.0, [1,1,0], [1,1,1], thread])
api.plot_results([30, 60, 20, 0.001, 12])