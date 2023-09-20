import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd 1000 all", input_path="../data", output_path="../results")

api.define_model("evpcd")

# api.fix_param("evp_s0",  3.14e1)
# api.fix_param("evp_R",   1.40e1)
# api.fix_param("evp_d",   1.00e1)
# api.fix_param("evp_n",   2.87e0)
# api.fix_param("evp_eta", 9.93e3)

api.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
api.remove_oxidation(0.1, 0.7)
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.read_data("creep/inl_1/AirBase_1000_12_G52.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
api.remove_oxidation(0.1, 0.7)
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
