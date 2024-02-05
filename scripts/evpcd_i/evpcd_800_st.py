import sys; sys.path += ["../.."]
from moga_neml.interface import Interface
from constants import PARAM_INDEX

itf = Interface("evpcd i 800 st", input_path="../data", output_path="../results")

itf.define_model("evpcd")

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