import sys; sys.path += [".."]
from moga_neml.api import API

api = API("vshai tensile constrained")

api.define_model("vshai", "ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 16)
# api.fix_param("ai_g0", 0.00010906 / 3)
# api.fix_param("ai_n", 15)

api.read_file("tensile/AirBase_20_D5.csv", True)

api.add_error("y_area", "tensile")

# api.record(1, 10)
# api.optimise(10000, 50, 25, 0.65, 0.35)
# api.plot_results(327.865,0.60553,81.307,0.001,15)
api.plot_results(522.489, 0.258374, 65.41575, 3.63533E-05, 15)