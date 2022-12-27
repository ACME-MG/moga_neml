"""
 Title:         Main file
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
from modules.api import API

# Code
api = API(True)
api.define_conditions(800, 80)
api.define_sm("thkr")
# api.sample_CCD(show_plot=False)
api.sample_random(5000, show_plot=False)
api.train(epochs=100, batch_size=100)
api.assess(20)