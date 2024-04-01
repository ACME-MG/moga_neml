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
import sys; sys.path += ["../../../"]
from moga_neml.optimise.driver import Driver
from moga_neml.optimise.curve import Curve
from moga_neml.models.evpcd import Model as EVPCD
from moga_neml.models.evpwdb import Model as EVPWD
from moga_neml.errors.yield_point import get_yield
from params import *

# Constants
LABEL_FONTSIZE = 16
OTHER_FONTSIZE = 13
MARKER_SIZE  = 12
LINEWIDTH    = 1
TRANSPARENCY = 0.2
DATA_PATH    = "../../data"

# Option
OPTION = [
    {"name": "cr_strain",   "info": r"$\bar{\epsilon}$ (mm/mm)",     "handle": lambda x : get_avg(x, "creep", "time", "strain"),      "limits": (0, 0.35)},
    {"name": "cr_min_rate", "info": r"$\dot{\epsilon}_{min}$ (1/h)", "handle": lambda x : get_min_rate(x, "creep", "time", "strain"), "limits": (0, 5e-4)},
    {"name": "cr_time_f",   "info": r"$t_f$ (h)",                    "handle": lambda x : get_max(x, "creep", "time"),                "limits": (0, 12000)},
    {"name": "cr_strain_f", "info": r"$\epsilon_f$ (mm/mm)",         "handle": lambda x : get_max(x, "creep", "strain"),              "limits": (0, 1.0)},
    {"name": "ts_stress",   "info": r"$\sigma_{UTS}$ (MPa)",         "handle": lambda x : get_max(x, "tensile", "stress"),            "limits": (0, 600)},
    {"name": "ts_yield",    "info": r"$\bar{\sigma}$ (MPa)",         "handle": lambda x : get_avg(x, "tensile", "strain", "stress"),  "limits": (0, 600)},
    {"name": "ts_uts",      "info": r"$\sigma_y$ (MPa)",             "handle": lambda x : get_yield_point(x, "tensile"),              "limits": (0, 600)},
    {"name": "ts_stress_f", "info": r"$\sigma_f$ (MPa)",             "handle": lambda x : get_end(x, "tensile", "stress"),            "limits": (0, 300)},
][int(sys.argv[1])]

# Model
MODEL = [
    {"name": "evpcd", "object": EVPCD(""), "opt_params": EVPCD_OPT_PARAMS, "oth_params": EVPCD_OTH_PARAMS},
    {"name": "evpwd", "object": EVPWD(""), "opt_params": EVPWD_OPT_PARAMS, "oth_params": EVPWD_OTH_PARAMS},
][int(sys.argv[2])]

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

# Gets simulation data from parameters
def get_sim_data(exp_info:list, params_str:str, model) -> dict:

    # Initialise
    params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
    results_dict = {}

    # Iterate through experimental data
    for exp_dict in exp_info:

        # Get experimental data
        exp_data = get_exp_data(exp_dict["path"])
        exp_data = remove_data(exp_data, "time", exp_dict["time_end"])
        for field in ["yield", "min_rate"]:
            exp_data[field] = exp_dict[field]
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

# Calculates the experimental and simulated max values
def get_max(results_dict:dict, data_type:str, label:str) -> tuple:
    exp_end_list, sim_end_list = [], []
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue
        exp_end = max(exp_data[label])
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:
            exp_end_list.append(exp_end)
            sim_end_list.append(max(sim_data[label]))
    return exp_end_list, sim_end_list

# Calculates the experimental and simulated end point
def get_end(results_dict:dict, data_type:str, label:str) -> tuple:
    exp_end_list, sim_end_list = [], []
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue
        exp_end = exp_data[label][-1]
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:
            exp_end_list.append(exp_end)
            sim_end_list.append(sim_data[label][-1])
    return exp_end_list, sim_end_list

# Calculates the experimental and simulated minimum rate
def get_min_rate(results_dict:dict, data_type:str, x_label:str, y_label:str) -> tuple:
    exp_end_list, sim_end_list = [], []
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue
        exp_min_rate = exp_data["min_rate"]
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:
            sim_interpolator = Interpolator(sim_data[x_label], sim_data[y_label])
            sim_interpolator.differentiate()
            sim_rate = sim_interpolator.evaluate(sim_data[x_label])
            sim_min_rate = sim_rate[len(sim_rate)//2]*3600
            exp_end_list.append(exp_min_rate)
            sim_end_list.append(sim_min_rate)
    return exp_end_list, sim_end_list

# Calculates the experimental and simulated vertical values of the curve
def get_avg(results_dict:dict, data_type:str, x_label:str, y_label:str) -> tuple:
    
    # Initialise
    exp_y_list, sim_y_list = [], []
    
    # Iterate through experimental curves
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue

        # Interpolate experimental curve
        exp_interpolator = Interpolator(exp_data[x_label], exp_data[y_label])
        exp_x_end = max(exp_data[x_label])

        # Iterate through simulations of experimental curve
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:

            # Interpolate simulated curve
            sim_interpolator = Interpolator(sim_data[x_label], sim_data[y_label])

            # Query experimental and simulated curves
            min_x_end = min(exp_x_end, max(sim_data[x_label]))
            x_list = list(np.linspace(0, min_x_end, 50+2))[1:-1]
            exp_y_values = exp_interpolator.evaluate(x_list)
            sim_y_values = sim_interpolator.evaluate(x_list)

            # Add to initialised super list
            exp_y_list.append(np.average(exp_y_values))
            sim_y_list.append(np.average(sim_y_values))
    
    # Return
    return exp_y_list, sim_y_list

# Calculates the experimental and simulated yield points
def get_yield_point(results_dict:dict, data_type:str) -> tuple:

    # Initialise
    exp_yield_list, sim_yield_list = [], []
    
    # Iterate through experimental curves
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue
        exp_yield = exp_data["yield"]

        # Iterate through simulations of experimental curve
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:
            sim_yield = get_yield(sim_data["strain"], sim_data["stress"])[1]
            exp_yield_list.append(exp_yield)
            sim_yield_list.append(sim_yield)
    
    # Return
    return exp_yield_list, sim_yield_list

# Gets experimental and simulation data
def get_data_points(exp_info:list, params_str:list, model) -> tuple:
    results_dict = get_sim_data(exp_info, params_str, model)
    exp_list, sim_list = OPTION["handle"](results_dict)
    if OPTION["name"] == "cr_time_f":
        exp_list = [t/3600 for t in exp_list]
        sim_list = [t/3600 for t in sim_list]
    return exp_list, sim_list

# Calibration data
cal_info_list = [[
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_70_G44.csv",  "time_end": None,     "yield": None, "min_rate": 9.0345e-5},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_80_G25.csv",  "time_end": None,     "yield": None, "min_rate": 2.3266e-4},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_800_D7.csv",      "time_end": None,     "yield": 291,  "min_rate": None},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_31_G50.csv",  "time_end": None,     "yield": None, "min_rate": 5.3682e-5},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_36_G22.csv",  "time_end": None,     "yield": None, "min_rate": 1.2199e-4},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_900_D10.csv",     "time_end": None,     "yield": 164,  "min_rate": None},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_13_G30.csv", "time_end": 16877844, "yield": None, "min_rate": 2.6645e-5},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_16_G18.csv", "time_end": 7756524,  "yield": None, "min_rate": 6.7604e-5},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_1000_D12.csv",    "time_end": None,     "yield": 90,   "min_rate": None},
]]

# Validation data
val_info_list = [[
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_60_G32.csv",  "time_end": None,     "yield": None, "min_rate": 2.8910e-5},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_65_G33.csv",  "time_end": None,     "yield": None, "min_rate": 5.0385e-5},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_26_G59.csv",  "time_end": 20541924, "yield": None, "min_rate": 2.1864e-5},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_28_G45.csv",  "time_end": None,     "yield": None, "min_rate": 3.5312e-5},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_11_G39.csv", "time_end": 19457424, "yield": None, "min_rate": 1.2941e-5},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_12_G48.csv", "time_end": 18096984, "yield": None, "min_rate": 9.8962e-6},
]]

# Prepare plot
fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

# Set labels and plot line
plt.xlabel(f"Simulated {OPTION['info']}", fontsize=LABEL_FONTSIZE)
plt.ylabel(f"Measured {OPTION['info']}", fontsize=LABEL_FONTSIZE)
plt.plot(OPTION["limits"], OPTION["limits"], linestyle="--", color="black", zorder=1)

# Iterate through parameters
marker_list = ["^", "s", "*"]
for i in range(len(MODEL["opt_params"])):

    # Get data
    oth_cal_exp_list, oth_cal_sim_list = get_data_points(cal_info_list[i], MODEL["oth_params"][i], MODEL["object"])
    oth_val_exp_list, oth_val_sim_list = get_data_points(val_info_list[i], MODEL["oth_params"][i], MODEL["object"])
    opt_cal_exp_list, opt_cal_sim_list = get_data_points(cal_info_list[i], MODEL["opt_params"][i], MODEL["object"])
    opt_val_exp_list, opt_val_sim_list = get_data_points(val_info_list[i], MODEL["opt_params"][i], MODEL["object"])

    # Plot data
    plt.scatter(oth_cal_sim_list, oth_cal_exp_list, zorder=2, edgecolor="none",  color="green", linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i], alpha=TRANSPARENCY)
    plt.scatter(oth_val_sim_list, oth_val_exp_list, zorder=2, edgecolor="none",  color="red",   linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i], alpha=TRANSPARENCY)
    plt.scatter(opt_cal_sim_list, opt_cal_exp_list, zorder=2, edgecolor="black", color="green", linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i])
    plt.scatter(opt_val_sim_list, opt_val_exp_list, zorder=2, edgecolor="black", color="red",   linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i])

# Add 'conservative' region
triangle_vertices = np.array([[OPTION["limits"][0], OPTION["limits"][0]], [OPTION["limits"][1], OPTION["limits"][0]], [OPTION["limits"][1], OPTION["limits"][1]]])
ax.fill(triangle_vertices[:, 0], triangle_vertices[:, 1], color="gray", alpha=0.3)
plt.text(OPTION["limits"][1]-0.48*(OPTION["limits"][1]-OPTION["limits"][0]), OPTION["limits"][0]+0.05*(OPTION["limits"][1]-OPTION["limits"][0]), "Non-conservative", fontsize=OTHER_FONTSIZE, color="black")

# Prepare legend for data type
handle_list = []
cal = plt.scatter([], [], color="green", label="Calibration", s=10**2)
val = plt.scatter([], [], color="red", label="Validation", s=10**2)
handles = [cal] if "ts" in OPTION["name"] else [cal, val]
legend = plt.legend(handles=handles, framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=OTHER_FONTSIZE, loc="upper right")
plt.gca().add_artist(legend)

# Add legend for temperature
bbox_pos = (0.6, 0.89) if "ts" in OPTION["name"] else (0.6, 0.815)
t800  = plt.scatter([], [], color="none", edgecolor="black", linewidth=LINEWIDTH,  label="800°C",  marker="^", s=MARKER_SIZE**2)
t900  = plt.scatter([], [], color="none", edgecolor="black", linewidth=LINEWIDTH,  label="900°C",  marker="s", s=MARKER_SIZE**2)
t1000 = plt.scatter([], [], color="none", edgecolor="black", linewidth=LINEWIDTH,  label="1000°C", marker="*", s=MARKER_SIZE**2)
legend = plt.legend(handles=[t800, t900, t1000], framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=OTHER_FONTSIZE,
                    loc="upper left", bbox_to_anchor=bbox_pos)
plt.gca().add_artist(legend)

# Format figure size
plt.gca().set_position([0.17, 0.12, 0.75, 0.75])
plt.gca().grid(which="major", axis="both", color="SlateGray", linewidth=1, linestyle=":")
plt.gcf().set_size_inches(5, 5)

# Format limits
plt.xlim(OPTION["limits"])
plt.ylim(OPTION["limits"])

# Format ticks
plt.xticks(fontsize=OTHER_FONTSIZE)
plt.yticks(fontsize=OTHER_FONTSIZE)
if OPTION["name"] == "cr_time_f":
    ax.ticklabel_format(axis="x", style="sci", scilimits=(3,3))
    ax.ticklabel_format(axis="y", style="sci", scilimits=(3,3))
    ax.xaxis.major.formatter._useMathText = True
    ax.yaxis.major.formatter._useMathText = True
if OPTION["name"] == "cr_min_rate":
    ax.ticklabel_format(axis="x", style="sci", scilimits=(-4,-4))
    ax.ticklabel_format(axis="y", style="sci", scilimits=(-4,-4))
    ax.xaxis.major.formatter._useMathText = True
    ax.yaxis.major.formatter._useMathText = True

# Save
plt.savefig(f"{MODEL['name']}_{OPTION['name']}.png")
