from modules.api import API
api = API(False, "vshai", True)
api.read_files(["other/t_i2.csv"])
api.define_model("vshai", ["other/input_orientations.csv", 1.0, [1,1,0], [1,1,1], 8])
api.plot_results([83.68041279,3.73928443,3.05569439,0.26831762,14.04134645])
# api.define_errors(["dy_area", "y_area", "y_end"])
# api.define_recorder(1, 10)
# api.optimise(10000, 5, 5, 0.65, 0.35)