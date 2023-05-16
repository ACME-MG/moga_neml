"""
 Title:         The Voce Slip Hardening Asaro Inelasticity Model
 Description:   Incorporates crystal plasticity
 Author:        Janzen Choi

"""

# Libraries
import modules.models.__model__ as model
from neml import elasticity, drivers
from neml.cp import crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polycrystal
from neml.math import rotations
from neml.nlsolvers import MaximumIterations

# Model Parameters
STRESS_RATE  = 0.0001
STRAIN_MAX   = 0.005
HOLD         = 11500.0 * 3600.0
NUM_STEPS_UP = 50
NUM_STEPS    = 100
MAX_ITER     = 16
MAX_DIVIDE   = 2

# The Voce Slip Hardening Asaro Inelasticity Class
class Model(model.ModelTemplate):

    # Runs at the start, once
    def prepare(self):

        # Add parameters
        self.add_param("vsh_ts", 0.0e0, 1.0e2)
        self.add_param("vsh_b",  0.0e0, 1.0e2)
        self.add_param("vsh_t0", 0.0e0, 1.0e2)
        self.add_param("ai_g0",  0.0e0, 1.0e0)
        self.add_param("ai_n",   0.0e0, 1.0e2)

        # Extract information from arguments
        orientation_file = self.args[0]
        lattice_a        = self.args[1]
        slip_direction   = self.args[2]
        slip_plane       = self.args[3]
        self.num_threads = self.args[4]

        # Define grain orientations
        file = open(f"input/{orientation_file}", "r")
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
        self.lattice = crystallography.CubicLattice(lattice_a)
        self.lattice.add_slip_system(slip_direction, slip_plane)
        
    # Gets the predicted curve
    #   api.define_model("vshai", ["cp_ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 16])
    def get_prd_curve(self, exp_curve, vsh_ts, vsh_b, vsh_t0, ai_g0, ai_n):

        # Define model
        elastic_model  = elasticity.IsotropicLinearElasticModel(exp_curve["youngs"], "youngs", exp_curve["poissons"], "poissons")
        strength_model = slipharden.VoceSlipHardening(vsh_ts, vsh_b, vsh_t0)
        slip_model     = sliprules.PowerLawSlipRule(strength_model, ai_g0, ai_n)
        ai_model       = inelasticity.AsaroInelasticity(slip_model)
        ep_model       = kinematics.StandardKinematicModel(elastic_model, ai_model)
        sc_model       = singlecrystal.SingleCrystalModel(ep_model, self.lattice, verbose=False, miter=MAX_ITER, max_divide=MAX_DIVIDE)
        vshai_model    = polycrystal.TaylorModel(sc_model, self.grain_orientations, nthreads=self.num_threads, weights=self.weights)

        # Get predictions
        if exp_curve["type"] == "creep":
            try:
                creep_results = drivers.creep(vshai_model, exp_curve["stress"], STRESS_RATE, HOLD, T=exp_curve["temp"], verbose=False,
                                                check_dmg=False, dtol=0.95, nsteps_up=NUM_STEPS_UP, nsteps=NUM_STEPS, logspace=False)
                return {"x": list(creep_results["rtime"] / 3600), "y": list(creep_results["rstrain"])}
            except MaximumIterations:
                return
        elif exp_curve["type"] == "tensile":
            strain_rate = exp_curve["strain_rate"] / 3600
            try:
                tensile_results = drivers.uniaxial_test(vshai_model, erate=strain_rate, T=exp_curve["temp"], verbose=False, emax=STRAIN_MAX, nsteps=NUM_STEPS)
                return {"x": list(tensile_results["strain"]), "y": list(tensile_results["stress"])}
            except MaximumIterations:
                return