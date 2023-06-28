import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evpcd 1000")
api.define_model("evpcd")

api.read_file("creep/inl_1/AirBase_1000_16_G18.csv", True)
api.remove_oxidised_creep(100, 0.7)
api.read_file("creep/inl_1/AirBase_1000_13_G30.csv", True)
api.remove_oxidised_creep(100, 0.6)
api.read_file("creep/inl_1/AirBase_1000_12_G52.csv", False)
api.remove_oxidised_creep(100, 0.7)
api.read_file("creep/inl_1/AirBase_1000_11_G39.csv", False)
api.remove_oxidised_creep(100, 0.7)
api.read_file("tensile/AirBase_1000_D12.csv", True)

api.visualise(type="creep")
api.visualise(type="tensile")
api.add_error("y_area", "creep")
api.add_error("x_end", "creep")
api.add_error("y_end", "creep")
api.add_error("y_area", "tensile")
api.record(10, 10)
api.optimise(10000, 200, 100, 0.65, 0.35)