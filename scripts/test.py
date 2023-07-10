import sys; sys.path += [".."]
from moga_neml.api import API

api = API("", verbose=False, output_here=True)
api.define_model("evp")

api.read_data("tensile/AirBase_900_D10.csv")
# api.remove_manual("strain", 0.4)
# api.add_error("damage")

# api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
# api.remove_damage(0.4, 0.8)
# api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
# api.remove_damage(0.4, 0.8)
# api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
# api.remove_damage(0.4, 0.8)
# api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
# api.remove_damage(0.4, 0.8)

# params = (18.54, 30.49, 2.523, 3.026, 1547.3)
params = (159.15, 12.871, 11.424, 1.5864, 1823.9)
api.get_results(*params)
# api.plot_predicted(*params, type="tensile")
# api.plot_predicted(*params, type="creep")
