import numpy as np

x_list = [-6, -5, -4, -3, -2, -1.5, -1, -0.5, 0]
y_list = [0, 25, 50, 75, 100, 250, 400, 450, 500]

polynomial = list(np.polyfit(y_list, x_list, deg=3))

print(polynomial)