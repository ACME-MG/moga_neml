import sys; sys.path += [".."]
from moga_neml.api import API

api = API("vshai tensile constrained")

api.def_model("vshai", "data/ebsd/input_stats.csv", 1.0, [1,1,0], [1,1,1], 16)
# api.fix_param("ai_g0", 0.00010906 / 3)
# api.fix_param("ai_n", 15)

api.read_file("tensile/AirBase_20_D5.csv", True)
api.add_error("y_area", "tensile")

api.fast_plot(380, 0.948, 74.1, 0.00010906 / 3, 15)

# api.start_rec(1, 10)
# api.start_opt(10000, 50, 25, 0.65, 0.35)