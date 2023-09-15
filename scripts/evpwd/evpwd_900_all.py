import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpwd 900 all", input_path="../data", output_path="../results")

api.define_model("evpwd")

# api.fix_param("evp_s0",  3.14e1)
# api.fix_param("evp_R",   1.40e1)
# api.fix_param("evp_d",   1.00e1)
# api.fix_param("evp_n",   2.87e0)
# api.fix_param("evp_eta", 9.93e3)

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end_value", "time")
api.add_error("end_value", "strain")
api.add_error("damage")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end_value", "time")
api.add_error("end_value", "strain")
api.add_error("damage")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("area", "time", "strain")
api.add_error("end_value", "time")
api.add_error("end_value", "strain")
api.add_error("damage")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("area", "time", "strain")
api.add_error("end_value", "time")
api.add_error("end_value", "strain")
api.add_error("damage")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(50, 10, True)
api.optimise(10000, 100, 50, 0.65, 0.35)
