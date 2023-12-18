import sys; sys.path += ["../.."]
from moga_neml.api import API

# model_name = "cvih"
# model_name = "riclih"
# model_name = "rilih"
# model_name = "rilikh"
# model_name = "riplih"
# model_name = "rivih"
# model_name = "vpclih"
model_name = "vpcvih"
# model_name = "vpplih"
# model_name = "vppvih"
api = API(model_name, input_path="../data", output_path="../results")
api.define_model(model_name)

# Optimise cycles
api.read_data("cyclic/Airbase316.csv", num_points=5000)
# api.change_data("num_cycles", 2)
# api.remove_manual("time", 250)
api.add_error("area_saddle", "time", "strain", num_points=100, tolerance=0.005)
api.add_error("area_saddle", "time", "stress", num_points=100, tolerance=10.0)
api.add_error("saddle", "time", "stress")
api.add_error("num_peaks", "time", "strain")
api.add_error("end", "time")

# Optimise initial tensile
api.read_data("cyclic/Airbase316.csv", num_points=5000)
api.change_data("num_cycles", 0)
api.remove_manual("strain", 0.014)
api.add_error("area", "strain", "stress", num_points=100)

# params_str = """
# 180.0	165.0	80.0e3	14.02e3	0.9e3	1.5e3
# """
# params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
# for params in params_list:
#     api.plot_prediction(*params)
#     api.get_results(*params)
# exit()

api.plot_experimental()
api.set_recorder(1, plot_opt=True)
api.optimise(100, 100, 50, 0.8, 0.01)
