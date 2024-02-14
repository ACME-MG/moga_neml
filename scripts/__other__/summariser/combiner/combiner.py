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
MODEL       = [EVPCD, EVPWD][1]
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
16.78	98.973	0.60186	4.4156	1780.3	92.942	466.64	124.21	627.18	5.7007	2.1874
5.6925	67.1	1.8542	4.7721	1621.6	72.41	404.77	243.19	619.93	2.4798	11.411
19.2	52.605	1.542	4.5105	1614.6	42.528	267.95	334.54	705.42	2.4141	9.9943
31.327	105.29	0.8549	3.7256	2576.7	54.271	333.56	307.45	694.47	1.9991	6.8035
22.154	462.34	0.17408	4.314	1828.1	40.1	260.65	408.44	853.65	1.9241	7.7562
12.372	53.15	7.1666	3.9502	2220.5	30.95	224.67	344.66	727.88	1.3355	5.8611
19.025	97.214	0.88069	4.5055	1667.4	50.238	313.98	237.66	764.67	2.0071	2.7731
25.12	307.1	0.32185	4.2607	1819.8	23.272	175.2	324.36	665.04	1.609	11.782
31.123	35.65	4.5809	3.6961	2581.8	33.788	237.43	566.68	982.88	1.6294	18.095
29.73	43.859	3.2743	3.9613	2101.3	32.4	228.95	430.57	764.96	1.5794	19.864
""", 900: """
5.1227	14.129	9.606	4.2421	1089.1	56.117	308.89	129.29	799.25	1.5668	1.985
11.192	16.738	5.9587	3.6369	1530.1	35.196	206.85	119.96	774.72	1.5092	2.5579
9.6829	13.118	13.621	3.5054	1604.4	19.213	129	110.83	868.84	1.0493	2.3566
5.6656	8.2222	14.47	4.3001	1006.2	144.26	644.21	178.5	935.23	10.004	2.8495
7.5309	23.5	5.1998	3.862	1374.9	24.858	154.83	511.79	997.24	2.0041	7.9977
4.8239	389.25	0.18435	4.4133	941.87	44.974	248.15	621.83	913.9	2.4338	7.0609
9.7277	49.011	4.1806	3.4099	1834.3	151.05	657.1	262.5	989.31	1.6647	1.0863
16.262	181.79	0.52517	3.0161	2376.6	29.326	172.8	434.17	894.26	2.192	2.8518
6.3647	183.42	0.44712	4.1839	1075.3	27.326	165.15	422.54	849.67	2.2181	10.568
6.5395	16.732	6.8581	4.1207	1096.5	119.77	547.38	572.3	678.83	2.3506	15.844
""", 1000: """
0.41121	8.3185	1.5488	4.8286	468.32	91.109	420.27	145.97	814.06	1.1305	2.2793
4.2741	163.31	0.37485	3.8721	766.51	41.394	218.54	47.517	291.43	4.5815	1.2543
0.012678	46.239	1.2403	4.7068	484.03	70.913	331.34	176.66	409.91	1.605	3.8136
0.036912	49.598	0.89182	4.7436	485.16	7.2738	50.913	269.77	601.74	1.564	8.739
0.70825	8.46	5.8882	4.4476	580.37	179.7	686.62	184.92	898.32	3.9585	1.5713
0.35996	30.971	4.9037	3.95	685.6	118.29	499.25	428.38	969.45	1.1971	13.733
0.48125	40.947	4.9225	4.0867	658	136.71	543.66	663.82	983.11	0.8828	5.8177
4.1412	50.155	3.0378	3.8809	705.19	178.99	671.24	181.75	794.11	7.1307	0.83784
2.1163	47.142	2.229	4.1175	563.88	134.99	568.22	777.7	978.51	0.95908	11.606
2.5964	240.51	0.063337	4.207	732.05	67.534	310.39	651.42	845.64	1.5385	10.23
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
