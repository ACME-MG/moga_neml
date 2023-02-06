"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "evpwd_s", False)
api.read_files(["inl_1/800_80_G25.csv"])
api.define_model("evpwd_s", [1.2817, 6.617, 3.276, 3.944, 3858])
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
# api.define_constraints(["dec_x_end", "inc_y_end"])
api.define_recorder(10, 10)
api.optimise(10000, 400, 400, 0.65, 0.35)

# api.read_files(["inl_1/800_80_G25.csv", "inl_1/800_70_G44.csv"], ["inl_1/800_65_G33.csv", "inl_1/800_60_G32.csv"])
# api.read_files(["inl_1/900_36_G22.csv", "inl_1/900_31_G50.csv"], ["inl_1/900_28_G45.csv", "inl_1/900_26_G59.csv"])
# api.read_files(["inl_1/1000_16_G18.csv", "inl_1/1000_13_G30.csv"], ["inl_1/1000_12_G52.csv", "inl_1/1000_11_G39.csv"])

# api = API(True, "vshai", False)
# api.read_files(["other/t_800_.csv"])
# api.define_model("vshai", ["other/input_orientations.csv", 1.0, [1,1,0], [1,1,1], 20])
# api.define_errors(["dy_area", "y_area"])
# api.define_recorder(10, 10)
# api.optimise(10000, 50, 50, 0.65, 0.35)