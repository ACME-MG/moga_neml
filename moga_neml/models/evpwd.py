"""
 Title:         The Elastic Viscoplastic Work Damage Model
 Description:   Incorporates elasto-viscoplasticity and work damage
 Author:        Janzen Choi

"""

# Libraries
import moga_neml.models.__model__ as model
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow, damage, interpolate

# The Elastic Visco Plastic Work Damage Class
class Model(model.__Model__):

    # Runs at the start, once
    def prepare(self):

        # Define parameters
        self.add_param("evp_s0",  0.0e1, 1.0e2)
        self.add_param("evp_R",   0.0e1, 1.0e2)
        self.add_param("evp_d",   0.0e1, 1.0e2)
        self.add_param("evp_n",   1.0e0, 1.0e2)
        self.add_param("evp_eta", 0.0e1, 1.0e6)
        self.add_param("wd_m",    0.0e1, 1.0e0)
        self.add_param("wd_b",    0.0e1, 1.0e1)
        self.add_param("wd_n",    1.0e0, 1.0e1)

        # Define test conditions
        exp_curve = self.get_exp_curve()
        self.youngs = exp_curve["youngs"]
        self.poissons = exp_curve["poissons"]

    # Gets the predicted curve
    def get_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_m, wd_b, wd_n):
        elastic_model = elasticity.IsotropicLinearElasticModel(self.youngs, "youngs", self.poissons, "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        wd_wc         = interpolate.PolynomialInterpolate([wd_m, wd_b])
        wd_model      = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=1e-40)
        evpwd_model   = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)
        return evpwd_model