import sys; sys.path += ["../../.."]
from moga_neml.api import API

api = API("evpcd 900 st fixed", input_path="../../data", output_path="../../results")

api.define_model("evpcd")

api.fix_param("evp_s0",  4.871e0)
api.fix_param("evp_R",   1.152e1)
api.fix_param("evp_d",   7.028e0)
api.fix_param("evp_n",   4.242e0)
api.fix_param("evp_eta", 1.138e3)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
