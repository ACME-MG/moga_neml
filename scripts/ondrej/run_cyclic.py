import sys; sys.path += ["../.."]
from moga_neml.api import API

model_name = "riclih"
api = API(model_name, input_path="../data", output_path="../results")
api.define_model(model_name)

api.read_data("cyclic/Airbase316.csv", num_points=5000)
api.change_data("num_cycles", 2)
api.remove_manual("time", 256)
api.add_error("area", "time", "strain", num_points=200)
api.add_error("area", "time", "stress", num_points=200)
api.add_error("max", "strain", weight=10)
api.add_error("max", "stress", weight=10)
api.add_error("end", "time", weight=10)
api.add_error("num_peaks", "time", "strain")

params_str = """
180.0	165.0	80.0e3	14.02e3	0.9e3	1.5e3
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
for params in params_list:
    api.plot_prediction(*params)
    api.get_results(*params)
exit()

api.plot_experimental()
api.set_recorder(1, plot_opt=True)
api.optimise(100, 50, 25, 0.8, 0.01)
