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
17.217	179.74	0.61754	4.4166	1783.5	1.5566	0.29131	3.3173	1.5368	0.48294	2.7461
5.6908	66.627	1.9851	4.7723	1621.6	1.9605	0.30275	3.2365	12.155	0.52965	2.9596
9.3076	32.596	5.8114	4.5263	1775.9	2.0875	0.46391	4.1625	2.0491	0.90242	3.307
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
                   "c_n": (0, 20), "c_0": (0, 1), "c_1": (0, 5), "t_n": (0, 20), "t_0": (0, 1), "t_1": (0, 5)},
    # log=True,
)
