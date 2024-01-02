import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

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
4.871	11.518	7.0281	4.2421	1138.3	1899.3	4.4974	9.6201
10.692	29.068	2.9831	3.7278	1433.5	1588.8	4.5518	5.8509
11.2	24.262	2.2615	3.9651	1163	1703.2	4.5818	9.0646
11.208	16.738	5.9587	3.6377	1530.1	2070.2	4.3164	7.4964
10.45	14.769	7.8792	3.54	1787.3	4771.9	3.6387	8.3943
11.011	11.071	13.523	3.5672	1593.8	1955.7	4.4015	8.5838
5.6656	8.2222	14.47	4.3001	1000.8	3494.5	3.9569	11.773
15.185	64.875	1.4526	3.2003	2110.6	2312.8	4.1948	6.7274
8.0572	29.804	2.5836	4.0204	1210.4	1624.1	4.5871	7.1367
7.5292	23.505	4.9899	3.8623	1369.1	2070.7	4.3049	6.8212
4.8238	378.86	0.1423	4.4021	1006.9	1532	4.6818	6.5257
7.1037	48.235	4.2972	3.4084	1829.9	2105.1	4.188	3.5083
3.0461	19.608	32.421	3.2736	2022.3	2242.6	4.4061	13.364
4.634	18.607	24.896	3.3436	1999.7	2639.7	4.377	21.834
16.287	181.45	0.52517	3.0161	2606.2	2445.2	4.13	5.8583
9.5313	148.61	0.37484	3.9621	1253.9	2014.6	4.3748	8.0504
6.3647	149.54	0.43913	4.1839	1127.6	1881.2	4.4539	6.9905
12.622	15.441	4.5386	3.7305	1371.6	1850.2	4.526	9.637
12.256	273.68	0.20866	3.8422	1242.3	1723.9	4.5678	7.4751
7.044	16.175	6.7949	4.1207	1090	1699.1	4.5578	8.0541
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
                   "cd_A": (0, 5000), "cd_xi": (0, 10), "cd_phi": (0, 30)},
)
