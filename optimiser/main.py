from modules.api import API
api = API("evpwd 80 sigmoid", 2)
api.read_files(["inl_1/AirBase_800_80_G25.csv"])
api.define_model("evpwd")
# api.define_model("evpwd_s", [4.118577172, 27.97814988, 0.637840909, 3.31618376, 8063.7164])
api.define_errors(["dy_area", "y_area", "x_end", "y_end"])
# api.define_constraints(["dec_x_end", "inc_y_end"])
api.define_recorder(1, 1)
api.optimise(10000, 10, 10, 0.65, 0.35)
