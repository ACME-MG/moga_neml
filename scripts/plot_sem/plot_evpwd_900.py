import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpwdb")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("dummy")
api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("dummy")

params_str = """
6.3647	149.54	0.43913	4.1839	1127.6	2.2016	0.28632	2.7416	1.1882	0.7039	0.082975
6.3647	149.54	0.43913	4.1839	1127.6	6.257	0.89091	6.7308	1.9514	0.28677	2.7726
6.3647	149.54	0.43913	4.1839	1127.6	2.0551	0.23855	2.5203	1.4574	0.21921	3.1674
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

# api.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
