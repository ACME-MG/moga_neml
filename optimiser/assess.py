from modules.api import API
api = API("assess", 0)
api.read_files(["inl_1/AirBase_800_80_G25.csv", "inl_1/AirBase_800_70_G44.csv", "inl_1/AirBase_800_65_G33.csv", "inl_1/AirBase_800_60_G32.csv"])
api.define_model("evpwd")
api.define_errors("creep", ["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints("creep", ["dec_x_end", "inc_y_end"])
api.plot_results([27.90870472,35.50328355,18.78682904,2.013188934,56819.68942,39.02659886,275.4846911,1.911204461])