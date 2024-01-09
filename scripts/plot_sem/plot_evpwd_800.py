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
5.6908	66.627	1.9851	4.7723	1621.6	1.8904	0.54329	4.6088	1.8685	0.093698	2.7472
5.6855	66.629	1.9915	4.7744	1679.7	1.8968	0.54329	4.5386	2.1025	0.048689	2.7472
5.5669	66.62	1.9668	4.7337	1621.6	1.8917	0.54077	4.6878	1.2908	0.13542	2.5828
5.6954	66.388	1.8568	4.8045	1649.1	1.9303	0.56396	4.6088	2.7125	0.094427	2.5427
5.6448	66.626	1.9578	4.7929	1621.6	2.2281	0.57036	4.6041	1.275	0.093493	2.7719

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
