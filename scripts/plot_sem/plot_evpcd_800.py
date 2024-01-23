import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("dummy")

params_str = """
1.9315	481.1	0.021642	4.1572	723.11	5015.3	3.1228	9.163
3.746	8.654	4.2439	3.932	749.09	9246.1	2.7896	5.7472
0.98812	26.958	0.64438	4.4936	567.97	2395	3.552	6.7482
0.34142	0.1263	3.568	4.658	537.81	5130.7	3.1514	9.5031
0.90237	5.2742	1.5201	4.5482	558.2	6762.3	2.971	7.3547
2.2723	17.684	0.52432	4.1895	695.87	4416.4	3.1836	7.1731
1.7845	0.26406	25.678	4.2799	669.49	9702.4	2.8408	8.8194
1.2224	0.036265	6.5932	4.3323	673.71	8825.2	2.8909	9.6678
1.5228	4.8478	3.7315	4.4061	590.03	4508.3	3.1535	6.3638
3.0295	12.903	2.3944	4.0586	713.26	3970.7	3.1777	4.9124

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 600), "evp_d": (0, 40), "evp_n": (0, 5), "evp_eta": (0, 4000),
                   "cd_A": (0, 10000), "cd_xi": (0, 6), "cd_phi": (0, 25)},
)
