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
8.3607	16.051	6.8304	4.1208	1027.9	118.84	540.51	572.43	680.2	2.267	16.872
7.044	16.159	6.7949	4.1207	1090	118.84	545.57	572.43	678.83	2.2784	16.872
7.0999	16.172	6.8232	4.151	1052.8	118.11	543.38	572.43	678.81	2.2715	16.868
7.044	16.175	6.7949	4.1207	1089.9	118.84	544.92	584.33	679.35	2.2784	16.872
7.044	16.175	6.7949	4.1207	1081.1	117.69	540.51	572.43	675.3	2.2784	16.872

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
