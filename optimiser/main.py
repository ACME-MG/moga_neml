from modules.api import API
api = API("all cnt", 0)
api.define_model("evpwd")

api.read_file("inl_1/AirBase_800_80_G25.csv", True)
api.read_file("inl_1/AirBase_800_70_G44.csv", True)
api.read_file("inl_1/AirBase_800_65_G33.csv", True)
api.read_file("inl_1/AirBase_800_60_G32.csv", True)
api.read_file("tensile/AirBase_800_D7.csv", True)

api.add_error("dy_area", "creep")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
# api.__add_custom_y_area__("creep", cdf=lambda x:x**2) # left
# api.__add_custom_y_area__("creep", cdf=lambda x:x**0.5) # right
api.add_error("y_area", "tensile")

api.add_constraint("dec_x_end", "creep", 10)
api.add_constraint("inc_y_end", "creep", 2)

api.record(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
# api.__plot_results__([0.886871296,48.24774054,45.73058568,2.275591139,33732.53423,0.26117023,2.918698784,4.810443668])