import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evp")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_manual("time", 900*3600)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_manual("time", 1800*3600)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_manual("time", 2100*3600)
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_manual("time", 2500*3600)
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("dummy")

params_str = """
1.9315	481.1	0.021642	4.1572	723.11
3.746	8.654	4.2439	3.932	749.09
0.004615	6.1843	2.2823	4.8326	460.27
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    clip        = True,
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
)
