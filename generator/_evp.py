# NEML Libraries
from neml import drivers
from neml import models, elasticity, surfaces, hardening, visco_flow, general_flow

# Model Constants
TEMPERATURE = 20
STRAIN_RATE = 1.0e-4
MAX_STRAIN  = 0.2
NUM_STEPS   = 251
REL_TOL     = 1.0E-6 # -6
ABS_TOL     = 1.0E-10 # -10
VERBOSE     = False

# The VSHAI Model
class Model:

    # Gets the calibrated VSHAI model
    def get_model(self, evp_s0, evp_R, evp_d, evp_n, evp_eta):
        elastic_model  = elasticity.IsotropicLinearElasticModel(211000, "youngs", 0.3, "poissons")
        yield_surface = surfaces.IsoJ2()
        iso_hardening = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power       = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model   = visco_flow.PerzynaFlowRule(yield_surface, iso_hardening, g_power)
        integrator    = general_flow.TVPFlowRule(elastic_model, visco_model)
        evp_model     = models.GeneralIntegrator(elastic_model, integrator, verbose=False)
        return evp_model

    # Gets the results from the driver and return
    def get_prediction(self, *params:tuple):
        calibrated_model = self.get_model(*params)
        results = drivers.uniaxial_test(calibrated_model, erate=STRAIN_RATE,
            T=TEMPERATURE, emax=MAX_STRAIN, nsteps=NUM_STEPS,
            verbose=VERBOSE, rtol=REL_TOL, atol=ABS_TOL)
        if len(results["strain"]) < 5 or results["strain"][-1] < MAX_STRAIN:
            raise ValueError
        return results # "strain", "stress"
    
    # Gets the value dictionary
    def get_value_dict(self):
        return {
            "evp_s0":  [1, 100, 200, 300, 400, 500],
            "evp_R":   [1, 500, 1000, 1500, 2000],
            "evp_d":   [0.1, 1, 10, 100],
            "evp_n":   [1, 5, 10],
            "evp_eta": [1e1, 1e2, 1e3, 1e4]
        }
        # return {
        #     "evp_s0":  [1, 100, 200, 300, 400, 500],
        #     "evp_R":   [1, 250, 500, 750, 1000, 1250, 1500, 1750, 2000],
        #     "evp_d":   [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100],
        #     "evp_n":   [1, 5, 10, 15, 20],
        #     "evp_eta": [1e0, 1e1, 1e2, 1e3, 1e4]
        # }
