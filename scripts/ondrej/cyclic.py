import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

model_name = "ricvih"
# model_name = "riclih"
# model_name = "rilih"
# model_name = "rilikh"
# model_name = "riplih"
# model_name = "rivih"
# model_name = "vpclih"
# model_name = "vpcvih"
# model_name = "vpplih"
# model_name = "vppvih"
itf = Interface(model_name, input_path="../data", output_path="../results")
itf.define_model(model_name)

# Optimise cycles
itf.read_data("cyclic/Airbase316.csv", num_points=5000)
# itf.change_data("num_cycles", 2)
# itf.remove_manual("time", 250)
itf.change_data("num_cycles", 4)
itf.remove_manual("time", 607)
itf.add_error("area_saddle", "time", "strain", num_points=200, tolerance=0.005)
itf.add_error("area_saddle", "time", "stress", num_points=200, tolerance=10.0)
itf.add_error("saddle", "time", "stress")
itf.add_error("num_peaks", "time", "strain")
# itf.add_error("end", "time")

# Optimise initial tensile
itf.read_data("cyclic/Airbase316.csv", num_points=5000)
itf.change_data("num_cycles", 0)
itf.remove_manual("strain", 0.014)
itf.add_error("area", "strain", "stress", num_points=100)

itf.plot_experimental()
itf.set_recorder(1, plot_opt=True)
itf.optimise(100, 100, 50, 0.8, 0.01)
