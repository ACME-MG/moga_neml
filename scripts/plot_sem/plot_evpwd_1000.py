import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_oxidation()
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("dummy")

params_str = """
0.004615	6.1843	2.2823	4.8326	460.27	7.2738	50.913	269.77	601.74	1.564	8.739
3.9207	130.97	0.16188	3.9466	752.32	7.2738	50.913	269.77	601.74	1.564	8.739
0.012675	18.528	0.99367	4.8134	471.18	7.2738	50.913	269.77	601.74	1.564	8.739
0.26123	35.054	0.42681	4.7436	490.7	7.2738	50.913	269.77	601.74	1.564	8.739
1.4714	3.11	5.9009	4.4241	584.77	7.2738	50.913	269.77	601.74	1.564	8.739
4.1445	21.946	1.2583	3.9467	726.26	7.2738	50.913	269.77	601.74	1.564	8.739
3.2085	17.287	1.3622	4.0769	697.16	7.2738	50.913	269.77	601.74	1.564	8.739
4.3446	10.148	2.2066	3.8806	776.41	7.2738	50.913	269.77	601.74	1.564	8.739
3.3748	51.076	0.45747	4.0575	700.49	7.2738	50.913	269.77	601.74	1.564	8.739
4.2665	246.76	0.084953	3.9445	738.14	7.2738	50.913	269.77	601.74	1.564	8.739

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
)
