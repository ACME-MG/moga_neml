import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpcd f 900 st", input_path="../data", output_path="../results")

api.define_model("evpcd")

fixed_params = "7.1037	48.235	4.2972	3.4084	1829.9"
api.fix_params([float(x) for x in fixed_params.split()])

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_31_G50.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_900_28_G45.csv")

api.read_data("creep/inl_1/AirBase_900_26_G59.csv")
api.remove_oxidation()

api.reduce_errors("square_average")
api.reduce_objectives("square_average")

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
