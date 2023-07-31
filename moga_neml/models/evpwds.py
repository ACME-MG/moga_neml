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
        self.add_param("wd_g_1",  0.0e0, 1.0e3)
        self.add_param("wd_g_2",  0.0e0, 1.0e3)

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
        try:
            x_list, y_list = get_damage(wd_x_f, wd_y_f, wd_x_t, wd_y_t, wd_g_1, wd_g_2)
        except:
            return
        wd_wc = interpolate.PiecewiseLinearInterpolate(x_list, y_list)
        
        # Define work damage model and return
        wd_model = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=1e-40, work_scale=1e5)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model

def get_damage(x_f:float, y_f:float, x_t:float, y_t:float, g_1:float, g_2:float):
    """
    Gets the damage interpolation sigmoid curve
    
    Parameters:
    * `x_f`: Scale factor for the x coordinates
    * `y_f`: Scale factor for the y coordinates
    * `x_t`: Translation amount for the x coordinates
    * `y_t`: Translation amount for the y coordinates
    * `g_1`: The gradient of the left side of the sigmoid
    * `g_2`: The gradient of the right side of the sigmoid
    
    Returns the x and y coordinates (on the log 10 scale)
    """
    
    # Initialise function
    f_0 = lambda x : y_f*math.tanh(x_f*x - x_t) + y_t
    x_1 = (x_t - math.atanh(math.sqrt(1 - g_1/y_f/x_f))) / x_f
    x_2 = (x_t + math.atanh(math.sqrt(1 - g_2/y_f/x_f))) / x_f
    x_0 = x_1 - f_0(x_1) / g_1
    
    # Determine x coordinates based on sigmoid shifts
    x_list = [x_0] + list(np.linspace(x_1, x_2, 16)) + [0]
    
    # Determine damage based on x coordinates
    def get_y(x):
        if x < x_1:
            return g_1 * (x-x_1) + f_0(x_1)
        elif x > x_2:
            return g_2 * (x-x_2) + f_0(x_2)
        else:
            return f_0(x)
    
    # Calculate x and y coordinates and return
    y_list = [get_y(x) for x in x_list]
    y_list = [math.log10(y) if y > 0 else 0 for y in y_list]
    return x_list, y_list
