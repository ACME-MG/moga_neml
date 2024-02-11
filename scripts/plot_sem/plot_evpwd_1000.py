import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpwdb")

itf.read_data("creep/inl_1/AirBase_1000_16_G18.csv")
itf.remove_oxidation()
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_13_G30.csv")
itf.remove_oxidation(0.1, 0.7)
itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_12_G48.csv")
itf.remove_oxidation()
# itf.add_error("dummy")
itf.read_data("creep/inl_1/AirBase_1000_11_G39.csv")
itf.remove_oxidation(0.1, 0.7)
# itf.add_error("dummy")
itf.read_data("tensile/inl/AirBase_1000_D12.csv")
itf.add_error("dummy")

params_str = """
0.41121	8.3185	1.5488	4.8286	468.32	91.109	420.27	145.97	814.06	1.1305	2.2793
4.2741	163.31	0.37485	3.8721	766.51	41.394	218.54	47.517	291.43	4.5815	1.2543
0.012678	46.239	1.2403	4.7068	484.03	70.913	331.34	176.66	409.91	1.605	3.8136
0.036912	49.598	0.89182	4.7436	485.16	7.2738	50.913	269.77	601.74	1.564	8.739
0.70825	8.46	5.8882	4.4476	580.37	179.7	686.62	184.92	898.32	3.9585	1.5713
0.35996	30.971	4.9037	3.95	685.6	118.29	499.25	428.38	969.45	1.1971	13.733
0.48125	40.947	4.9225	4.0867	658	136.71	543.66	663.82	983.11	0.8828	5.8177
4.1412	50.155	3.0378	3.8809	705.19	178.99	671.24	181.75	794.11	7.1307	0.83784
2.1605	63.978	0.84965	3.9678	701.83	145.06	551.14	772.16	978.5	2.1997	11.635
1.6011	196.8	0.53121	3.9438	706.71	115.92	468.23	654.29	742.61	1.5462	10.334

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 100), "evp_R": (0, 1000), "evp_d": (0, 100), "evp_n": (0, 100), "evp_eta": (0, 10000),
                   "c_0": (0, 1000), "c_1": (0, 1000), "t_0": (0, 1000), "t_1": (0, 1000), "c_n": (0, 20), "t_n": (0, 20)},
)
