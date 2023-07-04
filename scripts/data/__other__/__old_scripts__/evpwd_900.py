import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwd 900")
api.def_model("evpwd")

api.read_file("creep/inl_1/AirBase_900_36_G22.csv", True)
api.read_file("creep/inl_1/AirBase_900_31_G50.csv", True)
api.read_file("creep/inl_1/AirBase_900_28_G45.csv", False)
api.read_file("creep/inl_1/AirBase_900_26_G59.csv", False)
api.rm_ocreep(100, 0.7)
api.read_file("tensile/AirBase_900_D10.csv", True)

api.visualise("creep")
api.visualise("tensile")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
api.add_error("y_area", "tensile")
api.start_rec(10, 10)
api.start_opt(10000, 200, 100, 0.65, 0.35)