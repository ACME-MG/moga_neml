"""
 Title:         The Elastic Viscoplastic Work Damage Model
 Description:   Incorporates elasto-viscoplasticity and work damage
 Author:        Janzen Choi

"""

# Libraries
import modules.models.__model__ as model
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage, interpolate

# Model Parameters
STRESS_RATE  = 0.0001
TIME_HOLD    = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 2001
STRAIN_MAX   = 0.99
DAMAGE_TOL   = 0.95
EPSILON      = 1e-40

# The Elastic Visco Plastic Work Damage Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):
        self.add_param("evp_s0",  0.0e1, 1.0e2)
        self.add_param("evp_R",   0.0e1, 1.0e2)
        self.add_param("evp_d",   0.0e1, 1.0e2)
        self.add_param("evp_n",   1.0e0, 1.0e2)
        self.add_param("evp_eta", 0.0e1, 1.0e6)
        self.add_param("wd_m",    0.0e1, 1.0e0)
        self.add_param("wd_b",    0.0e1, 1.0e1)
        self.add_param("wd_n",    1.0e0, 1.0e1)

    # Gets the predicted curves
    def get_prd_curve(self, exp_curve, evp_s0, evp_R, evp_d, evp_n, evp_eta, wd_m, wd_b, wd_n):

        # Define model
        elastic_model = elasticity.IsotropicLinearElasticModel(exp_curve["youngs"], "youngs", exp_curve["poissons"], "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        wd_wc         = interpolate.PolynomialInterpolate([wd_m, wd_b])
        wd_model      = damage.WorkDamage(elastic_model, wd_wc, wd_n, log=True, eps=EPSILON)
        evpwd_model   = damage.NEMLScalarDamagedModel_sd(elastic_model, evp_model, wd_model, verbose=False)

        # Get predictions
        if exp_curve["type"] == "creep":
            with model.BlockPrint():
                creep_results = drivers.creep(evpwd_model, exp_curve["stress"], STRESS_RATE, TIME_HOLD, T=exp_curve["temp"], verbose=False,
                                                check_dmg=False, dtol=DAMAGE_TOL, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
            return {"x": list(creep_results["rtime"] / 3600), "y": list(creep_results["rstrain"])}
        elif exp_curve["type"] == "tensile":
            strain_rate = exp_curve["strain_rate"] / 3600
            with model.BlockPrint():
                tensile_results = drivers.uniaxial_test(evpwd_model, erate=strain_rate, T=exp_curve["temp"], emax=STRAIN_MAX, nsteps=NUM_STEPS)
            return {"x": list(tensile_results["strain"]), "y": list(tensile_results["stress"])}