"""
 Title:         The Model Factory
 Description:   For creating and returning model objects
 Author:        Janzen Choi

"""

# Models
from evp import EVP
from evpcd import EVPCD
from evpwd import EVPWD
from evpwd_s import EVPWD_S
from th import TH
from thkr import THKR
from vshai import VSHAI
from polynomial import Polynomial

# Creates and return a model
def get_model(model_name, exp_curves, args):
    model_list = (
        EVP(exp_curves),
        EVPCD(exp_curves),
        EVPWD(exp_curves),
        EVPWD_S(exp_curves),
        TH(exp_curves),
        THKR(exp_curves),
        VSHAI(exp_curves),
        Polynomial(exp_curves)
    )
    model = [model for model in model_list if model.get_name() == model_name][0]
    model.prepare(args)
    return model