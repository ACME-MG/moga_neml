import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

itf = Interface("plot", output_here=True, input_path="../data", output_path="../results")
itf.define_model("evpcd")

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
0.0046173	6.8476	2.2387	4.8326	460.38	2357.9	3.5989	6.8922
3.1901	126.5	0.16925	3.8924	802.2	2253.9	3.6876	11.145
0.31556	4.9177	4.2816	4.8134	468.63	3308.8	3.3387	5.7804
0.26189	37.662	0.20134	4.8079	478.84	2939.9	3.4262	5.9609
1.5332	6.9652	4.9491	4.3072	551.01	1467.1	4.0639	13.561
0.18711	42.057	1.22	3.9495	803.58	1759.6	3.8088	6.9718
3.4416	6.259	1.314	4.0782	707.11	4504.6	3.2162	8.2904
4.5325	14.166	2.2205	3.8813	731.02	2379.1	3.5504	6.0315
3.3203	95.748	0.45552	4.0634	574.87	1034.8	4.2291	6.0322
4.0855	246.68	0.084526	3.9321	776.2	2681.7	3.4426	5.5305

"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

itf.plot_simulation(
    params_list = params_list,
    # clip        = True,
    limits_dict = {"creep": ((0, 8000), (0, 0.35)), "tensile": ((0, 1.0), (0, 160))},
)

itf.plot_distribution(
    params_list = params_list,
    limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 600), "evp_d": (0, 40), "evp_n": (0, 5), "evp_eta": (0, 4000),
                   "cd_A": (0, 10000), "cd_xi": (0, 6), "cd_phi": (0, 25)},
)
