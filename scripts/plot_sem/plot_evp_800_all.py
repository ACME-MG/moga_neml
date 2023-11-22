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

params_str = """
10.077	32.911	21.906	3.5992	3063
11.695	101.28	1.1411	4.6827	1595.5
9.8172	101.47	1.4057	4.6857	1595.7
31.816	59.655	1.0424	3.6473	2944
20.016	69.863	1.1781	4.3255	1881.4
4.4611	35.628	31.021	3.6186	3016.2
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    clip        = True,
    limits_list = [((0, 8000), (0, 0.7))],
)

api.plot_distribution(
    params_list = params_list,
    # limits_list = [(-5, 50), (10, 50), (-10)],
    log=True,
)
