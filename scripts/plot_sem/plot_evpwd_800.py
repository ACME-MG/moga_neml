import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

params_str = """
2.0075	18.868	40.829	5.23	1080.5	83.223	506.32	431.59	687.99	99.233	79.532
1.0397	28.767	27.691	5.0763	984.17	113.4	625.86	784.14	735.86	85.061	26.917
2.5553	135.47	0.21264	4.4933	2254.1	255.4	7.239	606.06	427.14	78.389	45.302
3.7021	133.93	0.20074	4.2894	2588.8	224.52	4.4659	574.01	630.47	50.254	86.105
1.0775	45.42	0.64926	4.4738	2325.8	368.67	44.356	687.7	661.59	84.682	4.5493
38.129	76.572	0.74794	2.7822	7953	60.933	16.437	992.99	674.16	90.013	58.749
26.328	321.14	0.1796	3.118	6107.7	72.702	27.213	847.88	760.18	87.056	43.722
1.944	482.25	0.051481	4.596	2100.6	237.28	54.271	910.26	791.97	79.06	57.186
31.832	476.26	0.029354	4.2947	1515.8	258.91	23.016	670	695.4	97.515	18.749
3.587	496.18	0.05223	4.5264	2167.8	77.321	0.71048	922.66	818.1	57.133	76.646

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

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

red_obj_list = []
for params in params_list:
    obj_dict = itf.__controller__.calculate_objectives(*params)
    red_obj  = itf.__controller__.reduce_objectives(list(obj_dict.values()))
    red_obj_list.append(red_obj)
red_index = red_obj_list.index(min(red_obj_list))

itf.plot_simulation(
    params_list = params_list,
    alpha_list  = [0.2 if i != red_index else 1.0 for i in range(len(params_list))],
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

# itf.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
#                    "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 100), "t_n": (0, 100)},
# )
