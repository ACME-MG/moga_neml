from modules.api import API
api = API("assess", 0)
# api.read_files(["inl_1/AirBase_800_80_G25.csv", "inl_1/AirBase_800_70_G44.csv", "inl_1/AirBase_800_65_G33.csv", "inl_1/AirBase_800_60_G32.csv"])
api.read_files(["__other__/t_25.csv"])
api.define_model("evp")
api.define_errors("tensile", ["dy_area", "y_area"])
api.define_constraints("tensile", ["dec_x_end", "inc_y_end"])
# api.plot_results([28.1824, 33.46547, 28.03622, 2.002145, 56646.89, 39.80115, 277.1375, 1.970471])
api.plot_results([4.171565669, 66.96845392, 111.5429002, 12, 230.8312035])
