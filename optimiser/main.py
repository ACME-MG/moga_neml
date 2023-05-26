from modules.api import API
api = API("cihd constrained", 0)

api.define_model("cihd")
api.read_file("cyclic/AirBase316_time_strain.csv", True)
api.read_file("cyclic/AirBase316_time_stress.csv", True)
api.add_error("x_end", "cyclic-time-strain")
api.add_error("n_peaks", "cyclic-time-strain", 1000)
api.add_error("x_peaks", "cyclic-time-strain")
api.add_error("y_area", "cyclic-time-stress", 0.05)
api.add_error("y_max", "cyclic-time-stress", 10)

# api.define_model("evpcd")
# api.read_file("inl_1/AirBase_800_80_G25.csv", True)
# api.read_file("inl_1/AirBase_800_70_G44.csv", True)
# api.add_error("x_end", "creep")
# api.add_error("y_end", "creep")
# api.add_error("dy_area", "creep")
# api.add_error("y_area", "creep")

api.record(5, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)