import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

params_str = """
0.023943	73.076	0.0066875	5.0105	421.85	22.441	144.96	76.857	514.97	1.0336	9.6948
0.032304	890.58	2.06E-05	5.0037	440.67	5.2019	43.745	92.32	615.97	0.85094	37.585
0.16481	64.15	0.93214	4.9116	392.67	6.3168	45.084	261.32	607.53	1.5262	10.92
0.24772	894.83	0.15911	4.6699	475.07	34.091	183.41	216.56	575.62	0.84345	16.566
0.046558	7.3716	1.1796	4.8322	451.65	7.7491	58.418	102.61	723.39	0.79773	4.7677
8.1741	68.411	0.20474	2.9444	1772.2	7.0535	50.98	69.698	499.97	1.0324	2.7457
0.014379	88.424	2.3588	3.6449	1040.4	17.512	103.09	247.97	592.26	1.0116	9.317
0.11829	2.771	6.9302	4.6814	499.29	5.395	40.405	95.159	665.5	1.0548	7.321
0.030026	6.0735	21.152	4.3616	543.33	24.619	139.5	292.59	544.99	2.0265	13.93
1.1446	234.68	0.77954	3.7372	1082.7	46.989	231.14	195.38	488.42	0.93456	33.598

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
