import sys; sys.path += [".."]
from moga_neml.api import API

api = API("Chaboche Optimisation")
api.define_model("cih")

api.read_data("cyclic/Airbase316.csv")
api.add_error("area", "time", "strain")
api.add_error("area", "time", "stress")
api.add_error("num_peaks", "time", "strain")
api.add_error("peak_dist", "time", "strain")

api.plot_experimental()
api.set_recorder(1, True, True, True)
api.optimise(10000, 10, 5, 0.8, 0.01)
