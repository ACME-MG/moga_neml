"""
 Title:         The Elastic Visco Plastic Work Damage Model
 Description:   Predicts primary, secondary, and tertiary creep
 Author:        Janzen Choi

"""

# Libraries
import __model__ as model
from math import e as exp, pow
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage, interpolate
from neml.nlsolvers import MaximumIterations

# Model Parameters
YOUNGS       = 157000.0
POISSONS     = 0.3
S_RATE       = 0 # 1.0e-4
E_RATE       = 1.0e-4
HOLD         = 11500.0 * 3600.0
NUM_STEPS    = 251
MIN_DATA     = 50

# The Elastic Visco Plastic Work Damage Class
class EVPWD(model.Model):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__(
            name = "evpwd",
            param_info = [
                {"name": "evp_s0",  "min": 0.0e1,   "max": 1.0e2}, # 2
                {"name": "evp_R",   "min": 0.0e1,   "max": 1.0e2}, # 2
                {"name": "evp_d",   "min": 0.0e1,   "max": 1.0e2}, # 2
                {"name": "evp_n",   "min": 1.0e0,   "max": 1.0e1}, # 1
                {"name": "evp_eta", "min": 0.0e1,   "max": 1.0e4}, # 4
                {"name": "wd_xf",   "min": 1.0e0,   "max": 1.0e2}, # 2
                {"name": "wd_yf",   "min": 1.0e0,   "max": 1.0e3}, # 3
                {"name": "wd_yo",   "min": 1.0e0,   "max": 1.0e3}, # 3
                {"name": "wd_n",    "min": 0.0e1,   "max": 1.0e2}, # 2
            ],
            exp_curves = exp_curves
        )

    # Prepares the model
    def prepare(self, args):
        
        # Define auxiliary models
        self.elastic_model  = elasticity.IsotropicLinearElasticModel(YOUNGS, "youngs", POISSONS, "poissons")
        self.yield_surface  = surfaces.IsoJ2()
        
        # Define interpolator
        def sigmoid(x, x_factor=1, y_factor=1, y_offset=0.1):
            return y_factor/(1+pow(exp,-x_factor*x)) + y_offset
        self.interp_function = sigmoid

    # Gets the predicted curves
    def get_prd_curves(self, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_xf, wd_yf, wd_yo, wd_n):

        # Define interpolator
        x_interp = [2**i/wd_xf for i in range(-4,4)]
        y_interp = [self.interp_function(x, wd_xf, wd_yf, wd_yo) for x in x_interp]
        wd_wc    = interpolate.PiecewiseSemiLogXLinearInterpolate(x_interp, y_interp)

        # Define model
        iso_hardening   = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power         = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model     = visco_flow.PerzynaFlowRule(self.yield_surface, iso_hardening, g_power)
        integrator      = general_flow.TVPFlowRule(self.elastic_model, visco_model)
        evp_model       = models.GeneralIntegrator(self.elastic_model, integrator, verbose=False)
        wd_model        = damage.WorkDamage(self.elastic_model, wd_wc, wd_n)
        evpwd_model     = damage.NEMLScalarDamagedModel_sd(self.elastic_model, evp_model, wd_model, verbose=False)

        # Iterate through predicted curves
        prd_curves = super().get_prd_curves()
        for i in range(len(prd_curves)):

            # Get stress and temperature
            stress = self.exp_curves[i]["stress"]
            temp = self.exp_curves[i]["temp"]
            type = self.exp_curves[i]["type"]

            # Get predictions
            try:
                if type == "creep":
                    with model.BlockPrint():
                        creep_results = drivers.creep(evpwd_model, stress, S_RATE, HOLD, T=temp, verbose=False, check_dmg=False, dtol=0.95, nsteps_up=150, nsteps=NUM_STEPS, logspace=False)
                    prd_curves[i]["x"] = list(creep_results['rtime'] / 3600)
                    prd_curves[i]["y"] = list(creep_results['rstrain'])
                elif type == "tensile":
                    with model.BlockPrint():
                        tensile_results = drivers.uniaxial_test(evpwd_model, E_RATE, T=temp, emax=0.5, nsteps=NUM_STEPS)
                    prd_curves[i]["x"] = list(tensile_results['strain'])
                    prd_curves[i]["y"] = list(tensile_results['stress'])
            except MaximumIterations:
                return []

            # Make sure predictions contain more than MIN_DATA data points
            if len(prd_curves[i]["x"]) <= MIN_DATA or len(prd_curves[i]["y"]) <= MIN_DATA:
                return []

        # Return predicted curves
        return prd_curves