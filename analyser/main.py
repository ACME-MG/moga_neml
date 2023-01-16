"""
 Title:         Analyser Main
 Description:   For analysing creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True)
api.define_conditions(800, 80)
api.define_model("evpwd")
api.assess_dependency(1000)