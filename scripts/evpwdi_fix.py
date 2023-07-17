import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpwdi all fix x_end")
api.define_model("evpwdi")

api.fix_param("evp_s0",  4.871e0)
api.fix_param("evp_R",   1.152e1)
api.fix_param("evp_d",   7.028e0)
api.fix_param("evp_n",   4.242e0)
api.fix_param("evp_eta", 1.138e3)

api.read_data("tensile/inl/AirBase_900_D10.csv")
api.add_error("y_area", "strain", "stress")
api.add_error("damage")
api.add_error("yield")
api.add_error("x_end", "stress")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time")
api.add_error("x_end", "strain")
api.add_error("damage")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time")
api.add_error("x_end", "strain")
api.add_error("damage")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time")
api.add_error("x_end", "strain")
api.add_error("damage")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()
api.add_error("y_area", "time", "strain")
api.add_error("x_end", "time")
api.add_error("x_end", "strain")
api.add_error("damage")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.set_recorder(10, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)
