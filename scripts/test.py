import sys; sys.path += [".."]
from moga_neml.api import API

api = API("", verbose=False, output_here=True)
api.define_model("evpwd")

api.read_data("tensile/AirBase_900_D10.csv")
api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")

params = (14.955, 30.503, 2.5274, 3.026, 2500.7, 0.38852, 3.1987, 3.0996)
# params = (159.15, 12.871, 11.424, 1.5864, 1823.9)
api.get_results(*params)
# api.plot_predicted(*params, type="tensile")
# api.plot_predicted(*params, type="creep")
