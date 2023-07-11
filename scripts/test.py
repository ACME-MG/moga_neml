import sys; sys.path += [".."]
from moga_neml.api import API

api = API("", verbose=False, output_here=True)
api.define_model("evpwd")

api.read_data("tensile/AirBase_900_D10.csv")
api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")

params = (18.39, 30.036, 2.3999, 3.026, 2508.8, 0.80679, 5.4464, 3.8955)
# params = (159.15, 12.871, 11.424, 1.5864, 1823.9)
api.get_results(*params)
# api.plot_predicted(*params, type="tensile")
# api.plot_predicted(*params, type="creep")
