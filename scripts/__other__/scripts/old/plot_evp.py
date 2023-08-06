import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto")
api.define_model("evp")

api.read_data("tensile/ansto/AirBase_1e-2_A.csv")
api.remove_manual("strain", 0.1)
api.add_error("area", "strain", "stress")
api.add_error("yield", e_stress=400)

api.read_data("tensile/ansto/AirBase_1e-3_C.csv")
api.remove_manual("strain", 0.1)
api.add_error("area", "strain", "stress")
api.add_error("yield", e_stress=300)

api.read_data("tensile/ansto/AirBase_1e-4_B.csv")
api.remove_manual("strain", 0.1)
api.add_error("area", "strain", "stress")
api.add_error("yield", e_stress=200)

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

import matplotlib.pyplot as plt
api.plot_experimental()
plt.scatter(
    [0.006633], [504.3]
)
plt.scatter(
    [0.004512], [402.0]
)
plt.scatter(
    [0.002244], [246.1]
)
plt.savefig("plot")