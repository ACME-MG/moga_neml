import sys; sys.path += ["../.."]
from moga_neml.api import API

model_name = "cvih"
api = API(model_name, input_path="../data", output_path="../results")
api.define_model(model_name)

api.read_data("cyclic/Airbase316.csv", num_points=5000)
api.change_data("num_cycles", 1)
api.remove_manual("time", 180)
api.add_error("area", "time", "strain", num_points=50)
api.add_error("area", "time", "stress", num_points=50)
api.add_error("end", "time", weight=100)
api.add_error("end", "strain")

api.plot_experimental()

params_str = """
1.0012	2.2437	12.016	296870	49914	230910	111490
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
for params in params_list:
    api.plot_prediction(*params)
    api.get_results(*params)
exit()

api.set_recorder(1, plot_opt=True, plot_loss=True)
api.optimise(100, 50, 25, 0.8, 0.01)