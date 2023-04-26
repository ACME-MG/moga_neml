"""
 Title:         The Elastic Visco Plastic Work Damage Model
 Description:   Predicts primary, secondary, and tertiary creep
 Author:        Janzen Choi

"""

# Libraries
import __model__ as model
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage, interpolate
from neml.nlsolvers import MaximumIterations

# Model Parameters
YOUNGS       = 157000.0
POISSONS     = 0.3
STRESS_RATE  = 0.0001
TIME_HOLD    = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 2001
STRAIN_MAX   = 0.99
DAMAGE_TOL   = 0.95
EPSILON      = 1e-40

# The Elastic Visco Plastic Work Damage Class
class EVPWD(model.Model):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__(
            name = "evpwd",
            param_info = [
                {"name": "evp_s0",  "min": 0.0e0,   "max": 1.0e2},
                {"name": "evp_R",   "min": 0.0e0,   "max": 1.0e2},
                {"name": "evp_d",   "min": 0.0e0,   "max": 1.0e2},
                {"name": "evp_n",   "min": 1.0e0,   "max": 1.0e1}, # 2
                {"name": "evp_eta", "min": 0.0e0,   "max": 1.0e6},
                {"name": "wd_m",    "min": 0.0e0,   "max": 1.0e0}, # 2
                {"name": "wd_b",    "min": 0.0e0,   "max": 1.0e1}, # 2
                {"name": "wd_n",    "min": 1.0e0,   "max": 1.0e1},
            ],
            exp_curves = exp_curves
        )

    # Prepares the model
    def prepare(self, args):
        self.elastic_model = elasticity.IsotropicLinearElasticModel(YOUNGS, "youngs", POISSONS, "poissons")
        self.yield_surface = surfaces.IsoJ2()

    # Gets the predicted curves
    def get_prd_curves(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_m, wd_b, wd_n):

        # Define model
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(self.yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(self.elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(self.elastic_model, integrator, verbose=False)
        wd_wc         = interpolate.PolynomialInterpolate([wd_m, wd_b])
        wd_model      = damage.WorkDamage(self.elastic_model, wd_wc, wd_n, log=True, eps=EPSILON)
        evpwd_model   = damage.NEMLScalarDamagedModel_sd(self.elastic_model, evp_model, wd_model, verbose=False)

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
                        creep_results = drivers.creep(evpwd_model, stress_max, STRESS_RATE, TIME_HOLD,
                                                      T=temp, verbose=False, check_dmg=False, dtol=DAMAGE_TOL,
                                                      nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
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