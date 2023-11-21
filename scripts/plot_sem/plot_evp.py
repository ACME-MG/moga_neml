import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evp")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.remove_damage()
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.remove_damage()
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.remove_damage(0.1, 0.7)
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.remove_damage(0.1, 0.7)
# api.read_data("tensile/inl/AirBase_800_D7.csv")
# api.remove_manual("strain", 0.3)

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
    [
        [4.707, 29.9, 47.707, 3.6626, 3159.4],
        [0.67197, 25.75, 43.169, 4.4879, 1669.9],
        [29.487, 16.2498, 54.943, 2.3381, 29598],
        [41.512, 26.942, 0.38245, 2.5429, 18405],
        [6.5485, 44.046, 50.935, 2.0542, 68466],
    ],
    colour_list=["blue", "orange", "green", "red", "purple"],
    clip=True,
    # limits_list=[((0, 5000), (0, 0.25))],
    limits_list=[((0, 8000), (0, 0.7))],
)
# api.plot_prediction(11.695, 101.28, 1.1411, 4.6827, 1595.5)
