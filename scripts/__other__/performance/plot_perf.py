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

# Varying constants
OPTION_INDEX = int(sys.argv[1])
MODEL_INDEX  = int(sys.argv[2])

# Non-changing constants
MARKER_SIZE  = 10
LINEWIDTH    = 1
TRANSPARENCY = 0.2
DATA_PATH    = "../../data"
MODEL_NAME   = "evpcd" if MODEL_INDEX == 0 else "evpwd"
OPTION       = ["cr_strain", "cr_time_tf", "cr_strain_tf", "ts_stress", "ts_yield", "ts_uts"][OPTION_INDEX]
INFO         = [r"$\epsilon$ (mm/mm)", r"$t_f$ (h)", r"$\epsilon_f$ (mm/mm)",
                r"$\sigma$ (MPa)", r"$\sigma_y$ (MPa)", r"$\sigma_{UTS}$ (MPa)"][OPTION_INDEX]
MODEL        = [EVPCD, EVPWD][MODEL_INDEX]

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
        exp_data["yield"] = exp_dict["yield"]
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
def get_end_lists(results_dict:dict, data_type:str, label:str) -> tuple:
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

# Calculates the experimental and simulated vertical values of the curve
def get_y_list(results_dict:dict, data_type:str, x_label:str, y_label:str) -> tuple:
    
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
            x_list = list(np.linspace(0, min_x_end, 10+2))[1:-1]
            exp_y_values = exp_interpolator.evaluate(x_list)
            sim_y_values = sim_interpolator.evaluate(x_list)

            # Add to initialised super list
            exp_y_list += exp_y_values
            sim_y_list += sim_y_values
    
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

    # Get results
    results_dict = get_sim_data(exp_info, params_str, model)
    
    # Get experimental / simulation data
    if OPTION == "cr_strain_tf":
        exp_list, sim_list = get_end_lists(results_dict, "creep", "strain")
    if OPTION == "cr_time_tf":
        exp_list, sim_list = get_end_lists(results_dict, "creep", "time")
        exp_list = [t/3600 for t in exp_list]
        sim_list = [t/3600 for t in sim_list]
    if OPTION == "cr_strain":
        exp_list, sim_list = get_y_list(results_dict, "creep", "time", "strain")
    if OPTION == "ts_stress":
        exp_list, sim_list = get_y_list(results_dict, "tensile", "strain", "stress")
    if OPTION == "ts_yield":
        exp_list, sim_list = get_yield_point(results_dict, "tensile")
    if OPTION == "ts_uts":
        exp_list, sim_list = get_end_lists(results_dict, "tensile", "stress")

    # Return
    return exp_list, sim_list

# Calibration data
cal_info_list = [[
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_70_G44.csv",  "time_end": None,     "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_80_G25.csv",  "time_end": None,     "yield": None},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_800_D7.csv",      "time_end": None,     "yield": 291},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_31_G50.csv",  "time_end": None,     "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_36_G22.csv",  "time_end": None,     "yield": None},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_900_D10.csv",     "time_end": None,     "yield": 164},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_13_G30.csv", "time_end": 16877844, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_16_G18.csv", "time_end": 7756524,  "yield": None},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_1000_D12.csv",    "time_end": None,     "yield": 90},
]]

# Validation data
val_info_list = [[
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_60_G32.csv",  "time_end": None,     "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_65_G33.csv",  "time_end": None,     "yield": None},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_26_G59.csv",  "time_end": 20541924, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_28_G45.csv",  "time_end": None,     "yield": None},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_11_G39.csv", "time_end": 19457424, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_12_G48.csv", "time_end": 18096984, "yield": None},
]]

if MODEL_INDEX == 0:

    # Optimal parameters
    opt_params_str_list = [
    """
    23.304	276.66	0.32123	4.2592	1767.2	2168.5	5.3181	6.7619
    """,
    """
    3.6262	13.804	6.9825	4.2416	1138.2	1986	4.4408	9.193
    """,
    """
    0.31556	4.9177	4.2816	4.8134	468.63	3308.8	3.3387	5.7804
    """,
    ]

    # Other parameters
    params_str_list = [
    """
    16.994	187.83	0.26104	4.502	1784.8	3263.5	4.9231	13.172
    22.454	66.77	0.92681	4.4191	1610.1	2142	5.4844	11.449
    19.125	43.641	5.6148	4.1688	1616	1876.8	5.5594	6.8653
    31.647	120.62	0.85485	3.7266	2297.8	2165.7	5.3247	7.7724
    33.297	522.85	0.11871	3.9767	1762.4	1913.8	5.6638	11.287
    15.042	35.437	8.4	3.9586	2283.5	4184.6	4.4257	6.6603
    24.889	44.932	1.2076	4.5055	1527.9	2589.7	5.1066	8.695
    30.401	34.817	4.5983	3.5323	2583	2520.9	5.1559	8.5891
    5.0569	40.476	10.017	4.1585	1730.1	1998.1	5.5564	10.337
    """,
    """
    11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225
    11.394	13.887	7.532	3.5691	1581.2	1959.8	4.4121	8.5847
    5.6656	7.6357	9.1337	4.3001	1055.4	3494.5	3.9629	11.623
    8.0846	21.623	4.9985	3.8734	1330.8	2586.3	4.0925	6.8218
    8.7008	379.67	0.15739	4.2166	994.53	1533.4	4.6802	7.0461
    9.344	45.972	2.5375	3.4094	1902	2101.5	4.3022	6.1081
    16.257	181.45	0.5026	3.0154	2606.2	2445.1	4.1307	5.6964
    6.4694	149.62	0.29611	4.1942	1123.8	2045.9	4.4272	9.5323
    7.9997	25.008	2.2597	4.127	1102.2	1841.7	4.5535	10.206
    """,
    """
    0.0046173	6.8476	2.2387	4.8326	460.38	2357.9	3.5989	6.8922
    3.1901	126.5	0.16925	3.8924	802.2	2253.9	3.6876	11.145
    0.26189	37.662	0.20134	4.8079	478.84	2939.9	3.4262	5.9609
    1.5332	6.9652	4.9491	4.3072	551.01	1467.1	4.0639	13.561
    0.18711	42.057	1.22	3.9495	803.58	1759.6	3.8088	6.9718
    3.4416	6.259	1.314	4.0782	707.11	4504.6	3.2162	8.2904
    4.5325	14.166	2.2205	3.8813	731.02	2379.1	3.5504	6.0315
    3.3203	95.748	0.45552	4.0634	574.87	1034.8	4.2291	6.0322
    4.0855	246.68	0.084526	3.9321	776.2	2681.7	3.4426	5.5305
    """
    ]

if MODEL_INDEX == 1:

    # Optimal parameters
    opt_params_str_list = [
    """
    22.154	462.34	0.17408	4.314	1828.1	40.1	260.65	408.44	853.65	1.9241	7.7562
    """,
    """
    6.3647	183.42	0.44712	4.1839	1075.3	27.326	165.15	422.54	849.67	2.2181	10.568
    """,
    """
    0.2367	39.667	1.2775	4.4023	559.5	9.3449	62.201	262.65	587.44	2.0144	8.7398
    """,
    ]

    # Other parameters
    params_str_list = [
    """
    15.532	158.4	0.53509	4.4223	1866.2	38.705	252.32	356.78	743.33	1.9693	12.056
    5.6925	67.1	1.8542	4.7721	1621.6	72.41	404.77	243.19	619.93	2.4798	11.411
    19.2	52.605	1.542	4.5105	1614.6	42.528	267.95	334.54	705.42	2.4141	9.9943
    31.327	105.29	0.8549	3.7256	2576.7	54.271	333.56	307.45	694.47	1.9991	6.8035
    11.45	53.135	7.1795	3.9502	2205.4	30.864	224.62	340.9	729.26	1.3505	6.6858
    17.982	81.509	0.84105	4.509	1673.3	39.98	258.79	402.01	829.72	2.2452	8.533
    24	301.54	0.32008	4.2863	1836.9	23.714	176.69	323.4	686.91	1.6048	13.085
    27.852	31.391	9.837	3.6958	2458	31.947	224.92	521.29	982.66	1.5924	18.309
    29.914	48.373	2.3508	3.9615	2094.7	27.335	200.15	367.9	765.16	1.639	19.667
    """,
    """							
    5.82	16.046	8.3648	4.1595	1064.7	38.773	222.24	393.28	859.75	2.3825	4.5047
    11.616	16.725	6.3631	3.6491	1303.7	40.805	222.15	829.14	644.22	3.2018	1.2554
    9.8394	12.026	14.017	3.7429	1275	36.916	211.85	498.46	952.62	2.4338	11.505
    5.7368	8.3864	16.064	4.3916	855.39	33.396	191.41	420.91	779.17	3.6322	8.1479
    7.5309	23.5	5.1998	3.862	1374.9	24.858	154.83	511.79	997.24	2.0041	7.9977
    4.8239	389.25	0.18435	4.4133	941.87	44.974	248.15	621.83	913.9	2.4338	7.0609
    6.6289	48.408	4.0515	3.7586	1383.6	45.15	253.49	553.63	866.98	1.6648	8.7312
    16.262	181.79	0.52517	3.0161	2376.6	29.326	172.8	434.17	894.26	2.192	2.8518
    7.9872	16.104	7.2157	4.2939	892.7	13.577	93.551	360.21	764.12	1.9879	15.103
    """,
    """
    0.13199	6.5191	11.588	4.5757	530.9	7.2545	51.111	244.85	554.46	1.4924	7.066
    3.211	111.3	0.17971	4.0658	797.47	7.4637	50.736	283.99	637.4	1.4863	5.3119
    0.013628	19.84	4.4536	4.4892	542.97	7.6866	53.311	281.25	622.97	1.3136	7.8413
    1.3829	13.171	6.4312	4.1312	644.36	8.422	55.973	261.83	583.57	1.8614	11.981
    3.455	16.732	6.9347	3.865	726.51	8.2554	55.102	253.49	563.13	1.3979	7.9624
    2.7525	16.605	1.2867	4.2536	650.11	7.4409	51.438	248.11	562.08	1.554	8.8352
    3.7022	24.227	2.4711	3.6321	870.39	8.2223	55.404	257.43	593.35	1.9805	8.9843
    2.7156	41.193	0.31274	4.0819	825.7	10.001	64.808	248.52	559.21	1.6577	10.642
    3.32	381.2	0.07715	4.1319	716.42	7.8478	53.547	261.99	583.71	1.3314	8.2668
    """
    ]

# Prepare model and plot
model = MODEL(MODEL_NAME)
fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

# Define data specific settings
if OPTION == "cr_time_tf":
    limits = (0, 12000)
    ax.ticklabel_format(axis="x", style="sci", scilimits=(3,3))
    ax.xaxis.major.formatter._useMathText = True
    ax.ticklabel_format(axis="y", style="sci", scilimits=(3,3))
    ax.yaxis.major.formatter._useMathText = True
if OPTION == "cr_strain_tf":
    limits = (0, 0.8)
if OPTION == "cr_strain":
    limits = (0, 0.6)
if OPTION == "ts_yield":
    limits = (0, 600)
if OPTION == "ts_uts":
    limits = (0, 600)
if OPTION == "ts_stress":
    limits = (0, 600)

# Set labels and plot line
plt.xlabel(f"Simulated {INFO}", fontsize=15)
plt.ylabel(f"Measured {INFO}", fontsize=15)
plt.plot(limits, limits, linestyle="--", color="black", zorder=1)

# Testing parameters
# opt_params_str_list = ["23.304	276.66	0.32123	4.2592	1767.2	2168.5	5.3181	6.7619",
#                        "11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225"]
# params_str_list = ["16.994	187.83	0.26104	4.502	1784.8	3263.5	4.9231	13.172",
#                    "11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225"]

# Iterate through parameters
marker_list = ["^", "s", "*"]
for i in range(len(params_str_list)):

    # Get data
    cal_exp_list, cal_sim_list = get_data_points(cal_info_list[i], params_str_list[i], model)
    val_exp_list, val_sim_list = get_data_points(val_info_list[i], params_str_list[i], model)
    opt_cal_exp_list, opt_cal_sim_list = get_data_points(cal_info_list[i], opt_params_str_list[i], model)
    opt_val_exp_list, opt_val_sim_list = get_data_points(val_info_list[i], opt_params_str_list[i], model)

    # Plot data
    plt.scatter(cal_sim_list,     cal_exp_list,     zorder=2, edgecolor="none",  color="green",  linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i], alpha=TRANSPARENCY)
    plt.scatter(val_sim_list,     val_exp_list,     zorder=2, edgecolor="none",  color="red",    linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i], alpha=TRANSPARENCY)
    plt.scatter(opt_cal_sim_list, opt_cal_exp_list, zorder=2, edgecolor="black", color="green",  linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i])
    plt.scatter(opt_val_sim_list, opt_val_exp_list, zorder=2, edgecolor="black", color="red",    linewidth=LINEWIDTH, s=MARKER_SIZE**2, marker=marker_list[i])

# Add 'conservative' region
triangle_vertices = np.array([[limits[0], limits[0]], [limits[1], limits[0]], [limits[1], limits[1]]])
ax.fill(triangle_vertices[:, 0], triangle_vertices[:, 1], color="gray", alpha=0.3)
plt.text(limits[1]-0.45*(limits[1]-limits[0]), limits[0]+0.05*(limits[1]-limits[0]), "Non-conservative", fontsize=12, color="black")

# Prepare legend for data type
handle_list = []
if "ts" in OPTION:
    cal = plt.scatter([], [], color="green", label="Calibration", s=8**2)
    legend = plt.legend(handles=[cal], framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=12, loc="upper right")
else:
    cal = plt.scatter([], [], color="green", label="Calibration", s=8**2)
    val = plt.scatter([], [], color="red", label="Validation", s=8**2)
    legend = plt.legend(handles=[cal, val], framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=12, loc="upper right")
plt.gca().add_artist(legend)

# Prepare legend for data temperature
t800  = plt.scatter([], [], color="none", edgecolor="black", linewidth=LINEWIDTH,  label="800°C",  marker="^", s=MARKER_SIZE**2)
t900  = plt.scatter([], [], color="none", edgecolor="black", linewidth=LINEWIDTH,  label="900°C",  marker="s", s=MARKER_SIZE**2)
t1000 = plt.scatter([], [], color="none", edgecolor="black", linewidth=LINEWIDTH,  label="1000°C", marker="*", s=MARKER_SIZE**2)
legend = plt.legend(handles=[t800, t900, t1000], framealpha=1, edgecolor="black",
                    fancybox=True, facecolor="white", fontsize=12, bbox_transform=(0.75, 0.75))
plt.gca().add_artist(legend)

# Format everything else and save
plt.gca().set_position([0.17, 0.12, 0.75, 0.75])
plt.gca().grid(which="major", axis="both", color="SlateGray", linewidth=1, linestyle=":")
plt.xlim(limits)
plt.ylim(limits)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.gcf().set_size_inches(5, 5)
plt.savefig(f"{MODEL_NAME}_{OPTION}.png")
