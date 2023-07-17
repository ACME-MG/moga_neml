import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto youngs")
api.define_model("evp")

api.read_data("tensile/ansto/AirBase_A_1e-2.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.read_data("tensile/ansto/AirBase_A_1e-3.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.read_data("tensile/ansto/AirBase_A_1e-4.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.reduce_errors("sum")
api.reduce_objectives("sum")

api.set_recorder(10, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)
