from modules.api import API
api = API("", 0)
api.define_model("evpcd")

api.fix_param("evp_s0", 16.04428385)
api.fix_param("evp_R", 34.76332437)
api.fix_param("evp_d", 20.42808219)
api.fix_param("evp_n", 3.418109825)
api.fix_param("evp_eta", 3359.02242)

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

api.record(1, 10)
api.optimise(10000, 2, 1, 0.65, 0.35)