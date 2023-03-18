from modules.api import API
api = API("vshai_s", 0)

api.define_model("vshai", ["cp_ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 16, 1e-4/3, 15])
api.read_file("cp_ebsd/t_i2.csv", train=True)
api.add_error("y_area", "tensile")
api.record(1, 100)
api.optimise(10000, 50, 25, 0.65, 0.35)