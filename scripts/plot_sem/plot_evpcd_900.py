import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("plot", output_here=True, input_path="../data", output_path="../results")
api.define_model("evpcd")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("dummy")
api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("dummy")
api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("dummy")

params_str = """
4.871	11.518	7.0281	4.2421	1138.3	1899.3	4.4974	9.6201
10.692	29.068	2.9831	3.7278	1433.5	1588.8	4.5518	5.8509
11.2	24.262	2.2615	3.9651	1163	1703.2	4.5818	9.0646
11.208	16.738	5.9587	3.6377	1530.1	2070.2	4.3164	7.4964
10.45	14.769	7.8792	3.54	1787.3	4771.9	3.6387	8.3943
11.011	11.071	13.523	3.5672	1593.8	1955.7	4.4015	8.5838
5.6656	8.2222	14.47	4.3001	1000.8	3494.5	3.9569	11.773
"""
params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]

api.plot_predictions(
    params_list = params_list,
    limits_dict = {"creep": ((0, 7000), (0, 0.35)), "tensile": ((0, 1.0), (0, 250))},
)

# api.plot_distribution(
#     params_list = params_list,
#     limits_dict = {"evp_s0": (0, 40), "evp_R": (0, 500), "evp_d": (0, 50), "evp_n": (0, 10), "evp_eta": (0, 4000)},
#     # log=True,
# )
