"""
 Title:         The Elastic Viscoplastic Creep Damage Model
 Description:   Incorporates elasto-viscoplasticity and creep damage
 Author:        Janzen Choi

"""

# Libraries
import moga_neml.models.__model__ as model
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow, damage

# The Elastic Visco Plastic Creep Damage Class
class Model(model.__Model__):

    # Runs at the start, once
    def prepare(self):

        # Define parameters
        self.add_param("evp_s0",  1.0e2, 1.0e3)
        self.add_param("evp_R",   0.0e1, 1.0e4)
        self.add_param("evp_d",   0.0e1, 1.0e4)
        self.add_param("evp_n",   1.0e0, 1.0e3)
        self.add_param("evp_eta", 0.0e1, 1.0e6)
        self.add_param("cd_A",    0.0e1, 1.0e4)
        self.add_param("cd_xi",   0.0e1, 1.0e2)
        self.add_param("cd_phi",  0.0e1, 1.0e2)

        # Define test conditions
        exp_curve = self.get_exp_curve()
        self.youngs = exp_curve["youngs"]
        self.poissons = exp_curve["poissons"]
    
    # Gets the predicted curve
    #   Alloy 617 @ 800:    [48.96021,17.82262,9.568748,2.031041,56309.59,1995.801,5.438601,6.79012]
    #   Alloy 617 @ 900:    [0.567351,24.64534,34.15175,2.103748,31803.17,2679.531,4.155071,9.270845]
    #   Alloy 617 @ 1000:   [7.805677767,0.036500284,6.99330568,2.186529312,20539.05913,2388.920806,3.591732525,6.751795258]
    def get_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, cd_A, cd_xi, cd_phi):
        elastic_model = elasticity.IsotropicLinearElasticModel(self.youngs, "youngs", self.poissons, "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator)
        effective_stress = damage.VonMisesEffectiveStress()
        cd_model      = damage.ModularCreepDamage(elastic_model, cd_A, cd_xi, cd_phi, effective_stress)
        evpcd_model   = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, cd_model)
        return evpcd_model