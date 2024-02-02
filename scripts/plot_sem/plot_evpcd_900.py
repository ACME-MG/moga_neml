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
8.7008	379.67	0.15739	4.2166	994.53	1533.4	4.6802	7.0461
9.344	45.972	2.5375	3.4094	1902	2101.5	4.3022	6.1081
3.0011	18.974	32.389	3.2721	2021.2	2356.2	4.4101	17.539
2.1263	19.571	18.852	3.3525	1999.6	2639.8	4.3577	21.825
16.257	181.45	0.5026	3.0154	2606.2	2445.1	4.1307	5.6964
9.5315	149.26	0.37326	3.9582	1254.6	2014.8	4.3854	8.0511
6.4694	149.62	0.29611	4.1942	1123.8	2045.9	4.4272	9.5323
12.617	119.8	0.37544	3.7416	1366.4	1894.5	4.5371	9.6136
11.849	272.72	0.21347	3.8447	1238.3	1731	4.5635	7.4758
7.9997	25.008	2.2597	4.127	1102.2	1841.7	4.5535	10.206

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 600), "evp_d": (0, 40), "evp_n": (0, 5), "evp_eta": (0, 4000),
                   "cd_A": (0, 10000), "cd_xi": (0, 6), "cd_phi": (0, 25)},
)
