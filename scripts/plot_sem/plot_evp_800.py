import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evp")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.remove_damage()
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.remove_damage()
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.remove_damage(0.1, 0.7)
# api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.remove_damage(0.1, 0.7)
# api.add_error("dummy")
api.read_data("tensile/inl/AirBase_800_D7.csv")
api.remove_manual("strain", 0.3)
api.add_error("dummy")

params_str = """
31.327	104.92	0.8548	3.7508	2575.8
22.393	462.57	0.13573	4.314	1828.1
11.45	53.151	7.1666	3.9502	2221.6
37.742	49.123	2.4996	3.4102	3172
18.768	89.18	0.88069	4.5055	1677.4
23.304	306.58	0.32123	4.2592	1822.6
31.137	31.413	4.6003	3.6958	2583
29.726	45.991	2.3174	3.9613	2101.3
4.2227	26.503	4.0461	5.25	1261.4
4.4611	35.628	31.021	3.6186	3016.2
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    clip        = True,
    limits_dict = {"creep": ((0, 6000), (0, 0.8)), "tensile": ((0, 0.7), (0, 400))},
)

api.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
    # log=True,
)
