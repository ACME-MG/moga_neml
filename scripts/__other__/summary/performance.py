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

# Experimental data
exp_info_list = [[
    {"path": "../../data/creep/inl_1/AirBase_800_60_G32.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_800_65_G33.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_800_70_G44.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_800_80_G25.csv", "time_end": None},
    {"path": "../../data/tensile/inl/AirBase_800_D7.csv", "time_end": None},
], [
    {"path": "../../data/creep/inl_1/AirBase_900_26_G59.csv", "time_end": 21490000},
    {"path": "../../data/creep/inl_1/AirBase_900_28_G45.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_900_31_G50.csv", "time_end": None},
    {"path": "../../data/creep/inl_1/AirBase_900_36_G22.csv", "time_end": None},
    {"path": "../../data/tensile/inl/AirBase_900_D10.csv", "time_end": None},
], [
    {"path": "../../data/creep/inl_1/AirBase_1000_11_G39.csv", "time_end": 20610000},
    {"path": "../../data/creep/inl_1/AirBase_1000_12_G48.csv", "time_end": 19400000},
    {"path": "../../data/creep/inl_1/AirBase_1000_13_G30.csv", "time_end": 18500000},
    {"path": "../../data/creep/inl_1/AirBase_1000_16_G18.csv", "time_end": 8940000},
    {"path": "../../data/tensile/inl/AirBase_1000_D12.csv", "time_end": None},
]]

# Parameters
params_str_list = [
"""
16.994	187.83	0.26104	4.502	1784.8	3263.5	4.9231	13.172
22.454	66.77	0.92681	4.4191	1610.1	2142	5.4844	11.449
9.1648	36.326	12.337	4.2247	1776.1	2731	5.0411	8.3103
5.8951	36.907	5.3551	4.7311	1557.8	2224.1	5.2809	6.5113
4.1861	84.548	2.1125	4.767	1574.1	2883.2	4.8395	4.5431
27.868	89.339	0.59712	4.1982	1818	2645.2	5.1192	10.125
28.599	78.057	0.84292	3.8371	2441.5	2969.6	4.9976	10.642
29.979	119.58	0.552	3.8505	2314.4	2808.8	5.0354	9.5435
19.125	43.641	5.6148	4.1688	1616	1876.8	5.5594	6.8653
22.012	38.873	2.2033	4.245	1841.2	2377	5.2898	9.7712
""",
"""
3.6262	13.804	6.9825	4.2416	1138.2	1986	4.4408	9.193
10.683	31.381	2.9727	3.7155	1422	1626.7	4.552	6.2319
10.341	24.476	2.3226	3.9651	1176.4	1743	4.5865	9.1587
11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225
8.0818	9.2744	7.9562	3.9839	1310.7	4972.4	3.6443	9.6707
11.394	13.887	7.532	3.5691	1581.2	1959.8	4.4121	8.5847
5.6656	7.6357	9.1337	4.3001	1055.4	3494.5	3.9629	11.623
15.177	64.875	1.1737	3.2003	2165.3	2320.3	4.1948	6.7274
8.0268	28.899	2.5811	4.018	1213.4	1698.5	4.5711	7.3221
8.0846	21.623	4.9985	3.8734	1330.8	2586.3	4.0925	6.8218
""",
"""
1.9303	413.72	0.024258	4.1744	720.53	3740	3.2875	7.5471
3.745	5.5085	10.982	3.9323	723.41	9445.3	2.7645	5.3007
1.0051	41.568	0.5031	4.4626	582.32	2413	3.508	6.1178
0.34182	3.0001	2.6158	4.5224	605.76	9686.9	2.8177	7.5712
0.74811	4.813	1.5203	4.5427	578.84	5902.3	3.0358	7.2228
2.2985	17.765	0.53407	4.1895	695.87	4582.4	3.1498	6.8538
1.7065	2.9635	8.5672	4.2396	648.58	9968.2	2.8411	9.9029
1.257	4.6817	6.5932	4.2586	671.09	9375.2	2.7983	6.5297
0.54088	3.4417	3.8666	4.4062	640.31	9914.9	2.8044	7.6502
2.9772	13.58	2.2099	4.0601	697.13	2654.7	3.4465	5.4967
"""
]

# Get data
model = EVPCD("evpcd")
all_exp_list, all_sim_list = [], []
for i in range(len(exp_info_list)):
# for i in range(1):
    results_dict = get_sim_data(exp_info_list[i], params_str_list[i], model)
    exp_list, sim_list = get_end_lists(results_dict, "creep", "strain")
    # exp_list = [t/3600 for t in exp_list]
    # sim_list = [t/3600 for t in sim_list]
    all_exp_list += exp_list
    all_sim_list += sim_list

# Prepare plot
fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

# Define variable options
# limits = (0, 8000)
limits = (0.1, 0.5)
plt.xlabel("Experimental", fontsize=15)
plt.ylabel("Simulation", fontsize=15)

# Plot line then data
plt.plot(limits, limits, linestyle="--", color="black")
plt.scatter(all_exp_list, all_sim_list, color="green")

# Add 'conservative' region
triangle_vertices = np.array([[limits[0], limits[0]], [limits[1], limits[0]], [limits[1], limits[1]]])
ax.fill(triangle_vertices[:, 0], triangle_vertices[:, 1], color="gray", alpha=0.3)
plt.text(limits[1]-0.35*(limits[1]-limits[0]), limits[0]+0.05*(limits[1]-limits[0]), "Conservative", fontsize=12, color="black")

# Prepare legend
plt.plot([], [], color="black", label="1:1 Line", linestyle="--", linewidth=1.5)
plt.scatter([], [], color="green", label="Calibration", s=6**2)
plt.legend(framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=12)

# Format everything else and save
plt.gca().set_position([0.17, 0.12, 0.75, 0.75])
plt.gca().grid(which="major", axis="both", color="SlateGray", linewidth=1, linestyle=":")
plt.xlim(limits)
plt.ylim(limits)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.savefig("plot.png")
