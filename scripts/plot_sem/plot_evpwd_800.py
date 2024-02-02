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
18.768	89.18	0.88069	4.5055	1677.4	50.14	314.23	237.66	763.31	2.0077	2.4095
18.768	89.18	0.88069	4.5055	1677.4	37.853	250.25	526.62	906.97	1.9262	12.001
18.768	89.18	0.88069	4.5055	1677.4	143.4	732.37	373.19	989.94	2.0406	1.3773

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
