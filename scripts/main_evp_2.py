import sys; sys.path += [".."]
from opt_neml.api import API

api = API("evp t 20c constrained", 0)

api.define_model("evp")
api.fix_param("evp_n", 15)

api.read_file("tensile/AirBase_20_D5.csv", True)

api.add_error("y_area", "tensile")

api.record(50, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
