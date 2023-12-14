import sys; sys.path += ["../.."]
from moga_neml.api import API

model_name = "cvih"
api = API(model_name, input_path="../data", output_path="../results")
api.define_model(model_name)

api.read_data("cyclic/Airbase316.csv", num_points=5000)
api.change_data("num_cycles", 1)
api.add_error("area", "strain", "stress", num_points=500)
# api.add_error("area", "time", "strain", num_points=500)
# api.add_error("area", "time", "stress", num_points=500)

api.plot_experimental("time", "strain")
api.plot_experimental("time", "stress")
api.plot_experimental("strain", "stress")

# params_str = "258.16	116.08	25.137	333400	827990	251800	316990"
# params = [list(map(float, line.split())) for line in params_str.strip().split("\n")][0]
# api.get_results(*params)
# exit()

api.set_recorder(1, True, True, True)
api.optimise(100, 50, 25, 0.8, 0.01)