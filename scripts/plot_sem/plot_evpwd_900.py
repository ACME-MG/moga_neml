import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_900_36_G22.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_31_G50.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_28_G45.csv")
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.remove_oxidation()
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.add_error("dummy")

params_str = """
4.871	11.518	7.0281	4.2421	1138.3	70.744	372.25	129.2	799.23	1.5445	1.985
11.208	16.738	5.9587	3.6377	1530.1	35.196	206.85	120.11	774.72	1.494	2.7056
11.011	11.071	13.523	3.5672	1593.8	19.302	129.2	110.84	863	1.0022	2.3519
5.6656	8.2222	14.47	4.3001	1000.8	144.26	644.21	178.5	935.33	10.004	2.8495
7.5292	23.505	4.9899	3.8623	1369.1	24.327	153.59	513.02	958.93	2.0041	7.9154
4.8238	378.86	0.1423	4.4021	1006.9	44.823	247.59	621.83	914.87	2.4657	6.7609
7.1037	48.235	4.2972	3.4084	1829.9	148.52	657.13	264.15	989.31	1.6649	1.0629
16.287	181.45	0.52517	3.0161	2606.2	29.887	171.78	434.24	894.26	2.192	2.8378
6.3647	149.54	0.43913	4.1839	1127.6	27.188	165.15	422.54	852.26	2.2181	10.67
7.044	16.175	6.7949	4.1207	1090	118.84	540.51	572.43	678.83	2.2784	16.872
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 600), "evp_d": (0, 40), "evp_n": (0, 5), "evp_eta": (0, 4000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
)
