import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

params_str = """
1.2518	9.8124	49.627	4.9187	624.33	43.763	254.46	574.01	736.95	2.0636	49.521
0.20234	6.1326	0.0083622	5.2211	694.11	183.37	814.61	628.33	975.6	47.34	33.166
0.37696	9.067	0.050897	5.0266	777.46	89.539	468.99	588.44	811.98	86.48	18.617
8.5344	99.539	1.0497	3.5986	1869.5	279.46	973.95	556.53	981.98	2.1539	66.008
0.1847	0.00078914	62.764	4.9218	839.41	128.22	621.02	685.59	729.81	89.516	0.25781
1.2379	0.1221	41.206	5.8822	450.74	25.989	159.57	488.28	785.3	29.609	98.739
0.066496	730.95	0.00082174	5.029	783.48	2.5062	23.734	301.84	869.76	27.671	75.01
5.67E-06	0.000343	0.0085455	9.5827	145.71	6.4182	53.594	547.92	501.65	98.415	66.256
3.5302	123.6	0.0010834	4.6406	912.66	189.85	27.191	532.92	789.28	94.469	0.036985
6.7341	348.92	0.1137	3.6098	2088.4	176.56	35.189	618.72	938.12	84.855	70.677

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_900_36_G22.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")
itf.read_data("creep/inl_1/AirBase_900_31_G50.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")
itf.read_data("creep/inl_1/AirBase_900_28_G45.csv")
itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.remove_oxidation()
itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("yield_point", yield_stress=164)
itf.add_error("max", "stress")
itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

# red_obj_list = []
# for params in params_list:
#     obj_dict = itf.__controller__.calculate_objectives(*params)
#     red_obj  = itf.__controller__.reduce_objectives(list(obj_dict.values()))
#     red_obj_list.append(red_obj)
# red_index = red_obj_list.index(min(red_obj_list))
red_index = 8

itf.plot_simulation(
    params_list = params_list,
    alpha_list  = [0.2 if i != red_index else 1.0 for i in range(len(params_list))],
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 100), "t_n": (0, 100)},
)
