import sys; sys.path += [".."]
from moga_neml.api import API

api = API("plot", output_here=True)
api.define_model("evp")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.remove_damage()
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.remove_damage()
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.remove_damage(0.1, 0.7)
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.remove_damage(0.1, 0.7)
api.read_data("tensile/inl/AirBase_800_D7.csv")
api.remove_manual("strain", 0.3)

# api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
# api.remove_damage(0.1, 0.7)
# api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
# api.remove_damage(0.1, 0.7)
# api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
# api.remove_damage(0.1, 0.7)
# api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
# api.remove_damage(0.1, 0.7)
# api.read_data("tensile/inl/AirBase_900_D10.csv")

api.plot_predictions(
    [[9.8172, 101.47, 1.4057, 4.6857, 1595.7],
    [11.695, 101.28, 1.1411, 4.6827, 1595.5]],
    colour_list=["red", "blue"],
    clip=True,
    limits_list=[(0, 5000), (0, 0.7)]
)
# api.plot_prediction(11.695, 101.28, 1.1411, 4.6827, 1595.5)
