import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcvr")
api.define_model("evpcvr")

api.read_file("tensile/AirBase_800_D7.csv", True)
api.add_error("y_area", "tensile")

api.record(50, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)