"""
 Title:         Performance plotter
 Description:   Creates plots for looking at the performance of the simulations
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.interpolate import splev, splrep, splder
import sys; sys.path += ["../../../../"]
from moga_neml.optimise.driver import Driver
from moga_neml.optimise.curve import Curve
from moga_neml.models.evpcd import Model as EVPCD
from moga_neml.models.evpwdb import Model as EVPWD

# Command line arguments
DATA_TYPE   = sys.argv[1] # "creep", "tensile"
TEMPERATURE = int(sys.argv[2]) # 800, 900, 1000

# Variable constants
DATA_PATH   = "../../../data"
MODEL       = [EVPCD, EVPWD][0]
COMBINER    = np.average # np.median, np.average

# Unvariable constants
X_LABEL = "time" if DATA_TYPE == "creep" else "strain"
Y_LABEL = "strain" if DATA_TYPE == "creep" else "stress"
X_UNITS = "h" if DATA_TYPE == "creep" else "mm/mm"
Y_UNITS = "mm/mm" if DATA_TYPE == "creep" else "MPa"

# The Interpolator Class
class Interpolator:

    # Constructor
    def __init__(self, x_list, y_list, resolution=50, smooth=False):
        thin_x_list = get_thinned_list(x_list, resolution)
        thin_y_list = get_thinned_list(y_list, resolution)
        smooth_amount = resolution if smooth else 0
        self.spl = splrep(thin_x_list, thin_y_list, s=smooth_amount)
    
    # Convert to derivative
    def differentiate(self):
        self.spl = splder(self.spl)

    # Evaluate
    def evaluate(self, x_list):
        return list(splev(x_list, self.spl))

# For differentiating a curve
def differentiate_curve(curve, x_label, y_label):
    curve = deepcopy(curve)
    interpolator = Interpolator(curve[x_label], curve[y_label])
    interpolator.differentiate()
    curve[y_label] = interpolator.evaluate(curve[x_label])
    return curve

# Returns a thinned list
def get_thinned_list(unthinned_list:list, density:int) -> list:
    src_data_size = len(unthinned_list)
    step_size = src_data_size / density
    thin_indexes = [math.floor(step_size*i) for i in range(1, density - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Tries to float cast a value
def try_float_cast(value:str) -> float:
    try:
        return float(value)
    except:
        return value

# Converts CSV data into a curve dict
def get_exp_data_dict(headers:list, data:list) -> dict:
    
    # Get indexes of data
    list_indexes = [i for i in range(len(data[2])) if data[2][i] != ""]
    info_indexes = [i for i in range(len(data[2])) if data[2][i] == ""]
    
    # Create curve
    curve = {}
    for index in list_indexes:
        value_list = [float(d[index]) for d in data]
        value_list = get_thinned_list(value_list, 200)
        curve[headers[index]] = value_list
    for index in info_indexes:
        curve[headers[index]] = try_float_cast(data[0][index])

    # Return curve
    return curve

# Removes data from a curve
def remove_data(exp_data:dict, label:str, value:float=None) -> dict:

    # If the value is none, then don't remove anything
    if value == None:
        return exp_data

    # Create a copy of the curve with empty lists
    new_curve = deepcopy(exp_data)
    for header in new_curve.keys():
        if isinstance(new_curve[header], list) and len(new_curve[header]) == len(exp_data[label]):
            new_curve[header] = []
            
    # Remove data after specific value
    for i in range(len(exp_data[label])):
        if exp_data[label][i] > value:
            break
        for header in new_curve.keys():
            if isinstance(new_curve[header], list) and len(exp_data[header]) == len(exp_data[label]):
                new_curve[header].append(exp_data[header][i])
    
    # Return new data
    return new_curve

# Gets the curve dict given a file path
def get_exp_data(file_path:str) -> dict:
    with open(file_path, "r") as file:
        headers = file.readline().replace("\n","").split(",")
        data = [line.replace("\n","").split(",") for line in file.readlines()]
        exp_data = get_exp_data_dict(headers, data)
        return exp_data

# Gets experimental data
def get_exp_data_list(exp_info_list:list) -> list:
    exp_data_list = []
    for exp_info in exp_info_list:
        exp_data = get_exp_data(exp_info["path"])
        exp_data = remove_data(exp_data, "time", exp_info["time_end"])
        if exp_data["type"] != DATA_TYPE or exp_data["temperature"] != TEMPERATURE:
            continue
        exp_data_list.append(exp_data)
    return exp_data_list

# Gets simulation data from parameters
def get_sim_data(exp_info_list:list, params_str:str) -> dict:

    # Initialise
    model = MODEL("name")
    params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
    results_dict = {}

    # Iterate through experimental data
    for exp_info in exp_info_list:

        # Get experimental data
        exp_data = get_exp_data(exp_info["path"])
        exp_data = remove_data(exp_data, "time", exp_info["time_end"])
        if exp_data["type"] != DATA_TYPE or exp_data["temperature"] != TEMPERATURE:
            continue
        curve = Curve(exp_data, model)

        # Prepare results list
        title = curve.get_exp_data()["title"]
        results_dict[title] = {"exp": exp_data, "sim": []}

        # Iterate through parameters
        for params in params_list:
            model.set_exp_data(exp_data)
            calibrated_model = model.calibrate_model(*params)
            driver = Driver(curve, calibrated_model)
            results = driver.run()
            results_dict[title]["sim"].append(results)
    
    # Return dictionary
    return results_dict

# Calibration data
exp_info_list = [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_60_G32.csv",  "time_end": None,     "calibration": False},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_65_G33.csv",  "time_end": None,     "calibration": False},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_70_G44.csv",  "time_end": None,     "calibration": True},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_80_G25.csv",  "time_end": None,     "calibration": True},
    
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_26_G59.csv",  "time_end": 20541924, "calibration": False},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_28_G45.csv",  "time_end": None,     "calibration": False},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_31_G50.csv",  "time_end": None,     "calibration": True},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_36_G22.csv",  "time_end": None,     "calibration": True},
    
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_11_G39.csv", "time_end": 19457424, "calibration": False},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_12_G48.csv", "time_end": 18096984, "calibration": False},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_13_G30.csv", "time_end": 16877844, "calibration": True},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_16_G18.csv", "time_end": 7756524,  "calibration": True},

    {"path": f"{DATA_PATH}/tensile/inl/AirBase_800_D7.csv",      "time_end": None,     "calibration": True},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_900_D10.csv",     "time_end": None,     "calibration": True},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_1000_D12.csv",    "time_end": None,     "calibration": True},
]

# Parameters
params_str_list = {
    800: """
16.994	187.83	0.26104	4.502	1784.8	3263.5	4.9231	13.172
22.454	66.77	0.92681	4.4191	1610.1	2142	5.4844	11.449
19.125	43.641	5.6148	4.1688	1616	1876.8	5.5594	6.8653
31.647	120.62	0.85485	3.7266	2297.8	2165.7	5.3247	7.7724
33.297	522.85	0.11871	3.9767	1762.4	1913.8	5.6638	11.287
15.042	35.437	8.4	3.9586	2283.5	4184.6	4.4257	6.6603
24.889	44.932	1.2076	4.5055	1527.9	2589.7	5.1066	8.695
23.304	276.66	0.32123	4.2592	1767.2	2168.5	5.3181	6.7619
30.401	34.817	4.5983	3.5323	2583	2520.9	5.1559	8.5891
5.0569	40.476	10.017	4.1585	1730.1	1998.1	5.5564	10.337
""", 900: """
3.6262	13.804	6.9825	4.2416	1138.2	1986	4.4408	9.193
11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225
11.394	13.887	7.532	3.5691	1581.2	1959.8	4.4121	8.5847
5.6656	7.6357	9.1337	4.3001	1055.4	3494.5	3.9629	11.623
8.0846	21.623	4.9985	3.8734	1330.8	2586.3	4.0925	6.8218
8.7008	379.67	0.15739	4.2166	994.53	1533.4	4.6802	7.0461
9.344	45.972	2.5375	3.4094	1902	2101.5	4.3022	6.1081
16.257	181.45	0.5026	3.0154	2606.2	2445.1	4.1307	5.6964
6.4694	149.62	0.29611	4.1942	1123.8	2045.9	4.4272	9.5323
7.9997	25.008	2.2597	4.127	1102.2	1841.7	4.5535	10.206
""", 1000: """
0.0046173	6.8476	2.2387	4.8326	460.38	2357.9	3.5989	6.8922
3.1901	126.5	0.16925	3.8924	802.2	2253.9	3.6876	11.145
0.31556	4.9177	4.2816	4.8134	468.63	3308.8	3.3387	5.7804
0.26189	37.662	0.20134	4.8079	478.84	2939.9	3.4262	5.9609
1.5332	6.9652	4.9491	4.3072	551.01	1467.1	4.0639	13.561
0.18711	42.057	1.22	3.9495	803.58	1759.6	3.8088	6.9718
3.4416	6.259	1.314	4.0782	707.11	4504.6	3.2162	8.2904
4.5325	14.166	2.2205	3.8813	731.02	2379.1	3.5504	6.0315
3.3203	95.748	0.45552	4.0634	574.87	1034.8	4.2291	6.0322
4.0855	246.68	0.084526	3.9321	776.2	2681.7	3.4426	5.5305
"""
}

# Get data
model = MODEL("name")

# Combines all simulations
def combine_simulations(sim_data_list:list) -> dict:

    # Initialise the combined simulation
    num_points = 100
    combined_x_end = COMBINER([max(sim_data[X_LABEL]) for sim_data in sim_data_list])
    combined_x_list = list(np.linspace(0, combined_x_end, num_points))
    combined_y_list_list = [[] for _ in range(num_points)]

    # Iterate through the simulation data for each parameter
    for sim_data in sim_data_list:
        interpolator = Interpolator(sim_data[X_LABEL], sim_data[Y_LABEL])
        sim_x_list = list(np.linspace(0, max(sim_data[X_LABEL]), num_points))
        sim_y_list = interpolator.evaluate(sim_x_list)
        for i in range(len(sim_y_list)):
            combined_y_list_list[i].append(sim_y_list[i])

    # Combine the simulation and return
    combined_y_list = [COMBINER(c) for c in combined_y_list_list]
    combined_dict = {X_LABEL: combined_x_list, Y_LABEL: combined_y_list}
    return combined_dict

# Gets the simulation results from a list of parameter values
def get_simulations(info_list:list, params_str:str) -> list:
    sim_dict_list = []
    results_dict = get_sim_data(info_list, params_str)
    for title in results_dict.keys():
        sim_data_list = results_dict[title]["sim"]
        sim_dict_list.append(combine_simulations(sim_data_list))
    return sim_dict_list

# Initialise experimental and simulation information
cal_info_list = [exp_info for exp_info in exp_info_list if exp_info["calibration"]]
val_info_list = [exp_info for exp_info in exp_info_list if not exp_info["calibration"]]
params_str    = params_str_list[TEMPERATURE]

# Get (combined) simulation information
cal_sim_data_list = get_simulations(cal_info_list, params_str)
val_sim_data_list = get_simulations(val_info_list, params_str)

# Prepare plot
plt.figure(figsize=(5,5))
plt.gca().set_position([0.17, 0.12, 0.75, 0.75])
plt.gca().grid(which="major", axis="both", color="SlateGray", linewidth=1, linestyle=":")
x_limits = {
    "creep": {800: (0, 8000), 900: (0, 7000), 1000: (0, 8000)},
    "tensile": {800: (0, 1.0), 900: (0, 1.0), 1000: (0, 1.0)}
}[DATA_TYPE][TEMPERATURE]
y_limits = {
    "creep": {800: (0, 0.7), 900: (0, 0.35), 1000: (0, 0.35)},
    "tensile": {800: (0, 500), 900: (0, 250), 1000: (0, 160)}
}[DATA_TYPE][TEMPERATURE]
plt.xlim(x_limits)
plt.ylim(y_limits)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

# Plot experimental data
exp_data_list = get_exp_data_list(exp_info_list)
for exp_data in exp_data_list:
    exp_data[X_LABEL] = [t/3600 for t in exp_data[X_LABEL]] if DATA_TYPE == "creep" else exp_data[X_LABEL]
    plt.scatter(exp_data[X_LABEL], exp_data[Y_LABEL], color="silver", s=7**2, marker="o", linewidth=1)

# Plot calibration data
for cal_sim_data in cal_sim_data_list:
    cal_sim_data[X_LABEL] = [t/3600 for t in cal_sim_data[X_LABEL]] if DATA_TYPE == "creep" else cal_sim_data[X_LABEL]
    plt.plot(cal_sim_data[X_LABEL], cal_sim_data[Y_LABEL], color="green")

# Plot validation data
for val_sim_data in val_sim_data_list:
    val_sim_data[X_LABEL] = [t/3600 for t in val_sim_data[X_LABEL]] if DATA_TYPE == "creep" else val_sim_data[X_LABEL]
    plt.plot(val_sim_data[X_LABEL], val_sim_data[Y_LABEL], color="red")

# Add labels and legend and save
plt.xlabel(f"{X_LABEL.capitalize()} ({X_UNITS})", fontsize=15)
plt.ylabel(f"{Y_LABEL.capitalize()} ({Y_UNITS})", fontsize=15)
plt.scatter([], [], color="silver", label="Experimental", s=7**2)
plt.plot([], [], color="green", label="Calibration", linewidth=1.5)
if DATA_TYPE == "creep":
    plt.plot([], [], color="red", label="Validation", linewidth=1.5)
plt.legend(framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=12)
plt.savefig(f"plot_{DATA_TYPE}_{TEMPERATURE}.png")
