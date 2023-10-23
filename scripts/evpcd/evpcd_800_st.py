import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd 800 st", input_path="../data", output_path="../results")

api.define_model("evpcd")

api.fix_param("evp_s0",  14.535)
api.fix_param("evp_R",   347.93)
api.fix_param("evp_d",   0.33581)
api.fix_param("evp_n",   3.8755)
api.fix_param("evp_eta", 3156.8)

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
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, 10, True, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
