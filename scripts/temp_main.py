#!/usr/bin/env python3
import numpy as np

from neml.cp import polycrystal, crystallography, slipharden, sliprules, inelasticity, kinematics, singlecrystal, polefigures
from neml.math import rotations, tensors, nemlmath
from neml import elasticity, drivers
import matplotlib.pyplot as plt

N = 500

nthreads = 12

erate = 1.0e-4
steps = 400
emax = 0.5
nu = 0.3

T = 20
E = 211000
ts, b, t0, g0, n = 135, 0.5, 760, 0.001, 10

# T = 0
# E = 100000.0
# ts, b, t0, g0, n = 135, 0.5, 670, 0.0001, 20

# Setup
orientations = rotations.random_orientations(N)

lattice = crystallography.CubicLattice(1.0)
lattice.add_slip_system([1,1,0],[1,1,1])

strengthmodel = slipharden.VoceSlipHardening(ts, b, t0)
slipmodel = sliprules.PowerLawSlipRule(strengthmodel, g0, n)
imodel = inelasticity.AsaroInelasticity(slipmodel)
emodel = elasticity.IsotropicLinearElasticModel(E, "youngs", nu, "poissons")
kmodel = kinematics.StandardKinematicModel(emodel, imodel)

model = singlecrystal.SingleCrystalModel(kmodel, lattice)

pmodel = polycrystal.TaylorModel(model, orientations, nthreads = nthreads)

res = drivers.uniaxial_test(pmodel, erate, emax = emax, nsteps = steps)

plt.plot(res['strain'], res['stress'])
plt.show()
