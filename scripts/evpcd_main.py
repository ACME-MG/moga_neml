import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcd 900")

api.define_model("evpcd")

api.init_param("evp_s0",  3.14e1)
api.init_param("evp_R",   1.40e1)
api.init_param("evp_d",   1.00e1)
api.init_param("evp_n",   2.87e0)
api.init_param("evp_eta", 9.93e3)

api.init_param("wd_m",    2.905e-1)
api.init_param("wd_b",    6.832)

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time")
api.add_error("x_end", "strain")

api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time")
api.add_error("x_end", "strain")

api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")

api.set_recorder(10, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)
