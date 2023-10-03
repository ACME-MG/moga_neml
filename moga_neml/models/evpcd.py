"""
 Title:         The Elastic Viscoplastic Creep Damage Model
 Description:   Incorporates elasto-viscoplasticity and creep damage
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.models.__model__ import __Model__
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow, damage

# The Elastic Visco Plastic Creep Damage Class
class Model(__Model__):

    def initialise(self):
        """
        Runs at the start, once
        """
        self.add_param("evp_s0",  0.0e0, 1.0e3) # 2
        self.add_param("evp_R",   0.0e0, 1.0e4) # 2
        self.add_param("evp_d",   0.0e1, 1.0e3) # 2
        self.add_param("evp_n",   1.0e0, 1.0e2) # 2
        self.add_param("evp_eta", 0.0e1, 1.0e6) # 5
        self.add_param("cd_A",    0.0e1, 1.0e4)
        self.add_param("cd_xi",   0.0e1, 1.0e2)
        self.add_param("cd_phi",  0.0e1, 1.0e2)
    
    def calibrate_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, cd_A, cd_xi, cd_phi):
        """
        Gets the predicted curves

        Parameters:
        * `...`: ...

        Returns the calibrated model
        """
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator)
        eff_stress    = damage.VonMisesEffectiveStress()
        cd_model      = damage.ModularCreepDamage(elastic_model, cd_A, cd_xi, cd_phi, eff_stress)
        evpcd_model   = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, cd_model)
        return evpcd_model