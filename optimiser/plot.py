from modules.api import API
api = API("", 0)
api.define_model("evpwd")
api.read_file("inl_1/AirBase_800_80_G25.csv", True)
api.read_file("inl_1/AirBase_800_70_G44.csv", True)
api.read_file("inl_1/AirBase_800_65_G33.csv", False)
api.read_file("inl_1/AirBase_800_60_G32.csv", False)
api.__plot_results__([18.86405892,33.23117446,38.20413717,1.858935176,144710.3223,0.317900321,3.2405595,7.76553995])