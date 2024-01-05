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
31.327	104.92	0.8548	3.7508	2575.8	1.0369	0.33298	3.661	1.936	0.26542	3.1443
22.393	462.57	0.13573	4.314	1828.1	1.9733	0.27233	3.1234	2.0616	0.0095871	5.4309
11.45	53.151	7.1666	3.9502	2221.6	1.373	0.39922	3.891	3.8787	0.13688	2.6693
37.742	49.123	2.4996	3.4102	3172	2.0438	0.32084	3.3364	8.5211	0.38894	2.7609
18.768	89.18	0.88069	4.5055	1677.4	1.9628	0.35323	3.5571	4.0985	0.05932	2.5132
23.304	306.58	0.32123	4.2592	1822.6	1.6464	0.23887	2.9979	4.1621	0.0029885	2.3425
31.137	31.413	4.6003	3.6958	2583	1.2944	0.36685	3.8721	2.0034	0.2167	2.848
29.726	45.991	2.3174	3.9613	2101.3	1.5924	0.33025	3.5439	2.0625	0.012094	2.7164
0.85682	42.524	9.6283	4.5033	1707	1.2393	0.28849	3.4293	3.0654	0.119	2.6208
4.4611	35.628	31.021	3.6186	3016.2	9.5057	0.33046	3.327	4.6459	0.20498	2.728

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
