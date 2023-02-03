
import sys
from neml import interpolate
from math import e as exp, pow
sys.path += ["../__common__", "../__models__"]
from plotter import quick_plot_N

def half_sigmoid(x, factor=2, offset=0):
    return factor*(1/(1+pow(exp,-x)) - 0.5) + offset

x_interp = [2**i for i in range(-2,4)]
y_interp = [half_sigmoid(x) for x in x_interp]
# itp = interpolate.PiecewiseLinearInterpolate(x_interp, y_interp)
itp = interpolate.PiecewiseSemiLogXLinearInterpolate(x_interp, y_interp)

x_test = [i/10 for i in range(-100,100)]
y_test = [itp(x) for x in x_test]

quick_plot_N(".", "plot.png", [[{"x": x_interp, "y": y_interp}], [{"x": x_test, "y": y_test}]], ["train", "test"], ["r", "b"], ["scat", "line"])