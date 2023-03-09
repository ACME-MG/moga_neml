from modules.api import API
api = API("evp n 20", 0)
api.read_files(["__other__/t_25.csv"])
api.define_model("evp")
api.define_errors("tensile", ["y_area", "y_end"])
api.define_recorder(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)

# api.read_files(["inl_1/AirBase_800_80_G25.csv", "inl_1/AirBase_800_70_G44.csv"], ["inl_1/AirBase_800_65_G33.csv", "inl_1/AirBase_800_60_G32.csv"])
# api.define_constraints("creep", ["dec_x_end", "inc_y_end"])