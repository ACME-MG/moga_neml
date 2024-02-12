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
0.0030429	6.0057	6.3032	4.9738	466.69	95.95	443.77	127.06	817.16	1.5572	0.85064
0.12298	9.1243	3.1519	4.5922	539.1	95.949	262.85	143.39	792.9	1.4623	2.8229
0.10561	6.293	3.16	4.6134	542.91	95.949	273.15	143.87	812.45	1.5283	2.8592
0.0046154	4.8352	4.7828	4.8329	467.34	95.944	269	149.31	883.49	1.1257	2.235
0.004615	6.1843	4.9502	4.8326	460.84	95.945	279.57	144.14	800.16	1.1257	2.2364

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
