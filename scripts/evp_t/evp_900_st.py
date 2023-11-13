import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evp 900 st t", input_path="../data", output_path="../results")

api.define_model("evp")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.remove_damage(0.1, 0.7)

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_damage(0.1, 0.7)

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.remove_manual("strain", 0.3)
api.add_error("area", "strain", "stress", weight=0.5)

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
