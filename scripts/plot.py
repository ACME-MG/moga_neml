import sys; sys.path += [".."]
from moga_neml.api import API

api = API("plot")
api.define_model("evp")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.remove_damage(0.1, 0.7)
api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.remove_damage(0.1, 0.7)
# api.add_error("area", "time", "strain")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_damage(0.1, 0.7)
# api.add_error("area", "time", "strain")

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("area", "strain", "stress")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.get_results(4.871, 11.518, 7.0281, 4.2421, 1138.3)
# api.plot_predicted(4.871, 11.518, 7.0281, 4.2421, 1138.3)
# api.plot_predicted(3.4692, 11.414, 8.204, 4.304, 1127.5)
