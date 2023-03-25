# Libraries
import matplotlib.pyplot as plt

# Converts a CSV filename into a dictionary
def get_curve(file_name):

    # Read data
    file = open(file_name, "r")
    headers = file.readline().replace("\n","").split(",")
    data = [line.replace("\n","").split(",") for line in file.readlines()]
    file.close()
    
    # Get x and y data
    x_index = headers.index("x")
    y_index = headers.index("y")
    x_list = [float(d[x_index]) for d in data]
    y_list = [float(d[y_index]) for d in data]

    # Get auxiliary information
    curve_dict = {"x": x_list, "y": y_list}
    for i in range(len(headers)):
        if not headers[i] in ["x", "y"]:
            try:
                value = float(data[0][i])
            except:
                value = data[0][i]
            curve_dict[headers[i]] = value
    return curve_dict

# File names
file_names_list = [[
    {"file_name": "AirBase_800_60_G32.csv", "colour": "blue"},
    {"file_name": "AirBase_800_60_G47.csv", "colour": "royalblue"},
    {"file_name": "AirBase_800_65_G33.csv", "colour": "darkred"},
    {"file_name": "AirBase_800_65_G43.csv", "colour": "red"},
    {"file_name": "AirBase_800_70_G24.csv", "colour": "green"},
    {"file_name": "AirBase_800_70_G44.csv", "colour": "limegreen"},
    {"file_name": "AirBase_800_80_G25.csv", "colour": "darkorange"},
    {"file_name": "AirBase_800_80_G34.csv", "colour": "orange"},
],[
    {"file_name": "AirBase_900_26_G42.csv", "colour": "blue"},
    {"file_name": "AirBase_900_26_G59.csv", "colour": "royalblue"},
    {"file_name": "AirBase_900_28_G40.csv", "colour": "darkred"},
    {"file_name": "AirBase_900_28_G45.csv", "colour": "red"},
    {"file_name": "AirBase_900_31_G21.csv", "colour": "green"},
    {"file_name": "AirBase_900_31_G50.csv", "colour": "limegreen"},
    {"file_name": "AirBase_900_36_G19.csv", "colour": "darkorange"},
    {"file_name": "AirBase_900_36_G22.csv", "colour": "orange"},
    {"file_name": "AirBase_900_36_G63.csv", "colour": "gold"},
],[
    {"file_name": "AirBase_1000_11_G39.csv", "colour": "blue"},
    {"file_name": "AirBase_1000_12_G48.csv", "colour": "darkred"},
    {"file_name": "AirBase_1000_12_G52.csv", "colour": "red"},
    {"file_name": "AirBase_1000_13_G30.csv", "colour": "green"},
    {"file_name": "AirBase_1000_13_G51.csv", "colour": "limegreen"},
    {"file_name": "AirBase_1000_16_G18.csv", "colour": "darkorange"},
    {"file_name": "AirBase_1000_16_G38.csv", "colour": "orange"},
]]

# Prepares the plots
figure, axes = plt.subplots(1, 3)
figure.set_size_inches(17, 5)
titles = ["Alloy 617 at 800°C", "Alloy 617 at 900°C", "Alloy 617 at 1000°C"]

# Create plots
for i in range(3):
    axes[i].set_title(titles[i])
    axes[i].set_xlabel("Time (h)")
    axes[i].set_ylabel("Strain")
    axes[i].grid(which='major', axis='both', color='SlateGray', linewidth=0.5, linestyle=':')
    curve_dict_list = [get_curve(file_name["file_name"]) for file_name in file_names_list[i]]
    for j in range(len(curve_dict_list)):
        axes[i].scatter(curve_dict_list[j]["x"], curve_dict_list[j]["y"], marker="o", color=file_names_list[i][j]["colour"])
    stresses = [f"{round(curve_dict['stress'])} MPa" for curve_dict in curve_dict_list]
    axes[i].legend(stresses)

# Save results
figure.savefig("plot.png")