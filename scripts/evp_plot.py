import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwd test")
api.define_model("evpwd")

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.plot_predicted(13.47382181, 12.70302635, 17.06374005, 1.610019787, 389004.4574, 4.47441823, 0.281937081, 2.556607036)
