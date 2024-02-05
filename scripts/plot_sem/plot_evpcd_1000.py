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
3.745	5.5085	10.982	3.9323	723.41	9445.3	2.7645	5.3007
0.34182	3.0001	2.6158	4.5224	605.76	9686.9	2.8177	7.5712
0.74811	4.813	1.5203	4.5427	578.84	5902.3	3.0358	7.2228
2.2985	17.765	0.53407	4.1895	695.87	4582.4	3.1498	6.8538
1.257	4.6817	6.5932	4.2586	671.09	9375.2	2.7983	6.5297
0.54088	3.4417	3.8666	4.4062	640.31	9914.9	2.8044	7.6502
2.9772	13.58	2.2099	4.0601	697.13	2654.7	3.4465	5.4967
0.31556	4.9177	4.2816	4.8134	468.63	3308.8	3.3387	5.7804
0.26189	37.662	0.20134	4.8079	478.84	2939.9	3.4262	5.9609
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
