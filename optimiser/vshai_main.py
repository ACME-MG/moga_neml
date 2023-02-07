from modules.api import API
api = API(True, "vshai", False)
api.read_files(["other/t_i2.csv"])
api.define_model("vshai", ["other/input_orientations.csv", 1.0, [1,1,0], [1,1,1], 20])
api.define_errors(["dy_area", "y_area"])
api.define_recorder(5, 10)
api.optimise(10000, 50, 50, 0.65, 0.35)