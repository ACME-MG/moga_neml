from modules.api import API
api = API("assess", 0)
# api.read_files(["inl_1/AirBase_800_80_G25.csv", "inl_1/AirBase_800_70_G44.csv", "inl_1/AirBase_800_65_G33.csv", "inl_1/AirBase_800_60_G32.csv"])
api.read_files(["__other__/t_25.csv"])
api.define_model("evp")
api.define_errors(["dy_area", "y_area"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.plot_results([50, 110.915, 137.2604, 2.011812, 5302.926])
