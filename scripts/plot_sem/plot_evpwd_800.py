import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpwdb")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# api.add_error("dummy")
api.read_data("tensile/inl/AirBase_800_D7.csv")
api.add_error("dummy")

params_str = """
11.45	53.151	7.1666	3.9502	2221.6	1.373	0.39922	3.891	3.8787	0.13688	2.6693
11.45	53.151	7.1666	3.9502	2221.6	1.6202	0.4079	3.8417	1.01	0.81264	4.2534
11.45	53.151	7.1666	3.9502	2221.6	1.1096	0.50564	4.6887	1.3922	0.22739	2.9318
11.45	53.151	7.1666	3.9502	2221.6	1.4702	0.52088	4.4514	8.1588	0.41592	6.5574
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# api.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
