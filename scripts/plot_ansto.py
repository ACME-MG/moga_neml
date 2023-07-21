import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto", output_here=True, verbose=False)
api.define_model("evp")

api.read_data("tensile/ansto/AirBase_1e-2_A.csv")
api.add_error("dummy")

api.read_data("tensile/ansto/AirBase_1e-3_C.csv")
api.add_error("dummy")

api.read_data("tensile/ansto/AirBase_1e-4_A.csv")
api.read_data("tensile/ansto/AirBase_1e-4_B.csv")
api.read_data("tensile/ansto/AirBase_1e-4_C.csv")

api.plot_predicted(303.8, 243.6, 21.403, 2.7201, 808.58)
