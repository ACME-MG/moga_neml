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
12.256	273.68	0.20866	3.8422	1242.3
4.8238	378.86	0.1423	4.4021	1006.9
7.044	16.175	6.7949	4.1207	1090
4.6857	40.357	1.8658	4.6053	821.77
2.9947	38.689	2.0182	4.8173	747.28
4.5406	40.119	1.8075	4.5694	857.29
8.3596	21.471	9.7768	3.3579	2186.3
19.204	20.144	3.8052	2.9519	2743.9
9.1402	40.376	5.2268	3.0845	2730.7
7.1037	48.235	4.2972	3.4084	1829.9
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    clip        = True,
    # limits_dict = {"creep": ((0, 6000), (0, 0.8)), "tensile": ((0, 0.7), (0, 400))},  # 800
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 0.8), (0, 250))}, # 900
)

api.plot_distribution(
    params_list = params_list,
    # limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 200), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)}, # 800
    limits_dict = {"evp_s0": (0, 30), "evp_R": (0, 400), "evp_d": (0, 15), "evp_n": (0, 10), "evp_eta": (0, 3000)}, # 900
    # log=True,
)
