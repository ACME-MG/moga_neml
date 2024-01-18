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
4.871	11.518	7.0281	4.2421	1138.3	2.3686	44.152	268.35	6.2109	792.75	736.88
4.871	11.518	7.0281	4.2421	1138.3	6.9671	39.733	230.37	11.257	370.51	701.98
4.871	11.518	7.0281	4.2421	1138.3	1.6383	97.283	551.73	5.8218	205.44	960.96
4.871	11.518	7.0281	4.2421	1138.3	6.7179	198.85	597.73	7.206	417.21	692.63
4.871	11.518	7.0281	4.2421	1138.3	1.8284	56.416	340.6	12.401	644.04	765.58

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulations(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
