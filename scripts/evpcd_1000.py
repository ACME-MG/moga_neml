import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcd 1000")
api.def_model("evpcd")

api.read_file("creep/inl_1/AirBase_1000_16_G18.csv", True)
api.rm_ocreep(100, 0.7)
api.read_file("creep/inl_1/AirBase_1000_13_G30.csv", True)
api.rm_ocreep(100, 0.6)
api.read_file("creep/inl_1/AirBase_1000_12_G52.csv", False)
api.rm_ocreep(100, 0.7)
api.read_file("creep/inl_1/AirBase_1000_11_G39.csv", False)
api.rm_ocreep(100, 0.7)
api.read_file("tensile/AirBase_1000_D12.csv", True)

api.visualise("creep")
api.visualise("tensile")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
api.add_error("y_area", "tensile")
api.start_rec(10, 10)
api.start_opt(10000, 200, 100, 0.65, 0.35)