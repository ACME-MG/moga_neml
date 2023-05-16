from modules.api import API
api = API("", 0)
api.define_model("cih")

api.read_file("cyclic/AirBase316_time_strain.csv", True)
# api.read_file("cyclic/AirBase316_time_stress.csv", True)

api.add_error("x_end", "cyclic-time-strain", 100)
api.add_error("y_area", "cyclic-time-strain")
# api.add_error("n_cycles", "cyclic-time-strain")

api.record(1, 10)
api.optimise(10000, 10, 10, 0.65, 0.35)