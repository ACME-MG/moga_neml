import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp test")
api.define_model("evp")

api.add_custom_data("tensile", {
    "time": [0],
    "strain": [0],
    "stress": [0],
    "temperature": 20,
    "strain_rate": 1e-4,
    "youngs": 211000,
    "poissons": 0.3
})

api.plot_predicted(1, 1, 0.01, 1, 1)
