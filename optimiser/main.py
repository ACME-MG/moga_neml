"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "evpwd", False)
api.read_data(["800_80_G25.csv", "800_70_G44.csv"], ["800_65_G33.csv", "800_60_G32.csv"])
# api.define_model("evpwd")
api.define_model("evpwd_s", [0.671972514, 25.74997349, 43.16881374, 4.487884698, 1669.850786])
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.define_recorder(10, 10)
api.optimise(10000, 400, 400, 0.65, 0.35)

# api.define_model("vshai", ["input_orientations.csv", 1.0, [1,1,0], [1,1,1]])
# api.read_data(["1000_16_G18.csv", "1000_13_G30.csv"], ["1000_12_G52.csv", "1000_11_G39.csv"])
# api.read_data(["900_36_G22.csv", "900_31_G50.csv"], ["900_28_G45.csv", "900_26_G59.csv"])
# api.read_data(["800_80_G25.csv", "800_70_G44.csv"], ["800_65_G33.csv", "800_60_G32.csv"])