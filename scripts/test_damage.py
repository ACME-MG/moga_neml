import math

def get_work(work_rate, x_f, y_f, x_o, y_o):
    return y_f * math.tanh(x_f * work_rate - x_o) + y_o

x_list = list(range(-10, 10))
y_list = [get_work(x, 0.1, 1, 0, 0) for x in x_list]

import matplotlib.pyplot as plt
plt.scatter(x_list, y_list)
plt.savefig("plot")