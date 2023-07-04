"""
 Title:         The Elastic Viscoplastic Model
 Description:   Incorporates elasto-viscoplasticity
 Author:        Janzen Choi

"""

# Libraries
import moga_neml.models.__model__ as model
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow

# The Elastic Visco Plastic Class
class Model(model.__Model__):

    # Runs at the start, once
    def initialise(self):
        
        # Define parameters
        self.add_param("evp_s0",  0.0e0, 1.0e3) # 2
        self.add_param("evp_R",   0.0e0, 1.0e4) # 2
        self.add_param("evp_d",   0.0e1, 1.0e3) # 2
        self.add_param("evp_n",   1.0e0, 1.0e2) # 2
        self.add_param("evp_eta", 0.0e1, 1.0e6) # 5
        
    # Gets the model
    def get_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta):
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        return evp_model