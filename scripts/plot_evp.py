import sys; sys.path += [".."]
from moga_neml.api import API

api = API("test", output_here=True)
api.define_model("evpwd")

# api.read_data("tensile/inl/AirBase_900_D10.csv")
api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.set_driver(num_steps=2000)

api.plot_predicted(
    13.47382181, 12.70302635, 17.06374005, 1.610019787, 389004.4574, 4.47441823, 0.281937081, 2.556607036
    # 17.44404723, 12.40270485, 7.750245769, 1.924995791, 70080.79199, 2370.035856, 4.202826388, 7.287150159
)
