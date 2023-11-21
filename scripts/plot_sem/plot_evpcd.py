import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpcd")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
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
        [4.707, 29.9, 47.707, 3.6626, 3159.4, 2169, 5.6903, 26.372],
        [14.535, 347.93, 0.33581, 3.8755, 3156.8, 2603.4, 4.9169, 4.2123],
        [16.044, 34.763, 20.428, 3.4181, 3359, 1810.4, 5.6613, 8.1353],
        [12.929, 37.18, 29.643, 2.9072, 7297.7, 1732, 5.777, 9.6077],
        [18.531, 28.649, 24.827, 3.3282, 3890.9, 1867, 5.661, 10.398],
    ],
    colour_list=["blue", "orange", "green", "red", "purple"],
    # clip=True,
    limits_list=[((0, 8000), (0, 0.7))],
)
# api.plot_prediction(11.695, 101.28, 1.1411, 4.6827, 1595.5)
