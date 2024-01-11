import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("dummy")

params_str = """
16.994	187.83	0.26104	4.502	1784.8	3263.5	4.9231	13.172
22.454	66.77	0.92681	4.4191	1610.1	2142	5.4844	11.449
9.1648	36.326	12.337	4.2247	1776.1	2731	5.0411	8.3103
5.8951	36.907	5.3551	4.7311	1557.8	2224.1	5.2809	6.5113
4.1861	84.548	2.1125	4.767	1574.1	2883.2	4.8395	4.5431
27.868	89.339	0.59712	4.1982	1818	2645.2	5.1192	10.125
28.599	78.057	0.84292	3.8371	2441.5	2969.6	4.9976	10.642
29.979	119.58	0.552	3.8505	2314.4	2808.8	5.0354	9.5435
19.125	43.641	5.6148	4.1688	1616	1876.8	5.5594	6.8653
22.012	38.873	2.2033	4.245	1841.2	2377	5.2898	9.7712
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
                   "cd_A": (0, 5000), "cd_xi": (0, 10), "cd_phi": (0, 30)},
)
