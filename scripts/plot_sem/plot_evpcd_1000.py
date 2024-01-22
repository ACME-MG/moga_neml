import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("dummy")

params_str = """
0.004615	6.1843	2.2823	4.8326	460.27	3173	3.4123	7.686
0.004615	6.1843	2.2823	4.8326	460.27	3478.8	3.3414	7.403
0.004615	6.1843	2.2823	4.8326	460.27	3491.9	3.3461	7.3952
0.004615	6.1843	2.2823	4.8326	460.27	2349.8	3.6332	8.8389
0.004615	6.1843	2.2823	4.8326	460.27	3054.6	3.4511	8.5961

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    clip        = True,
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
#                    "cd_A": (0, 5000), "cd_xi": (0, 10), "cd_phi": (0, 30)},
# )
