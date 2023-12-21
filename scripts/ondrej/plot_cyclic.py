import sys; sys.path += ["../.."]
from moga_neml.api import API

model_name = "ricvih"
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

params_str = """
208.12	132.18	5.0125	3378	83.722	134030	5191.1
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
for params in params_list:
    api.plot_simulation(params)
    # api.get_results(params)
    # api.save_model(params)
