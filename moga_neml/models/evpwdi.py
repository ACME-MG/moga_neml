"""
 Title:         The Elastic Viscoplastic Work Damage Model with an inverse polynomial for work damage
 Description:   Incorporates elasto-viscoplasticity and work damage
 Author:        Janzen Choi

"""

# Libraries
import math, numpy as np
from copy import deepcopy
from numpy.polynomial.polynomial import polyval
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
        self.add_param("wd_0",    0.0e0, 1.0e0) # -6
        self.add_param("wd_1",   -1.0e0, 0.0e0) # -3
        self.add_param("wd_2",    0.0e0, 1.0e0) # -1
        self.add_param("wd_3",   -1.0e1, 0.0e0) # 1

    # Gets the predicted curve
    def calibrate_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_n, wd_0, wd_1, wd_2, wd_3):
        
        # Define EVP model
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        
        # Define interpolator
        wd_params = [wd_0, wd_1, wd_2, wd_3]
        l_bounds = get_root(wd_params, -16)
        u_bounds = get_root(wd_params, 0)
        if len(l_bounds) == 0 or len(u_bounds) == 0:
            return
        
        # Get interpolation
        y_list = list(np.linspace(min(l_bounds), max(u_bounds), 32))
        x_list = [polyval(y, np.flip(np.array(wd_params))) for y in y_list]
        for y in y_list:
            if y <= 0:
                return
        y_list = [math.log10(y) for y in y_list]
        wd_wc  = interpolate.PiecewiseLinearInterpolate(x_list, y_list)
        
        # Define work damage model and return
        wd_model = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=1e-40, work_scale=1e5)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model

# Gets the root of a polynomial (highest order first)
def get_root(polynomial:list, value:float, eps:float=1e-5):
    offset_polynomial = deepcopy(polynomial)
    offset_polynomial[-1] -= value
    roots = np.roots(offset_polynomial)
    real_roots = roots.real[abs(roots.imag) < eps]
    return real_roots