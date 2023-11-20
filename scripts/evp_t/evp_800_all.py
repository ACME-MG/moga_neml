import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evp 800 all t", input_path="../data", output_path="../results")

api.define_model("evp")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.remove_damage()
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.remove_damage()
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("tensile/inl/AirBase_800_D7.csv")
api.remove_manual("strain", 0.3)
api.add_error("yield")
api.add_error("area", "strain", "stress")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
