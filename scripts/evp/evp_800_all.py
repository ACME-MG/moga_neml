import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evp 800 all", input_path="../data", output_path="../results")

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

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
