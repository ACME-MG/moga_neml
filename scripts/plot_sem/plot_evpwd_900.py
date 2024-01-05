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
4.8238	378.86	0.1423	4.4021	1006.9	1.3282	0.54573	4.6946	3.1679	0.25372	2.5292
7.1037	48.235	4.2972	3.4084	1829.9	1.3602	0.34182	3.1635	12.426	0.21156	3.3578
3.0461	19.608	32.421	3.2736	2022.3	1.9328	0.593	4.7255	2.6515	0.25479	2.5724
4.634	18.607	24.896	3.3436	1999.7	2.2488	0.2734	2.6326	4.8822	0.17643	2.3942
16.287	181.45	0.52517	3.0161	2606.2	7.6341	0.55246	7.7807	2.0292	0.31213	2.8618
9.5313	148.61	0.37484	3.9621	1253.9	2.5961	0.27946	2.6425	1.018	0.10278	2.3904
6.3647	149.54	0.43913	4.1839	1127.6	2.2016	0.28632	2.7416	1.1882	0.7039	0.082975
12.622	15.441	4.5386	3.7305	1371.6	2.186	0.20261	2.2958	8.5666	0.39078	2.7238
12.256	273.68	0.20866	3.8422	1242.3	1.8719	0.38353	3.4465	3.8253	0.19616	2.4364
7.044	16.175	6.7949	4.1207	1090	2.2447	0.43215	3.6272	5.3938	0.16179	2.391

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
