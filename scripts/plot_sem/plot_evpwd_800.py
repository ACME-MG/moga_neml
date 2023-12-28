import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpwdb")

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
18.768	89.18	0.88069	4.5055	1677.4	1.9628	0.35323	3.5571	4.0985	0.05932	2.5132
18.768	89.18	0.88069	4.5055	1677.4	2.0849	0.21866	2.8095	11.717	0.1914	3.3398
18.768	89.18	0.88069	4.5055	1677.4	1.0046	0.4349	6.408	1.6682	0.3255	3.4685
18.768	89.18	0.88069	4.5055	1677.4	1.9834	0.30295	3.2772	6.6388	0.40108	0.96951

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
