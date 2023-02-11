"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "evpwd 80 sigmoid", False)
api.read_files(["inl_1/800_80_G25.csv"])
api.define_model("evpwd")
# api.define_model("evpwd_s", [4.118577172, 27.97814988, 0.637840909, 3.31618376, 8063.7164])
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_recorder(1, 1)
api.optimise(10000, 10, 10, 0.65, 0.35)

# api.define_constraints(["dec_x_end", "inc_y_end"])
# api.read_files(["inl_1/800_80_G25.csv", "inl_1/800_70_G44.csv"], ["inl_1/800_65_G33.csv", "inl_1/800_60_G32.csv"])
# api.read_files(["inl_1/900_36_G22.csv", "inl_1/900_31_G50.csv"], ["inl_1/900_28_G45.csv", "inl_1/900_26_G59.csv"])
# api.read_files(["inl_1/1000_16_G18.csv", "inl_1/1000_13_G30.csv"], ["inl_1/1000_12_G52.csv", "inl_1/1000_11_G39.csv"])