import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("ondrej evpy", input_path="../data", output_path="../results")
api.define_model("evpy", yield_function="IsoJ2")

api.read_data("cyclic/Airbase316.csv")
api.change_data("type", "cyclic")
api.remove_manual("strain", 0.014)
api.add_error("area", "strain", "stress")
api.add_error("end", "strain")

api.read_data("cyclic/Airbase316.csv")
api.change_data("type", "tensile")
api.remove_manual("strain", 0.014)
api.add_error("area", "strain", "stress")
api.add_error("end", "strain")

api.set_recorder(1, True, True, True)
api.optimise(50, 50, 25, 0.8, 0.01)
