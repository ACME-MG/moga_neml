import numpy as np
from copy import deepcopy
from numpy.polynomial.polynomial import polyval

def get_root(polynomial:list, value:float, eps:float=1e-5):
    offset_polynomial = deepcopy(polynomial)
    offset_polynomial[-1] -= value
    roots = np.roots(offset_polynomial)
    real_roots = roots.real[abs(roots.imag) < eps]
    return real_roots

wd_params = [2.0341658462549762e-07, -0.00018143403386635193, 0.05229715944397075, -6.039797477003599]
l_bounds = get_root(wd_params, -8)
u_bounds = get_root(wd_params, 0)
if len(l_bounds) == 0 or len(u_bounds) == 0:
    pass

y_list = list(np.linspace(min(l_bounds), max(u_bounds), 100))
x_list = [polyval(y, np.flip(np.array(wd_params))) for y in y_list]
# x_list = [polyval(y, np.array(wd_params)) for y in y_list]

import matplotlib.pyplot as plt
plt.scatter(x_list, y_list)
plt.savefig("plot")
