import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evp")

# api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
# api.remove_damage()
# api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
# api.remove_damage()
# api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# api.remove_damage(0.1, 0.7)
# api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# api.remove_damage(0.1, 0.7)
# api.read_data("tensile/inl/AirBase_800_D7.csv")
# api.remove_manual("strain", 0.3)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.remove_damage(0.1, 0.7)
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.remove_damage(0.1, 0.7)
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.remove_damage(0.1, 0.7)
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_damage(0.1, 0.7)
api.read_data("tensile/inl/AirBase_900_D10.csv")
api.remove_manual("strain", 0.3)

params_str = """
4.871	11.518	7.0281	4.2421	1138.3
12.885	37.379	2.4398	3.4975	1647.4
13.14	39.934	2.5283	3.4655	1648.3
5.1103	11.731	11.74	4.1926	1109.8
3.4692	11.414	8.204	4.304	1127.5
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    clip        = True,
    limits_dict = {"creep": ((0, 6000), (0, 0.8)), "tensile": ((0, 0.7), (0, 400))},  # 800
    # limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 0.8), (0, 250))}, # 900
)

api.plot_distribution(
    params_list = params_list,
    # limits_list = [(-5, 50), (10, 50), (-10)],
    log=True,
)
