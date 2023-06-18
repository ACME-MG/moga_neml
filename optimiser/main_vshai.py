from modules.api import API
api = API("vshai tensile unconstrained", 0)

api.define_model("vshai", "ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 16)
# api.fix_param("ai_g0", 0.001)
# api.fix_param("ai_n", 15)

api.read_file("tensile/AirBase_20_D5.csv", True)

api.add_error("y_area", "tensile")

api.record(1, 10)
api.optimise(10000, 50, 25, 0.65, 0.35)
# api.plot_results(327.865,0.60553,81.307,0.001,15)