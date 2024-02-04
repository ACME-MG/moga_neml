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
0.004615	6.1843	2.2823	4.8326	460.27	95.945	455.06	144.67	804.12	1.1257	2.212
3.9207	130.97	0.16188	3.9466	752.32	41.394	219.89	47.172	291.43	4.5824	1.806
0.012675	18.528	0.99367	4.8134	471.18	64.659	330.07	176.31	409.25	1.6171	3.8136
0.26123	35.054	0.42681	4.7436	490.7	6.877	51.307	271.4	601.55	1.5584	9.5123
1.4714	3.11	5.9009	4.4241	584.77	172.19	693.66	175.36	903.63	3.9591	1.9576
4.1445	21.946	1.2583	3.9467	726.26	111.62	502.2	509.49	969.18	1.5902	13.461
3.2085	17.287	1.3622	4.0769	697.16	136.85	584.7	669.43	983.14	1.6515	5.8275
4.3446	10.148	2.2066	3.8806	776.41	178.93	713.6	182.86	794.32	7.1326	1.7726
3.3748	51.076	0.45747	4.0575	700.49	137.86	593.98	777.75	978.49	1.4766	11.635
4.2665	246.76	0.084953	3.9445	738.14	69.612	348.59	651.24	742.61	1.5462	10.334

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
