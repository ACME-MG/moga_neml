"""
 Title:         The Model Factory
 Description:   For creating and returning model objects
 Author:        Janzen Choi

"""

# Models
from evp import EVP
from evpcd import EVPCD
from evpwd import EVPWD
from th import TH
from thkr import THKR

# NEML Path
NEML_PATH = "/home/janzen/moose/neml"

# Creates and return a model
def get_model(model_name, exp_curves):
    model_list = (
        EVP(exp_curves),
        EVPCD(exp_curves),
        EVPWD(exp_curves),
        TH(exp_curves),
        THKR(exp_curves),
    )
    model_list = [model for model in model_list if model.get_name() == model_name]
    return model_list[0]