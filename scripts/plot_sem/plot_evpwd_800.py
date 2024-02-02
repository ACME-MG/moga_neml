import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

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
4.1862	84.548	2.1123	4.7752	1574.3	75.478	425.59	251.11	537.64	2.1764	11.252
4.1862	84.548	2.1123	4.7752	1574.3	76.845	426.48	538.73	819.21	2.2127	13.073
4.1862	84.548	2.1123	4.7752	1574.3	66.288	365.89	242.53	486.11	2.7732	19.203
4.1862	84.548	2.1123	4.7752	1574.3	96.054	498.14	507.56	749.55	2.6688	3.9596
4.1862	84.548	2.1123	4.7752	1574.3	46.873	285.58	445.98	862.08	2.0514	19.771

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
#                    "c_n": (0, 20), "c_0": (0, 1), "c_1": (0, 5), "t_n": (0, 20), "t_0": (0, 1), "t_1": (0, 5)},
#     # log=True,
# )
