import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpcd")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
# api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
# api.add_error("dummy")
api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("dummy")

params_str = """
3.6262	13.804	6.9825	4.2416	1138.2	1986	4.4408	9.193
10.683	31.381	2.9727	3.7155	1422	1626.7	4.552	6.2319
10.341	24.476	2.3226	3.9651	1176.4	1743	4.5865	9.1587
11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225
8.0818	9.2744	7.9562	3.9839	1310.7	4972.4	3.6443	9.6707
11.394	13.887	7.532	3.5691	1581.2	1959.8	4.4121	8.5847
5.6656	7.6357	9.1337	4.3001	1055.4	3494.5	3.9629	11.623
15.177	64.875	1.1737	3.2003	2165.3	2320.3	4.1948	6.7274
8.0268	28.899	2.5811	4.018	1213.4	1698.5	4.5711	7.3221
8.0846	21.623	4.9985	3.8734	1330.8	2586.3	4.0925	6.8218
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

api.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

api.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
                   "cd_A": (0, 5000), "cd_xi": (0, 10), "cd_phi": (0, 30)},
)
