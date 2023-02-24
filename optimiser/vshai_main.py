from modules.api import API
api = API("vshai", 2)
api.read_files(["__other__/t_i2.csv"])
api.define_model("vshai", ["__other__/input_orientations.csv", 1.0, [1,1,0], [1,1,1], 8])
api.define_errors(["dy_area", "y_area", "y_end"])
api.plot_results([30,60,20,0.001,12])
# api.define_recorder(1, 10)
# api.optimise(10000, 5, 5, 0.65, 0.35)