from modules.api import API
api = API(True, "test", False)
api.read_files(["inl_1/800_80_G25.csv"])
api.define_model("evpwd_s", [4.118577172, 27.97814988, 0.637840909, 3.31618376, 8063.7164])
api.plot_results([41.155155, 186.835582, 59.7954794, 520])