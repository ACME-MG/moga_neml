import sys; sys.path += [".."]
from moga_neml.api import API

api = API("new rates")
api.define_model("evpwdb")

# api.fix_param("evp_s0",  4.871)
# api.fix_param("evp_R",   11.518)
# api.fix_param("evp_d",   7.0281)
# api.fix_param("evp_n",   4.2421)
# api.fix_param("evp_eta", 1138.3)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
# api.add_error("damage")
# api.add_constraint("inc_end", "strain")
# api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
# api.add_error("damage")
# api.add_constraint("inc_end", "strain")
# api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
# api.add_error("damage")
# api.add_constraint("inc_end", "strain")
# api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
# api.add_error("damage")
# api.add_constraint("inc_end", "strain")
# api.add_constraint("dec_end", "time")

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("area", "strain", "stress")
api.add_error("end", "strain")
api.add_error("end", "stress")
# api.add_error("damage")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
# api.set_recorder(1, True, True, True)
# api.optimise(10000, 100, 50, 0.65, 0.35)
# api.optimise(10000, 10, 5, 0.8, 0.01)
api.plot_prediction(4.871, 11.518, 7.0281, 4.2421, 1138.3,
                    1.2072, 0.4455, 3.8687, 3.6877, 0.25385, 2.53081)
