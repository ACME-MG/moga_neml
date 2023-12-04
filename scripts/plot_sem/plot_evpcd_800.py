import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpcd")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.add_error("dummy")
api.read_data("tensile/inl/AirBase_800_D7.csv")
api.add_error("dummy")

params_str = """
31.327	104.92	0.8548	3.7508	2575.8	2126.4	5.3209	6.5504
22.393	462.57	0.13573	4.314	1828.1	1912.9	5.5169	6.9639
11.45	53.151	7.1666	3.9502	2221.6	4328.7	4.3679	5.3108
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.8)), "tensile": ((0, 1.0), (0, 500))},
)

# api.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
