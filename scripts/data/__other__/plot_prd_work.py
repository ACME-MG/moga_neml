import math, numpy as np
from copy import deepcopy
from numpy.polynomial.polynomial import polyval

def get_root(polynomial:list, value:float, eps:float=1e-5):
    offset_polynomial = deepcopy(polynomial)
    offset_polynomial[-1] -= value
    roots = np.roots(offset_polynomial)
    real_roots = roots.real[abs(roots.imag) < eps]
    return real_roots

# Evaluates a fourth degree polynomial
def my_poly(y, wd_0, wd_1, wd_2, wd_x, wd_y):
    y -= wd_y
    x = wd_0*math.pow(y, 3) + wd_1*math.pow(y, 2) + wd_2*(y) + wd_x
    return x

wd_params = [0.2, 1.4, 3, 1.4, 0]
l_bounds = get_root(wd_params[:-1], -8)
u_bounds = get_root(wd_params[:-1], 0)
if len(l_bounds) == 0 or len(u_bounds) == 0:
    pass

y_list = list(np.linspace(min(l_bounds) + wd_params[-1], max(u_bounds) + wd_params[-1], 10))
x_list = [my_poly(y, *wd_params) for y in y_list]

import matplotlib.pyplot as plt
plt.scatter(x_list, y_list)
plt.savefig("plot")

# x_interp        = [10**i for i in [-10, -5, 0, 5, 10]]
# y_interp        = [line(x, wd_m, wd_b) for x in x_interp]
# wd_wc           = interpolate.PiecewiseSemiLogXLinearInterpolate(x_interp, y_interp)