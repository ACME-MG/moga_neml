
import sys
from neml import interpolate
from math import e as exp, pow
sys.path += ["../__common__", "../__models__"]

x_f, y_f, y_o = 41.155155, 186.835582, 59.7954794

def sigmoid(x, x_factor=1, y_factor=1, y_offset=0.1):
    return y_factor/(1+pow(exp,-x_factor*x)) + y_offset
x_interp = [2**i/x_f for i in range(-4,4)]
y_interp = [sigmoid(x, x_f, y_f, y_o) for x in x_interp]
itp = interpolate.PiecewiseSemiLogXLinearInterpolate(x_interp, y_interp)

x_test = [2**i for i in range(-30,10)]
y_test = [itp(x) for x in x_test]

import matplotlib.pyplot as plt
plt.scatter(x_interp, y_interp, marker="o", color="silver")
plt.plot(x_test, y_test, color="red")
plt.legend(["train", "test"])
plt.xscale("log")
plt.savefig("plot.png")