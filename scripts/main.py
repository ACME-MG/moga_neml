import sys; sys.path += [".."]
from moga_neml.api import API

api = API()
api.define_model("evpwdb")

api.read_data("creep/inl_1/AirBase_900_36_G22.csv")
api.add_error("area", "time", "strain")
api.add_error("end", "time")
api.add_error("end", "strain")

api.get_results(4.871, 11.518, 7.0281, 4.2421, 1138.3, 1.2072, 0.4455, 3.8687, 3.6877, 0.25385, 2.53081)
