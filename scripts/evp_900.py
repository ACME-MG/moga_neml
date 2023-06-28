import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp 900")
api.define_model("evp")

api.read_file("creep/inl_1/AirBase_900_36_G22.csv", True)
api.remove_tertiary_creep(200, 0.8)
api.read_file("creep/inl_1/AirBase_900_31_G50.csv", True)
api.remove_tertiary_creep(200, 0.8)
api.read_file("creep/inl_1/AirBase_900_28_G45.csv", False)
api.remove_tertiary_creep(200, 0.8)
api.read_file("creep/inl_1/AirBase_900_26_G59.csv", False)
api.remove_tertiary_creep(200, 0.8)
api.read_file("tensile/AirBase_900_D10.csv", True)

api.visualise(type="creep")
api.visualise(type="tensile")
api.add_error("y_area", "creep")
api.add_error("y_area", "tensile")
api.record(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)
