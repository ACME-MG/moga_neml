import sys; sys.path += [".."]
from moga_neml.api import API

api = API("temp")

api.define_model("evpcd")

api.fix_param("evp_s0",  4.7070)
api.fix_param("evp_R",   29.900)
api.fix_param("evp_d",   47.707)
api.fix_param("evp_n",   3.6626)
api.fix_param("evp_eta", 3159.4)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end_cons", "time")
api.add_error("end_cons", "strain")

api.plot_experimental()
# api.plot_predicted(17.44404723, 12.40270485, 7.750245769, 1.924995791, 70080.79199, 2370.035856, 4.202826388, 7.287150159)
api.set_recorder(1, 10, True)
api.optimise(10000, 10, 5, 0.65, 0.35)
