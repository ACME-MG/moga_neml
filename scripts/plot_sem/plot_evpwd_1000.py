import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

params_str = """
0.004615	6.1843	2.2823	4.8326	460.27	10.326	67.404	122.39	990.45	0.87756	2.7258
3.9207	130.97	0.16188	3.9466	752.32	9.8931	65.32	266.42	615.81	1.6109	7.1756
0.012675	18.528	0.99367	4.8134	471.18	9.7242	66.13	106.76	770.47	0.82109	2.8892
0.26123	35.054	0.42681	4.7436	490.7	7.9856	55.975	344.42	683.77	1.527	12.105
1.4714	3.11	5.9009	4.4241	584.77	7.3485	51.754	252.12	569.23	1.6585	9.6836
4.1445	21.946	1.2583	3.9467	726.26	8.5299	58.228	186.98	444.68	1.6245	9.6083
3.2085	17.287	1.3622	4.0769	697.16	9.4243	63.606	363.28	725.13	1.6587	9.3212
4.3446	10.148	2.2066	3.8806	776.41	7.9052	54.721	192.78	474.96	1.5705	2.7174
3.3748	51.076	0.45747	4.0575	700.49	7.2333	50.35	251.53	579.58	1.6332	5.6766
4.2665	246.76	0.084953	3.9445	738.14	12.755	80.266	367.62	812.95	1.6497	11.679

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_oxidation()
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_oxidation()
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)
itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("yield_point", yield_stress=90)
itf.add_error("max", "stress")
itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

# red_obj_list = []
# for params in params_list:
#     obj_dict = itf.__controller__.calculate_objectives(*params)
#     red_obj  = itf.__controller__.reduce_objectives(list(obj_dict.values()))
#     red_obj_list.append(red_obj)
# red_index = red_obj_list.index(min(red_obj_list))

red_index = 3

itf.plot_simulation(
    params_list = params_list,
    alpha_list  = [0.2 if i != red_index else 1.0 for i in range(len(params_list))],
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 100), "t_n": (0, 100)},
)
