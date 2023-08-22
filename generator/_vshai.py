
# NEML Libraries
from neml import elasticity, drivers
from neml.cp import crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polycrystal
from neml.math import rotations

# Model Constants
ORI_PATH    = "input_stats.csv"
LATTICE     = 1.0
SLIP_DIR    = [1,1,0]
SLIP_PLANE  = [1,1,1]
NUM_THREADS = 12
M_ITER      = 16
MAX_DIVIDE  = 2

# Driver Constants
TEMPERATURE = 20
STRAIN_RATE = 1.0e-4
MAX_STRAIN  = 0.2
NUM_STEPS   = 100
REL_TOL     = 1.0E-6 # -6
ABS_TOL     = 1.0E-10 # -10
VERBOSE     = False

# The VSHAI Model
class Model:

    # Runs at the start, once
    def __init__(self):

        # Define grain orientations
        file = open(ORI_PATH, "r")
        self.grain_orientations, self.weights = [], []
        for line in file.readlines():
            data = line.replace("\n","").split(",")
            phi_1 = float(data[0])
            Phi   = float(data[1])
            phi_2 = float(data[2])
            if phi_1 == 0 and Phi == 0 and phi_2 == 0:
                continue
            self.grain_orientations.append(rotations.CrystalOrientation(phi_1, Phi, phi_2, angle_type="degrees", convention="bunge"))
            self.weights.append(int(data[3]))
        file.close()

        # Define lattice structure
        self.lattice = crystallography.CubicLattice(LATTICE)
        self.lattice.add_slip_system(SLIP_DIR, SLIP_PLANE)

    # Gets the calibrated VSHAI model
    def get_model(self, vsh_ts, vsh_b, vsh_t0, ai_g0, ai_n):
        elastic_model  = elasticity.IsotropicLinearElasticModel(211000, "youngs", 0.3, "poissons")
        strength_model = slipharden.VoceSlipHardening(vsh_ts, vsh_b, vsh_t0)
        slip_model     = sliprules.PowerLawSlipRule(strength_model, ai_g0, ai_n)
        ai_model       = inelasticity.AsaroInelasticity(slip_model)
        ep_model       = kinematics.StandardKinematicModel(elastic_model, ai_model)
        sc_model       = singlecrystal.SingleCrystalModel(ep_model, self.lattice, verbose=False, miter=M_ITER, max_divide=MAX_DIVIDE)
        vshai_model    = polycrystal.TaylorModel(sc_model, self.grain_orientations, nthreads=NUM_THREADS, weights=self.weights)
        return vshai_model

    # Gets the results from the driver and return
    def get_prediction(self, *params:tuple):
        calibrated_model = self.get_model(*params)
        results = drivers.uniaxial_test(calibrated_model, erate=STRAIN_RATE,
            T=TEMPERATURE, emax=MAX_STRAIN, nsteps=NUM_STEPS,
            verbose=VERBOSE, rtol=REL_TOL, atol=ABS_TOL)
        return results # "strain", "stress"

    # Gets the value dictionary
    def get_value_dict(self):
        return {
            "vsh_t0": [923.24],
            "vsh_ts": [394.24],
            "vsh_b":  [0.86869],
            "ai_n":   [0.13795],
            "ai_g0":  [round_sf(1e-4/3, 5)]
        }
        # return {
        #     "vsh_t0": [100, 200, 300, 400, 500],
        #     "vsh_ts": [1, 500, 1000, 1500, 2000],
        #     "vsh_b":  [0.1, 1, 10],
        #     "ai_n":   [1, 5, 10, 15, 20],
        #     "ai_g0":  [round_sf(1e-4/3, 5)]
        # }

# Rounds a float to a number of significant figures
def round_sf(value:float, sf:int) -> float:
    format_str = "{:." + str(sf) + "g}"
    rounded_value = float(format_str.format(value))
    return rounded_value
