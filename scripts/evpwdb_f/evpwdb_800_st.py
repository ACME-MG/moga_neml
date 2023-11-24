import sys; sys.path += ["../.."]
from moga_neml.api import API

api = API("evpwdb f 800 st", input_path="../data", output_path="../results")

api.define_model("evpwdb")

fixed_params = "31.327	104.92	0.8548	3.7508	2575.8"
api.fix_params([float(x) for x in fixed_params.split()])

api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
# api.add_error("damage")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_70_G44.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")
# api.add_error("damage")
api.add_constraint("inc_end", "strain")
api.add_constraint("dec_end", "time")

api.read_data("creep/inl_1/AirBase_800_65_G33.csv")

api.read_data("creep/inl_1/AirBase_800_60_G32.csv")

api.read_data("tensile/inl/AirBase_800_D7.csv")
api.add_error("area", "strain", "stress")
api.add_error("end", "strain")
api.add_error("end", "stress")

api.reduce_errors("square_average")
api.reduce_objectives("square_average")
# api.group_errors(name=True, type=False, labels=True)

api.plot_experimental()
api.set_recorder(10, True, True, True)
api.optimise(10000, 100, 50, 0.8, 0.01)
