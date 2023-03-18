"""
 Title:         The Elastic Visco Plastic Work Damage Model (Separated)
 Description:   Predicts primary, secondary, and tertiary creep
 Author:        Janzen Choi

"""

# Libraries
import __model__ as model
import math
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage, interpolate
from neml.nlsolvers import MaximumIterations

# Model Parameters
YOUNGS       = 157000.0
POISSONS     = 0.3
STRESS_RATE  = 0.0001
HOLD         = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 251
STRAIN_MAX   = 0.5

# The Elastic Visco Plastic Work Damage (Separated) Class
class EVPWD_S(model.Model):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__(
            name = "evpwd_s",
            param_info = [
                {"name": "wd_m",    "min": 0.0e0,   "max": 1.0e2},
                {"name": "wd_b",    "min": 0.0e0,   "max": 2.0e1},
                {"name": "wd_n",    "min": 0.0e1,   "max": 2.0e0},
            ],
            exp_curves = exp_curves
        )

    # Prepares the model
    # api.define_model("evpwd_s", [41.51219348, 26.94208619, 0.382454248, 2.54294033, 18404.70135]) # A617, 800C
    def prepare(self, args):

        # Define elastic-plastic parameters
        self.evp_s0  = args[0]
        self.evp_R   = args[1]
        self.evp_d   = args[2]
        self.evp_n   = args[3]
        self.evp_eta = args[4]

        # Define elastic-plastic model
        self.elastic_model = elasticity.IsotropicLinearElasticModel(YOUNGS, "youngs", POISSONS, "poissons")
        yield_surface  = surfaces.IsoJ2()
        iso_hardening  = hardening.VoceIsotropicHardeningRule(self.evp_s0, self.evp_R, self.evp_d)
        g_power        = visco_flow.GPowerLaw(self.evp_n, self.evp_eta)
        visco_model    = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator     = general_flow.TVPFlowRule(self.elastic_model, visco_model)
        self.evp_model = models.GeneralIntegrator(self.elastic_model, integrator, verbose=False)

        # Define interpolator
        def log_line(x, m=1, b=0):
            return m*math.log10(x) + b
        self.interp_function = log_line

    # Gets the predicted curves
    def get_prd_curves(self, wd_m, wd_b, wd_n):

        # Define model
        x_interp    = [10**i for i in [-10, -5, 0, 5, 10]]
        y_interp    = [self.interp_function(x, wd_m, wd_b) for x in x_interp]
        wd_wc       = interpolate.PiecewiseSemiLogXLinearInterpolate(x_interp, y_interp)
        wd_model    = damage.WorkDamage(self.elastic_model, wd_wc, wd_n)
        evpwd_model = damage.NEMLScalarDamagedModel_sd(self.elastic_model, self.evp_model, wd_model, verbose=False)

        # Iterate through predicted curves
        prd_curves = super().get_prd_curves()
        for i in range(len(prd_curves)):

            # Get stress and temperature
            temp = self.exp_curves[i]["temp"]
            type = self.exp_curves[i]["type"]

            # Get predictions
            try:
                if type == "creep":
                    stress_max = self.exp_curves[i]["stress"]
                    with model.BlockPrint():
                        creep_results = drivers.creep(evpwd_model, stress_max, STRESS_RATE, HOLD, T=temp, verbose=False, check_dmg=False, dtol=0.95, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
                    prd_curves[i]["x"] = list(creep_results['rtime'] / 3600)
                    prd_curves[i]["y"] = list(creep_results['rstrain'])
                elif type == "tensile":
                    strain_rate = self.exp_curves[i]["strain_rate"] / 3600
                    with model.BlockPrint():
                        tensile_results = drivers.uniaxial_test(evpwd_model, erate=strain_rate, T=temp, emax=STRAIN_MAX, nsteps=NUM_STEPS)
                    prd_curves[i]["x"] = list(tensile_results['strain'])
                    prd_curves[i]["y"] = list(tensile_results['stress'])
            except MaximumIterations:
                return []

        # Return predicted curves
        return prd_curves