from modules.api import API
api = API("vshai", 0)
api.read_files(["cp_ebsd/t_i2.csv"])
api.define_model("vshai", ["cp_ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 20])
api.define_errors(["dy_area", "y_area", "y_end"])
# api.plot_results([30, 60, 20, 0.001, 12])
api.define_recorder(10, 100)
api.optimise(10000, 100, 50, 0.65, 0.35)