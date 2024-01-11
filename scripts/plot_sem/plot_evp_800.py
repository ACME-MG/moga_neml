import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evp")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.remove_damage()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.remove_damage()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.remove_damage(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.remove_damage(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.remove_manual("strain", 0.3)
itf.add_error("dummy")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5
5.6908	66.627	1.9851	4.7723	1621.6
9.3076	32.596	5.8114	4.5263	1775.9
5.8951	36.245	5.3757	4.7311	1598.4
4.1862	84.548	2.1123	4.7752	1574.3
25.038	90.693	0.61002	4.1982	1944.6
27.547	78.081	0.84273	3.8992	2454.8
27.885	124.89	0.65636	3.8874	2390.5
19.2	52.204	1.7579	4.5105	1614.6
8.5923	38.904	5.4829	4.4795	1841
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    clip        = True,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
)
