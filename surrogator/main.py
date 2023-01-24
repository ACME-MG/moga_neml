"""
 Title:         Main file
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
from modules.api import API

# Code
api = API(True, verbose=True)
api.define_conditions("creep", 800, 80)
api.define_model("evpwd_s")
api.define_trainer("simple")
api.define_surrogate("ann")
api.read_input_output("evpwd_s_io.csv", size=1000)
api.train()
api.read_input_output("evpwd_s_io.csv", size=10)
api.assess()