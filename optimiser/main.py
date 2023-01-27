"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "test", False)
api.read_train_data(["c_800_80.csv", "c_800_70.csv"])
api.read_test_data(["c_800_65.csv", "c_800_60.csv"])
api.remove_oxidised_creep(300)
api.define_model("evpcd")
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.define_recorder(10, 10)
api.optimise(10000, 400, 400, 0.65, 0.35)

# api.read_train_data(["c_800_80.csv", "c_800_70.csv"])
# api.read_test_data(["c_800_65.csv", "c_800_60.csv"])
# api.read_train_data(["c_900_36.csv", "c_900_31.csv"])
# api.read_test_data(["c_900_28.csv", "c_900_26.csv"])
# api.read_train_data(["c_1000_16.csv", "c_1000_13.csv"])
# api.read_test_data(["c_1000_12.csv", "c_1000_11.csv"])
# api.define_model("vshai", ["input_orientations.csv", 1.0, [1,1,0], [1,1,1]])