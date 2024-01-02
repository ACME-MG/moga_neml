import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

model_name = "ricvih"
itf = Interface(model_name, input_path="../data", output_path="../results")
itf.define_model(model_name)

# Optimise cycles
itf.read_data("cyclic/Airbase316.csv", num_points=5000)
# itf.change_data("num_cycles", 2)
# itf.remove_manual("time", 250)
itf.add_error("area_saddle", "time", "strain", num_points=100, tolerance=0.005)
itf.add_error("area_saddle", "time", "stress", num_points=100, tolerance=10.0)
itf.add_error("saddle", "time", "stress")
itf.add_error("num_peaks", "time", "strain")
itf.add_error("end", "time")

params_str = """
208.12	132.18	5.0125	3378	83.722	134030	5191.1
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
for params in params_list:
    itf.plot_simulation(params)
    # itf.get_results(params)
    # itf.save_model(params)
