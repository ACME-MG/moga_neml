import sys; sys.path += ["../.."]
from moga_neml.interface import Interface
from constants import PARAM_INDEX

itf = Interface("evpcd i 1000 all", input_path="../data", output_path="../results")

itf.define_model("evpcd")

params_str = """
1.9315	481.1	0.021642	4.1572	723.11	3740	3.2786	7.5526
3.746	8.654	4.2439	3.932	749.09	9410	2.7617	5.2934
0.98812	26.958	0.64438	4.4936	567.97	1468.2	3.8722	6.1178
0.34142	0.1263	3.568	4.658	537.81	9589.8	2.8539	9.4673
0.90237	5.2742	1.5201	4.5482	558.2	5918.3	3.0358	7.2259
2.2723	17.684	0.52432	4.1895	695.87	4582.3	3.1498	7.1169
1.7845	0.26406	25.678	4.2799	669.49	9813.7	2.8523	10.242
1.2224	0.036265	6.5932	4.3323	673.71	9449.6	2.8869	11.575
1.5228	4.8478	3.7315	4.4061	590.03	9411	2.8044	6.3835
3.0295	12.903	2.3944	4.0586	713.26	1346.8	3.9352	5.4934
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
itf.init_params(params_list[PARAM_INDEX])

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
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("end", "strain")
itf.add_error("arg_max", "strain", "stress")
itf.add_error("yield", yield_stress=90)

itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

itf.plot_experimental()
itf.set_recorder(10, plot_opt=True, plot_loss=True)
itf.optimise(10000, 100, 50, 0.8, 0.01)
