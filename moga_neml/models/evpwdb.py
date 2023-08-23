"""
 Title:         The Elastic Viscoplastic Work Damage Model with bilinear function for work damage
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
        self.add_param("wd_a_n",  1.0e0, 2.0e1)
        self.add_param("wd_a_0",  0.0e0, 1.0e0)
        self.add_param("wd_a_1",  0.0e0, 1.0e1)
        self.add_param("wd_b_n",  1.0e0, 2.0e1)
        self.add_param("wd_b_0",  0.0e0, 1.0e0)
        self.add_param("wd_b_1",  0.0e0, 1.0e1)

    # Gets the predicted curve
    def calibrate_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_a_n, wd_a_0, wd_a_1, wd_b_n, wd_b_0, wd_b_1):
        
        # Define EVP model
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        
        # Get work - work-rate interpolation
        try:
            x_list, y_list = get_damage(wd_a_0, wd_a_1, wd_b_0, wd_b_1)
        except:
            return
        wd_wc = interpolate.PiecewiseLinearInterpolate(x_list, y_list)
        
        # TODO temporary relation (should be interpolator too)
        wd_n = wd_a_n if self.get_data("type") == "creep" else wd_b_n # tensile
        
        # Define work damage model and return
        wd_model = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=1e-40, work_scale=1e5)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model

def get_damage(a_0:float, a_1:float, b_0:float, b_1:float):
    """
    Gets the damage interpolation bilinear curve
    
    Parameters:
    * `a_0`: Gradient for left side of bilinear function
    * `a_1`: Vertical intercept for left side of bilinear function
    * `b_0`: Gradient for right side of bilinear function
    * `b_1`: Vertical intercept for right side of bilinear function
    
    Returns the x and y coordinates (on the log10-log10 scale)
    """
    
    # Get x values
    x_0 = -a_1 / a_0                # x intercept of left line and x axis
    x_1 = (b_1 - a_1) / (a_0 - b_0) # x intercept of two lines
    x_2 = 2                         # x intercept of right line and x=2
    
    # Get y values
    y_0 = 0                         # y intercept of left line and x axis
    y_1 = a_0 * x_1 + a_1           # y intercept of two lines
    y_2 = b_0 * x_2 + b_1           # y intercept of right line and x=2
    
    # Combine, log, and return
    num_points = 16
    x_list = list(np.linspace(x_0, x_1, num_points)) + list(np.linspace(x_1, x_2, num_points))
    y_list = list(np.linspace(y_0, y_1, num_points)) + list(np.linspace(y_1, y_2, num_points))
    return x_list, y_list
