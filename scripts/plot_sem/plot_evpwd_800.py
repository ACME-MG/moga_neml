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
25.038	90.693	0.61002	4.1982	1944.6	1.3414	0.39294	3.9001	4.3861	0.24361	2.9091
25.038	90.693	0.61002	4.1982	1944.6	1.6014	0.36698	3.6794	1.284	0.35039	4.3111
25.038	90.693	0.61002	4.1982	1944.6	1.6385	0.31782	3.3939	1.0134	0.01092	2.2708
25.038	90.693	0.61002	4.1982	1944.6	10.255	0.71789	5.3785	1.5834	0.31965	3.6119
25.038	90.693	0.61002	4.1982	1944.6	1.9335	0.70083	5.3671	5.0886	0.028529	2.4187

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
