from modules.api import API
api = API("900 all", 0)
api.define_model("evpwd")

# api.read_file("inl_1/AirBase_800_80_G25.csv", True)
# api.read_file("inl_1/AirBase_800_70_G44.csv", True)
# api.read_file("inl_1/AirBase_800_65_G33.csv", True)
# api.read_file("inl_1/AirBase_800_60_G32.csv", True)
# api.read_file("tensile/AirBase_800_D7.csv", True)

api.read_file("inl_1/AirBase_900_36_G22.csv", True)
api.read_file("inl_1/AirBase_900_31_G50.csv", True)
api.read_file("inl_1/AirBase_900_28_G45.csv", True)
api.read_file("inl_1/AirBase_900_26_G59.csv", True)
api.__remove_oxidised_creep__()
api.read_file("tensile/AirBase_900_D10.csv", False)

api.add_error("dy_area", "creep")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
# api.__add_custom_y_area__("creep", cdf=lambda x:x**2) # left
# api.__add_custom_y_area__("creep", cdf=lambda x:x**0.5) # right
# api.add_error("y_area", "tensile")
api.add_constraint("dec_x_end", "creep", 10)
api.add_constraint("inc_y_end", "creep", 2)

api.record(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)