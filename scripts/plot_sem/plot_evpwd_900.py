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
16.287	181.45	0.52517	3.0161	2606.2	7.6341	0.55246	7.7807	2.0292	0.31213	2.8618
16.287	181.45	0.52517	3.0161	2606.2	6.2576	0.51718	6.4	1.9986	0.29654	2.7967
16.287	181.45	0.52517	3.0161	2606.2	2.4676	0.51727	3.9828	1.6998	0.0019762	2.3233
16.287	181.45	0.52517	3.0161	2606.2	2.0434	0.31543	2.8725	12.12	0.78594	3.2221
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
