import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp 800 all")
api.define_model("evp")

api.read_data("tensile/AirBase_800_D7.csv")
api.remove_manual("strain", 0.4)
api.add_error("area", "strain", "stress")
api.add_error("yield")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.remove_damage(0.4, 0.8)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.remove_damage(0.4, 0.8)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.remove_damage(0.4, 0.8)

api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.remove_damage(0.4, 0.8)

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

api.set_recorder(10, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
