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

"""

"""
params_str = """
4.2665	246.76	0.084953	3.9445	738.14	69.612	348.59	651.24	742.61	1.5462	10.334
4.2665	246.76	0.084953	3.9445	738.14	164.73	661.49	512.87	911.43	1.6015	7.6116
4.2665	246.76	0.084953	3.9445	738.14	147.84	627.9	587.54	657.35	1.5931	10.203
4.2665	246.76	0.084953	3.9445	738.14	100.91	464.45	278.38	932.3	1.7513	0.85303
4.2665	246.76	0.084953	3.9445	738.14	73.599	358.68	107.99	681.12	0.84391	1.726
4.2665	246.76	0.084953	3.9445	738.14	144.98	611.63	709.38	815.85	1.6985	0.24059
4.2665	246.76	0.084953	3.9445	738.14	133.4	507.2	509.82	811.08	1.8178	5.4432

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
