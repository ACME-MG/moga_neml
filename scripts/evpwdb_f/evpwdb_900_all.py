import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpwdb 900 all", input_path="../data", output_path="../results")

api.define_model("evpwdb")

api.fix_param("evp_s0",  17.420)
api.fix_param("evp_R",   217.36)
api.fix_param("evp_d",   0.33131)
api.fix_param("evp_n",   2.0340)
api.fix_param("evp_eta", 42591.0)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time", weight=5)
api.add_error("end", "strain", weight=5)
# api.add_error("damage")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time", weight=5)
api.add_error("end", "strain", weight=5)
# api.add_error("damage")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time", weight=5)
api.add_error("end", "strain", weight=5)
# api.add_error("damage")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end", "time", weight=5)
api.add_error("end", "strain", weight=5)
# api.add_error("damage")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("area", "strain", "stress")
api.add_error("end", "strain", weight=5)
api.add_error("end", "stress", weight=5)

api.reduce_errors("square_average")
api.reduce_objectives("square_average")
# api.group_errors(name=True, type=False, labels=True)

api.plot_experimental()
api.set_recorder(10, 10, True, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
