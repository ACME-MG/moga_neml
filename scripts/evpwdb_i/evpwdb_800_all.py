import sys; sys.path += ["../.."]
from moga_neml.interface import Interface
from constants import PARAM_INDEX

itf = Interface("evpwdb i 800 all", input_path="../data", output_path="../results")

itf.define_model("evpwdb")

params_str = """
17.217	179.74	0.61754	4.4166	1783.5	1.0026	0.41061	4.2331	2.2349	0.29106	3.1743
5.6908	66.627	1.9851	4.7723	1621.6	1.8904	0.54329	4.6088	1.8685	0.093698	2.7472
9.3076	32.596	5.8114	4.5263	1775.9	1.8394	0.71551	5.8657	1.8921	0.34444	3.5433
5.8951	36.245	5.3757	4.7311	1598.4	2.4487	0.36314	3.4647	9.3417	0.10058	3.1582
4.1862	84.548	2.1123	4.7752	1574.3	1.6472	0.34209	3.5358	10.343	0.55238	2.4053
25.038	90.693	0.61002	4.1982	1944.6	1.3414	0.39294	3.9001	4.3861	0.24361	2.9091
27.547	78.081	0.84273	3.8992	2454.8	1.8298	0.44322	4.1135	4.666	0.072485	2.4856
27.885	124.89	0.65636	3.8874	2390.5	1.1933	0.1876	2.4326	2.4598	0.27823	3.0879
19.2	52.204	1.7579	4.5105	1614.6	1.0317	0.54349	5.2065	3.1557	0.27357	3.1248
8.5923	38.904	5.4829	4.4795	1841	2.2498	0.39954	3.722	4.2567	0.19838	3.5486
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
itf.init_params(params_list[PARAM_INDEX])

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
