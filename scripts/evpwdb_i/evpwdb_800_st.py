import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("evpwdb i 800 st", input_path="../data", output_path="../results")

itf.define_model("evpwdb")

params_str = """
31.327	104.92	0.8548	3.7508	2575.8	1.0369	0.33298	3.661	1.936	0.26542	3.1443
22.393	462.57	0.13573	4.314	1828.1	1.9733	0.27233	3.1234	2.0616	0.0095871	5.4309
11.45	53.151	7.1666	3.9502	2221.6	1.373	0.39922	3.891	3.8787	0.13688	2.6693
37.742	49.123	2.4996	3.4102	3172	1.0524	0.68115	6.5024	1.6216	0.19822	2.7773
18.768	89.18	0.88069	4.5055	1677.4	1.9628	0.35323	3.5571	4.0985	0.05932	2.5132
23.304	306.58	0.32123	4.2592	1822.6	1.6464	0.23887	2.9979	4.1621	0.0029885	2.3425
31.137	31.413	4.6003	3.6958	2583	1.2944	0.36685	3.8721	2.0034	0.2167	2.848
29.726	45.991	2.3174	3.9613	2101.3	1.617	0.27363	3.2206	5.6995	0.96151	3.9527
0.85682	42.524	9.6283	4.5033	1707	1.2393	0.28849	3.4293	3.0654	0.119	2.6208
4.4611	35.628	31.021	3.6186	3016.2	9.5057	0.33046	3.327	4.6459	0.20498	2.728
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
itf.init_params(params_list[1])

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("end", "strain", weight=0.5)
itf.add_error("arg_max", "strain", "stress", weight=0.5)
itf.add_error("yield", yield_stress=291)
# itf.add_error("end", "stress")

itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")
# itf.group_errors(name=True, type=False, labels=True)

itf.plot_experimental()
itf.set_recorder(10, plot_opt=True, plot_loss=True)
itf.optimise(10000, 100, 50, 0.8, 0.01)
