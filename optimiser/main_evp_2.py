from modules.api import API
api = API("evp all", 0)

api.define_model("evp")

api.read_file("tensile/AirBase_20_D5.csv", True)

api.add_error("y_area", "tensile")

api.record(50, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
