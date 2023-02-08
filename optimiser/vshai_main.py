from modules.api import API
api = API(False, "vshai", True)
api.read_files(["other/t_i2.csv"])
api.define_model("vshai", ["other/input_orientations.csv", 1.0, [1,1,0], [1,1,1], 16])
api.define_errors(["dy_area", "y_area"])
api.define_recorder(1, 10)
api.optimise(10000, 25, 50, 0.65, 0.35)