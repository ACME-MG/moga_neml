from modules.api import API
api = API("vshai tensile", 0)

api.define_model("vshai", "cp_ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 16)
api.read_file("tensile/AirBase_20_D5.csv", True)
api.add_error("y_area", "tensile")

api.record(1, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)