import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp 800")
api.define_model("evp")

api.read_file("creep/inl_1/AirBase_800_80_G25.csv", True)
api.remove_tertiary_creep()
api.read_file("creep/inl_1/AirBase_800_70_G44.csv", True)
api.remove_tertiary_creep()
api.read_file("creep/inl_1/AirBase_800_65_G33.csv", False)
api.remove_tertiary_creep()
api.read_file("creep/inl_1/AirBase_800_60_G32.csv", False)
api.remove_tertiary_creep()
api.read_file("tensile/AirBase_800_D7.csv", True)
api.remove_manual(0.4)

api.visualise("creep")
api.visualise("tensile")
api.add_error("y_area", "creep")
api.add_error("y_area", "tensile")
api.record(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
