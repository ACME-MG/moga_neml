"""
 Title:         The Voce Slip Hardening Asaro Inelasticity Model
 Description:   Incorporates crystal plasticity
 Author:        Janzen Choi

"""

# Libraries
from neml import elasticity
from neml.cp import crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polycrystal
from neml.math import rotations
from moga_neml.models.__model__ import __Model__

# The Voce Slip Hardening Asaro Inelasticity Class
class Model(__Model__):

    # Runs at the start, once
    def initialise(self):

        # Define parameters
        self.add_param("vsh_ts", 0.0e0, 2.0e3) # 1e2
        self.add_param("vsh_b",  0.0e0, 1.0e3) # 1e2
        self.add_param("vsh_t0", 0.0e0, 1.0e3) # 1e2
        self.add_param("ai_g0",  0.0e0, 1.0e0)
        self.add_param("ai_n",   0.0e0, 1.0e2)
    
        # Extract information from arguments
        orientation_file = self.get_arg(0)
        lattice_a        = self.get_arg(1)
        slip_direction   = self.get_arg(2)
        slip_plane       = self.get_arg(3)
        self.num_threads = self.get_arg(4)

        # Define grain orientations
        file = open(f"{orientation_file}", "r")
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

        # Random rotation
        num_grains = len(self.grain_orientations)
        self.grain_orientations = rotations.random_orientations(num_grains)

        # Define lattice structure
        self.lattice = crystallography.CubicLattice(lattice_a)
        self.lattice.add_slip_system(slip_direction, slip_plane)
        
    # Gets the predicted curve
    #   api.define_model("vshai", "ebsd/ebsd_statistics.csv", 1.0, [1,1,0], [1,1,1], 16)
    def calibrate_model(self, vsh_ts, vsh_b, vsh_t0, ai_g0, ai_n):
        elastic_model  = elasticity.IsotropicLinearElasticModel(self.get_data("youngs"), "youngs", self.get_data("poissons"), "poissons")
        strength_model = slipharden.VoceSlipHardening(vsh_ts, vsh_b, vsh_t0)
        slip_model     = sliprules.PowerLawSlipRule(strength_model, ai_g0, ai_n)
        ai_model       = inelasticity.AsaroInelasticity(slip_model)
        ep_model       = kinematics.StandardKinematicModel(elastic_model, ai_model)
        sc_model       = singlecrystal.SingleCrystalModel(ep_model, self.lattice, verbose=False, miter=16, max_divide=2)
        vshai_model    = polycrystal.TaylorModel(sc_model, self.grain_orientations, nthreads=self.num_threads, weights=self.weights)
        return vshai_model