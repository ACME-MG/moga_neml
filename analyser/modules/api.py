"""
 Title:         API for Surrogate Modelling
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
import sys
import modules.domain_explorer as domain_explorer

# Helper libraries
sys.path += ["../__common__", "../__models__"]
from api_template import APITemplate
from __model_factory__ import get_model
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

    # Assesses the individual parameters
    def assess_domain(self, dependency=False, trials=10):
        if dependency:
            self.add(f"Assessing the interdependency of the parameters in their domains")
            domain_explorer.assess_dependency(self.model, self.get_output("dependent"), trials)
        else:
            self.add(f"Assessing the parameters in their domains")
            domain_explorer.assess_individual(self.model, self.get_output("individual"), trials)
    
    # Asees