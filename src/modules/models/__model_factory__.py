"""
 Title:         The Model Factory
 Description:   For creating and returning model objects
 Author:        Janzen Choi

"""

# Models
from modules.models.evp import EVP
from modules.models.evpcd import EVPCD
from modules.models.evpwd import EVPWD
from modules.models.evpwd_s import EVPWD_S
from modules.models.th import TH
from modules.models.thkr import THKR
from modules.models.vshai import VSHAI

# Creates and return a model
def get_model(model_name, exp_curves, args):
    model_list = (
        EVP(exp_curves),
        EVPCD(exp_curves),
        EVPWD(exp_curves),
        EVPWD_S(exp_curves),
        TH(exp_curves),
        THKR(exp_curves),
        VSHAI(exp_curves)
    )
    model = [model for model in model_list if model.get_name() == model_name][0]
    model.prepare(args)
    return model