import sys; sys.path += [".."]
from moga_neml.api import API

api = API("vshai ansto y_area")
api.define_model("vshai", ori_path="data/ebsd/input_stats.csv", lattice=1.0, slip_dir=[1,1,0], slip_plane=[1,1,1], num_threads=16)

api.read_data("tensile/ansto/AirBase_1e-2_A.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")

api.read_data("tensile/ansto/AirBase_1e-3_C.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")

api.read_data("tensile/ansto/AirBase_1e-4_C.csv") # B
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)