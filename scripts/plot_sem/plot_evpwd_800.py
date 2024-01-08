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
4.4611	35.628	31.021	3.6186	3016.2	9.5057	0.33046	3.327	4.6459	0.20498	2.728
4.4611	35.628	31.021	3.6186	3016.2	2.4046	0.25622	3.0598	3.8758	0.47408	3.6607
4.4611	35.628	31.021	3.6186	3016.2	1.2356	0.51763	4.6133	3.3669	0.38282	3.6432
4.4611	35.628	31.021	3.6186	3016.2	2.7457	0.31821	3.2895	6.7714	0.20974	2.9335
4.4611	35.628	31.021	3.6186	3016.2	3.5449	0.60721	4.727	2.4806	0.85454	4.637
4.4611	35.628	31.021	3.6186	3016.2	3.7521	0.55025	4.3437	9.8801	0.076986	2.5808

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
