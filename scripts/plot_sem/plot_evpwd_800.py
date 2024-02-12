import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("dummy")

params_str = """
31.91	46.602	2.3174	3.9685	2091.2	32.887	230.31	430.83	854.33	1.6352	19.951
28.496	31.593	3.2744	3.9474	2101.3	32.4	214.35	386.41	790.69	2.3459	19.997
29.564	43.11	2.9139	3.9613	2112.4	32.432	230.15	430.96	780.08	1.6499	19.91
29.737	46.145	2.4195	3.9613	2101.8	32.67	230.13	430.89	762.5	1.6549	19.93
30.149	46.328	2.3812	3.9779	2145.9	31.855	223.98	367.44	762.57	1.6215	19.929
29.726	55.667	2.1292	3.9613	2109.3	32.401	228.3	430.89	764.21	1.6536	19.93

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
#                    "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
# )
