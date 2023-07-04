import sys; sys.path += [".."]
from moga_neml.api import API

api = API("test")
api.def_model("evp")

api.read_file("tensile/Airbase_20_D5.csv")
api.add_error("yield", "strain", "stress")

api.start_rec(10)
api.start_opt()