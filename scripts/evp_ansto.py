import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto")
api.define_model("evp")

api.read_data("tensile/ansto/AirBase_1e-2_A.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield", e_stress=400)
api.add_error("hardening", strain_0=0.02)

api.read_data("tensile/ansto/AirBase_1e-3_C.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield", e_stress=300)
api.add_error("hardening", strain_0=0.02)

api.read_data("tensile/ansto/AirBase_1e-4_C.csv") # B
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield", e_stress=200)
api.add_error("hardening", strain_0=0.02)

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
