"""
 Title:         The Elastic Viscoplastic Model with Custom Yield
 Description:   Incorporates elasto-viscoplasticity and allows users to define custom yield functions
 Author:        Janzen Choi

"""

# Libraries
from moga_neml.models.__model__ import __Model__
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow

# The Elastic Visco Plastic Class
class Model(__Model__):

    def initialise(self, yield_function:str="IsoJ2"):
        """
        Runs at the start, once
        """
        
        # Define parameters
        self.add_param("evp_s0",  0.0e0, 1.0e2)
        self.add_param("evp_R",   0.0e0, 1.0e3)
        self.add_param("evp_d",   0.0e0, 1.0e2)
        self.add_param("evp_n",   1.0e0, 1.0e2)
        self.add_param("evp_eta", 0.0e0, 1.0e4)

        # Define the yield surface function
        self.yield_function = yield_function
        if yield_function == "IsoJ2":
            self.yield_surface = surfaces.IsoJ2
        elif yield_function == "IsoJ2I1":
            self.yield_surface = surfaces.IsoJ2I1
            self.add_param("ys_h", 0.0e0, 1.0e2)
            self.add_param("ys_l", 0.0e0, 1.0e0)
        
    def calibrate_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, ys_h=None, ys_l=None):
        """
        Gets the predicted curves

        Parameters:
        * `...`: ...

        Returns the calibrated model
        """
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs",
                                                               self.get_data("poissons"), "poissons")
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        yield_surface = self.yield_surface(ys_h, ys_l) if self.yield_function == "IsoJ2I1" else self.yield_surface()
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        return evp_model