import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd i 900 st", input_path="../data", output_path="../results")

api.define_model("evpcd")

api.init_param("evp_s0",  17.937)
api.init_param("evp_R",   7.4195)
api.init_param("evp_d",   15.251)
api.init_param("evp_n",   2.4442)
api.init_param("evp_eta", 9880.2)
api.init_param("cd_A",    1271.1)
api.init_param("cd_xi",   5.1067)
api.init_param("cd_phi",  13.687)

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

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
