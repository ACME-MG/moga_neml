import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp")
api.def_model("evp")
api.read_file("creep/inl_1/AirBase_800_80_G25.csv", True)

api.fix_param("evp_n",    15)
api.set_param("evp_d",    1.3077)
api.set_param("evp_eta",  286.853)

api.add_error("y_area", "creep")
api.add_error("y_area", "tensile")
api.start_rec(10, 10)
api.start_opt(10000, 200, 100, 0.65, 0.35)
