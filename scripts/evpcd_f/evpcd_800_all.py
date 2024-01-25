import sys; sys.path += ["../.."]
from moga_neml.interface import Interface
from constants import PARAM_INDEX

itf = Interface("evpcd f 800 all", input_path="../data", output_path="../results")

itf.define_model("evpcd")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5
5.6908	66.627	1.9851	4.7723	1621.6
9.3076	32.596	5.8114	4.5263	1775.9
5.8951	36.245	5.3757	4.7311	1598.4
4.1862	84.548	2.1123	4.7752	1574.3
25.038	90.693	0.61002	4.1982	1944.6
27.547	78.081	0.84273	3.8992	2454.8
27.885	124.89	0.65636	3.8874	2390.5
19.2	52.204	1.7579	4.5105	1614.6
8.5923	38.904	5.4829	4.4795	1841
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
itf.fix_params(params_list[PARAM_INDEX])

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
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

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
