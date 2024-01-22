import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_900_36_G22.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_31_G50.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_28_G45.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.add_error("dummy")

params_str = """
10.692	29.068	2.9831	3.7278	1433.5	2.5967	44.025	259.35	6.7335	364.63	719.77
10.692	29.068	2.9831	3.7278	1433.5	2.2438	43.292	264.01	4.6216	937.78	992.85
10.692	29.068	2.9831	3.7278	1433.5	2.5726	39.986	242.95	14.221	419.94	879.74
10.692	29.068	2.9831	3.7278	1433.5	2.0232	42.145	260.6	19.866	783.6	864.93
10.692	29.068	2.9831	3.7278	1433.5	2.5541	75.207	433.72	2.9771	178.38	794.02

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    # limits_dict = {"creep": ((0, 20000), (0, 0.50)), "tensile": ((0, 1.0), (0, 250))},
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
