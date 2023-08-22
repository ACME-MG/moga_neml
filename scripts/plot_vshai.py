import sys; sys.path += [".."]
from moga_neml.api import API

api = API("vshai ansto area")
api.define_model("vshai", ori_path="data/ebsd/input_stats.csv", lattice=1.0, slip_dir=[1,1,0], slip_plane=[1,1,1], num_threads=16)
api.read_data("tensile/inl/AirBase_20_D5.csv")
api.set_driver(num_steps=1000)
api.get_results(30, 60, 20, 0.001, 12)
