import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_900_36_G22.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_31_G50.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_28_G45.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.add_error("dummy")

params_str = """
7.044	16.175	6.7949	4.1207	1090	2.0956	0.37018	3.2638	5.5659	0.16176	2.3751
7.044	16.175	6.7949	4.1207	1090	2.234	0.28666	2.7211	5.4216	0.052496	2.1837
7.044	16.175	6.7949	4.1207	1090	2.2447	0.43215	3.6272	5.3938	0.16179	2.391
7.044	16.175	6.7949	4.1207	1090	2.4833	0.53108	4.1548	5.2406	0.12363	2.3448
7.044	16.175	6.7949	4.1207	1090	2.0994	0.26546	2.6652	8.7854	0.065358	2.122

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
