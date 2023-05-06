from modules.api import API
api = API("", 0)
api.define_model("thkr")

api.read_file("inl_1/AirBase_800_80_G25.csv", True)
# api.read_file("inl_1/AirBase_800_70_G44.csv", True)
# api.read_file("inl_1/AirBase_800_65_G33.csv", True)
# api.read_file("inl_1/AirBase_800_60_G32.csv", True)
# api.__remove_tertiary_creep__()
# api.read_file("tensile/AirBase_800_D7.csv", True)

api.add_error("dy_area", "creep")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
# api.add_error("y_area", "tensile", 2)
# api.add_constraint("dec_x_end", "creep", 10)
# api.add_constraint("inc_y_end", "creep", 2)

api.record(10, 10)
api.optimise(10000, 20, 10, 0.65, 0.35)