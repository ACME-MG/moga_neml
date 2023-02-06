"""
 Title:         The Voce Slip Hardening Asaro Inelasticity Model
 Description:   Predicts primary creep via crystal plasticity
 Author:        Janzen Choi
"""

# Libraries
import __model__ as model
from neml import elasticity, drivers
from neml.cp import crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polycrystal
from neml.math import rotations
from neml.nlsolvers import MaximumIterations

# Model Parameters
YOUNGS      = 211000.0
POISSONS    = 0.3
S_RATE      = 1.0e-4
E_RATE      = 1.0e-4
E_MAX       = 0.05
HOLD        = 11500.0 * 3600.0
NUM_STEPS   = 100
MIN_DATA    = 50
VERBOSE     = False

# The Voce Slip Hardening Asaro Inelasticity Class
class VSHAI(model.Model):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__(
            name = "vshai",
            param_info = [
                {"name": "vsh_ts",  "min": 0.0e1,   "max": 1.0e2},
                {"name": "vsh_b",   "min": 0.0e1,   "max": 1.0e2},
                {"name": "vsh_t0",  "min": 0.0e1,   "max": 1.0e1},
                {"name": "ai_g0",   "min": 0.0e1,   "max": 1.0e1},
                {"name": "ai_n",    "min": 0.0e1,   "max": 1.0e2},
            ],
            exp_curves = exp_curves
        )

    # Prepares the model
    # Alloy 617: ["other/input_orientations.csv", 1.0, [1,1,0], [1,1,1], 8]
    def prepare(self, args):

        # Extract information from arguments
        orientation_file = args[0]
        lattice_a        = args[1]
        slip_direction   = args[2]
        slip_plane       = args[3]
        self.num_threads = args[4]

        # Define grain orientations
        file = open(f"input/{orientation_file}", "r")
        self.grain_orientations = []
        for line in file.readlines():
            data = line.replace("\n","").split(",")
            phi_1 = float(data[0])
            Phi   = float(data[1])
            phi_2 = float(data[2])
            self.grain_orientations.append(rotations.CrystalOrientation(phi_1, Phi, phi_2, angle_type="degrees", convention="bunge"))
        file.close()

        # Define lattice structure
        self.elastic_model = elasticity.IsotropicLinearElasticModel(YOUNGS, "youngs", POISSONS, "poissons")
        self.lattice = crystallography.CubicLattice(lattice_a)
        self.lattice.add_slip_system(slip_direction, slip_plane)

    # Gets the predicted curves
    def get_prd_curves(self, vsh_ts, vsh_b, vsh_t0, ai_g0, ai_n):

        # Define model
        strength_model  = slipharden.VoceSlipHardening(vsh_ts, vsh_b, vsh_t0)
        slip_model      = sliprules.PowerLawSlipRule(strength_model, ai_g0, ai_n)
        ai_model        = inelasticity.AsaroInelasticity(slip_model)
        ep_model        = kinematics.StandardKinematicModel(self.elastic_model, ai_model)
        cp_model        = singlecrystal.SingleCrystalModel(ep_model, self.lattice, verbose=False)
        cptm_model      = polycrystal.TaylorModel(cp_model, self.grain_orientations, nthreads=self.num_threads)

        # Iterate through predicted curves
        prd_curves = super().get_prd_curves()
        for i in range(len(prd_curves)):

            # Get stress and temperature
            temp = self.exp_curves[i]["temp"]
            type = self.exp_curves[i]["type"]

            # Get predictions
            try:
                if type == "creep":
                    stress = self.exp_curves[i]["stress"]
                    creep_results = drivers.creep(cptm_model, stress, S_RATE, HOLD, T=temp, verbose=VERBOSE, check_dmg=False, dtol=0.95, nsteps_up=150, nsteps=NUM_STEPS, logspace=False)
                    prd_curves[i]["x"] = list(creep_results['rtime'] / 3600)
                    prd_curves[i]["y"] = list(creep_results['rstrain'])
                elif type == "tensile":
                    tensile_results = drivers.uniaxial_test(cptm_model, E_RATE, T=temp, verbose=VERBOSE, emax=E_MAX, nsteps=NUM_STEPS)
                    prd_curves[i]["x"] = list(tensile_results['strain'])
                    prd_curves[i]["y"] = list(tensile_results['stress'])
            except MaximumIterations:
                return []

            # Make sure predictions contain more than MIN_DATA data points
            if len(prd_curves[i]["x"]) <= MIN_DATA or len(prd_curves[i]["y"]) <= MIN_DATA:
                return []

        # Return predicted curves
        return prd_curves