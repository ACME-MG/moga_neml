"""
 Title:         Experiment related data
 Description:   Stores maps for experiment results
 Author:        Janzen Choi

"""

# Defines how much data points to store
DATA_DENSITY = 500

# Stores required fields for experimental data
DATA_FIELD_DICT = {
    "common":  {"lists": [], "values": ["temperature", "youngs", "poissons"]},
    "creep":   {"lists": ["time", "strain"], "values": ["stress"]},
    "tensile": {"lists": ["time", "strain", "stress"], "values": ["strain_rate"]},
    "cyclic":  {"lists": ["time", "strain", "stress"], "values": ["num_cycles", "strain_rate"]},
}

# Stores labels for each type of test
NEML_FIELD_CONVERSION = {
    "creep":   {"rtime": "time", "rstrain": "strain", "history": "damage"},
    "tensile": {"strain": "strain", "stress": "stress"},
    "cyclic":  {"time": "time", "strain": "strain", "stress": "stress"}
}

# Identifies which fields to plot by default
DATA_FIELD_PLOT_MAP = {
    "creep":   {"x": "time", "y": "strain"},
    "tensile": {"x": "strain", "y": "stress"},
    "cyclic":  {"x": "strain", "y": "stress"},
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