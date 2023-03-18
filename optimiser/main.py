from modules.api import API
api = API("left", 0)
api.define_model("evp")

# api.read_file("inl_1/AirBase_800_80_G25.csv", True)
# api.read_file("inl_1/AirBase_800_70_G44.csv", True)
# api.read_file("inl_1/AirBase_800_65_G33.csv", True)
# api.read_file("inl_1/AirBase_800_60_G32.csv", True)
api.read_file("tensile/AirBase_800_D7.csv", True)

# api.add_error("dy_area", "creep")
# api.add_error("y_area", "creep")
# api.add_error("x_end", "creep")
# api.add_error("y_end", "creep")
# api.add_error("y_area", "tensile")
api.__add_custom_y_area__("tensile", cdf=lambda x:x**2)

# api.add_constraint("dec_x_end", "creep")
# api.add_constraint("inc_y_end", "creep")

api.record(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)