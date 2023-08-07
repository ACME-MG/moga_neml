"""
 Title:         Material Modelling Surrogate for VSHAI
 Description:   Generates VSHAI parameters and corresponding output
 Author:        Janzen Choi

"""

# Libraries
import itertools
import numpy as np

# NEML Libraries
from neml import drivers
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow

# Model Constants
TEMPERATURE = 20
STRAIN_RATE = 1.0e-4
MAX_STRAIN  = 0.2
NUM_STEPS   = 251
REL_TOL     = 1.0E-6 # -6
ABS_TOL     = 1.0E-10 # -10
VERBOSE     = False

# Surrogate Modelling Constants
NUM_STRAINS = 20

# Rounds a float to a number of significant figures
def round_sf(value:float, sf:int) -> float:
    format_str = "{:." + str(sf) + "g}"
    rounded_value = float(format_str.format(value))
    return rounded_value

# Transposes a 2D list of lists
def transpose(list_of_lists:float) -> list:
    transposed = np.array(list_of_lists).T.tolist()
    return transposed

# The VSHAI Model
class Model:

    # Gets the calibrated VSHAI model
    def get_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta):
        elastic_model  = elasticity.IsotropicLinearElasticModel(211000, "youngs", 0.3, "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        return evp_model

    # Gets the results from the driver and return
    def get_prediction(self, *params:tuple):
        calibrated_model = self.get_model(*params)
        results = drivers.uniaxial_test(calibrated_model, erate=STRAIN_RATE,
            T=TEMPERATURE, emax=MAX_STRAIN, nsteps=NUM_STEPS,
            verbose=VERBOSE, rtol=REL_TOL, atol=ABS_TOL)
        return results # "strain", "stress"

# Converts a dictionary into a CSV file
def dict_to_csv(data_dict:dict, csv_path:str) -> None:
    
    # Extract headers and turn all values into lists
    headers = data_dict.keys()
    for header in headers:
        if not isinstance(data_dict[header], list):
            data_dict[header] = [data_dict[header]]
    
    # Open CSV file and write headers
    csv_fh = open(csv_path, "w+")
    csv_fh.write(",".join(headers) + "\n")
    
    # Write data and close
    max_list_size = max([len(data_dict[header]) for header in headers])
    for i in range(max_list_size):
        row_list = [str(data_dict[header][i]) if i < len(data_dict[header]) else "" for header in headers]
        row_str = ",".join(row_list)
        csv_fh.write(row_str + "\n")
    csv_fh.close()

# Finds the index corresponding to the nearest value
def find_nearest(array, value):
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return index

# Initialise parameter values
value_dict = {
    "evp_s0":  [1, 100, 200, 300, 400, 500],
    "evp_R":   [1, 500, 1000, 1500, 2000],
    "evp_d":   [0.1, 1, 10, 100],
    "evp_n":   [1, 5, 10],
    "evp_eta": [1e1, 1e2, 1e3, 1e4]
}

# Get all combinations
value_grid   = list(value_dict.values())
combinations = list(itertools.product(*value_grid))
combinations = [list(c) for c in combinations]
print(f"Generated {len(combinations)} combinations")

# Initialise model
model = Model()

# Prepare parameter dictionary
transposed_combinations = transpose(combinations)
param_dict = {key: value for key, value in zip(list(value_dict.keys()), transposed_combinations)}

# Prepare combined dictionary
headers = list(param_dict.keys()) + ["x_end"] + [f"y_{i+1}" for i in range(NUM_STRAINS)]
empty_lists = [[] for _ in range(len(headers))]
combined_dict = {key: value for key, value in zip(headers, empty_lists)}

# Iterate through parameters
fail_count = 0
for params in combinations:
    
    # Get prediction
    try:
        result = model.get_prediction(*params)
    except:
        fail_count += 1
        continue
    
    # Add parameters
    for i in range(len(params)):
        param_name = list(param_dict.keys())[i]
        combined_dict[param_name].append(params[i])
    
    # Add end point
    x_end = result["strain"][-1]
    combined_dict["x_end"].append(x_end)

    # Add strain values
    for i in range(1,NUM_STRAINS+1):
        y_index = find_nearest(result["strain"], x_end/NUM_STRAINS*i)
        y_value = round_sf(result["stress"][y_index], 5)
        combined_dict[f"y_{i}"].append(y_value)

# Write results
print(f"Results failed = {fail_count}")
dict_to_csv(combined_dict, "params.csv")
