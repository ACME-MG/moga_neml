from modules.api import API
api = API("assess", 0)
api.read_files(["inl_1/AirBase_800_80_G25.csv", "inl_1/AirBase_800_70_G44.csv", "inl_1/AirBase_800_65_G33.csv", "inl_1/AirBase_800_60_G32.csv"])
api.define_model("evpwd")
api.define_errors("creep", ["dy_area", "y_area", "x_end", "y_end"])
api.define_constraints("creep", ["dec_x_end", "inc_y_end"])
api.plot_results([35.86124898,30.0385608,9.112239385,1.924571367,206802.6822,14.05202661,1.865805494,0.755478337])
