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
9.3076	32.596	5.8114	4.5263	1775.9	4.7868	38.674	197.2	1.0148	156.11	881.68
9.3076	32.596	5.8114	4.5263	1775.9	7.0573	115.59	648.26	2.1125	260.24	998.91
9.3076	32.596	5.8114	4.5263	1775.9	2.9965	102.62	563.69	5.7802	278.16	710.15
9.3076	32.596	5.8114	4.5263	1775.9	2.8175	99.074	537.13	1.5418	392.78	631.03
9.3076	32.596	5.8114	4.5263	1775.9	6.9431	134.12	751.85	1.3762	217.26	997.61

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000),
#                    "c_n": (0, 20), "c_0": (0, 1), "c_1": (0, 5), "t_n": (0, 20), "t_0": (0, 1), "t_1": (0, 5)},
#     # log=True,
# )
