import sys; sys.path += [".."]
from moga_neml.api import API

api = API("")

api.read_file("creep/inl_2/AirBase_750_118_b.csv", True)
api.read_file("creep/inl_2/AirBase_750_137_a.csv", True)
api.read_file("creep/inl_2/AirBase_750_95_a.csv", True)
api.read_file("tensile/AirBase_750_D6.csv", True)

api.visualise()