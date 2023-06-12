from modules.api import API
api = API("cihd", 0)

api.define_model("cihd")
api.read_file("cyclic/AirBase316_time_strain.csv", True)
api.read_file("cyclic/AirBase316_time_stress.csv", True)
api.read_file("cyclic/AirBase316_stress_strain.csv", False)
api.add_error("x_end", "cyclic-time-strain")
api.add_error("n_peaks", "cyclic-time-strain", 10)
api.add_error("x_peaks", "cyclic-time-strain")
api.add_error("y_area", "cyclic-time-stress", 0.1)

api.record(10, 10)
api.optimise(10000, 100, 50, 0.65, 0.35)