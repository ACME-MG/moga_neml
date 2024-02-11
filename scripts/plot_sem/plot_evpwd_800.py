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
29.73	43.859	3.2743	3.9613	2101.3	32.4	228.95	430.57	764.96	1.5794	19.864
31.91	46.602	2.3174	3.9685	2091.2	32.887	230.31	430.83	854.33	1.6352	19.951
27.875	38.378	4.4409	3.9265	2101.3	32.43	229.94	430.89	764.65	1.6534	19.921
33.249	47.143	2.108	3.9613	2083.5	27.095	195.99	432.15	788.41	1.652	19.973
29.606	46.499	4.8371	3.9608	1525	32.92	232.72	371.79	764.18	1.6504	19.93
34.303	44.988	2.3189	3.9613	1967.2	33.585	234.01	400.05	856.26	1.6599	19.943

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
