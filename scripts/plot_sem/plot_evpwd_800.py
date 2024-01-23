import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("dummy")

params_str = """
10.692	29.068	2.9831	3.7278	1433.5	2.458	46.876	283.24	9.6821	483.84	931.11
10.692	29.068	2.9831	3.7278	1433.5	7.0266	148.29	400.81	3.3555	471.57	987.55
10.692	29.068	2.9831	3.7278	1433.5	2.5967	44.025	259.35	6.7335	364.63	719.77
10.692	29.068	2.9831	3.7278	1433.5	2.5726	39.986	242.95	14.221	419.94	879.74
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
#                    "c_n": (0, 20), "c_0": (0, 1), "c_1": (0, 5), "t_n": (0, 20), "t_0": (0, 1), "t_1": (0, 5)},
#     # log=True,
# )
