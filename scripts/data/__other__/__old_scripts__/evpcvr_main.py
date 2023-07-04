import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcvr")
api.def_model("evpcvr")

# api.read_file("tensile/AirBase_700_D4.csv", True)
api.read_file("tensile/AirBase_800_D7.csv", True)
api.add_error("y_area", "tensile")

api.start_rec(50, 10)
api.start_opt(10000, 200, 100, 0.65, 0.35)