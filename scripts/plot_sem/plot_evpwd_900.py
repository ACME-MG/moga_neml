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
5.1227	14.129	9.606	4.2421	1089.1	56.117	308.89	129.29	799.25	1.5668	1.985
11.192	16.738	5.9587	3.6369	1530.1	35.196	206.85	119.96	774.72	1.5092	2.5579
9.6829	13.118	13.621	3.5054	1604.4	19.213	129	110.83	868.84	1.0493	2.3566
5.6656	8.2222	14.47	4.3001	1006.2	144.26	644.21	178.5	935.23	10.004	2.8495
7.5309	23.5	5.1998	3.862	1374.9	24.858	154.83	511.79	997.24	2.0041	7.9977
4.8239	389.25	0.18435	4.4133	941.87	44.974	248.15	621.83	913.9	2.4338	7.0609
9.7277	49.011	4.1806	3.4099	1834.3	151.05	657.1	262.5	989.31	1.6647	1.0863
16.262	181.79	0.52517	3.0161	2376.6	29.326	172.8	434.17	894.26	2.192	2.8518
6.3647	183.42	0.44712	4.1839	1075.3	27.326	165.15	422.54	849.67	2.2181	10.568
6.5395	16.732	6.8581	4.1207	1096.5	119.77	547.38	572.3	678.83	2.3506	15.844

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
)
