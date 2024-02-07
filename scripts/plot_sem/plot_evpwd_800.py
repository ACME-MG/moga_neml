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
4.871	11.518	7.0281	4.2421	1138.3	70.744	372.25	129.2	799.23	1.5445	1.985
4.871	11.518	7.0281	4.2421	1138.3	59.282	306.69	415.18	946.11	2.7542	0.16406
4.871	11.518	7.0281	4.2421	1138.3	53.862	283.32	212.39	774.22	2.7708	1.0411
4.871	11.518	7.0281	4.2421	1138.3	51.859	282.26	925.08	968.62	2.4075	5.8037
4.871	11.518	7.0281	4.2421	1138.3	66.579	319.64	101.6	513.08	15.408	1.0626
4.871	11.518	7.0281	4.2421	1138.3	73.858	355.03	417.03	960.25	3.215	0.29919
4.871	11.518	7.0281	4.2421	1138.3	106.1	491.72	554.45	963.91	2.5307	7.5245

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
