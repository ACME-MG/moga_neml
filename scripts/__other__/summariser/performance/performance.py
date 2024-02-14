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
from moga_neml.errors.yield_point import get_yield

# Varying constants
OPTION_INDEX = int(sys.argv[1])
MODEL_INDEX  = 1

# Non-changing constants
DATA_PATH = "../../../data"
OPTION    = ["creep_strain_area", "creep_time_tf", "creep_strain_tf", "tensile_stress_area", "tensile_yield"][OPTION_INDEX]
UNIT      = ["mm/mm", "h", "mm/mm", "MPa", "MPa"][OPTION_INDEX]
MODEL     = [EVPCD, EVPWD][MODEL_INDEX]

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
def get_sim_data(exp_info_list:list, params_str:str, model) -> dict:

    # Initialise
    params_list = [list(map(float, line.split())) for line in params_str.strip().split("\n")]
    results_dict = {}

    # Iterate through experimental data
    for exp_info in exp_info_list:

        # Get experimental data
        exp_data = get_exp_data(exp_info["path"])
        exp_data = remove_data(exp_data, "time", exp_info["time_end"])
        exp_data["min_dy"] = exp_info["min_dy"]
        exp_data["yield"] = exp_info["yield"]
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

# Calculates the experimental and simulated minimum derivative values of the curve
def get_min_dy_lists(results_dict:dict, data_type:str, x_label:str, y_label:str) -> tuple:

    # Initialise
    exp_min_dy_list, sim_min_dy_list = [], []
    
    # Iterate through experimental curves
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue
        exp_min_dy = exp_data["min_dy"]

        # Iterate through simulations of experimental curve
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:

            # Get simulated minimum derivative value
            sim_d_data = differentiate_curve(sim_data, x_label, y_label)
            sim_min_dy = sim_d_data[y_label][len(sim_d_data[y_label])//2]
            
            # Add to initialised super list
            exp_min_dy_list.append(exp_min_dy)
            sim_min_dy_list.append(sim_min_dy * 3600)
    
    # Return
    return exp_min_dy_list, sim_min_dy_list


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

            # # Normalise
            # max_value = max(exp_y_values)
            # exp_y_values = linearly_map(exp_y_values, 0, max_value)
            # sim_y_values = linearly_map(sim_y_values, 0, max_value)

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

# Calculates the experimental and simulated arg max value
def get_arg_max(results_dict:dict, data_type:str, x_label:str, y_label:str) -> tuple:

    # Initialise
    exp_arg_max_list, sim_arg_max_list = [], []
    
    # Iterate through experimental curves
    for title in results_dict.keys():
        exp_data = results_dict[title]["exp"]
        if exp_data["type"] != data_type:
            continue

        # Getting arg max of experimental curve
        exp_max_index = exp_data[y_label].index(max(exp_data[y_label]))
        exp_arg_max = exp_data[x_label][exp_max_index]

        # Iterate through simulations of experimental curve
        sim_data_list = results_dict[title]["sim"]
        for sim_data in sim_data_list:
            sim_data[y_label] = list(sim_data[y_label])
            sim_max_index = sim_data[y_label].index(max(sim_data[y_label]))
            sim_arg_max = sim_data[x_label][sim_max_index]
            exp_arg_max_list.append(exp_arg_max)
            sim_arg_max_list.append(sim_arg_max)
    
    # Return
    return exp_arg_max_list, sim_arg_max_list

# Linearly maps a list of values to 0 and 1
def linearly_map(value_list:list, min_value:float, max_value:float) -> list:
    range_val = max_value - min_value
    value_list = [(value - min_value) / range_val for value in value_list]
    return value_list

# Gets experimental and simulation data
def get_data_points(info_list:list, params_str_list:list, model) -> tuple:

    # Initialise and iterate through parameters
    all_exp_list, all_sim_list = [], []
    for i in range(len(params_str_list)):
        results_dict = get_sim_data(info_list[i], params_str_list[i], model)
        
        # Get experimental / simulation data
        if OPTION == "creep_strain_tf":
            exp_list, sim_list = get_end_lists(results_dict, "creep", "strain")
        if OPTION == "creep_time_tf":
            exp_list, sim_list = get_end_lists(results_dict, "creep", "time")
            exp_list = [t/3600 for t in exp_list]
            sim_list = [t/3600 for t in sim_list]
        if OPTION == "creep_strain_area":
            exp_list, sim_list = get_y_list(results_dict, "creep", "time", "strain")
        if OPTION == "tensile_stress_area":
            exp_list, sim_list = get_y_list(results_dict, "tensile", "strain", "stress")
        if OPTION == "tensile_yield":
            exp_list, sim_list = get_yield_point(results_dict, "tensile")

        # Add to super lists
        all_exp_list += exp_list
        all_sim_list += sim_list

    # Return
    return all_exp_list, all_sim_list

# Calibration data
cal_info_list = [[
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_70_G44.csv",  "time_end": None,     "min_dy": 9.0345e-5, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_80_G25.csv",  "time_end": None,     "min_dy": 2.3266e-4, "yield": None},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_800_D7.csv",      "time_end": None,     "min_dy": None,      "yield": 291},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_31_G50.csv",  "time_end": None,     "min_dy": 5.3682e-5, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_36_G22.csv",  "time_end": None,     "min_dy": 1.2199e-4, "yield": None},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_900_D10.csv",     "time_end": None,     "min_dy": None,      "yield": 164},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_13_G30.csv", "time_end": 16877844, "min_dy": 2.6645e-5, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_16_G18.csv", "time_end": 7756524,  "min_dy": 6.7604e-5, "yield": None},
    {"path": f"{DATA_PATH}/tensile/inl/AirBase_1000_D12.csv",    "time_end": None,     "min_dy": None,      "yield": 90},
]]

# Validation data
val_info_list = [[
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_60_G32.csv",  "time_end": None,     "min_dy": 2.8910e-5, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_800_65_G33.csv",  "time_end": None,     "min_dy": 5.0385e-5, "yield": None},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_26_G59.csv",  "time_end": 20541924, "min_dy": 2.1864e-5, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_900_28_G45.csv",  "time_end": None,     "min_dy": 3.5312e-5, "yield": None},
], [
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_11_G39.csv", "time_end": 19457424, "min_dy": 1.2941e-5, "yield": None},
    {"path": f"{DATA_PATH}/creep/inl_1/AirBase_1000_12_G48.csv", "time_end": 18096984, "min_dy": 9.8962e-6, "yield": None},
]]

# Parameters
params_str_list = [
"""
16.78	98.973	0.60186	4.4156	1780.3	92.942	466.64	124.21	627.18	5.7007	2.1874
5.6925	67.1	1.8542	4.7721	1621.6	72.41	404.77	243.19	619.93	2.4798	11.411
19.2	52.605	1.542	4.5105	1614.6	42.528	267.95	334.54	705.42	2.4141	9.9943
31.327	105.29	0.8549	3.7256	2576.7	54.271	333.56	307.45	694.47	1.9991	6.8035
22.154	462.34	0.17408	4.314	1828.1	40.1	260.65	408.44	853.65	1.9241	7.7562
11.45	53.135	7.1795	3.9502	2205.4	30.864	224.62	340.9	729.26	1.3505	6.6858
19.025	97.214	0.88069	4.5055	1667.4	50.238	313.98	237.66	764.67	2.0071	2.7731
24	301.54	0.32008	4.2863	1836.9	23.714	176.69	323.4	686.91	1.6048	13.085
27.852	31.391	9.837	3.6958	2458	31.947	224.92	521.29	982.66	1.5924	18.309
29.914	48.373	2.3508	3.9615	2094.7	27.335	200.15	367.9	765.16	1.639	19.667
""",
"""
5.7151	13.737	7.017	4.2421	1138.4	70.744	372.33	129.14	800.2	1.5445	1.9831
11.192	16.738	5.9587	3.6369	1530.1	35.196	206.85	119.96	774.72	1.5092	2.5579
9.6829	13.118	13.621	3.5054	1604.4	19.213	129	110.83	868.84	1.0493	2.3566
5.6656	8.2222	14.47	4.3001	1006.2	144.26	644.21	178.5	935.23	10.004	2.8495
7.5309	23.5	5.1998	3.862	1374.9	24.858	154.83	511.79	997.24	2.0041	7.9977
4.8239	389.25	0.18435	4.4133	941.87	44.974	248.15	621.83	913.9	2.4338	7.0609
5.4767	43.262	6.1148	3.4084	1788.2	150.14	656.75	266.01	957.42	1.6911	1.0717
16.262	181.79	0.52517	3.0161	2376.6	29.326	172.8	434.17	894.26	2.192	2.8518
6.3647	183.42	0.44712	4.1839	1075.3	27.326	165.15	422.54	849.67	2.2181	10.568
6.5395	16.732	6.8581	4.1207	1096.5	119.77	547.38	572.3	678.83	2.3506	15.844
""",
"""
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
]
# params_str_list = [
# """
# 16.994	187.83	0.26104	4.502	1784.8	3263.5	4.9231	13.172
# 22.454	66.77	0.92681	4.4191	1610.1	2142	5.4844	11.449
# 19.125	43.641	5.6148	4.1688	1616	1876.8	5.5594	6.8653
# 31.647	120.62	0.85485	3.7266	2297.8	2165.7	5.3247	7.7724
# 33.297	522.85	0.11871	3.9767	1762.4	1913.8	5.6638	11.287
# 15.042	35.437	8.4	3.9586	2283.5	4184.6	4.4257	6.6603
# 24.889	44.932	1.2076	4.5055	1527.9	2589.7	5.1066	8.695
# 23.304	276.66	0.32123	4.2592	1767.2	2168.5	5.3181	6.7619
# 30.401	34.817	4.5983	3.5323	2583	2520.9	5.1559	8.5891
# 5.0569	40.476	10.017	4.1585	1730.1	1998.1	5.5564	10.337
# """,
# """
# 3.6262	13.804	6.9825	4.2416	1138.2	1986	4.4408	9.193
# 11.112	18.959	5.9505	3.6368	1471.6	2064.3	4.3164	7.225
# 11.394	13.887	7.532	3.5691	1581.2	1959.8	4.4121	8.5847
# 5.6656	7.6357	9.1337	4.3001	1055.4	3494.5	3.9629	11.623
# 8.0846	21.623	4.9985	3.8734	1330.8	2586.3	4.0925	6.8218
# 8.7008	379.67	0.15739	4.2166	994.53	1533.4	4.6802	7.0461
# 9.344	45.972	2.5375	3.4094	1902	2101.5	4.3022	6.1081
# 16.257	181.45	0.5026	3.0154	2606.2	2445.1	4.1307	5.6964
# 6.4694	149.62	0.29611	4.1942	1123.8	2045.9	4.4272	9.5323
# 7.9997	25.008	2.2597	4.127	1102.2	1841.7	4.5535	10.206
# """,
# """
# 0.0046173	6.8476	2.2387	4.8326	460.38	2357.9	3.5989	6.8922
# 3.1901	126.5	0.16925	3.8924	802.2	2253.9	3.6876	11.145
# 0.31556	4.9177	4.2816	4.8134	468.63	3308.8	3.3387	5.7804
# 0.26189	37.662	0.20134	4.8079	478.84	2939.9	3.4262	5.9609
# 1.5332	6.9652	4.9491	4.3072	551.01	1467.1	4.0639	13.561
# 0.18711	42.057	1.22	3.9495	803.58	1759.6	3.8088	6.9718
# 3.4416	6.259	1.314	4.0782	707.11	4504.6	3.2162	8.2904
# 4.5325	14.166	2.2205	3.8813	731.02	2379.1	3.5504	6.0315
# 3.3203	95.748	0.45552	4.0634	574.87	1034.8	4.2291	6.0322
# 4.0855	246.68	0.084526	3.9321	776.2	2681.7	3.4426	5.5305
# """
# ]

# Get data
model = MODEL("name")
cal_exp_list, cal_sim_list = get_data_points(cal_info_list, params_str_list, model)
val_exp_list, val_sim_list = get_data_points(val_info_list, params_str_list, model)

# Prepare plot
fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

# Define data specific settings
if OPTION == "creep_strain_tf":
    limits = (0.1, 0.5)
if OPTION == "creep_time_tf":
    limits = (0, 10000)
if OPTION == "creep_strain_area":
    limits = (0, 0.35)
if OPTION == "tensile_stress_area":
    limits = (0, 400)
if OPTION == "tensile_yield":
    limits = (50, 350)
# ax.ticklabel_format(axis="x", style="sci", scilimits=(-4,-4))
# ax.xaxis.major.formatter._useMathText = True
# ax.ticklabel_format(axis="y", style="sci", scilimits=(-4,-4))
# ax.yaxis.major.formatter._useMathText = True

# Set labels
plt.xlabel(f"Experimental ({UNIT})", fontsize=15)
plt.ylabel(f"Simulation ({UNIT})", fontsize=15)

# Plot line then data
plt.plot(limits, limits, linestyle="--", color="black")
plt.scatter(cal_exp_list, cal_sim_list, color="green")
plt.scatter(val_exp_list, val_sim_list, color="red")

# Add 'conservative' region
triangle_vertices = np.array([[limits[0], limits[0]], [limits[1], limits[0]], [limits[1], limits[1]]])
ax.fill(triangle_vertices[:, 0], triangle_vertices[:, 1], color="gray", alpha=0.3)
plt.text(limits[1]-0.35*(limits[1]-limits[0]), limits[0]+0.05*(limits[1]-limits[0]), "Conservative", fontsize=12, color="black")

# Prepare legend
if OPTION != "tensile_strain_tf":
    plt.plot([], [], color="black", label="1:1 Line", linestyle="--", linewidth=1.5)
    if not "tensile" in OPTION:
        plt.scatter([], [], color="red", label="Validation", s=6**2)
    plt.scatter([], [], color="green", label="Calibration", s=6**2)
    plt.legend(framealpha=1, edgecolor="black", fancybox=True, facecolor="white", fontsize=12)

# Format everything else and save
plt.gca().set_aspect("equal", adjustable="box")
plt.gca().set_position([0.17, 0.12, 0.75, 0.75])
plt.gca().grid(which="major", axis="both", color="SlateGray", linewidth=1, linestyle=":")
plt.xlim(limits)
plt.ylim(limits)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.savefig(f"plot_{OPTION}.png")
