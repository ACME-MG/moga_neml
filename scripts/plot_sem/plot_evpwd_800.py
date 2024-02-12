import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

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
16.78	98.973	0.60186	4.4156	1780.3	92.942	466.64	124.21	627.18	5.7007	2.1874
5.6925	67.1	1.8542	4.7721	1621.6	72.41	404.77	243.19	619.93	2.4798	11.411
19.2	52.605	1.542	4.5105	1614.6	42.528	267.95	334.54	705.42	2.4141	9.9943
31.327	105.29	0.8549	3.7256	2576.7	54.271	333.56	307.45	694.47	1.9991	6.8035
22.154	462.34	0.17408	4.314	1828.1	40.1	260.65	408.44	853.65	1.9241	7.7562
11.45	53.135	7.1795	3.9502	2205.4	30.864	224.62	340.9	729.26	1.3505	6.6858
19.025	97.214	0.88069	4.5055	1667.4	50.238	313.98	237.66	764.67	2.0071	2.7731
24	301.54	0.32008	4.2863	1836.9	23.714	176.69	323.4	686.91	1.6048	13.085
27.852	31.391	9.837	3.6958	2458	31.947	224.92	521.29	982.66	1.5924	18.309
29.914	48.373	2.3508	3.9615	2094.7	27.335	200.15	367.9	765.16	1.639	19.667

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.7)), "tensile": ((0, 1.0), (0, 500))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
)
