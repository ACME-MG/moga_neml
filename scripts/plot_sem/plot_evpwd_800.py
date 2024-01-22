import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("dummy")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5	3.1894	107.49	562.41	15.996	403.29	761.78
17.217	179.74	0.61754	4.4166	1783.5	3.7285	88.721	497.05	5.1099	408.26	749.96
17.217	179.74	0.61754	4.4166	1783.5	3.298	69.202	395.39	2.5218	952.79	648.23
17.217	179.74	0.61754	4.4166	1783.5	6.6333	83.803	475.42	1.6357	362.54	877.42
17.217	179.74	0.61754	4.4166	1783.5	5.9162	82.59	473.12	7.209	489	888.16
17.217	179.74	0.61754	4.4166	1783.5	6.3288	99.967	572.25	1.9183	194.04	773.55
17.217	179.74	0.61754	4.4166	1783.5	3.39	95.223	525.57	7.1109	473.17	835.41
17.217	179.74	0.61754	4.4166	1783.5	5.8887	110	624.85	1.2745	266.84	966.6
17.217	179.74	0.61754	4.4166	1783.5	3.4882	136.9	730.49	2.5696	261.31	965.19
17.217	179.74	0.61754	4.4166	1783.5	3.7656	74.381	423.03	1.6293	812.37	562.63

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
#                    "c_n": (0, 20), "c_0": (0, 1), "c_1": (0, 5), "t_n": (0, 20), "t_0": (0, 1), "t_1": (0, 5)},
#     # log=True,
# )
