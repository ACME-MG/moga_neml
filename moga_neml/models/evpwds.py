"""
 Title:         The Elastic Viscoplastic Work Damage Model with an inverse polynomial for work damage
 Description:   Incorporates elasto-viscoplasticity and work damage
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from moga_neml.models.__model__ import __Model__
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow, damage, interpolate

# The Elastic Visco Plastic Work Damage Class
class Model(__Model__):

    # Runs at the start, once
    def initialise(self):
        
        # Define parameters
        self.add_param("evp_s0",  0.0e0, 1.0e3) # 2
        self.add_param("evp_R",   0.0e0, 1.0e4) # 2
        self.add_param("evp_d",   0.0e1, 1.0e3) # 2
        self.add_param("evp_n",   1.0e0, 1.0e2) # 2
        self.add_param("evp_eta", 0.0e1, 1.0e6)
        self.add_param("wd_n",    1.0e0, 1.0e2)
        self.add_param("wd_x_f",  0.0e0, 1.0e2)
        self.add_param("wd_y_f",  0.0e0, 1.0e3)
        self.add_param("wd_x_t", -1.0e2, 0.0e0)
        self.add_param("wd_y_t",  0.0e0, 1.0e3)
        self.add_param("wd_g_1",  0.0e0, 1.0e0)
        self.add_param("wd_g_2",  0.0e0, 1.0e0)

    # Gets the predicted curve
    def calibrate_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_n, wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2):
        
        # Define EVP model
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        
        # Get interpolation
        x_list = list(np.linspace(-16, 0, 20))
        try:
            y_list = [get_damage(x, wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2) for x in x_list]
            y_list = [math.log10(y) for y in y_list]
        except:
            return
        wd_wc  = interpolate.PiecewiseLinearInterpolate(x_list, y_list)
        
        # Define work damage model and return
        wd_model = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=1e-40, work_scale=1e5)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model

# Gets the damage value for interpolation
#   x_f and y_f for scaling
#   x_t and y_t for translating
#   g_1 and g_2 are left and right gradients (0, 1)
def get_damage(x_0, x_f, y_f, x_t, y_t, g_1, g_2):
    
    # Get all possible values
    f_0 = lambda x : y_f*math.tanh(x_f*x - x_t) + y_t
    x_1 = (x_t - math.atanh(math.sqrt(1 - g_1/y_f/x_f))) / x_f
    x_2 = (x_t + math.atanh(math.sqrt(1 - g_2/y_f/x_f))) / x_f
    
    # Determine which part of the curve the x_0 value lies
    if x_0 < x_1:
        return g_1 * (x_0 - x_1) + f_0(x_1)
    elif x_0 > x_2:
        return g_2 * (x_0 - x_2) + f_0(x_2)
    else:
        return f_0(x_0)
