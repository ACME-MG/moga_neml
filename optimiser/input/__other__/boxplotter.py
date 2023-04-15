import matplotlib.pyplot as plt
import numpy as np

def reject_outliers(data, m=2):
    data = np.array(data)
    return data[abs(data - np.mean(data)) < m * np.std(data)]

with open("times", "r") as file:
    all_lines = file.readlines()
all_times = reject_outliers([float(line) for line in all_lines])
# all_times = [time for time in all_times if time < 1 and time > 0.5]
figure = plt.figure(figsize=(5, 7))
plt.boxplot(all_times, showfliers=False, widths=(0.8))
plt.scatter(np.random.normal(1, 0.1, len(all_times)), all_times, color="orange")
plt.rc('ytick', labelsize=10)
plt.savefig("plot.png")