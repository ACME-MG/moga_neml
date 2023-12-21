import sys; sys.path += ["../.."]
from moga_neml.api import API

# Define model
model_name = "ricvih"
# model_name = "vpcvih"
api = API(f"{model_name}_1", input_path="../data", output_path="../results")
api.define_model(model_name)

# Add initial tensile curve
api.read_data("cyclic/Airbase316.csv", num_points=5000)
api.change_data("num_cycles", 0)
api.remove_manual("strain", 0.014)
api.add_error("area", "strain", "stress", num_points=100)

# First optimisation
api.set_recorder(1, plot_opt=True)
opt_params = api.optimise(50, 100, 50, 0.8, 0.01)

# Redefine model
api = API(f"{model_name}_2", input_path="../data", output_path="../results")
api.define_model(model_name)

# Initialise with tensile parameters
for param_name in ["vih_s0", "c_gs1", "c_gs2", "c_cs1", "c_cs2"]:
    api.init_param(param_name, opt_params[param_name])

# Add entire cyclic curve
api.read_data("cyclic/Airbase316.csv", num_points=5000)
api.add_error("area_saddle", "time", "strain", num_points=100, tolerance=0.005)
api.add_error("area_saddle", "time", "stress", num_points=100, tolerance=10.0)
api.add_error("saddle", "time", "stress")
api.add_error("num_peaks", "time", "strain")
# api.add_error("end", "time")

# Second optimisation
api.set_recorder(1, plot_opt=True)
opt_params = api.optimise(100, 100, 50, 0.8, 0.01)