import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd i 800 all", input_path="../data", output_path="../results")

api.define_model("evpcd")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5	3109.8	4.8245	6.6364
5.6908	66.627	1.9851	4.7723	1621.6	1995	5.4751	6.686
9.3076	32.596	5.8114	4.5263	1775.9	2723.1	5.0412	9.5797
5.8951	36.245	5.3757	4.7311	1598.4	2223.9	5.2809	6.7355
4.1862	84.548	2.1123	4.7752	1574.3	2883.2	4.8534	4.6837
25.038	90.693	0.61002	4.1982	1944.6	2654.9	5.1296	10.248
27.547	78.081	0.84273	3.8992	2454.8	2960.7	4.9867	10.836
27.885	124.89	0.65636	3.8874	2390.5	2711.4	5.0382	7.7607
19.2	52.204	1.7579	4.5105	1614.6	1951.3	5.5552	8.4003
8.5923	38.904	5.4829	4.4795	1841	2195.8	5.3108	6.956
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
api.init_params(params_list[7])

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("tensile/inl/AirBase_800_D7.csv")
api.add_error("area", "strain", "stress")
api.add_error("end", "strain", weight=0.5)
api.add_error("arg_max", "strain", "stress", weight=0.5)
api.add_error("yield", yield_stress=291)

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, plot_opt=True, plot_loss=True)
api.optimise(10000, 100, 50, 0.8, 0.01)
