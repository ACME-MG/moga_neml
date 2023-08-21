import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwd 900 tensile")
api.define_model("evpwd")

api.fix_param("evp_s0",  4.871e0)
api.fix_param("evp_R",   1.152e1)
api.fix_param("evp_d",   7.028e0)
api.fix_param("evp_n",   4.242e0)
api.fix_param("evp_eta", 1.138e3)

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("area", "strain", "stress")
api.add_error("yield")
api.add_error("end_value", "strain")
api.add_error("end_value", "stress")
api.add_error("damage", weight=0.1)

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.set_recorder(50, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
