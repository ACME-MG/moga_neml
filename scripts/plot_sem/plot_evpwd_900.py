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
7.044	16.175	6.7949	4.1207	1090	118.84	540.51	572.43	678.83	2.2784	16.872
7.044	16.175	6.7949	4.1207	1090	77.6	394.27	586.27	973.85	2.0788	16.11
7.044	16.175	6.7949	4.1207	1090	95.888	463.78	472.86	676.54	2.1587	15.21
7.044	16.175	6.7949	4.1207	1090	52.446	290.34	305.27	724.56	2.0111	2.8957
7.044	16.175	6.7949	4.1207	1090	158.77	678.25	307.66	984.99	2.2715	0.85277
7.044	16.175	6.7949	4.1207	1090	50.569	275.72	532.51	747.69	2.2795	6.4318
7.044	16.175	6.7949	4.1207	1090	72.689	372.74	384.69	773.94	2.1162	10.932

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
