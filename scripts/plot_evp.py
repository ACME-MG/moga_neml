import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp ansto")
api.define_model("evp")

api.read_data("tensile/ansto/AirBase_1e-2_A.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.read_data("tensile/ansto/AirBase_1e-3_C.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.read_data("tensile/ansto/AirBase_1e-4_B.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.reduce_errors("square_sum")
api.reduce_objectives("square_sum")

import matplotlib.pyplot as plt
api.plot_experimental()
plt.scatter([0.004085162408375337], [439.9692681103977])
plt.scatter([0.00384235904308254], [388.737758090416])
plt.scatter([0.0032312984627436304], [259.803975638906])
plt.savefig("plot")