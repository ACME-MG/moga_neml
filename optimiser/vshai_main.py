from modules.api import API
api = API("vshai_s", 0)
api.read_files(["cp_ebsd/t_i2.csv"])
api.define_model("vshai_s", ["cp_ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 20, 1e-4/3, 15])
api.define_errors(["dy_area", "y_area", "y_end"])
api.define_recorder(1, 100)
api.optimise(10000, 1, 1, 0.65, 0.35)