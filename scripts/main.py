import sys; sys.path += [".."]
from moga_neml.interface import Interface

itf = Interface("evpwdb power")

itf.define_model("evpwdb")

itf.fix_params([17.217, 179.74, 0.61754, 4.4166, 1783.5])
# itf.fix_param("c_0", 14.5622)
# itf.fix_param("c_1", 99.3968)
# itf.fix_param("t_0", 316.145)
# itf.fix_param("t_1", 690.339)

itf.read_data("creep/inl_1/AirBase_800_80_G25.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_70_G44.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_65_G33.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("creep/inl_1/AirBase_800_60_G32.csv")
itf.add_error("area", "time", "strain")
itf.add_error("end", "time")
itf.add_error("end", "strain")
itf.add_constraint("inc_end", "strain")
itf.add_constraint("dec_end", "time")

itf.read_data("tensile/inl/AirBase_800_D7.csv")
itf.add_error("area", "strain", "stress")
itf.add_error("end", "strain", weight=0.5)
itf.add_error("arg_max", "strain", "stress", weight=0.5)
itf.add_error("yield", yield_stress=291)

itf.reduce_errors("square_average")
itf.reduce_objectives("square_average")

itf.plot_experimental()
itf.set_recorder(1, plot_opt=True, plot_loss=True)
itf.optimise(10000, 100, 50, 0.8, 0.01)
