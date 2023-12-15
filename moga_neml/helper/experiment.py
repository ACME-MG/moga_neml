"""
 Title:         Experiment related data
 Description:   Stores maps for experiment results
 Author:        Janzen Choi

"""

# Stores required fields for experimental data
DATA_FIELD_DICT = {
    "common":  {"lists": [], "values": ["temperature", "youngs", "poissons"]},
    "creep":   {"lists": ["time", "strain"], "values": ["stress"]},
    "tensile": {"lists": ["time", "strain", "stress"], "values": ["strain_rate"]},
    "cyclic":  {"lists": ["time", "strain", "stress"], "values": ["num_cycles", "strain_rate"]},
}

# Stores labels for each type of test
NEML_FIELD_CONVERSION = {
    "creep":   {"rtime": "time", "rstrain": "strain", "history": "history"},
    "tensile": {"strain": "strain", "stress": "stress", "history": "history"},
    "cyclic":  {"time": "time", "strain": "strain", "stress": "stress", "history": "history"}
}

# Identifies which fields to plot by default
DATA_FIELD_PLOT_MAP = {
    "creep":   [{"x": "time", "y": "strain"}],
    "tensile": [{"x": "strain", "y": "stress"}],
    "cyclic":  [{"x": "strain", "y": "stress"}, {"x": "time", "y": "strain"}, {"x": "time", "y": "stress"}],
}

# Stores all the units
DATA_UNITS = {
    "poissons": "",
    "stress": "MPa",
    "strain": "mm/mm",
    "temperature": "°C",
    "time": "h",
    "youngs": "MPa",
}

# Returns a list of x and y labels for a data type
def get_labels_list(type:str) -> list:
    labels_list = []
    for i in range(len(DATA_FIELD_PLOT_MAP[type])):
        x_label = DATA_FIELD_PLOT_MAP[type][i]["x"]
        y_label = DATA_FIELD_PLOT_MAP[type][i]["y"]
        labels_list.append((x_label, y_label))
    return labels_list
