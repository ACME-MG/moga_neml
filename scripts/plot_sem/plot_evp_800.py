import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evp")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.remove_damage()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.remove_damage()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.remove_damage(0.1, 0.7)
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.remove_damage(0.1, 0.7)
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.remove_manual("strain", 0.3)
itf.add_error("dummy")

params_str = """
1.9315	481.1	0.021642	4.1572	723.11
3.746	8.654	4.2439	3.932	749.09
0.98812	26.958	0.64438	4.4936	567.97
0.34142	0.1263	3.568	4.658	537.81
0.90237	5.2742	1.5201	4.5482	558.2
2.2723	17.684	0.52432	4.1895	695.87
1.7845	0.26406	25.678	4.2799	669.49
1.2224	0.036265	6.5932	4.3323	673.71
1.5228	4.8478	3.7315	4.4061	590.03
3.0295	12.903	2.3944	4.0586	713.26

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    clip        = True,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 600), "evp_d": (0, 40), "evp_n": (0, 5), "evp_eta": (0, 4000)},
)
