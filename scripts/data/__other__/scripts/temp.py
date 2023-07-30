import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto")
api.define_model("vshai", ori_path="data/ebsd/input_stats.csv", lattice=1.0, slip_dir=[1,1,0], slip_plane=[1,1,1], num_threads=16)

api.read_data("tensile/inl/AirBase_900_D10.csv")

api.set_recorder()
api.optimise(10,1,1)
