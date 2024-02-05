"""
 Title:         Performance plotter
 Description:   Creates plots for looking at the performance of the simulations
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import sys; sys.path += ["../../../"]
from moga_neml.optimise.driver import Driver
from moga_neml.optimise.curve import Curve
from moga_neml.models.evpcd import Model as EVPCD
from moga_neml.models.evpwdb import Model as EVPWD

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

# Gets simulation data from parameters
def get_sim_data(exp_info_list:list, params_str:str, model) -> dict:

    # Initialise
    params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
    results_dict = {}

    # Iterate through experimental data
    for exp_info in exp_info_list:

        # Get experimental data
        exp_data = get_exp_data(exp_info["path"])
        exp_data = remove_data(exp_data, "time", exp_info["time_end"])
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

# Calculates the experimental and simulated end point
def get_end_lists(results_dict:dict, data_type:str, label:str) -> list:
    exp_end_list, sim_end_list = [], []
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue
        exp_end = max(exp_data[label])
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:
            sim_end = max(sim_data[label])
            exp_end_list.append(exp_end)
            sim_end_list.append(sim_end)
    return exp_end_list, sim_end_list

# Gets experimental and simulation data
def get_data_points(info_list:list, params_str_list:list, model) -> tuple:
    all_exp_list, all_sim_list = [], []
    for i in range(len(params_str_list)):
        results_dict = get_sim_data(info_list[i], params_str_list[i], model)
        exp_list, sim_list = get_end_lists(results_dict, "creep", "strain")
        exp_list, sim_list = get_end_lists(results_dict, "creep", "time")
        exp_list = [t/3600 for t in exp_list]
        sim_list = [t/3600 for t in sim_list]
        all_exp_list += exp_list
        all_sim_list += sim_list
    return all_exp_list, all_sim_list

# Calibration data
cal_info_list = [[
    {"path": "../../data/creep/inl_1/AirBase_800_70_G44.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_800_80_G25.csv", "time_end": None},
    {"path": "../../data/tensile/inl/AirBase_800_D7.csv", "time_end": None},
], [
    {"path": "../../data/creep/inl_1/AirBase_900_31_G50.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_900_36_G22.csv", "time_end": None},
    {"path": "../../data/tensile/inl/AirBase_900_D10.csv", "time_end": None},
], [
    {"path": "../../data/creep/inl_1/AirBase_1000_13_G30.csv", "time_end": 18500000},
    {"path": "../../data/creep/inl_1/AirBase_1000_16_G18.csv", "time_end": 8940000},
    {"path": "../../data/tensile/inl/AirBase_1000_D12.csv", "time_end": None},
]]

# Validation data
val_info_list = [[
    {"path": "../../data/creep/inl_1/AirBase_800_60_G32.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_800_65_G33.csv", "time_end": None},
], [
    {"path": "../../data/creep/inl_1/AirBase_900_26_G59.csv", "time_end": 21490000},
    {"path": "../../data/creep/inl_1/AirBase_900_28_G45.csv", "time_end": None},
], [
    {"path": "../../data/creep/inl_1/AirBase_1000_11_G39.csv", "time_end": 20610000},
    {"path": "../../data/creep/inl_1/AirBase_1000_12_G48.csv", "time_end": 19400000},
]]

# Parameters
params_str_list = [
"""
31.647	120.62	0.85485	3.7266	2297.8	2165.7	5.3247	7.7724
33.297	522.85	0.11871	3.9767	1762.4	1913.8	5.6638	11.287
15.042	35.437	8.4	3.9586	2283.5	4184.6	4.4257	6.6603
38.181	51.055	2.4819	3.2572	3154.4	2725.2	5.0167	8.33
24.889	44.932	1.2076	4.5055	1527.9	2589.7	5.1066	8.695
23.304	276.66	0.32123	4.2592	1767.2	2168.5	5.3181	6.7619
30.401	34.817	4.5983	3.5323	2583	2520.9	5.1559	8.5891
5.0569	40.476	10.017	4.1585	1730.1	1998.1	5.5564	10.337
31.809	43.194	2.2399	3.9613	1820.1	2245.4	5.3179	8.5096
0.36499	45.374	15.687	3.6105	2878.3	3325.8	4.847	12.328
""",
"""
8.7008	379.67	0.15739	4.2166	994.53	1533.4	4.6802	7.0461
9.344	45.972	2.5375	3.4094	1902	2101.5	4.3022	6.1081
3.0011	18.974	32.389	3.2721	2021.2	2356.2	4.4101	17.539
2.1263	19.571	18.852	3.3525	1999.6	2639.8	4.3577	21.825
16.257	181.45	0.5026	3.0154	2606.2	2445.1	4.1307	5.6964
9.5315	149.26	0.37326	3.9582	1254.6	2014.8	4.3854	8.0511
6.4694	149.62	0.29611	4.1942	1123.8	2045.9	4.4272	9.5323
12.617	119.8	0.37544	3.7416	1366.4	1894.5	4.5371	9.6136
11.849	272.72	0.21347	3.8447	1238.3	1731	4.5635	7.4758
7.9997	25.008	2.2597	4.127	1102.2	1841.7	4.5535	10.206
""",
"""
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
]


# Get data
model = EVPCD("evpcd")
cal_exp_list, cal_sim_list = get_data_points(cal_info_list, params_str_list, model)
val_exp_list, val_sim_list = get_data_points(val_info_list, params_str_list, model)

# Prepare plot
fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

# Define variable options
limits = (0, 8000)
# limits = (0.1, 0.5)
plt.xlabel("Experimental", fontsize=15)
plt.ylabel("Simulation", fontsize=15)

# Plot line then data
plt.plot(limits, limits, linestyle="--", color="black")
plt.scatter(cal_exp_list, cal_sim_list, color="green")
plt.scatter(val_exp_list, val_sim_list, color="red")

# Add 'conservative' region
triangle_vertices = np.array([[limits[0], limits[0]], [limits[1], limits[0]], [limits[1], limits[1]]])
ax.fill(triangle_vertices[:, 0], triangle_vertices[:, 1], color="gray", alpha=0.3)
plt.text(limits[1]-0.35*(limits[1]-limits[0]), limits[0]+0.05*(limits[1]-limits[0]), "Conservative", fontsize=12, color="black")

# Prepare legend
plt.plot([], [], color="black", label="1:1 Line", linestyle="--", linewidth=1.5)
plt.scatter([], [], color="green", label="Calibration", s=6**2)
plt.scatter([], [], color="red", label="Validation", s=6**2)
plt.legend(framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=12)

# Format everything else and save
plt.gca().set_position([0.17, 0.12, 0.75, 0.75])
plt.gca().grid(which="major", axis="both", color="SlateGray", linewidth=1, linestyle=":")
plt.xlim(limits)
plt.ylim(limits)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.savefig("plot.png")
