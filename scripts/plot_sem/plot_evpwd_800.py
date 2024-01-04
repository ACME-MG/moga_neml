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
17.217	179.74	0.61754	4.4166	1783.5	1.6217	0.2946	3.3558	1.0135	0.34162	3.4578
5.6908	66.627	1.9851	4.7723	1621.6	1.8904	0.54329	4.6088	1.8685	0.093698	2.7472
9.3076	32.596	5.8114	4.5263	1775.9	12.116	0.72907	9.6295	2.1265	0.31592	3.2599

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
