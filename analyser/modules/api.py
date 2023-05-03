"""
 Title:         API for Surrogate Modelling
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
import sys
import modules.domain_explorer as domain_explorer
import modules.param_changer as param_changer

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from api_template import APITemplate
from __model__ import get_model
from curve import get_curve

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title="", display=2):
        super().__init__(title, display)
        self.plot_count = 1
        self.curve_list = []

    # Adds a curve and defines its conditions
    def add_curve(self, info_dict={"type": "creep", "stress": 80, "temp": 800}):
        curve = get_curve([0], [0], info_dict)
        self.curve_list.append(curve)

    # Defines the model
    def define_model(self, model_name=""):
        self.add(f"Defining the {model_name} model")
        self.model = get_model(model_name, self.curve_list)
        self.change_params = self.model.get_param_names()

    # Assesses the failure points for individual parameters
    def locate_failure(self, dependency=False, trials=10):
        if dependency:
            self.add(f"Locates model failures for parameter pairs")
            domain_explorer.assess_dependency(self.model, self.get_output(f"plot_{self.plot_count}"), trials)
        else:
            self.add(f"Locates model failures for individual parameter")
            domain_explorer.assess_individual(self.model, self.get_output(f"plot_{self.plot_count}"), trials)
        self.plot_count += 1
    
    # Isolates the parameters for changing
    def isolate_params(self, params):
        self.add(f"Isolating {len(params)} parameters")
        self.change_params = params

    # Investigates the effects of changing individual parameters
    def param_effects(self, base_params, change=0.1, steps=3):
        self.add(f"Investigating the effects of changing parameters")
        param_changer.investigate_params(self.model, self.change_params, base_params, change, steps, self.get_output(f"plot_{self.plot_count}"))
        self.plot_count += 1