import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

params_str = """
17.217	179.74	0.61754	4.4166	1783.5	3109.8	4.8245	6.6364
5.6908	66.627	1.9851	4.7723	1621.6	1995	5.4751	6.686
19.2	52.204	1.7579	4.5105	1614.6	1951.3	5.5552	8.4003
31.327	104.92	0.8548	3.7508	2575.8	2126.4	5.3209	6.5504
22.393	462.57	0.13573	4.314	1828.1	1912.9	5.5169	6.9639
11.45	53.151	7.1666	3.9502	2221.6	4188.9	4.3604	4.7172
18.768	89.18	0.88069	4.5055	1677.4	2589.7	5.1066	8.5635
23.304	306.58	0.32123	4.2592	1822.6	2169.1	5.3202	6.8598
31.137	31.413	4.6003	3.6958	2583	2511.7	5.1559	8.7353
29.726	45.991	2.3174	3.9613	2101.3	2259.2	5.3187	8.5096
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("yield_point", yield_stress=291)
itf.add_error("max", "stress")
itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

# red_obj_list = []
# for params in params_list:
#     obj_dict = itf.__controller__.calculate_objectives(*params)
#     red_obj  = itf.__controller__.reduce_objectives(list(obj_dict.values()))
#     red_obj_list.append(red_obj)
# red_index = red_obj_list.index(min(red_obj_list))

red_index = 7

itf.plot_simulation(
    params_list = params_list,
    alpha_list  = [0.2 if i != red_index else 1.0 for i in range(len(params_list))],
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "cd_A": (0, 10000), "cd_xi": (0, 100), "cd_phi": (0, 100)},
)
