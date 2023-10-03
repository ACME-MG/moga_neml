import sys; sys.path += [".."]
from moga_neml.api import API

api = API("temp", output_here=True)

api.define_model("evpcd")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.read_data("creep/inl_1/AirBase_900_36_G63.csv")
api.read_data("creep/inl_1/AirBase_900_31_G21.csv")
api.read_data("creep/inl_1/AirBase_900_28_G40.csv")
api.remove_manual("strain", 0.24)
api.read_data("creep/inl_1/AirBase_900_26_G42.csv")
api.remove_manual("strain", 0.15)

# api.plot_experimental()
api.plot_predicted(17.44404723, 12.40270485, 7.750245769, 1.924995791, 70080.79199, 2370.035856, 4.202826388, 7.287150159)
