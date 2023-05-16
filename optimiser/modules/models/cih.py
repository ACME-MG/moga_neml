"""
 Title:         The Chaboche Isotropic Hardening Model
 Description:   Predicts cyclic behaviour
 Author:        Janzen Choi

"""

# Libraries
from neml import models, elasticity, drivers, surfaces, hardening, ri_flow
import modules.models.__model__ as model
from neml.nlsolvers import MaximumIterations

# Constants
CYCLIC_STRAIN_RATIO = -1
NUM_STEPS           = 51

# The Chaboche Isotropic Hardening Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):
        self.add_param("ih_s0", 0.0e0, 1.0e3)
        self.add_param("ih_Q",  0.0e0, 1.0e3)
        self.add_param("ih_b",  0.0e0, 1.0e2)
        self.add_param("c_gs1", 0.0e0, 1.0e6)
        self.add_param("c_gs2", 0.0e0, 1.0e6)
        self.add_param("c_cs1", 0.0e0, 1.0e6)
        self.add_param("c_cs2", 0.0e0, 1.0e6)
        self.c_As = [0.0, 0.0]
        self.c_ns = [2.0, 2.0]
    
    # Gets the predicted curves
    def get_prd_curve(self, exp_curve, ih_s0, ih_Q, ih_b, c_gs1, c_gs2, c_cs1, c_cs2):

        # Define model
        elastic_model      = elasticity.IsotropicLinearElasticModel(exp_curve["youngs"], "youngs", exp_curve["poissons"], "poissons")
        yield_surface      = surfaces.IsoKinJ2()
        iso_hardening      = hardening.VoceIsotropicHardeningRule(ih_s0, ih_Q, ih_b)
        gamma_hardening    = [hardening.ConstantGamma(g) for g in [c_gs1, c_gs2]]
        chaboche_hardening = hardening.Chaboche(iso_hardening, [c_cs1, c_cs2], gamma_hardening, self.c_As, self.c_ns)
        non_ass_hardening  = ri_flow.RateIndependentNonAssociativeHardening(yield_surface, chaboche_hardening)
        cih_model          = models.SmallStrainRateIndependentPlasticity(elastic_model, non_ass_hardening)

        # Get predictions
        if "cyclic" in exp_curve["type"]:
            try:
                cylic_results = drivers.strain_cyclic(cih_model, T=exp_curve["temp"], emax=exp_curve["max_strain"], erate=exp_curve["strain_rate"],
                                                      R=CYCLIC_STRAIN_RATIO, ncycles=int(exp_curve["num_cycles"]), nsteps=NUM_STEPS)
            except MaximumIterations:
                return
            if exp_curve["type"] == "cyclic-time-strain":
                return {"x": cylic_results["time"], "y": cylic_results["strain"]}
            if exp_curve["type"] == "cyclic-time-stress":
                return {"x": cylic_results["time"], "y": cylic_results["stress"]}
            if exp_curve["type"] == "cyclic-strain-stress":
                return {"x": cylic_results["strain"], "y": cylic_results["stress"]}