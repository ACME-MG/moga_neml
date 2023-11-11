import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd i 800 all", input_path="../data", output_path="../results")

api.define_model("evpcd")

api.init_param("evp_s0",  4.7070)
api.init_param("evp_R",   29.900)
api.init_param("evp_d",   47.707)
api.init_param("evp_n",   3.6626)
api.init_param("evp_eta", 3159.4)
api.init_param("cd_A",    2169.0)
api.init_param("cd_xi",   5.6903)
api.init_param("cd_phi",  26.372)

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
