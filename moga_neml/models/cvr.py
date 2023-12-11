"""
 Title:         The Chaboche Voce Recovery Model
 Description:   Incorporates elasto-viscoplasticity and some Chaboche hardening
 Author:        Janzen Choi

"""

# Libraries
import math
from moga_neml.models.__model__ import __Model__
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow

# The Elastic Visco Plastic Class
class Model(__Model__):

    def initialise(self):
        """
        Runs at the start, once
        """

        # Define parameters
        self.add_param("evp_eta",   0.0e0,  1.0e5)
        self.add_param("evp_n",     0.0e0,  1.0e2)
        self.add_param("cvr_s0",    0.0e0,  1.0e4)
        self.add_param("cvr_t0",    0.0e0,  1.0e5)
        self.add_param("cvr_R_min", 0.0e0,  1.0e4)
        self.add_param("cvr_R_max", 0.0e0,  1.0e4)
        self.add_param("cvr_r1",   -1.4e1, -8.0e0)
        self.add_param("cvr_r2",    1.0e0,  2.0e1)

        # Remove backstress
        self.c_s = [0]
        self.g_s = [hardening.ConstantGamma(r) for r in [0, 0]]
        self.a_s = [0, 0]
        self.n_s = [1, 1]

    def calibrate_model(self, evp_eta, evp_n, cvr_s0, cvr_t0, cvr_R_min, cvr_R_max, cvr_r1, cvr_r2):
        """
        Gets the predicted curves

        Parameters:
        * `...`: ...

        Returns the calibrated model
        """
        cvr_r1 = math.pow(10, cvr_r1)
        if cvr_R_min >= cvr_R_max:
            return None
        elastic_model = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs",
                                                               self.get_data("poissons"), "poissons")
        yield_surface = surfaces.IsoKinJ2()
        cvr_model     = hardening.ChabocheVoceRecovery(cvr_s0, cvr_t0, cvr_R_max, cvr_R_min, cvr_r1, cvr_r2,
                                                       self.c_s, self.g_s, self.a_s, self.n_s)
        fluidity      = visco_flow.ConstantFluidity(evp_eta)
        visco_model   = visco_flow.ChabocheFlowRule(yield_surface, cvr_model, fluidity, evp_n)
        tvp_flow      = general_flow.TVPFlowRule(elastic_model, visco_model)
        cvrevp_model  = models.GeneralIntegrator(elastic_model, tvp_flow, verbose=False)
        return cvrevp_model