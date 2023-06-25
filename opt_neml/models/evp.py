"""
 Title:         The Elastic Viscoplastic Model
 Description:   Incorporates elasto-viscoplasticity
 Author:        Janzen Choi

"""

# Libraries
import opt_neml.models.__model__ as model
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow
from neml.nlsolvers import MaximumIterations

# Model Parameters
STRESS_RATE  = 0.0001
HOLD         = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 251
STRAIN_MAX   = 0.47

# The Elastic Visco Plastic Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):

        # Define parameters
        self.add_param("evp_s0",  1.0e2, 1.0e3) # 2
        self.add_param("evp_R",   0.0e0, 1.0e4) # 2
        self.add_param("evp_d",   0.0e1, 1.0e3) # 2
        self.add_param("evp_n",   1.0e0, 1.0e2) # 2
        self.add_param("evp_eta", 0.0e1, 1.0e5) # 5

        # Define test conditions
        exp_curve = self.get_exp_curve()
        self.youngs = exp_curve["youngs"]
        self.poissons = exp_curve["poissons"]
        self.temp = exp_curve["temp"]
        self.type = exp_curve["type"]

    # Gets the predicted curve
    def get_prd_curve(self, evp_s0, evp_R, evp_d, evp_n, evp_eta):

        # Define model
        elastic_model = elasticity.IsotropicLinearElasticModel(self.youngs, "youngs", self.poissons, "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        # chaboche voce recovery for static recovery
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)

        # Get predictions
        exp_curve = self.get_exp_curve()
        if self.type == "creep":
            try:
                stress = exp_curve["stress"]
                creep_results = drivers.creep(evp_model, stress, STRESS_RATE, HOLD, T=self.temp, verbose=False,
                                              check_dmg=False, dtol=0.95, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
                return {"x": list(creep_results["rtime"] / 3600), "y": list(creep_results["rstrain"])}
            except MaximumIterations:
                return
        elif self.type == "tensile":
            try:
                strain_rate = exp_curve["strain_rate"] / 3600
                tensile_results = drivers.uniaxial_test(evp_model, erate=strain_rate, T=self.temp, emax=STRAIN_MAX, nsteps=NUM_STEPS)
                return {"x": list(tensile_results["strain"]), "y": list(tensile_results["stress"])}
            except MaximumIterations:
                return