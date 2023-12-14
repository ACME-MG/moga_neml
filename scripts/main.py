import sys; sys.path += [".."]
from moga_neml.api import API

api = API()
api.define_model("evpcd")
api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.read_data("creep/inl_1/AirBase_800_80_G25.csv")
api.add_error("area", "time", "strain")
api.set_recorder(interval=1, save_model=True)
api.optimise(population=10, offspring=5)