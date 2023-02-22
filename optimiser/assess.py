from modules.api import API
api = API("assess", 0)
api.read_files(["inl_1/AirBase_800_80_G25.csv", "inl_1/AirBase_800_70_G44.csv", "inl_1/AirBase_800_65_G33.csv", "inl_1/AirBase_800_60_G32.csv"])
api.define_model("evpwd")
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints(["dec_x_end", "inc_y_end"])
api.plot_results([18.91314,54.35003,12.0449,1.74566,297662.5,43.8387,66.32941,51.06135,0.828872])
