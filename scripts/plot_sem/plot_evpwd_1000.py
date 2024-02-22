import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

params_str = """
0.004615	6.1843	2.2823	4.8326	460.27	7.7189	53.075	240.63	545.4	1.656	8.8478
3.9207	130.97	0.16188	3.9466	752.32	6.4544	45.842	271.13	616.6	1.6568	5.7724
0.012675	18.528	0.99367	4.8134	471.18	7.9505	55.476	281.36	641.18	1.6591	8.0621
0.26123	35.054	0.42681	4.7436	490.7	8.3182	57.604	272.5	625.75	1.657	8.7635
1.4714	3.11	5.9009	4.4241	584.77	7.3485	51.754	252.12	569.23	1.6585	9.6836
4.1445	21.946	1.2583	3.9467	726.26	7.1225	49.66	255.19	580.53	1.6443	9.1841
3.2085	17.287	1.3622	4.0769	697.16	7.0655	49.337	251.91	666.91	1.6585	10.62
4.3446	10.148	2.2066	3.8806	776.41	7.7189	53.075	240.63	745.4	1.656	8.8478
3.3748	51.076	0.45747	4.0575	700.49	8.2016	56.205	265.96	695.48	1.6605	10.322
4.2665	246.76	0.084953	3.9445	738.14	7.4835	51.702	252.58	668.71	1.654	8.1339

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
