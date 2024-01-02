import sys; sys.path += ["../.."]
from moga_neml.interface import Interface

# Define model
model_name = "ricvih"
# model_name = "vpcvih"
itf = Interface(f"{model_name}_1", input_path="../data", output_path="../results")
itf.define_model(model_name)

# Add initial tensile curve
itf.read_data("cyclic/Airbase316.csv", num_points=5000)
itf.change_data("num_cycles", 0)
itf.remove_manual("strain", 0.014)
itf.add_error("area", "strain", "stress", num_points=100)

# First optimisation
itf.set_recorder(1, plot_opt=True)
opt_params = itf.optimise(50, 100, 50, 0.8, 0.01)

# Redefine model
itf = Interface(f"{model_name}_2", input_path="../data", output_path="../results")
itf.define_model(model_name)

# Initialise with tensile parameters
for param_name in ["vih_s0", "c_gs1", "c_gs2", "c_cs1", "c_cs2"]:
    itf.init_param(param_name, opt_params[param_name])

# Add entire cyclic curve
itf.read_data("cyclic/Airbase316.csv", num_points=5000)
itf.add_error("area_saddle", "time", "strain", num_points=100, tolerance=0.005)
itf.add_error("area_saddle", "time", "stress", num_points=100, tolerance=10.0)
itf.add_error("saddle", "time", "stress")
itf.add_error("num_peaks", "time", "strain")
# itf.add_error("end", "time")

# Second optimisation
itf.set_recorder(1, plot_opt=True)
opt_params = itf.optimise(100, 100, 50, 0.8, 0.01)
