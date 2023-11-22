"""
 Title:         The Elastic Viscoplastic Work Damage Model with bilinear function for work damage
 Description:   Incorporates elasto-viscoplasticity and work damage
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
from moga_neml.models.__model__ import __Model__
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow, damage, interpolate

# The Elastic Visco Plastic Work Damage Class
class Model(__Model__):

    def initialise(self):
        """
        Runs at the start, once
        """

        # Elastic parameters
        self.add_param("evp_s0",  0.0e0, 1.0e1) # 3
        self.add_param("evp_R",   0.0e0, 1.0e2) # 4
        self.add_param("evp_d",   0.0e0, 1.0e1) # 2
        self.add_param("evp_n",   1.0e0, 1.0e1) # 2
        self.add_param("evp_eta", 0.0e0, 1.0e4) # 5
        
        # Creep damage parameters
        self.add_param("c_n", 1.0e0, 2.0e1)
        self.add_param("c_0", 0.0e0, 1.0e0)
        self.add_param("c_1", 0.0e0, 1.0e1)

        # Tensile damage parameters
        self.add_param("t_n", 1.0e0, 2.0e1)
        self.add_param("t_0", 0.0e0, 1.0e0)
        self.add_param("t_1", 0.0e0, 1.0e1)

    def calibrate_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, c_n, c_0, c_1, t_n, t_0, t_1):
        """
        Gets the predicted curves

        Parameters:
        * `...`: ...

        Returns the calibrated model
        """
        
        # Define EVP model
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        
        # Prepare the critical points of the bilinear curve
        x_0, x_1, x_2, y_0, y_1, y_2 = get_bilinear(c_0, c_1, t_0, t_1)
        
        # Get work-work_rate interpolation
        try:
            x_list, y_list = get_wc(x_0, x_1, x_2, y_0, y_1, y_2)
        except:
            return
        wd_wc = interpolate.PiecewiseLinearInterpolate(x_list, y_list)
        
        # Get n-work_rate interpolation
        try:
            x_list, y_list = get_n(x_0, x_1, x_2, c_n, t_n)
        except:
            return
        wd_n = interpolate.PiecewiseLinearInterpolate(x_list, y_list)
        
        # Define work damage model and return
        wd_model = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=1e-40, work_scale=1e5)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model

def get_bilinear(a_0:float, a_1:float, b_0:float, b_1:float):
    """
    Gets the interpolation bilinear points
    
    Parameters:
    * `a_0`: Gradient for left side of bilinear function
    * `a_1`: Vertical intercept for left side of bilinear function
    * `b_0`: Gradient for right side of bilinear function
    * `b_1`: Vertical intercept for right side of bilinear function
    
    Returns the x and y coordinates of the critical points of the bilinear function
    """
    
    # Get x values
    x_0 = -a_1 / a_0                # x intercept of left line and x axis
    x_1 = (b_1 - a_1) / (a_0 - b_0) # x intercept of two lines
    x_2 = 3                         # x intercept of right line and x=3
    
    # Get y values
    y_0 = 0                         # y intercept of left line and x axis
    y_1 = a_0 * x_1 + a_1           # y intercept of two lines
    y_2 = b_0 * x_2 + b_1           # y intercept of right line and x=3

    # Return the x and y values
    return x_0, x_1, x_2, y_0, y_1, y_2

def get_wc(x_0:float, x_1:float, x_2:float, y_0:float, y_1:float, y_2:float):
    """
    Gets the critical work interpolation bilinear curve
    
    Parameters:
    * `x_0`: The x coordinate corresponding to the start of the bilinear function
    * `x_1`: The x coordinate corresponding to the corner of the bilinear function
    * `x_2`: The x coordinate corresponding to the end of the bilinear function
    * `y_0`: The y coordinate corresponding to the start of the bilinear function
    * `y_1`: The y coordinate corresponding to the corner of the bilinear function
    * `y_2`: The y coordinate corresponding to the end of the bilinear function
    
    Returns the x (w_rate) and y (w_crit) values (on the log10-log10 scale)
    """
    num_points = 16
    x_list = list(np.linspace(x_0, x_1, num_points)) + list(np.linspace(x_1, x_2, num_points))
    y_list = list(np.linspace(y_0, y_1, num_points)) + list(np.linspace(y_1, y_2, num_points))
    return x_list, y_list

def get_n(x_0:float, x_1:float, x_2:float, a_n:float, b_n:float):
    """
    Gets the n interpolation bilinear curve
    
    Parameters:
    * `x_0`: The x coordinate corresponding to the start of the bilinear function
    * `x_1`: The x coordinate corresponding to the corner of the bilinear function
    * `x_2`: The x coordinate corresponding to the end of the bilinear function
    * `a_n`: The n value before the corner
    * `b_n`: The n value after the corner
    
    Returns the x (w_rate) and y (n) values (on the log10-log10 scale)
    """
    num_points = 16
    x_list = list(np.linspace(x_0, x_1, num_points)) + list(np.linspace(x_1, x_2, num_points))
    y_list = [a_n] * num_points + [b_n] * num_points
    return x_list, y_list
    