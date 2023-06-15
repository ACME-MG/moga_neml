from modules.api import API
api = API("evp all", 0)

api.define_model("evp")

api.read_file("creep/inl_1/AirBase_800_80_G25.csv", True)
api.read_file("creep/inl_1/AirBase_800_70_G44.csv", True)
api.read_file("creep/inl_1/AirBase_800_65_G33.csv", True)
api.read_file("creep/inl_1/AirBase_800_60_G32.csv", True)
api.__remove_tertiary_creep__()
api.read_file("tensile/AirBase_800_D7.csv", True)

api.add_error("y_area", "creep")
api.add_error("y_area", "tensile")

api.record(50, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
