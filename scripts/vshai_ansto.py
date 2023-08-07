import sys; sys.path += [".."]
from moga_neml.api import API

api = API("vshai ansto area")
api.define_model("vshaig", ori_path="data/ebsd/input_stats.csv", lattice=1.0, slip_dir=[1,1,0], slip_plane=[1,1,1], num_threads=16)
api.fix_param("ai_n", 4.4517)

api.read_data("tensile/ansto/AirBase_1E-2_A.csv")
api.remove_manual("strain", 0.4)
api.add_error("area", "strain", "stress")
api.add_error("yield", yield_stress=490)

api.read_data("tensile/ansto/AirBase_1E-3_C.csv")
api.remove_manual("strain", 0.4)
api.add_error("area", "strain", "stress")
api.add_error("yield", yield_stress=390)

api.read_data("tensile/ansto/AirBase_1E-4_C.csv") # B
api.remove_manual("strain", 0.4)
api.add_error("area", "strain", "stress")
api.add_error("yield", yield_stress=310)

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
