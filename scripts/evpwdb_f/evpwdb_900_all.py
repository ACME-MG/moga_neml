import sys; sys.path += ["../.."]
from moga_neml.interface import Interface
from constants import PARAM_INDEX

itf = Interface("evpwdb f 900 all", input_path="../data", output_path="../results")

itf.define_model("evpwdb")

params_str = """
4.871	11.518	7.0281	4.2421	1138.3
10.692	29.068	2.9831	3.7278	1433.5
11.2	24.262	2.2615	3.9651	1163
11.208	16.738	5.9587	3.6377	1530.1
10.45	14.769	7.8792	3.54	1787.3
11.011	11.071	13.523	3.5672	1593.8
5.6656	8.2222	14.47	4.3001	1000.8
15.185	64.875	1.4526	3.2003	2110.6
8.0572	29.804	2.5836	4.0204	1210.4
7.5292	23.505	4.9899	3.8623	1369.1
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
itf.fix_params(params_list[PARAM_INDEX])

itf.read_data("creep/inl_1/AirBase_900_36_G22.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_900_31_G50.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_900_28_G45.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_900_26_G59.csv")
itf.remove_oxidation()
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
# itf.add_error("damage")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("tensile/inl/AirBase_900_D10.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("end", "strain", weight=0.5)
itf.add_error("arg_max", "strain", "stress", weight=0.5)
itf.add_error("yield", yield_stress=164)
# itf.add_error("end", "stress")

itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")
# itf.group_errors(name=True, type=False, labels=True)

itf.plot_experimental()
itf.set_recorder(10, plot_opt=True, plot_loss=True)
itf.optimise(10000, 100, 50, 0.8, 0.01)
