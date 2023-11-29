import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpwdb")

# api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
# api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
# api.read_data("creep/inl_1/AirBase_800_65_G33.csv")
# api.read_data("creep/inl_1/AirBase_800_60_G32.csv")
# api.read_data("tensile/inl/AirBase_800_D7.csv")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.read_data("tensile/inl/AirBase_900_D10.csv")

params_str = """
4.8238	378.86	0.1423	4.4021	1006.9	1.3282	0.54573	4.6946	3.1679	0.25372	2.5292
"""
# 17.42	217.36	0.33131	2.034	42591	2632.8	4.0648	5.8117
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    # limits_dict = {"creep": ((0, 6000), (0, 0.8)), "tensile": ((0, 0.7), (0, 400))},  # 800
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 0.8), (0, 250))}, # 900
)

api.plot_distribution(
    params_list = params_list,
    # limits_dict = [(-5, 50), (10, 50), (-10)],
    log=True,
)
