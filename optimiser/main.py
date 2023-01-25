"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "test", False)
api.read_data(["c_800_80.csv"])
# api.define_model("vshai", ["input_orientations.csv", 1.0, [1,1,0], [1,1,1]])
api.define_model("evpwd")
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.define_recorder(100, 10)
api.optimise(10000, 400, 400, 0.65, 0.35)
