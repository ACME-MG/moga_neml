"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "evpwd full sigmoid", False)
api.read_data(["inl_1/800_80_G25.csv", "inl_1/800_70_G44.csv"], ["inl_1/800_65_G33.csv", "inl_1/800_60_G32.csv"])
api.define_model("evpwd")
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.define_recorder(10, 10)
api.optimise(10000, 400, 400, 0.65, 0.35)

# api.define_model("vshai", ["input_orientations.csv", 1.0, [1,1,0], [1,1,1]])
# api.read_data(["inl_1/1000_16_G18.csv", "inl_1/1000_13_G30.csv"], ["inl_1/1000_12_G52.csv", "inl_1/1000_11_G39.csv"])
# api.read_data(["inl_1/900_36_G22.csv", "inl_1/900_31_G50.csv"], ["inl_1/900_28_G45.csv", "inl_1/900_26_G59.csv"])
# api.read_data(["inl_1/800_80_G25.csv", "inl_1/800_70_G44.csv"], ["inl_1/800_65_G33.csv", "inl_1/800_60_G32.csv"])