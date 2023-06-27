"""
 Title:         The Chaboche Isotropic Hardening Model
 Description:   Predicts cyclic behaviour
 Author:        Janzen Choi

"""

# Libraries
from neml import models, elasticity, surfaces, hardening, ri_flow
import moga_neml.models.__model__ as model

# The Chaboche Isotropic Hardening Class
class Model(model.__Model__):

    # Runs at the start, once
    def prepare(self):

        # Define parameters
        self.add_param("ih_s0", 0.0e0, 1.0e3)
        self.add_param("ih_Q",  0.0e0, 1.0e3)
        self.add_param("ih_b",  0.0e0, 1.0e2)
        self.add_param("c_gs1", 0.0e0, 1.0e6)
        self.add_param("c_gs2", 0.0e0, 1.0e6)
        self.add_param("c_cs1", 0.0e0, 1.0e6)
        self.add_param("c_cs2", 0.0e0, 1.0e6)
        
        # Define test conditions
        exp_curve = self.get_exp_curve()
        self.youngs = exp_curve["youngs"]
        self.poissons = exp_curve["poissons"]
    
    # Gets the predicted curves
    def get_model(self, ih_s0, ih_Q, ih_b, c_gs1, c_gs2, c_cs1, c_cs2):
        elastic_model      = elasticity.IsotropicLinearElasticModel(self.youngs, "youngs", self.poissons, "poissons")
        yield_surface      = surfaces.IsoKinJ2()
        iso_hardening      = hardening.VoceIsotropicHardeningRule(ih_s0, ih_Q, ih_b)
        gamma_hardening    = [hardening.ConstantGamma(g) for g in [c_gs1, c_gs2]]
        chaboche_hardening = hardening.Chaboche(iso_hardening, [c_cs1, c_cs2], gamma_hardening, [0.0, 0.0], [2.0, 2.0])
        non_ass_hardening  = ri_flow.RateIndependentNonAssociativeHardening(yield_surface, chaboche_hardening)
        cih_model          = models.SmallStrainRateIndependentPlasticity(elastic_model, non_ass_hardening)
        return cih_model