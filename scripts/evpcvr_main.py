import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcvr 800 yield")
api.define_model("evpcvr")

# api.read_data("tensile/AirBase_20_D5.csv")
api.read_data("tensile/AirBase_800_D7.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.set_recorder(10, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)
