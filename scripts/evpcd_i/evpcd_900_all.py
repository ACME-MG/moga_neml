import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd 900 all", input_path="../data", output_path="../results")

api.define_model("evpcd")

api.init_param("evp_s0",  17.420)
api.init_param("evp_R",   217.36)
api.init_param("evp_d",   0.33131)
api.init_param("evp_n",   2.0340)
api.init_param("evp_eta", 42591.0)
api.init_param("cd_A",    2632.8)
api.init_param("cd_xi",   4.0648)
api.init_param("cd_phi",  5.8117)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, 10, True, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
