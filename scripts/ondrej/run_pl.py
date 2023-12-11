import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("ondrej pl", input_path="../data", output_path="../results")
api.define_model("pl")

api.read_data("cyclic/Airbase316_tensile.csv")
api.remove_manual("strain", 0.014)
api.add_error("area", "strain", "stress")
api.add_error("end", "strain")

api.set_driver(max_strain=0.014)
api.set_recorder(1, True, True, True, True)
api.optimise(20, 50, 25, 0.8, 0.01)
