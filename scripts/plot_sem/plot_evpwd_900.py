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
6.5395	16.732	6.8581	4.1207	1096.5	119.77	547.38	572.3	678.83	2.3506	15.844
10.431	29.083	6.7096	3.6244	949.01	114.11	523.37	568.99	675.16	1.9581	16.209
7.0411	16.589	14.937	4.1207	1092.3	114.2	540.48	572.43	678.82	1.4337	16.872
5.7198	15.768	6.7957	5.0945	701.79	90.987	479.52	728.55	678.98	0.9403	16.877
16.702	39.245	6.8125	3.4592	1010.3	70.276	387.78	570.02	678.82	0.85265	16.872
7.0439	46.174	6.7853	4.1644	1086	92.909	471.07	572.45	678.83	0.85907	16.892

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
