import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwd")

api.def_model("evpwd")

api.set_param("evp_s0",  3.14e1)
api.set_param("evp_R",   1.40e1)
api.set_param("evp_d",   1.00e1)
api.set_param("evp_n",   2.87e0)
api.set_param("evp_eta", 9.93e3)

api.read_file("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time", weight=2)
api.add_error("x_end", "strain")

api.read_file("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time", weight=2)
api.add_error("x_end", "strain")

api.read_file("creep/inl_1/AirBase_800_65_G33.csv")
api.read_file("creep/inl_1/AirBase_800_60_G32.csv")

api.start_rec(50, 10)
api.start_opt(10000, 100, 50, 0.65, 0.35)
