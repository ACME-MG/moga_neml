import sys; sys.path += [".."]
from moga_neml.api import API

api = API("evp", verbose=False, output_here=True)
api.define_model("evp")

api.read_data("tensile/AirBase_900_D10.csv")
api.remove_manual("strain", 0.4)
api.add_error("y_area", "strain", "stress")
api.add_error("yield")

api.plot_predicted(105.35, 234.5, 0.0794, 1.5435, 15716)
