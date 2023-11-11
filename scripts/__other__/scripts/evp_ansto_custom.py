import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto")
api.define_model("evp")

api.read_data("tensile/ansto/AirBase_1E-2_A.csv")
api.remove_manual("strain", 0.4)
api.add_error("custom_area", "strain", "stress", values=[0.1, 0.2, 0.3, 0.4])
api.add_error("yield", yield_stress=490)

api.read_data("tensile/ansto/AirBase_1E-3_C.csv")
api.remove_manual("strain", 0.4)
api.add_error("custom_area", "strain", "stress", values=[0.1, 0.2, 0.3, 0.4])
api.add_error("yield", yield_stress=390)

api.read_data("tensile/ansto/AirBase_1E-4_C.csv") # B
api.remove_manual("strain", 0.4)
api.add_error("custom_area", "strain", "stress", values=[0.1, 0.2, 0.3, 0.4])
api.add_error("yield", yield_stress=310)

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
