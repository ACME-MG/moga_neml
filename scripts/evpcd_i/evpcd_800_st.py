import sys; sys.path += ["../.."]
from moga_neml.interface import Interface
from constants import PARAM_INDEX

itf = Interface("evpcd i 800 st", input_path="../data", output_path="../results")

itf.define_model("evpcd")

params_str = """
31.327	104.92	0.8548	3.7508	2575.8	1408.8	6.034	5.1292
22.393	462.57	0.13573	4.314	1828.1	3819.7	4.5826	7.8606
11.45	53.151	7.1666	3.9502	2221.6	4188.9	4.3604	4.7172
37.742	49.123	2.4996	3.4102	3172	4176.1	4.3178	4.5786
18.768	89.18	0.88069	4.5055	1677.4	2973.6	4.9088	8.794
23.304	306.58	0.32123	4.2592	1822.6	1698.6	5.7249	5.5871
31.137	31.413	4.6003	3.6958	2583	3523.9	4.55	4.9625
29.726	45.991	2.3174	3.9613	2101.3	3064.2	4.855	7.1608
0.85682	42.524	9.6283	4.5033	1707	1685.9	5.7223	5.7749
4.4611	35.628	31.021	3.6186	3016.2	2231.9	5.3814	10.492
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
itf.init_params(params_list[PARAM_INDEX])

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
itf.add_error("end", "strain")
itf.add_error("arg_max", "strain", "stress")
itf.add_error("yield", yield_stress=291)

itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

itf.plot_experimental()
itf.set_recorder(10, plot_opt=True, plot_loss=True)
itf.optimise(10000, 100, 50, 0.8, 0.01)