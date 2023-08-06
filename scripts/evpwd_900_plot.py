import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwd 900")
api.define_model("evpwd")

api.fix_param("evp_s0",  4.871e0)
api.fix_param("evp_R",   1.152e1)
api.fix_param("evp_d",   7.028e0)
api.fix_param("evp_n",   4.242e0)
api.fix_param("evp_eta", 1.138e3)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.plot_predicted(4.4744, 0.28194, 2.5566)
