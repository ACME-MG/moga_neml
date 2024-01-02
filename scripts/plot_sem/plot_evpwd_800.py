import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpwdb")

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.add_error("dummy")
api.read_data("tensile/inl/AirBase_800_D7.csv")
api.add_error("dummy")

params_str = """
0.85682	42.524	9.6283	4.5033	1707	1.5074	0.46747	4.2224	7.0061	0.72074	4.0982
0.85682	42.524	9.6283	4.5033	1707	1.5164	0.53809	4.5782	10.842	0.97196	2.5855
0.85682	42.524	9.6283	4.5033	1707	2.2164	0.67483	5.4836	1.0033	0.22495	3.1484
0.85682	42.524	9.6283	4.5033	1707	4.3629	0.55176	5.0999	1.1569	0.16061	2.726

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# api.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
